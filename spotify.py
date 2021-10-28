"""
Spotify Music Acessing Tools

useful tutorials:
- https://github.com/juandes/spotify-audio-features-data-experiment

Omodayo Origunwa
10.26.2022
"""

import argparse
import pprint
import sys
import os
import subprocess
import json
import spotipy.util as util
import pandas as pd
import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()


class spotifyApi:
    def __init__(self):
        self.name = "Omodayo Origunwa"
        self.username = 12178525311
        self.email = "dayo1523@gmail.com"
        self.client_id = os.environ.get("spotifyClientID")
        self.client_secret = os.environ.get("spotifyClientSecret")
        self.data_path = "/Users/dayoorigunwa/code_base/music_mapping/data/"

    def __str__(self):
        return "Spotify API Helper"

    def getClient(self):
        auth_manager = SpotifyClientCredentials(
            client_id=self.client_id, client_secret=self.client_secret
        )
        client = spotipy.Spotify(auth_manager=auth_manager)
        return client

    def get_playlist_content(self, username, playlist, sp):
        playlist_id = playlist["id"]
        offset = 0
        songs = []
        while True:
            content = sp.user_playlist_tracks(
                username,
                playlist_id,
                fields=None,
                limit=100,
                offset=offset,
                market=None,
            )
            songs += content["items"]
            if content["next"] is not None:
                offset += 100
            else:
                break

        with open(
            self.data_path + "{}-{}".format(username, playlist["name"]), "w"
        ) as outfile:
            json.dump(songs, outfile)

    def get_playlist_audio_features(self, username, playlist, sp):
        playlist_id = playlist["id"]
        offset = 0
        songs = []
        items = []
        ids = []
        while True:
            content = sp.user_playlist_tracks(
                username,
                playlist_id,
                fields=None,
                limit=100,
                offset=offset,
                market=None,
            )
            songs += content["items"]
            if content["next"] is not None:
                offset += 100
            else:
                break

        for i in songs:
            ids.append(i["track"]["id"])

        ids = [iD for iD in ids if iD]
        index = 0
        audio_features = []
        while index < len(ids):
            audio_features += sp.audio_features(ids[index : index + 50])
            index += 50

        features_list = []
        for features in audio_features:
            features_list.append(
                [
                    features["energy"],
                    features["liveness"],
                    features["tempo"],
                    features["speechiness"],
                    features["acousticness"],
                    features["instrumentalness"],
                    features["time_signature"],
                    features["danceability"],
                    features["key"],
                    features["duration_ms"],
                    features["loudness"],
                    features["valence"],
                    features["mode"],
                    features["type"],
                    features["uri"],
                ]
            )

        df = pd.DataFrame(
            features_list,
            columns=[
                "energy",
                "liveness",
                "tempo",
                "speechiness",
                "acousticness",
                "instrumentalness",
                "time_signature",
                "danceability",
                "key",
                "duration_ms",
                "loudness",
                "valence",
                "mode",
                "type",
                "uri",
            ],
        )
        df.to_csv(
            self.data_path + "{}-{}.csv".format(username, playlist["name"]), index=False
        )

    def get_user_playlists(self, username, sp):
        playlists = sp.user_playlists(username)
        payload = playlists["items"]
        for playlist in playlists["items"]:
            print(
                "Name: {}, Number of songs: {}, Playlist ID: {} ".format(
                    playlist["name"].encode("utf8"),
                    playlist["tracks"]["total"],
                    playlist["id"],
                )
            )
        return payload

    def test(self, username, playlist):
        print("Initializing Client")
        sp = self.getClient()
        print("Getting user playlists")
        my_playlists = self.get_user_playlists(username, sp)
        for playlist in my_playlists:
            print("Getting playlist content")
            self.get_playlist_content(username, playlist, sp)
            print("Getting playlist audio features")
            self.get_playlist_audio_features(username, playlist, sp)
