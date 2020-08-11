import os
#from __future__ import print_function    # (at top of module)
from spotipy.oauth2 import SpotifyClientCredentials
import json
import spotipy
import time
import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.io
import csv
import pandas as pd

USER = os.getenv('CLIENT_ID')
PASSWORD = os.environ.get('CLIENT_SECRET')

def initialize():
	cid = os.getenv('CLIENT_ID')
	secret = os.environ.get('CLIENT_SECRET')
	client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret) 
	sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
	sp.trace=False 
	return sp 

def get_song_features(feature_list):
	#attributes = ["danceability", "energy", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo"]
	attributes = ["energy", "speechiness", "acousticness", "instrumentalness", "liveness", "valence"]
	chosen_features = []
	for attribute in attributes:
		chosen_features.append(feature_list.get(attribute))
	return chosen_features

def get_playlist_features(playlist_id):
	sp = initialize()
	playlist = sp.playlist(playlist_id)
	songs = playlist["tracks"]["items"]
	ids = []

	results = playlist["tracks"]
	for i in range(len(results["items"])): 
	    ids.append(results["items"][i]["track"]["id"]) 
	while results["next"]:
	    results = sp.next(results)
	    for i in range(len(results["items"])): 
	        ids.append(results["items"][i]["track"]["id"]) 

	# features is a list of JSONs with featuers for each song
	features = []
	for i in range(0, len(ids), 100):
	    features.extend(sp.audio_features(ids[i:i+100]))

	data = []
	for i in range(len(features)):
	    chosen_features = get_song_features(features[i])
	    chosen_features.append(playlist_id)
	    data.append(chosen_features)
	return data

def create_csv(playlists):
	final_df = pd.DataFrame()
	final_df_length = 0
	final_list = []
	for i in range(len(playlists)):
		final_list.extend(get_playlist_features(playlists[i]))
	with open('playlists.csv', 'w', newline='') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerows(final_list)

# Sad Songs: spotify:playlist:7ABD15iASBIpPP5uJ5awvq
# Party Hits: spotify:playlist:6IfGK9nLC9ChgD7FTZzkLJ
# Lofi: spotify:playlist:0vvXsWCC9xrXsKd4FyS8kM
# Sleep: spotify:playlist:37i9dQZF1DWZd79rJ6a7lp
playlists = ["7ABD15iASBIpPP5uJ5awvq", "6IfGK9nLC9ChgD7FTZzkLJ"]
create_csv(playlists)