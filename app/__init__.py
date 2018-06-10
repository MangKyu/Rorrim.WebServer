
from flask import Flask
from app import news, weather, FirebaseManager, pi_connector, FaceID

host = '0.0.0.0'
#host = 'sd100.iptime.org'
#host = '203.213.123.123'
#host = '14.42.10.176'
#host = '192.168.0.3'
#host = '172.16.28.163'
#host = '203.252.166.206'
socket_port = 8099

app = Flask(__name__)
fb = FirebaseManager.FirebaseManager()
face_classification = FaceID.FaceID()
#mirror_list = []
connector = pi_connector.pi_connector(host, socket_port)

n = news.News()#mirror_list)
w = weather.Weather()#mirror_list)
from app.routes import *