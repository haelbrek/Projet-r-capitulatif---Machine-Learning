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
            tracks = request.POST.get('tracks')
        artiste = request.POST.get('artiste')
        query = form.cleaned_data
        access_token = get_access_token(client_ID, client_secret)

        # utilisez la query pour requeter l'api de spotify
        id = get_track_id(query['artiste'], query['tracks'], access_token)
        res = get_audio_features(id, access_token)
        col_names = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
                     'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms']

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
        )

        parameters.save()

        model = requests.post(url=url, data=features, headers=headers)
        model_result = round(float(model.text), 0)
        form(
            tracks=tracks,
            artiste=artiste,
            user=request.user,
            popularity=model_result

        )
        form.save()
        return render(request, 'result.html', context={'result': model_result})

    else:
        return render(request, "homepage.html", context={'predict':  predict})


def profil_request(request):
    labels = []
    data = []
    history = Prediction.objects.filter(user=request.user)

    return render(request, 'profil.html',context = {'history':history})
