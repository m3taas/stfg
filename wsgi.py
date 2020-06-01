# flask
from flask import Flask, send_from_directory
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


@app.route("/feed/<req_type>")
@cache.cached(timeout=540)
def rss(req_type):

    mk.update()

    if req_type == "rss":
        response = app.make_response(mk.rss_str())
        response.headers.set("Content-Type", "application/rss+xml")
    elif req_type == "atom":
        response = app.make_response(mk.atom_str())
        response.headers.set("Content-Type", "application/rss+xml")

    return response

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, "media"), "favicon.ico", mimetype="image/vnd.microsoft.icon")

if __name__ == "__main__":
      app.run(host="127.0.0.1", port=5000)
