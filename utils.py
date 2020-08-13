import os
#from __future__ import print_function    # (at top of module)
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
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
ATTRIBUTES = ["energy", "speechiness", "acousticness", "instrumentalness", "liveness", "valence"]
SCOPE = "user-top-read"
URI = "https://localhost:5000/callback/"
RANGES = ['short_term', 'medium_term', 'long_term']
cid = os.getenv('CLIENT_ID')
secret = os.environ.get('CLIENT_SECRET')
USERNAME = os.environ.get('USERNAME')

def initialize():
	client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret) 
	sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
	sp.trace=False 
	return sp 

def get_song_features(feature_list, attributes):
	#e.g. attributes = ["danceability", "energy", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo"]
	chosen_features = []
	for attribute in attributes:
		chosen_features.append(feature_list.get(attribute))
	return chosen_features

def get_playlist_features(playlist_id, attributes):
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

	# features is a list of JSONs with features for each song
	features = []
	for i in range(0, len(ids), 100):
	    features.extend(sp.audio_features(ids[i:i+100]))

	data = []
	for i in range(len(features)):
	    chosen_features = get_song_features(features[i], ATTRIBUTES)
	    chosen_features.append(playlist_id)
	    data.append(chosen_features)
	return data

def create_csv(playlists):
	final_df = pd.DataFrame()
	final_df_length = 0
	final_list = []
	for i in range(len(playlists)):
		final_list.extend(get_playlist_features(playlists[i], ATTRIBUTES))
	with open('playlists.csv', 'w', newline='') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerows(final_list)

def get_top_tracks_with_attributes(attributes):
	sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = cid, client_secret=secret, scope=SCOPE, redirect_uri=URI, username=USERNAME))
	scope_to_id, id_to_song_meta = get_top_tracks_with_id(sp)
	# scope to features: (scope, a list of JSONs with features for each song)
	scope_to_features = {}
	for sp_range in RANGES:
		ids = scope_to_id[sp_range]
		features = sp.audio_features(ids)
		all_track_features = []
		for i in range(len(features)):
			chosen_features = get_song_features(features[i], ATTRIBUTES)
			chosen_features.append(ids[i])
			all_track_features.append(chosen_features)
		scope_to_features[sp_range] = all_track_features
	#print(scope_to_features)
	#print(id_to_song_meta)
	return scope_to_features, id_to_song_meta

def get_top_tracks_with_id(sp):
	scope_to_id = {}
	id_to_song_meta = {}
	for sp_range in RANGES:
		ids = []
		results = sp.current_user_top_tracks(time_range=sp_range, limit=50)
		for i, item in enumerate(results['items']):
			track_id = results['items'][i]['id']
			track_name = item['name']
			artist_name = item['artists'][0]['name']
			ids.append(track_id)
			id_to_song_meta[track_id] = [track_name, artist_name]
			# print(i, item['name'], '//', item['artists'][0]['name'])
		scope_to_id[sp_range] = ids
	return scope_to_id, id_to_song_meta


# Sad Songs: spotify:playlist:7ABD15iASBIpPP5uJ5awvq
# Party Hits: spotify:playlist:6IfGK9nLC9ChgD7FTZzkLJ
# Lofi: spotify:playlist:0vvXsWCC9xrXsKd4FyS8kM
# Sleep: spotify:playlist:37i9dQZF1DWZd79rJ6a7lp
playlists = ["7ABD15iASBIpPP5uJ5awvq", "6IfGK9nLC9ChgD7FTZzkLJ", "0vvXsWCC9xrXsKd4FyS8kM"]
create_csv(playlists)

#get_top_tracks_with_attributes(ATTRIBUTES)