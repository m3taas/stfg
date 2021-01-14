#!/usr/bin/env python3

import configparser, logging, requests, json
from twitchfeed import Helix, TwitchFeed
from twitchfeed.cred_exception import CredentialException

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

class MkFeed:

    def __init__(self, config_file, section):

        # parse config file
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.config_section = self.config[section]
        self.config_file = config_file

        # attributes
        self.rss_out = self.config_section["rss_out"]
        self.atom_out = self.config_section["atom_out"]

        self.renew_helix_api()
        self.__twitch_feed = TwitchFeed.TwitchFeed(self.__helix)

    def renew_bearer_token(self) -> None:

        token_in_config = False

        try:
            invalid_bearer_token = self.config_section["bearer_token"]
            logging.info("Updating invalid bearer_token: '{}'".format(invalid_bearer_token))
            token_in_config = True
        except KeyError:
            pass

        try:

            if not token_in_config:
                logging.info("Obtaining bearer_token for client_id: '{}'".format(self.config_section['client_id']))

            api_endpoint = "https://id.twitch.tv/oauth2/token"
            params = { "client_id": self.config_section['client_id'],
                    "client_secret": self.config_section['client_secret'],
                    "grant_type": "client_credentials" }

            new_bearer_token = requests.post(api_endpoint, data = params).json()['access_token']
        except KeyError:
            raise CredentialException(self.config_section['client_id'], self.config_section['client_secret'])

        # set new bearer token in config section
        self.config_section["bearer_token"] = new_bearer_token

        # update config file
        with open(self.config_file, "w") as configfile:
            self.config.write(configfile)

    def renew_helix_api(self) -> None:
        # if the initializatoin of a Helix object fails, renew the bearer_token and retry
        for _ in range(2):
            try:
                self.__helix = Helix(self.config_section["client_id"],
                        self.config_section["bearer_token"],
                        self.config_section["username"])
            # the bearer_token has expired
            except RuntimeError:
                self.renew_bearer_token()
                continue
            # in 'bearer_token' was not specified in the config file
            except KeyError:
                self.renew_bearer_token()
                continue
            else:
                break

    def update(self) -> None:

        # if self.__helix.update_streams() fails, renew the helix api
        for _ in range(2):
            try:
                self.__helix.update_streams()
            except KeyError:
                self.renew_helix_api()
                continue
            else:
                break

        self.__twitch_feed.flush()
        self.__twitch_feed.parse_feed_helix(self.__helix)

    def feed_str(self, channel=None, feed_type="rss"):
        if channel is not None:
            fg = self.__twitch_feed.parse_feed_single(self.__helix, channel)

            if feed_type == "rss":
                return fg.rss_str(pretty=True)
            elif feed_type == "atom":
                return fg.atom_str(pretty=True)
        else:
            if feed_type == "rss":
                return self.__twitch_feed.fg.rss_str(pretty=True)
            elif feed_type == "atom":
                return self.__twitch_feed.fg.atom_str(pretty=True)

    def feed_file(self, channel=None, feed_type="rss"):
        if channel is not None:
            fg = self.__twitch_feed.parse_feed_single(self.__helix, channel)

            if feed_type == "rss":
                return fg.rss_file(self.rss_out, pretty=True)
            elif feed_type == "atom":
                return fg.atom_file(self.atom_out, pretty=True)
        else:
            if feed_type == "rss":
                return self.__twitch_feed.fg.rss_file(self.rss_out, pretty=True)
            elif feed_type == "atom":
                return self.__twitch_feed.fg.atom_file(self.atom_out, pretty=True)
