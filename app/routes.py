from flask import render_template, request, send_file, abort, Markup, jsonify
from app import app, n, w, fb#,face_classification
import os
import datetime

IMAGE_FOLDER = os.path.join('Files', 'FaceID')#'smartmirror_user')
AUDIO_FOLDER = os.path.join('Files', 'Audio')
app.config['IMAGE_FOLDER'] = IMAGE_FOLDER
app.config['AUDIO_FOLDER'] = AUDIO_FOLDER


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


@app.route('/get_news', methods=['GET', 'POST'])
def get_news():
    uid = request.values.get('uid')
    category = fb.get_category(uid)
    n.news = fb.get_news()
    #category = request.args.get('category')
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
            return Markup(ret)

'''
@app.route('/getMirrorID', methods=['GET'])
def get_mirror_uid():
    uid = request.args.get('uid')
    mirror_uid = fb.get_mirror_id(uid)
    if mirror_uid is None:
        mirror_uid = "null"
    return jsonify(mirror_uid)
'''

@app.route('/get_weather', methods=['GET','POST'])
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
            full_filename = os.path.join(app.config['IMAGE_FOLDER'], uid, profile_name)
            print('send profile' + full_filename)
            return send_file(full_filename, as_attachment=True)
        except Exception as e:
            full_filename = os.path.join(app.config['IMAGE_FOLDER'], '1.jpg')
            print('send 1')
            print(e)
            return render_template("image.html", user_image=full_filename)
    else:
        print('send 1')
        full_filename = os.path.join(app.config['IMAGE_FOLDER'], '1.jpg')
        return render_template("image.html", user_image=full_filename)


@app.route("/sendSwitchStatus", methods=['GET'])
def send_switch_status():
    uid = request.args.get('uid')
    activity_name = request.args.get('activityName').split('.')
    is_checked = request.args.get('isChecked')
    mirror_uid = request.args.get('mirrorUid')

    alarm_dict = {
        activity_name[1]: is_checked
    }

    from app import connector
    try:
        if connector.mirror_list[mirror_uid].user_uid == uid:
            send_dict = {
                '/SWITCH': alarm_dict
            }
            connector.mirror_list[mirror_uid].send_msg(send_dict)
            print('pi 존재한다.')
    except Exception as e:
        pass
    finally:

        fb.update_switch(uid, alarm_dict)

    return 'True'


@app.route("/sendCategory", methods=['GET'])
def recieveCategory():
    uid = request.args.get('uid')
    category = request.args.get('category')
    print(category)
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
    return "True"


@app.route("/login", methods=['GET'])
def login():
    login_flag = False

    uid = request.args.get('uid')
    profile_name = fb.get_profile_name(uid)
    if profile_name is not None:
        try:
            full_filename = os.path.join(app.config['IMAGE_FOLDER'], uid, profile_name)
            #login_flag = face_classification.login(uid, full_filename)
        except Exception as e:
            print(e)
    print(login_flag)
    ########################### send login flag to PI


@app.route("/sendImage", methods=['POST'])
def save_image():
    mirror_uid = request.values.get('mirrorUid')
    uid = request.values.get('uid')
    file = request.files.get('Image')

    file_ext = os.path.splitext(file.filename)[1]
    file_name = datetime.datetime.now().strftime('%Y%m%d_%H-%M-%S') + file_ext

    try:
        file_dir = os.path.join(app.config['IMAGE_FOLDER'], mirror_uid, 'user_photos', uid)
        if not os.path.isdir(file_dir):
            os.makedirs(file_dir)
    except Exception as e:
        print(e)
    finally:
        file.save(file_dir +'//'+file_name)
        image_url = {
            'url': file_name
        }
        fb.update_image(uid, image_url)

    return jsonify('test')

@app.route("/getPath", methods=['GET'])
def send_path():
    startX = request.args.get('startX')
    startY = request.args.get('startY')
    endX = request.args.get('endX')
    endY = request.args.get('endY')
    return render_template('path.html',startX=startX, startY=startY, endX=endX, endY=endY)

@app.route("/sendLocation", methods=['GET', 'POST'])
def recieveLocation():
    uid = request.args.get('uid')
    location = request.args.get('location')
    category_dict = {"location": location}
    fb.update_location(uid, category_dict)
    print(location)
    return "True"