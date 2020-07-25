#!/usr/bin/env python3

import requests, datetime, logging

class Helix:

    BASE_URL = "https://api.twitch.tv/helix"

    def __init__(self, client_id, bearer_token, username):

        # set instance fields
        self.username = username
        # request headers for auth, etc
        self.headers = {
            "Client-ID": client_id,
            "Authorization": "Bearer " + bearer_token
        }

        # set user id
        try:
            self.__set_user_id()
        except KeyError:
            raise RuntimeError("Could not get 'user_id'. Check your authentication parameters.")

        self.game_dict = {}

    """
    String representation
    """
    def __str__(self):
        return "Helix:{}:{}".format(self.username, self.user_id)

    """
    Update stream list
    """
    def update_streams(self):
        followed_channels = self.__get_followed()
        self.streams = self.get_streams(followed_channels, "user_id")
        self.__update_games(self.streams)
        logging.info("{}: Updated streams".format(self))

    """
    Update game_dict from current streams
    """
    def __update_games(self, streams):

        # current game ids
        game_ids = []
        for stream in streams:
            _id = stream["game_id"]
            if not _id in self.game_dict.keys():
                game_ids.append(_id)

        # if there are any new ids to fetch
        if game_ids:
            params = []
            for _id in game_ids:
                params.append(("id", _id))
            games_req = requests.get(self.BASE_URL + "/games", params=params, headers=self.headers)

            for game in games_req.json()["data"]:
                self.game_dict[game["id"]] = game["name"]

    """
    Ret user id attribute
    """
    def __set_user_id(self):
        # get user id
        user_id_req = requests.get(self.BASE_URL + "/users", params={"login": self.username}, headers=self.headers)
        self.user_id =  user_id_req.json()["data"][0]["id"]
        logging.debug("Obtained user id for '{}': '{}'".format(self.username, self.user_id))

    """
    Return current followed channels as a list of strings
    """
    def __get_followed(self):
        followed_req =  requests.get(self.BASE_URL + "/users/follows", params={"from_id": self.user_id} , headers=self.headers)
        channels = []

        for user in followed_req.json()["data"]:
            channels.append(user["to_id"])
        return channels

    """
    Return current live streams as a list of dictionarys
    """
    def get_streams(self, channels, api_backend):

        params = []
        if isinstance(channels, list):
            for _id in channels:
                params.append((api_backend, _id))
        else:
            params = [(api_backend, channels)]

        streams_req =  requests.get(self.BASE_URL + "/streams", params=params, headers=self.headers)

        streams = []
        for stream in streams_req.json()["data"]:
            if stream["type"] == "live":
                streams.append(stream)

        return streams
