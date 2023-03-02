from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from . import models
# Create your forms here.

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		
		fields = ["username", "email", "password1", "password2"]
    
	def __init__(self, *args, **kwargs):
		super(NewUserForm, self).__init__(*args, **kwargs)
		self.fields['email'].label = "Veuillez entrer votre adresse mail"
		self.fields['password1'].label = "Veuillez entrer votre mot de passe"
		self.fields['password2'].label = "Veuillez confirmer votre mot de passe"
	
	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class SearchForm(forms.ModelForm):
	
	class Meta:
		model = models.Prediction
		fields = ['tracks','artiste']
		labels = {
			'tracks' : 'Choisissez le nom de la chanson',
			'artiste' : "Choisissez le nom de l'artiste"
		}

