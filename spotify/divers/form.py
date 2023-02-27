from django import forms 


class TrackSearchForm (forms.Form) :
    artist_name=forms.CharField(initial="Ray LaMontagne")
    track_name=forms.CharField(initial="I Was Born To Love You")
    
    