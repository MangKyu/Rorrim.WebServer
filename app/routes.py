from werkzeug.datastructures import ImmutableMultiDict
from flask import render_template, request, send_file, abort, Markup, jsonify
from app import app, n, w, User, fb
import os
import datetime

IMAGE_FOLDER = os.path.join('Files', 'Image')
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
    category = request.args.get('category')
    if category is None:
        abort(400)
    else:
        try:
            if n.news[category] is None:
                abort(400)
            else:
                ret = ""
                for i in n.news[category]:
                    ret = ret + "<news>" + "<title>" + i[0] + "</title>" + "<content>" + i[1] + "</content>" + "</news>"
                #data = json.dumps(n.news[category], ensure_ascii=False)
                #return data
                return Markup(ret)
        except Exception as e:
            abort(400)

@app.route('/get_weather', methods=['GET','POST'])
def get_weather():
    info = w.get_weather()
    ret = ""
    for i in info.keys():
        ret = ret + "<" + str(i) + ">" + str(info[i]) + "</" + str(i) + ">"
    return Markup(ret)
    #return json.dumps(info, ensure_ascii=False)

'''
@app.route('/recieve_image', methods = ['GET', 'POST'])
def send_image():
    file_name = request.args.get('fileName')
    if file_name is not None:
        try:
            full_filename = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
            return render_template("image.html", user_image=full_filename)
        except Exception as e:
            abort(411)
    else:
        full_filename = os.path.join(app.config['UPLOAD_FOLDER'], '1.jpg')
        return render_template("image.html", user_image=full_filename)
'''

@app.route('/login', methods = ['POST'])
def login():
    data = request.get_json()
    user = User.User(data['id'], data['pw'], data['money'])
    return jsonify(user.getStr())


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

@app.route("/sendAlarmStatus", methods=['GET'])
def sendAlarmStatis():
    activity_name= request.args.get('activityName')
    is_checked = request.args.get('isChecked')
    alarm_dict={
        activity_name: is_checked
    }
    print('Send Status Alarm')
    #send data to pi
    return True


@app.route("/sendImage", methods=['POST'])
def sendProfileUrl():
    uid = request.values.get('uid')
    file = request.files.get('Image')
    file_ext = os.path.splitext(file.filename)[1]
    file_name = datetime.datetime.now().strftime('%Y%m%d_%H-%M-%S') + file_ext

    try:
        file_dir = os.path.join(app.config['IMAGE_FOLDER'], uid)
        if not os.path.isdir(file_dir):
            os.makedirs(file_dir)
    except Exception as e:
        print(e)
    finally:
        file.save(file_dir +'//'+file_name)
        image_url = {
            'url':file_name
        }
        fb.update_image(uid, image_url)

    return jsonify('test')
