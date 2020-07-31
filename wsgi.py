#!/usr/bin/env python3

# flask
from flask import Flask, send_from_directory, request
from flask_caching import Cache
import os
# external
from twitchfeed import mkfeed

# twitchfeed
mk = mkfeed.MkFeed("config.cfg", "general")

# create flask instance
app = Flask(__name__)
# setup cache
cache = Cache(config={"CACHE_TYPE": "simple"})
cache.init_app(app)
# 5 minute cache timeout
cache_timeout = 300

@app.route('/feed')
@cache.cached(timeout=cache_timeout)
def follow_feed():
    feed_type = request.args.get("ft", "rss")
    return stfg(feed_type)

@app.route('/feed/<channel>')
@cache.cached(timeout=cache_timeout)
def channel_feed(channel):
    feed_type = request.args.get("ft", "rss")
    return stfg(feed_type, channel)

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, "media"), "favicon.ico", mimetype="image/vnd.microsoft.icon")

def stfg(feed_type=None, channel=None, update=True):

    if feed_type is None:
        feed_type = "rss"

    if update:
        mk.update()

    if feed_type == "rss":
        response = app.make_response(mk.rss_str(channel))
        response.headers.set("Content-Type", "application/rss+xml")
        return response
    elif feed_type == "atom":
        response = app.make_response(mk.atom_str(channel))
        response.headers.set("Content-Type", "application/atom+xml")
        return response

if __name__ == "__main__":
      app.run(host="127.0.0.1", port=5000)
