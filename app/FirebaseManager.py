
import firebase_admin
from firebase_admin import credentials, db

class FirebaseManager:

    def __init__(self):
        cred = credentials.Certificate('Files/Auth/smartmirror-75b89-firebase-adminsdk-vx8is-56d6e1cacc.json')
        #default_app = firebase_admin.initialize_app(cred)
        firebase_admin.initialize_app(cred, {
            'databaseURL' : 'https://smartmirror-75b89.firebaseio.com'
        })
        self.root = db.reference()
        self.weather = self.root.child('weather')
        self.image = self.root.child('image')
        self.news = self.root.child('news')
        self.status = self.root.child('status')

    def update_weather(self, weather_data):
        self.weather.update(weather_data)

    def get_weather(self):
        weather_data = db.reference('weather'.format(self.weather.key)).get()
        return weather_data

    def update_image(self, uid, image_url):
        self.root.child('user').child(uid).update(image_url)

    def update_user(self, mirror_uid, user_dict):
        self.root.child('rorrim').child(mirror_uid).update(user_dict)

    def get_profile_name(self, uid):
        return self.image.child(uid).child('url').get()

    def update_news(self, news_data):
        self.news.update(news_data)

    def update_switch(self, uid, alarm_dict):
        self.root.child('user').child(uid).child('status').update(alarm_dict)

    def update_category(self, uid, category_dict):
        self.root.child('user').child(uid).update(category_dict)

    def update_location(self, uid, location_dict):
        self.root.child('user').child(uid).update(location_dict)

    def get_user_list(self, mirror_uid):
        user_list = self.root.child('rorrim').child(mirror_uid).get().keys()
        return list(user_list)

    def get_category(self, uid):
        return self.root.child('user').child(uid).child('category').get()

    def get_news(self):
        return self.news.get()
