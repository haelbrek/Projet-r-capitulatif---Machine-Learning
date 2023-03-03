from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Prediction(models.Model):

    tracks = models.CharField(null=False,max_length=40)
    artiste = models.CharField(null=False,max_length=40)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    popularity = models.IntegerField(null=True)
    genre = models.CharField(null=True,max_length=80)

class Parameters(models.Model) :
    duration_ms = models.PositiveIntegerField(null=True)
    danceability = models.FloatField(null=True)
    energy  = models.FloatField(null=True)
    key = models.PositiveIntegerField(null=True)
    loudness= models.FloatField(null=True)
    mode =models.IntegerField(null=True)
    speechiness = models.FloatField(null=True)
    acousticness = models.FloatField(null=True)
    instrumentalness = models.FloatField(null=True)
    liveness = models.FloatField(null=True)
    valence =models.FloatField(null=True)
    tempo = models.FloatField(null=True)
    time_signature = models.PositiveIntegerField(null=True)
    genre = models.CharField(null=True,max_length=80)
    
