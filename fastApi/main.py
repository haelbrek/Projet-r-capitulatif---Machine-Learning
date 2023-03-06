import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
pickle_in = open('random_shearch.pkl', 'rb') 
Pipeline_lr = joblib.load(pickle_in)

app = FastAPI()
class Request_Body(BaseModel):
    duration_ms: float
    # genre: str	
    danceability: float
    loudness: float
    acousticness: float	
    instrumentalness: float	
    year: float


@app.post('/predict')

def predict(data:Request_Body):
    new_data=pd.DataFrame(dict(data),index = [0])

    class_idx=Pipeline_lr.predict(new_data)[0]
    return  float(class_idx)