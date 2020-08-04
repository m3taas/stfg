#!/usr/bin/env python3

# flask
from flask import Flask, send_from_directory, request, url_for, render_template
from flask_caching import Cache
import os
from twitchfeed import mkfeed

URL_PREFIX = "feed"
CONFIG_NAME = "config.cfg"
CACHE_DEFAULT_TIMEOUT = 300

# twitchfeed
mk = mkfeed.MkFeed(CONFIG_NAME, "general")

# create flask instance
app = Flask(__name__, static_url_path="/static")
# setup cache
cache = Cache(config={"CACHE_TYPE": "simple",
    "CACHE_DEFAULT_TIMEOUT": CACHE_DEFAULT_TIMEOUT})
cache.init_app(app)

# index page
@app.route('/')
def index():

    feed_url = url_for("feed", _external=True)
    feed_url_channel = "{}/CHANNEL".format(feed_url)
    feed_url_channel_example = "{}/esl_csgo".format(feed_url)
    html_data = {
        "title" : "Simple Twitch Feed Generator",
        "feed_url" : feed_url,
        "feed_url_channel" : feed_url_channel,
        "feed_url_channel_example" : feed_url_channel_example,
    }

    return render_template("index.html", data=html_data)

@app.route('/{}'.format(URL_PREFIX))
@app.route('/{}/<channel>'.format(URL_PREFIX))
def feed(channel=None):
    feed_type = request.args.get("ft", "rss")

    response = cache.get("followed_{}_{}".format(feed_type, channel))
    if response is None:
        response_rss = stfg("rss", channel)
        response_atom = stfg("atom", channel, False)
        cache.set("followed_rss_{}".format(channel), response_rss)
        cache.set("followed_atom_{}".format(channel), response_atom)
        response = cache.get("followed_{}_{}".format(feed_type, channel))

    return response

def stfg(feed_type=None, channel=None, update=True):

    if feed_type is None:
        feed_type = "rss"

    if update:
        mk.update()

    if feed_type == "rss":
        response = app.make_response(mk.feed_str(channel))
        response.headers.set("Content-Type", "application/rss+xml")
        return response
    elif feed_type == "atom":
        response = app.make_response(mk.feed_str(channel, "atom"))
        response.headers.set("Content-Type", "application/atom+xml")
        return response

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, "media"), "favicon.ico", mimetype="image/vnd.microsoft.icon")

if __name__ == "__main__":
      app.run(host="127.0.0.1", port=5000)
