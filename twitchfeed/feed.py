#!/usr/bin/env python3

from feedgen.feed import FeedGenerator
import datetime, logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

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

def parse_feed(helix):

    try:
        for stream in helix.streams:
            logging.debug("Stream: {}".format(stream))
            # convert time to local timezone
            start_date = datetime.datetime.strptime(stream["started_at"], "%Y-%m-%dT%H:%M:%SZ")
            start_date = start_date.replace(tzinfo=datetime.timezone.utc)
            start_date = start_date.astimezone()

            title = "{}".format(stream["title"])
            description = "{} is playing '{}'".format(stream["user_name"], helix.game_dict[stream["game_id"]])

            """ add the start time of the stream as a parameter
            this is necessary because many rss readers identify feed entries by their content url
            without this new streams of the same streamer wouldn"t get recognized as new feed entries """
            url = "https://www.twitch.tv/" + stream["user_name"] + "?started=" + str(start_date).replace(" ", "_")

            # add feed entry
            fe = fg.add_entry()
            fe.title(title)
            fe.description(description)
            fe.link(href=url)
            fe.id(url)
            fe.published(start_date)

            media_width = "1280"
            media_height = "720"
            # add a preview of the stream
            thumbnail_url = stream["thumbnail_url"]
            thumbnail_url = thumbnail_url.replace("{width}", media_width)
            thumbnail_url = thumbnail_url.replace("{height}", media_height)
            fe.media.content(url=thumbnail_url, width=media_width, height=media_height)
            fe.media.thumbnail(url=thumbnail_url, width=media_width, height=media_height)

    except AttributeError as e:
            helix.update_streams()
            parse_feed(helix)
