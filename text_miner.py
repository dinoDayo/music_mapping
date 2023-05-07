# code for Genius webscraping: * https://medium.com/swlh/how-to-leverage-spotify-api-genius-lyrics-for-data-science-tasks-in-
# pt 2: https://dev.to/willamesoares/how-to-integrate-spotify-and-genius-api-to-easily-crawl-song-lyrics-with-python-4o62python-c36cdfb55cf3


# TODO:
# - Add NLP Analysis Tools to this class
# - Implement functional example of polymorphism via the geniusAPI (?)

import os
import requests

import pandas as pd
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from datetime import datetime

load_dotenv()


#########################


class geniusApi:
    def __init__(self):
        self.name = "genius API helper"
        self.base_url = "https://api.genius.com"
        self.genius_key = os.environ.get("geniusClientAccessToken")
        self.genius_client_id = os.environ.get("geniusClientID")
        self.genius_client_secret = os.environ.get("geniusClientSecret")
        self.headers = {"Authorization": "Bearer " + self.genius_key}

    def get_song_lyrics(self, track_name, track_artist, genius_url):
        print(
            f"Searching for a match for: {track_name}, by {track_artist},\nwith: {search_url}"
        )
        response = requests.get(search_url, headers=self.headers)
        return response

    def search_api(self, track_name, track_artist, debug=True):
        search_url = self.base_url + "/search?q=" + track_name + " " + track_artist
        if debug:
            print(f"Searching for a match for: {track_name}, {track_artist}")
        response = requests.get(search_url, headers=self.headers)
        return response

    def request_song_info(self, track_name, track_artist, debug=True):
        search_url = self.base_url + "/search?q=" + track_name + " " + track_artist
        if debug:
            print(f"Searching for a match for: {track_name}, {track_artist}")
        response = requests.get(search_url, headers=self.headers)
        return response

    def check_hits(self, response, track_artist, debug=True):
        json = response.json()
        remote_song_info = None
        candidates = [
            hit["result"]["primary_artist"]["name"].lower()
            for hit in json["response"]["hits"]
        ]
        for hit in json["response"]["hits"]:
            if track_artist.lower() in hit["result"]["primary_artist"]["name"].lower():
                if debug:
                    print("Found a match!")
                remote_song_info = hit
                break
        return remote_song_info


class textMiner:
    def __init__(self):
        self.name = "text mining helper"
        self.data_path = os.environ.get("musicDataPath")
        self.genius = geniusApi()

    def save_df(self, filename, df):
        date_piece = datetime.today().strftime("%Y-%m-%d")
        df.to_csv(self.data_path + f"{filename}_{date_piece}.csv")
        
    def get_html_text(self, text_blocks):
        lyrics = ""
        for htmlObj in text_blocks:
            for s in htmlObj.strings:
                lyrics += s + " "
        return lyrics

    def scrape_genius_lyrics(self, artistname, songname, url=None):
        # webpage aqquisition logic...
        if url:
            # leverage known endpoint...
            page = requests.get(url)
        else:
            # formatting search string...
            artistname2 = (
                str(artistname.replace(" ", "-"))
                if " " in artistname
                else str(artistname)
            )
            songname2 = (
                str(songname.replace(" ", "-")) if " " in songname else str(songname)
            )
            url = "https://genius.com/" + artistname2 + "-" + songname2 + "-" + "lyrics"

        # general extraction logic...
        html = BeautifulSoup(page.text, "html.parser")

        # Had to find this header manually...
        text_blocks = html.find_all(
            "div",
            attrs={
                "class": lambda e: e.startswith("Lyrics__Container") if e else False
            },
        )
        lyrics = self.get_html_text(text_blocks)
        return lyrics

    def search_genius_song(self, track_name, track_artist, debug=True):
        response = self.genius.request_song_info(track_name, track_artist, debug=debug)
        song_info = self.genius.check_hits(response, track_artist, debug=debug)
        return song_info

    def lyrics_onto_frame(self, df1, artist_name):
        # function to attach lyrics onto data frame
        # artist_name should be inserted as a string
        for i, x in enumerate(df1["track"]):
            test = scrape_lyrics(artist_name, x)
            df1.loc[i, "lyrics"] = test
        return df1
