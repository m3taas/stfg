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
    string representation
    """
    def __str__(self):
        return "Helix:{}:{}".format(self.username, self.user_id)

    """
    update stream list
    """
    def update_streams(self):
        followed_channels = self.__get_followed()
        self.streams = self.__get_streams(followed_channels)
        self.__update_games()
        logging.info("{}: Updated streams".format(self))

    """
    update game_dict from current streams
    """
    def __update_games(self):

        # current game ids
        game_ids = []
        for stream in self.streams:
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
    set user id attribute
    """
    def __set_user_id(self):
        # get user id
        user_id_req = requests.get(self.BASE_URL + "/users", params={"login": self.username}, headers=self.headers)
        self.user_id =  user_id_req.json()["data"][0]["id"]
        logging.debug("Obtained user id for '{}': '{}'".format(self.username, self.user_id))

    """
    return current followed channels as a list of strings
    """
    def __get_followed(self):
        followed_req =  requests.get(self.BASE_URL + "/users/follows", params={"from_id": self.user_id} , headers=self.headers)
        channels = []

        for user in followed_req.json()["data"]:
            channels.append(user["to_id"])
        return channels

    """
    return current live streams as a list of dictionarys
    """
    def __get_streams(self, channels):

        params = []
        for _id in channels:
            params.append(("user_id", _id))

        streams_req =  requests.get(self.BASE_URL + "/streams", params=params, headers=self.headers)

        streams = []
        for stream in streams_req.json()["data"]:
            if stream["type"] == "live":
                streams.append(stream)

        return streams
