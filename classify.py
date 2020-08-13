# pytorch mlp for multiclass classification
from numpy import vstack
from numpy import argmax
from pandas import read_csv
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from torch import Tensor
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from torch.utils.data import random_split
from torch.nn import Linear
from torch.nn import ReLU
from torch.nn import Softmax
from torch.nn import Module
from torch.optim import SGD
from torch.nn import CrossEntropyLoss
from torch.nn.init import kaiming_uniform_
from torch.nn.init import xavier_uniform_
import torch
from train import MLP
from utils import get_playlist_features, get_top_tracks_with_attributes

ATTRIBUTES = ["energy", "speechiness", "acousticness", "instrumentalness", "liveness", "valence"]
NUM_CLUSTERS = 3
RANGES = ['short_term', 'medium_term', 'long_term']
CLASSIFICATION_DICT = {0: 'lofi', 1: 'party pop', 2: 'sad songs'}

# make a class prediction for one row of data
def predict(row, model):
    # convert row to data
    row = Tensor([row])
    # make prediction
    yhat = model(row)
    # retrieve numpy array
    yhat = yhat.detach().numpy()
    return yhat

def outside_predict(model, playlist_id, expected_index, attributes):
    songs = get_playlist_features(playlist_id, attributes)
    [song.pop() for song in songs] # last attribute is playlist id
    classification_count = outside_playlist_classification(model, songs)
    return classification_count[expected_index] / len(songs)

# songs should be a list of atribute lists
def outside_playlist_classification(model, songs):
    classification_count = {}
    for i in range(NUM_CLUSTERS):
        classification_count[i] = 0
    for song in songs:
        yhat = predict(song, model)
        classification_count[argmax(yhat)] += 1
    return classification_count

def key_with_max_value(dictionary):
    max_key_value = [None, float('-inf')]
    for key in dictionary.keys():
        if dictionary[key] > max_key_value[1]:
            max_key_value = [key, dictionary[key]]
    return max_key_value[0]

def main_classify():
    model = torch.load("model.pt")

    # make predictions based on my own playlists
    outside_acc_1 = outside_predict(model, "4SG13QaZvkAQmPh4BweFEs", 1, ATTRIBUTES)
    print('Accuracy for my pop playlist: %.3f' % outside_acc_1)

    # sort my listening data
    NUM_SONGS = 50 # for the listening data
    scope_to_features, id_to_song_meta = get_top_tracks_with_attributes(ATTRIBUTES)
    for sp_range in RANGES: 
        features = scope_to_features[sp_range]
        [f.pop() for f in features]
        classification_count = outside_playlist_classification(model, features)
        print("Your", sp_range, "listening has been")
        for i in range(NUM_CLUSTERS):
            print("-", round(classification_count[i] / NUM_SONGS * 100, 2), "%", CLASSIFICATION_DICT[i])