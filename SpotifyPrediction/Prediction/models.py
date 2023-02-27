from django.db import models


class Prediction(models.Model):

    tracks = models.CharField(null=False,max_length=40)
    artiste = models.CharField(null=False,max_length=40)
    # duration_ms = models.PositiveIntegerField()
    # explicit = models.PositiveIntegerField()
    # danceability = models.FloatField()
    # energy  = models.FloatField()
    # key = models.PositiveIntegerField()
    # loudness= models.PositiveIntegerField()
    # mode =models.PositiveIntegerField()
    # speechiness = models.FloatField()
    # acousticness = models.FloatField()
    # instrumentalness = models.FloatField()
    # liveness = models.FloatField()
    # valence =models.FloatField()
    # tempo = models.FloatField()
    # time_signature = models.PositiveIntegerField()