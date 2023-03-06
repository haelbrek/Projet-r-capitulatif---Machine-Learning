import pickle
import pandas as pd
import numpy as np
import pickle
from typing import  Optional
from fastapi import FastAPI
from pydantic import BaseModel
import joblib

pickle_in = open('api.pkl', 'rb') 
Pipeline_lr = joblib.load(pickle_in)


app = FastAPI()
class Request_Body(BaseModel):
    
    danceability : float
    energy : float
    key : int
    loudness : float
    mode : int
    speechiness :float
    acousticness :float
    instrumentalness:float
    liveness:float
    valence :float
    tempo:float
    duration_ms :int
    genre : str

@app.post('/predict')

def predict(data:Request_Body):
    new_data=pd.DataFrame(dict(data),index = [0])

    class_idx=Pipeline_lr.predict(new_data)[0]
    return  float(class_idx)

