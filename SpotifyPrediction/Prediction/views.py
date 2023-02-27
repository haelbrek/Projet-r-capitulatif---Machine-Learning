from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . import forms
import requests
import json
from django.shortcuts import redirect
from .fonctions import *


def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Inscription réussie.")
			return render(request,"homepage.html")
		messages.error(request, "Les informations renseignées ne sont pas conformes.")
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
				messages.info(
					request, f"Vous etes connecté en tant que {username}.")
				return render(request,"homepage.html")
			else:
				messages.error(request, "Mot de passe ou pseudo invalide")
		else:
			messages.error(request, "Mot de passe ou pseudo invalide")
	form = AuthenticationForm()
	return render(request=request, template_name="connexion.html", context={"login_form": form})


def homepage_view(request):

	predict = forms.SearchForm
	headers = {'accept': 'application/json',
			   'Content-Type': 'application/json'}
	get_token()
	
	if request.method == 'POST':
		form = predict(request.POST or None)
		if form.is_valid():
			url = ''
			query = form.cleaned_data
			print(query)
			#utilisez la query pour requeter l'api de spotify
			id = get_track_id(query['artiste'],query['tracks'])
			res = get_audio_features(id)

			features = res.text 
			model = requests.post(url = url, data = features,headers=headers)
			model_result = model.text

			return render(request,'result.html',context= {'result' : model_result})
			
	else:
		return render(request, "homepage.html",context = {'predict':  predict})

def profil_request(request):
	return render(request,'profil.html')

