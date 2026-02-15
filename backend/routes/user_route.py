import datetime
import os
import time

from flask import Blueprint, jsonify, request
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename

from database import db, User, HealthySuggestion
from config import client

user_bp = Blueprint('user', __name__, url_prefix='/api')

bcrypt = Bcrypt()

UPLOAD_FOLDER = 'static'  # # Upload directory, place the image under /static
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Allowed file types

# Make sure that the upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "The username and password cannot be empty"}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"msg": "The username already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password=hashed_password, avatar='/static/assets/BlankAvatar-Cl_LpKw_.png')
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "Registration is successful"}), 201

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "The username and password cannot be empty"}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"msg": "Wrong username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    return jsonify({"msg": f"Welcome {current_user}，This is your personal information"}), 200

@user_bp.route('/user/info', methods=['GET'])
@jwt_required()
def user_info():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    data = {
        "id": user.id,
        "username": user.username,
        "height": user.height,
        "weight": user.weight,
        "age": user.age,
        "role": user.role,
    }
    return jsonify({
        "code": 0,
        "data": data,
        "message": "Success"
        }), 200

@user_bp.route('/user/info', methods=['PUT'])
@jwt_required()
def update_info():
    data = request.get_json()
    username = get_jwt_identity()
    height = data.get('height')
    weight = data.get('weight')
    age = data.get('age')
    user = User.query.filter_by(username=username).first()
    user.height = height
    user.weight = weight
    user.age = age
    db.session.commit()
    user = User.query.filter_by(username=username).first()
    data = {
        "id": user.id,
        "username": user.username,
        "height": user.height,
        "weight": user.weight,
        "age": user.age,
    }
    return jsonify({
        "code": 0,
        "data": data,
        "message": "Profile updated successfully!"
    }), 200

@user_bp.route('/health-suggestion', methods=['POST'])
@jwt_required()
def health_suggestion():
    ask = True
    data = request.get_json()
    lang = data.get('lang')
    username = get_jwt_identity()
    hs = HealthySuggestion.query.filter_by(username=username).first()
    nowTime = datetime.datetime.now()
    if hs:
        oldTime = hs.datetime
        if abs(nowTime - oldTime) < datetime.timedelta(hours=4):
            ask = False
    if ask:
        month = data.get('month')
        age = data.get('age')
        weight = data.get('weight')
        height = data.get('height')

        dic = {
            1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August",
            9: "September", 10: "October", 11: "November", 12: "December",
        }

        messages_en = [{
            "role": "assistant",
            "content": f"Suppose you are a Chinese medicine health expert, I have a user here, age is {age} years "
                       f"old, height is {height}cm, weight is {weight}kg, the current is {dic.get(month)}, please give "
                       f"conditioning suggestions, note, just reply to the suggestion, the number of words does not "
                       f"exceed 150 words, in english. Attention, Some user information may be missing, so don't "
                       f"worry about it, just respond based on what you already have"
        }]

        messages_zh = [{
            "role": "assistant",
            "content": f"假设你是一个中药养生专家，我这里有个用户，年龄{age}岁，身高{height}cm，体重{weight}kg，当前是{month}月，"
                       f"请给出调理建议，注意，只需回复建议就可以，字数不超过150字，有些用户信息可能是缺失的，那就不用管，只需要根据已有"
                       f"信息做出回应就可以"
        }]

        response_en = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages_en
        )

        response_zh = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages_zh
        )

        response_message_en = response_en.choices[0].message.content
        response_message_zh = response_zh.choices[0].message.content

        if hs:
            hs.datetime = nowTime
            hs.suggestion_en = response_message_en
            hs.suggestion_zh = response_message_zh
        else:
            hs = HealthySuggestion(username=username, datetime=nowTime, suggestion_en=response_message_en,
                                   suggestion_zh=response_message_zh)
            db.session.add(hs)
        db.session.commit()

        if lang == 'zh':
            return jsonify({
                "suggestion": response_message_zh
            }), 200
        else:
            return jsonify({
                "suggestion": response_message_en
            }), 200
    if lang == 'zh':
        return jsonify({
            "suggestion": hs.suggestion_zh
        }), 200
    else:
        return jsonify({
            "suggestion": hs.suggestion_en
        }), 200

@user_bp.route('/user/avatar', methods=['POST'])
@jwt_required()
def user_avatar():

    if 'avatar' not in request.files:
        return jsonify({'error': 'No file found!'}), 400
    avatar = request.files['avatar']

    if avatar.filename == '':
        return jsonify({'error': 'No file selected!'}), 400

    if avatar and allowed_file(avatar.filename):
        avatarName = secure_filename(avatar.filename)
        uName = f"{int(time.time())}_{avatarName}"
        filepath = os.path.join(UPLOAD_FOLDER, uName)
        avatar.save(filepath)
        username = get_jwt_identity()
        user = User.query.filter_by(username=username).first()
        user.avatar = '/' + UPLOAD_FOLDER + '/' + uName
        db.session.commit()
        return jsonify({
            'message': 'File uploaded successfully',
        }), 200

    return jsonify({'error': 'File type not allowed'}), 400

@user_bp.route('/user/getAvatar', methods=['GET'])
@jwt_required()
def get_avatar():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    return jsonify({
        'avatar': user.avatar,
    }), 200
