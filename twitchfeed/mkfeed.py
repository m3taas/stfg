#!/usr/bin/env python3

import configparser, logging
from twitchfeed import Helix, feed

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

class MkFeed:

    __helix = None

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

    def update(self):
        self.__helix.update_streams()

        # remove all saved feeds from feed.fg
        while not len(feed.fg.entry()) == 0:
            feed.fg._FeedGenerator__feed_entries.pop()

        feed.parse_feed(self.__helix)

    def atom_str(self):
        return feed.fg.atom_str(pretty=True)

    def rss_str(self):
        return feed.fg.rss_str(pretty=True)
