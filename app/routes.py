from flask import render_template, request, send_file, abort, Markup, jsonify
from app import app, n, w, fb, face_classification
import os
import datetime, time
from pyrebase import pyrebase
from shutil import copyfile

IMAGE_FOLDER = os.path.join('Files', 'FaceID')
AUDIO_FOLDER = os.path.join('Files', 'Audio')
PROFILE_FOLDER = os.path.join('Files', 'Profile')
app.config['IMAGE_FOLDER'] = IMAGE_FOLDER
app.config['AUDIO_FOLDER'] = AUDIO_FOLDER
app.config['PROFILE_FOLDER'] = PROFILE_FOLDER
config = {
  "apiKey": "AIzaSyAByxlclpYZDLQBk5Enmeg7ImrLlfsD9yU",
  "authDomain": "smartmirror-75b89.firebaseapp.com",
  "databaseURL": "https://smartmirror-75b89.firebaseio.com",
  "storageBucket": "smartmirror-75b89.appspot.com",
  "serviceAccount": "Files/Auth/smartmirror-75b89-firebase-adminsdk-vx8is-56d6e1cacc.json"
}

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/get_json', methods=['GET'])
def get_json():
    data = [{"name": "Ford", "models": ["Fiesta", "Focus", "Mustang"]}, {"name": "BMW", "models": ["320", "X3", "X5"]},
     {"name": "Fiat", "models": ["500", "Panda"]}]
    return jsonify(data)


@app.route('/recieve_file', methods=['GET','POST'])
def get_file():
    file_name = request.args.get('fileName')
    if file_name is not None:
        try:
            return send_file(os.path.dirname(os.path.realpath(__file__))+"/files/"+file_name, as_attachment=True)
        except Exception as e:
            abort(400)
    else:
        abort(400)


@app.route('/sendUserInfo', methods=['POST'])
def set_user_info():
    mirror_uid = request.values.get('mirror_uid')
    user_uid = request.values.get('user_uid')
    from app import connector
    try:
        connector.mirror_list[mirror_uid].user_uid = user_uid
    except Exception as e:
        print(e)
    return jsonify('True')


@app.route('/setMirror', methods=['POST'])
def set_mirror():
    mirror_uid = request.values.get('mirrorUid')
    user_uid = request.values.get('uid')
    email = request.values.get('email')

    auth_code = 'auth'

    from app import connector
    auth_flag = connector.authenticate(mirror_uid, '/AUTH', auth_code)
    if auth_flag == 'True':
        user_dict = {
            user_uid : email
        }
        fb.update_user(mirror_uid, user_dict)
    # we have to do => send socket amd accept authentication
    print(auth_flag)
    return auth_flag


@app.route('/getNews', methods=['POST'])
def get_news():
    uid = request.values.get('uid')
    if uid == 'None':
        category = 'world'
    else:
        category = fb.get_category(uid)
    n.news = fb.get_news()
    if category is None:
        category = 'world'
    else:
        try:
            if n.news[category] is None:
                n.news = fb.get_news()
        except Exception as e:
            abort(400)
            #firebase로부터 Data 얻어오기
        finally:#else:
            ret = ""
            for i in n.news[category]:
                ret = ret + "<news>" + "<title>" + i[0] + "</title>" + "<content>" + i[1] + "</content>" + "</news>"
            #data = json.dumps(n.news[category], ensure_ascii=False)
            #return jsonify(ret)
            print('news')
            return Markup(ret)


@app.route('/getWeather', methods=['GET','POST'])
def get_weather():
    print('get_weather')
    weather_data = fb.get_weather()
    return jsonify(weather_data)


@app.route('/profileImage.jpg', methods=['GET', 'POST'])
def send_image():
    uid = request.args.get('fileName')
    profile_name = fb.get_profile_name(uid)
    if profile_name is not None:
        try:
            full_filename = os.path.join(app.config['PROFILE_FOLDER'], profile_name)
            print('send profile' + full_filename)
            return send_file(full_filename, as_attachment=True)
        except Exception as e:
            full_filename = os.path.join(app.config['IMAGE_FOLDER'], '1.jpg')
            print('send 1')
            print(e)
            return render_template("image.html", user_image=full_filename)
    else:
        print('send 2')
        full_filename = os.path.join(app.config['IMAGE_FOLDER'], '1.jpg')
        return render_template("image.html", user_image=full_filename)


@app.route("/sendImage", methods=['POST'])
def save_image():
    mirror_uid = request.values.get('mirrorUid')
    uid = request.values.get('uid')
    file = request.files.get('Image')

    file_ext = os.path.splitext(file.filename)[1]
    file_name = uid + '_' + datetime.datetime.now().strftime('%Y%m%d_%H-%M-%S') + file_ext

    try:
        file_dir = os.path.join(app.config['IMAGE_FOLDER'], mirror_uid, 'user_photos', uid)
        if not os.path.isdir(file_dir):
            os.makedirs(file_dir)
    except Exception as e:
        print(e)
    finally:
        file_path = file_dir + '//' + file_name
        file.save(file_path)
        image_url = {
            'url': file_name
        }
        fb.update_image(uid, image_url)
        copyfile(file_path, app.config['PROFILE_FOLDER'] +'//' + file_name)
        #file = open(file_path, 'rb')
        #file.save(app.config['PROFILE_FOLDER'] +'//' + file_name)

    return jsonify('test')

