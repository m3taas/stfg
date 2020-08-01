#!/usr/bin/env python3

from twitchfeed import mkfeed, TwitchFeed
import logging

# for usage without flask
if __name__ == "__main__":
    mk = mkfeed.MkFeed("config.cfg", "general")
    mk.update()

    if mk.rss_out:
       mk.feed_file()
       logging.info("Generated rss feed: '{}'".format(mk.rss_out))

    if mk.atom_out:
       mk.feed_file(feed_type="atom")
       logging.info("Generated atom feed: '{}'".format(mk.atom_out))
