"""
Spotify Music Acessing Tools

useful tutorials:
- Audio Analysis: https://github.com/juandes/spotify-audio-features-data-experiment
- Text Analysis: https://medium.com/swlh/how-to-leverage-spotify-api-genius-lyrics-for-data-science-tasks-in-python-c36cdfb55cf3

Omodayo Origunwa
10.26.2022
"""

import os
import sys
import json
import pprint
import spotipy
import argparse
import requests
import subprocess
import pandas as pd
from os import listdir
import spotipy.util as util
from bs4 import BeautifulSoup
from os.path import isfile, join
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
        self.sp = self.getClient()

    def __str__(self):
        return "Spotify API Helper"

    def getClient(self):
        auth_manager = SpotifyClientCredentials(
            client_id=self.client_id, client_secret=self.client_secret
        )
        client = spotipy.Spotify(auth_manager=auth_manager)
        return client

    def get_playlist_content(self, username, playlist, sp, csv=True):
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
        if csv:
            with open(
                self.data_path + "{}-{}".format(username, playlist["name"]), "w"
            ) as outfile:
                json.dump(songs, outfile)
        else:
            return songs

    def get_playlist_audio_features(self, username, playlist, sp, csv=True):
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
        if csv:
            df.to_csv(
                self.data_path + "{}-{}.csv".format(username, playlist["name"]),
                index=False,
            )
        else:
            return df

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

    def get_followed_users(self, username, sp):
        users = sp.current_user_following_users(
            ids=[
                username,
            ]
        )
        return users

    def test(self, username):
        print("Initializing Client")
        sp = self.getClient()
        print("Getting user playlists")
        my_playlists = self.get_user_playlists(username, sp)
        for playlist in my_playlists:
            print("Getting playlist content")
            self.get_playlist_content(username, playlist, sp)
            print("Getting playlist audio features")
            self.get_playlist_audio_features(username, playlist, sp)

    def download_spotify_playlist_audio_features(self):
        my_playlists = self.get_user_playlists(username=self.username, sp=self.sp)
        for playlist in my_playlists:
            print("Getting playlist content")
            self.get_playlist_content(self.username, playlist, sp)
            print("Getting playlist audio features")
            self.get_playlist_audio_features(self.username, playlist, sp)

    def rename_spotify_songs(self, data_path=None):
        # Renaming files - No longer necessary
        if data_path:
            pass
        else:
            data_path = self.data_path
        onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path, f))]
        id_to_name = {playlist["id"]: playlist["name"] for playlist in my_playlists}
        for filename in onlyfiles:
            if "-" in filename:
                playlist_id = filename.split("-")[-1].split(".")[0]
                if playlist_id in list(id_to_name.keys()):
                    os.rename(
                        data_path + filename,
                        data_path
                        + filename.replace(playlist_id, id_to_name[playlist_id]),
                    )

    def get_album_tracks(self, uri_info):
        # insert the URI as a string into the function
        uri = []
        track = []
        duration = []
        explicit = []
        track_number = []
        one = self.sp.album_tracks(uri_info, limit=50, offset=0, market="US")
        df1 = pd.DataFrame(one)

        for i, x in df1["items"].items():
            uri.append(x["uri"])
            track.append(x["name"])
            duration.append(x["duration_ms"])
            explicit.append(x["explicit"])
            track_number.append(x["track_number"])

        df2 = pd.DataFrame(
            {
                "uri": uri,
                "track": track,
                "duration_ms": duration,
                "explicit": explicit,
                "track_number": track_number,
            }
        )

        return df2

    def get_track_info(self, df):
        # insert output dataframe from the get_album_tracks function
        danceability = []
        energy = []
        key = []
        loudness = []
        speechiness = []
        acousticness = []
        instrumentalness = []
        liveness = []
        valence = []
        tempo = []
        for i in df["uri"]:
            for x in self.sp.audio_features(tracks=[i]):
                danceability.append(x["danceability"])
                energy.append(x["energy"])
                key.append(x["key"])
                loudness.append(x["loudness"])
                speechiness.append(x["speechiness"])
                acousticness.append(x["acousticness"])
                instrumentalness.append(x["instrumentalness"])
                liveness.append(x["liveness"])
                valence.append(x["valence"])
                tempo.append(x["tempo"])

        df2 = pd.DataFrame(
            {
                "danceability": danceability,
                "energy": energy,
                "key": key,
                "loudness": loudness,
                "speechiness": speechiness,
                "acousticness": acousticness,
                "instrumentalness": instrumentalness,
                "liveness": liveness,
                "valence": valence,
                "tempo": tempo,
            }
        )

        return df2
