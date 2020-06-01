#!/usr/bin/env python3

from twitchfeed import mkfeed, feed
import logging

# for usage without flask
if __name__ == "__main__":
    mk = mkfeed.MkFeed("config.cfg", "general")
    mk.update()

    if mk.rss_out:
       feed.fg.rss_file(mk.rss_out, pretty=True)
       logging.info("Generated rss feed: '{}'".format(mk.rss_out))

    if mk.atom_out:
       feed.fg.atom_file(mk.atom_out, pretty=True)
       logging.info("Generated atom feed: '{}'".format(mk.atom_out))
