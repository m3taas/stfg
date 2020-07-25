#!/usr/bin/env python3

import configparser, logging
from twitchfeed import Helix, TwitchFeed

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

class MkFeed:

    __helix = None
    __twitch_feed = None

    def __init__(self, config_file, profile):

        # parse config file
        config = configparser.ConfigParser()
        config.read(config_file)

        # attributes
        self.rss_out = config.get(profile, "rss_out", fallback=None)
        self.atom_out = config.get(profile, "atom_out", fallback=None)

        self.__helix = Helix(config.get(profile, "client_id"),
                config.get(profile, "bearer_token"),
                config.get(profile, "username"))

        self.__twitch_feed = TwitchFeed.TwitchFeed(self.__helix)

    def update(self):
        self.__helix.update_streams()
        self.__twitch_feed.flush()
        self.__twitch_feed.parse_feed_helix(self.__helix)

    def atom_str(self, channel=None):
        if channel is not None:
            return self.__twitch_feed.parse_feed_single(self.__helix, channel, "atom")
        else:
            return self.__twitch_feed.fg.atom_str(pretty=True)

    def rss_str(self, channel=None):
        if channel is not None:
            return self.__twitch_feed.parse_feed_single(self.__helix, channel, "rss")
        else:
            return self.__twitch_feed.fg.rss_str(pretty=True)
