from django.urls import path # Import du module Path  
from .views import * # Import de notre fichier views

urlpatterns = [
    path("", homepage_view, name="home"),
    path("inscription/", register_request, name="inscription")]