@app.route("/sendSwitchStatus", methods=['GET'])
def send_switch_status():
    uid = request.args.get('uid')
    activity_name = request.args.get('activityName').split('.')
    is_checked = request.args.get('isChecked')
    mirror_uid = request.args.get('mirrorUid')

    alarm_dict = {activity_name[1]: is_checked }

    from app import connector
    msg = connector.update_pi(mirror_uid, uid, '/SWITCH', alarm_dict)
    fb.update_switch(uid, alarm_dict)
    return msg


@app.route("/sendCategory", methods=['POST'])
def get_category():
    uid = request.values.get('uid')
    category = request.values.get('category')
    mirror_uid = request.values.get('mirrorUid')

    if category == '정치':
        category = 'politics'
    elif category == '경제':
        category = 'economy'
    elif category == '사회':
        category = 'society'
    elif category == '생활/문화':
        category = 'life'
    elif category == '세계':
        category = 'world'
    elif category == 'IT/과학':
        category = 'it'
    else:
        category = 'world'
    category_dict = {'category': category}
    fb.update_category(uid, category_dict)

    from app import connector
    msg = connector.update_pi(mirror_uid, uid, '/NEWS', 'UPDATE NEWS')

    return msg


@app.route("/login", methods=['POST'])
def login():
    mirror_uid = request.values.get('mirror_uid')
    file = request.files.get('file_name')
    uid = None
    if file is not None or mirror_uid is not None:
        try:
            file_path = os.path.join(app.config['IMAGE_FOLDER'], mirror_uid, 'test.jpg')
            file.save(file_path)
            uid= face_classification.login(mirror_uid)
        except Exception as e:
            print(e)
    print(uid)
    return jsonify(uid)


@app.route("/getPath", methods=['GET'])
def send_path():
    startX = request.args.get('startX')
    startY = request.args.get('startY')
    endX = request.args.get('endX')
    endY = request.args.get('endY')
    return render_template('path.html',startX=startX, startY=startY, endX=endX, endY=endY)


@app.route("/sendLocation", methods=['GET', 'POST'])
def get_location():
    latitude = request.values.get('latitude')
    longitude = request.values.get('longitude')
    uid = request.values.get('uid')

    location_dict = {
        "latitude": latitude,
        "longitude": longitude
    }

    fb.update_location(uid, location_dict)
    return 'True'

@app.route('/getMusic', methods=['GET', 'POST'])
def get_music():
    mirror_uid = request.values.get('mirrorUid')
    uid = request.values.get('uid')
    fileName = request.values.get('fileName')
    file_dir = ''

    try:
        print('start')
        file_dir = os.path.join(app.config['AUDIO_FOLDER'], mirror_uid, 'music', uid)
        if not os.path.isdir(file_dir):
            os.makedirs(file_dir)
    except Exception as e:
        print(e)
    finally:
        #pyrebse 접근
        firebase = pyrebase.initialize_app(config)

        # Get a reference to the auth service
        auth = firebase.auth()

        # Get a reference to the database service
        db = firebase.database()

        # Get user key in database
        storage = firebase.storage()
        print(fileName)
        storage.child(uid + "/" + fileName).download(file_dir + "//" + fileName)
        trigger = {'update': fileName}

        from app import connector
        msg = connector.update_pi(mirror_uid, uid, '/PLAYLIST', trigger)

        return 'true'

@app.route("/getPlayList", methods=['GET', 'POST'])
def playList():
    mirror_uid = request.values.get('mirrorUid')
    uid = request.values.get('uid')
    dic = {}
    i = 0
    path_dir = os.path.join(app.config['AUDIO_FOLDER'], mirror_uid, 'music', uid)
    if not os.path.isdir(path_dir):
        os.makedirs(path_dir)
    file_list = os.listdir(path_dir)
    for word in file_list:
        dic[i] = word
        i = i + 1
    print(dic)
    return jsonify(dic)

@app.route('/removeMusic', methods=['GET', 'POST'])
def remove():
    mirror_uid = request.values.get('mirrorUid')
    uid = request.values.get('uid')
    fileName = request.values.get('fileName')
    artist = request.values.get('artist')
    song = request.values.get('song')
    file_dir = os.path.join(app.config['AUDIO_FOLDER'], mirror_uid, 'music', uid)
    file = file_dir + '//' + fileName
    print(file)
    # pyrebse 접근
    firebase = pyrebase.initialize_app(config)

    # Get a reference to the auth service
    auth = firebase.auth()

    # Get a reference to the database service
    db = firebase.database()

    if os.path.isfile(file):
        os.remove(file)
        fb.remove_music(uid, artist, song)
        trigger = {'remove': fileName}

        from app import connector
        msg = connector.update_pi(mirror_uid, uid, '/PLAYLIST', trigger)

        return 'true'
    else:
        return 'false'

@app.route("/getMusicFile", methods=['GET', 'POST'])
def get_playlist():
    mirror_uid = request.values.get('mirrorUid')
    uid = request.values.get('uid')
    fileName = request.values.get('fileName')

    file_dir = os.path.join(app.config['AUDIO_FOLDER'], mirror_uid, 'music', uid)
    try:
        return send_file(file_dir + '//' + fileName, attachment_filename=fileName);
    except Exception as e:
        print(e)
        return 'false'


@app.route("/setName", methods=['GET', 'POST'])
def set_name():
    uid = request.values.get('uid')
    name = request.values.get('name')
    name_dic = {'name' : name}
    fb.update_name(uid, name_dic)

    return 'true'