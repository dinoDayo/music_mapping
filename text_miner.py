# code for Genius webscraping: * https://medium.com/swlh/how-to-leverage-spotify-api-genius-lyrics-for-data-science-tasks-in-
# pt 2: https://dev.to/willamesoares/how-to-integrate-spotify-and-genius-api-to-easily-crawl-song-lyrics-with-python-4o62python-c36cdfb55cf3

import os
import pandas as pd
from bs4 import BeautifulSoup
import requests


class geniusApi:
    def __init__(self):
        self.name = "genius API helper"
        self.base_url = "https://api.genius.com"
        self.genius_key = os.environ.get("geniusClientAccessToken")
        self.genius_client_id = os.environ.get("geniusClientID")
        self.genius_client_secret = os.environ.get("geniusClientSecret")
        self.headers = {"Authorization": "Bearer " + self.genius_key}

    def request_song_info(self, track_name, track_artist):
        search_url = self.base_url + "/search"
        data = {"q": track_name + " " + track_artist}
        response = requests.get(search_url, data=data, headers=self.headers)
        return response

    def check_hits(self, response, track_artist):
        json = response.json()
        remote_song_info = None
        for hit in json["response"]["hits"]:
            if track_artist.lower() in hit["result"]["primary_artist"]["name"].lower():
                remote_song_info = hit
                break
        return remote_song_info


class textMiner:
    def __init__(self):
        self.name = "text mining helper"
        self.genius = geniusApi()

    def scrape_genius_lyrics(self, artistname, songname):
        # function to scrape lyrics from genius
        artistname2 = (
            str(artistname.replace(" ", "-")) if " " in artistname else str(artistname)
        )
        songname2 = (
            str(songname.replace(" ", "-")) if " " in songname else str(songname)
        )
        url = "https://genius.com/" + artistname2 + "-" + songname2 + "-" + "lyrics"
        page = requests.get(url)
        html = BeautifulSoup(page.text, "html.parser")
        lyric_sets = html.find_all(
            "div",
            attrs={
                "class": lambda e: e.startswith("Lyrics__Container") if e else False
            },
        )
        for htmlObj in lyric_sets:
            lyrics = htmlObj.get_text()
            if lyrics:
                return lyrics
        return 0

    def search_genius_song(self, track_name, track_artist):
        response = self.genius.request_song_info(track_name, track_artist)
        song_info = self.genius.check_hits(response, track_artist)
        return song_info

    def lyrics_onto_frame(self, df1, artist_name):
        # function to attach lyrics onto data frame
        # artist_name should be inserted as a string
        for i, x in enumerate(df1["track"]):
            test = scrape_lyrics(artist_name, x)
            df1.loc[i, "lyrics"] = test
        return df1
