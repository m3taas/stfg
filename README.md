# Simple Twitch Feed Generator

Generates a rss/atom feed notifying you when Twitch streamers you follow go live. It can be used with flask or with static xml files which you can serve however you like. The feed includes which game is being played and a stream preview. It uses the 'New Twitch API' aka 'Helix'.

## Installation

### Register a twitch application

* Go to [twitch console](https://dev.twitch.tv/console/apps)
* Choose a _Name_
* Set _OAuth Redirect URLs_ to `http://localhost`
* Choose a _Category_
* Note your `Client ID` and `Client Secret`

### Obtain your oauth2 token

	$ ./scripts/obtain_oauth2.sh YOUR_CLIENT_ID YOUR_CLIENT_SECRET

### Set your config

Create and edit your config with the previously obtained parameters

	$ cp -vi .config.cgf.preset config.cfg
	$ vim config.cfg

### Install dependencies

	$ python -m venv env && source env/bin/activate # optional
	$ pip install -r requirements.txt

Python version: 3.7.3

## Run

Run using flasks built in server. **This is not suitable for production.**

	$ flask run --host=HOST_IP --port=5000

Generate atom/rss files

	$ mkdir -p /srv/http
	$ python genfeed.py

You can easily add a cronjob on your server to update the feed.

Test your feed

	$ curl http://HOST_IP:5000/feed/atom
	$ curl http://HOST_IP:5000/feed/rss

# [Twitch Helix api reference](https://dev.twitch.tv/docs/api/reference)
