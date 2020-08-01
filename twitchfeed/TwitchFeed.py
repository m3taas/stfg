#!/usr/bin/env python3

from feedgen.feed import FeedGenerator
import datetime, logging

class TwitchFeed:

    # setup feed
    fg = FeedGenerator()
    fg.title("Twitch")

    # logo_url = ""
    # fg.logo(logo=logo_url)
    # fg.icon(icon=logo_url)
    fg.subtitle("Twitch follower feed")
    link = "https://twitch.tv"
    fg.id(link) # atom
    fg.link( href=link, rel="alternate" ) # rss
    fg.language("en")
    # media extension
    fg.load_extension("media", atom=True, rss=True)

    def __init__(self, helix):

        self.helix = helix

    """
    Remove all saved feeds from a given fg
    """
    def flush(self, fg=None):
        if fg is None:
            self.flush(self.fg)
        else:
            while not len(fg.entry()) == 0:
                fg._FeedGenerator__feed_entries.pop()

    """
    Add feed entries from a helix to fg
    """
    def parse_feed_helix(self, helix):
        self.parse_feeds(helix.streams, helix.game_dict)

    """
    Add feed entries from a streams to fg, where streams are json objects
    """
    def parse_feeds(self, streams, game_dict):
        for stream in streams:
            self.parse_feed(stream, game_dict, self.fg)

    """
    Add a feed entry from a stream to fg, where stream is a json object
    """
    def parse_feed(self, stream, game_dict, fg):

        # logging.debug("Stream: {}".format(stream))
        # convert time to local timezone
        start_date = datetime.datetime.strptime(stream["started_at"], "%Y-%m-%dT%H:%M:%SZ")
        start_date = start_date.replace(tzinfo=datetime.timezone.utc)
        start_date = start_date.astimezone()

        title = "{}".format(stream["title"])

        # twitch decided to allow empty game id's so we need to handle this edge case
        try:
            description = "{} is playing '{}'".format(stream["user_name"], game_dict[stream["game_id"]])
        except KeyError as e:
            description = "{} has gone live".format(stream["user_name"])

        """ add the start time of the stream as a parameter
        this is necessary because many rss readers identify feed entries by their content url
        without this new streams of the same streamer wouldn't get recognized as new feed entries """
        url = "https://www.twitch.tv/" + stream["user_name"] + "?started=" + str(start_date).replace(" ", "_")

        # add feed entry
        self.fe = fg.add_entry()
        self.fe.title(title)
        self.fe.description(description)
        self.fe.link(href=url)
        self.fe.id(url)
        self.fe.published(start_date)

        media_width = "1280"
        media_height = "720"
        # add a preview of the stream
        thumbnail_url = stream["thumbnail_url"]
        thumbnail_url = thumbnail_url.replace("{width}", media_width)
        thumbnail_url = thumbnail_url.replace("{height}", media_height)
        self.fe.media.content(url=thumbnail_url, width=media_width, height=media_height)
        self.fe.media.thumbnail(url=thumbnail_url, width=media_width, height=media_height)

    """
    Generate a feed for a single channel
    """
    def parse_feed_single(self, helix, channel):

        # setup feed
        fg = FeedGenerator()
        fg.title("Twitch: {}".format(channel))

        # logo_url = ""
        # fg.logo(logo=logo_url)
        # fg.icon(icon=logo_url)
        fg.subtitle("Twitch follower feed")
        link = "https://twitch.tv"
        fg.id(link) # atom
        fg.link( href=link, rel="alternate" ) # rss
        fg.language("en")
        # media extension
        fg.load_extension("media", atom=True, rss=True)

        try:
            stream = helix.get_streams(channel, "user_login")[0]
            self.parse_feed(stream, helix.game_dict, fg)
            logging.debug("Stream: {}".format(stream))
        finally:
            return fg
