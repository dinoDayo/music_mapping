"""
Spotify Music Acessing Tools

Omodayo Origunwa
10.26.2022
"""

from dotenv import load_dotenv
import os 
load_dotenv()

class spotifyApi:

	def __init__(self):
		self.name = "Omodayo Origunwa"
		self.email = "dayo1523@gmail.com"
		self.client_id = os.environ.get('spotifyClientID')
		self.client_secret = os.environ.get('spotifyClientSecret')	

	def __str__(self):
		return "Spotify API Helper"

	def getClient(self):
		return True		

