import requests
import os
import base64
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time


def get_access_token(client_id, client_secret):
   
    client_str = f"{client_id}:{client_secret}"
    client_b64 = base64.b64encode(client_str.encode()).decode()

    headers = {"Authorization": f"Basic {client_b64}"}
    data = {"grant_type": "client_credentials"}

    
    response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)

    token_data = response.json()
    
    return token_data['access_token']

def get_track_id(artist_name, track_name,access_token):
    
    url = "https://api.spotify.com/v1/search"
    params = {
        "q": f"{artist_name} {track_name}",
        "type": "track",
        "limit": 1
    }
    response = requests.get(
        url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        },
        params=params
    )
    if response.status_code == 200:
        data = response.json()
        if data["tracks"]["items"]:
            return data["tracks"]["items"][0]["id"]
        else:
            return 'yoyo'
    else:
        return 'None'

def get_audio_features(track_id,access_token):
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    response = requests.get(
        url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"
        }
    )
    if response.status_code == 200:
        data = response.json()
        return [
            data["danceability"],
            data["energy"],
            data["key"],
            data["loudness"],
            data["mode"],
            data["speechiness"],
            data["acousticness"],
            data["instrumentalness"],
            data["liveness"],
            data["valence"],
            data["tempo"],
            data["duration_ms"],
            
        ]
    else:
        return 'none'