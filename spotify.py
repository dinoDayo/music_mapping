"""
Spotify Music Acessing Tools

Omodayo Origunwa
10.26.2022
"""

from dotenv import load_dotenv
import os 

load_dotenv()
print(os.environ.get('spotifyClientID'))
print(os.environ.get('spotifyClientSecret'))

