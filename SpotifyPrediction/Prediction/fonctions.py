import requests
import os
import base64
import requests


client_ID = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
# encode client_id and client_secret in base64
client_credentials = f"{client_ID}:{client_secret}".encode("ascii")
base64_credentials = base64.b64encode(client_credentials).decode("ascii")

# make request for access token
def get_token():
    url = "https://accounts.spotify.com/api/token"
    response = requests.post(
        url,
        headers={
            "Authorization": f"Basic {base64_credentials}",
            "Content-Type": "application/x-www-form-urlencoded"
        },
        data={"grant_type": "client_credentials"}
    )

    if response.status_code == 200:
        access_token = response.json()["access_token"]
        return response.text
        print(f"Access Token: {access_token}")
    else:
        print(f"Error: {response.text}")

def get_track_id(artist_name, track_name,token):
    global access_token
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
        return 'okok'

def get_audio_features(track_id):
    global access_token
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