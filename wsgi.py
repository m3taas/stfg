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


# @cache.cached(timeout=540)
@app.route('/feed')
def stfg():
    feed_type = request.args.get("ft", "rss")
    channel = request.args.get("user", None)

    if channel is None:
        mk.update()

    if feed_type == "rss":
        response = app.make_response(mk.rss_str(channel))
        response.headers.set("Content-Type", "application/rss+xml")
        return response
    elif feed_type == "atom":
        response = app.make_response(mk.atom_str(channel))
        response.headers.set("Content-Type", "application/atom+xml")
        return response

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, "media"), "favicon.ico", mimetype="image/vnd.microsoft.icon")

if __name__ == "__main__":
      app.run(host="127.0.0.1", port=5000)
