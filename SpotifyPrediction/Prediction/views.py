from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . import forms
import requests
import json
from django.shortcuts import redirect
from .fonctions import *
import os
from .models import Parameters,Prediction
from dotenv import load_dotenv
import requests

liste_genre = ['acoustic', 'afrobeat', 'alt-rock', 'alternative', 'ambient',
       'anime', 'black-metal', 'bluegrass', 'blues', 'brazil',
       'breakbeat', 'british', 'cantopop', 'chicago-house', 'children',
       'chill', 'classical', 'club', 'comedy', 'country', 'dance',
       'dancehall', 'death-metal', 'deep-house', 'detroit-techno',
       'disco', 'drum-and-bass', 'dub', 'dubstep', 'edm', 'electro',
       'electronic', 'emo', 'folk', 'forro', 'french', 'funk', 'garage',
       'german', 'gospel', 'goth', 'grindcore', 'groove', 'grunge',
       'guitar', 'happy', 'hard-rock', 'hardcore', 'hardstyle',
       'heavy-metal', 'hip-hop', 'honky-tonk', 'house', 'idm', 'indian',
       'indie', 'indie-pop', 'industrial', 'iranian', 'j-dance', 'j-idol',
       'j-pop', 'j-rock', 'jazz', 'k-pop', 'kids', 'latin', 'latino',
       'malay', 'mandopop', 'metal', 'metalcore', 'minimal-techno', 'mpb',
       'new-age', 'opera', 'pagode', 'party', 'piano', 'pop', 'pop-film',
       'power-pop', 'progressive-house', 'psych-rock', 'punk',
       'punk-rock', 'r-n-b', 'reggae', 'reggaeton', 'rock', 'rock-n-roll',
       'rockabilly', 'romance', 'sad', 'salsa', 'samba', 'sertanejo',
       'show-tunes', 'singer-songwriter', 'ska', 'sleep', 'songwriter',
       'soul', 'spanish', 'study', 'swedish', 'synth-pop', 'tango',
       'techno', 'trance', 'trip-hop', 'turkish', 'world-music']
def get_genre(track_name,artist_name,liste_genre):

    base_url = 'http://ws.audioscrobbler.com/2.0/'
    params = {'method': 'track.gettoptags',
            'artist': artist_name,
            'track': track_name,
            'api_key': 'd30646344918494a4e45ea08ad6fc629',
            'format': 'json'}

    # Make the request to LastFM

    response = requests.get(base_url, params=params)
    # Check to make sure the request was successful
    if response.status_code == 200:
        # Get the tags from the response
        tags = response.json().get('toptags', {}).get('tag', [])
        for tag in tags:
            
            if tag.get('name') in liste_genre:
                print(tag.get('name'))
                return tag.get('name')
                    

        
    

load_dotenv()
client_ID = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Inscription réussie.")
            return redirect('home')
        messages.error(
            request, "Les informations renseignées ne sont pas conformes.")
    form = NewUserForm()

    return render(request=request, template_name="inscription.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm(

        )
        return render(request=request, template_name="connexion.html", context={"login_form": form})


def homepage_view(request):

    predict = forms.SearchForm
    headers = {'accept': 'application/json',
               'Content-Type': 'application/json'}

    if request.method == 'POST':
        form = predict(request.POST or None)
        if form.is_valid():

            url = 'http://127.0.0.1:8001/predict'
            
            query = form.cleaned_data
            access_token = get_access_token(client_ID, client_secret)
            # utilisez la query pour requeter l'api de spotify
            id = get_track_id(query['artiste'], query['tracks'], access_token)
            res = get_audio_features(id, access_token)
           

            stock = get_genre(f"{query['tracks']}" , f"{query['artiste']}", liste_genre)
            # stock = get_genre('Shape of you','Ed Sheeran',liste_genre)

            print(stock)

            res.append(stock)
            col_names = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
                        'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms','genre']

            features = json.dumps(dict(zip(col_names, res)))

            parameters = Parameters(
                danceability=res[0],
                energy=res[1],
                key=res[2],
                loudness=res[3],
                mode=res[4],
                speechiness=res[5],
                acousticness=res[6],
                instrumentalness=res[7],
                liveness=res[8],
                valence=res[9],
                tempo=res[10],
                duration_ms=res[11],
                genre = str(res[12])
            )
            
            parameters.save()
            
            model = requests.post(url=url, data=features, headers=headers)
            model_result = int(round(float(model.text),0))
            historique = Prediction(
                tracks=query['tracks'],
                artiste=query['artiste'],
                user=request.user,
                popularity=model_result,
                genre = str(res[12])

            )
            historique.save()
            return render(request, 'result.html', context={'result': model_result})

    else:
        return render(request, "homepage.html", context={'predict':  predict})


def profil_request(request):
    
    genres = []

    queryset = Prediction.objects.filter(user=request.user)
    for obj in queryset:
        genres.append(obj.genre)
    dico = dict((x,genres.count(x)) for x in set(genres))
    labels =dico.keys()
    data= dico.values()
    print(dico)
    [((elt*100)/sum(data)) for elt in data]
    
    

    return render(request, 'profil.html',context = {'labels':labels, 'data':data , 'historic':queryset})
