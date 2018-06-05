from flask import Flask
from app import news, weather, FirebaseManager#, FaceID

app = Flask(__name__)
fb = FirebaseManager.FirebaseManager()
#face_classification = FaceID.FaceID()
n = news.News()
w = weather.Weather()

from app.routes import *