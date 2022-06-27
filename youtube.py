"""
Spotify Music Acessing Tools

useful resources:
- Audio Collection: https://dev.to/kalebu/how-to-download-youtube-video-as-audio-using-python-33g9
- Python Libraries: https://github.com/ytdl-org/youtube-dl

Omodayo Origunwa
03.08.2022
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
from dotenv import load_dotenv
from pytube import YouTube
