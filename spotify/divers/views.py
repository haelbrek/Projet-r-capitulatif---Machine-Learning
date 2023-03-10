from django.shortcuts import render
from .form import TrackSearchForm
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import joblib
import pandas as pd
from django.shortcuts import render
import requests
import json
from fastapi import FastAPI, Request
from spotipy.oauth2 import SpotifyClientCredentials

client_id = "57b235e173ab4a8e819796e3d085577f"
client_secret = "588d7118aed6407096d2e70d6484d7b4"
client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
access_token = 'BQBM5Qk49-H3RgXGbbYz6koQJhWLuM5x0WRqYldhVLoynbTAAFQxuRWMr41OP8D23VVvkt6aWXQJsbUAzetPPXcBoSPjsb5VkC7ZeHcVj4R_p-7t2o-N'
def get_track_info(artist_name, track_name):
    global access_token
    url = "https://api.spotify.com/v1/search"
    params = {
        "q": f"artist:{artist_name} track:{track_name}",
        "type": "track",
        "limit": 1
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, params=params, headers=headers)
    if response.status_code != 200:
        return None
    data = response.json()
    
    if data["tracks"]["total"] == 0:
        return None
    track_id = data["tracks"]["items"][0]["id"]
    data = sp.audio_features(track_id)[0]
    
    track_url = f"https://api.spotify.com/v1/tracks/{track_id}"
    track_response = requests.get(track_url, headers=headers)
    if track_response.status_code != 200:
        return None
    track_data = track_response.json()
    year=int(track_data['album']['release_date'].split('-')[0])
    year=int(track_data['album']['release_date'].split('-')[0])
    feature={
            "duration_ms":data["duration_ms"],
            # "genre":data["danceability"],
            "danceability":data["danceability"],
            "loudness":data["loudness"],
            "acousticness":data["acousticness"],
            "instrumentalness":data["instrumentalness"],
            "duration_ms.1":data["duration_ms"],
            "year":year,
              }

    return feature

def search_track(request):
    header = {
        'accept': 'application/json',
        'Content-Type': 'application/json'}
    form1 = TrackSearchForm
    if request.method == 'POST':
        form=form1(request.POST or None)
        if form.is_valid():
            artist_name = form.cleaned_data['artist_name']
            track_name = form.cleaned_data['track_name']
            track_info = get_track_info(artist_name, track_name)
            if track_info:
                data = json.dumps(track_info)
                print(data)
                response=requests.post('http://127.0.0.1:8000/predict', headers=header, data=data)
                print(response)
                return render(request, 'formulaire.html', context={'response': response.text, 'form': form1})
            else:
                form.add_error(None, 'Could not find track')
    else:
        context={'form' : form1}
        return render(request, 'formulaire.html', context=context)
    
               


















                       #     "energy":[data["energy"]],
        #     "key":[data["key"]],
            
        #     "mode":[data["mode"]],
        #     "speechiness":[data["speechiness"]],
        #     "liveness":[data["liveness"]],
        #     "valence":[data["valence"]],
        #    "tempo": [data["tempo"]],