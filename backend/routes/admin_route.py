import json
import os
import re
import time

from flask import Blueprint, jsonify, request
from fuzzywuzzy import fuzz
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from collections import defaultdict

from database import db, Herb, Prescription, ChinesePrescription, ChineseHerb, User, Image

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

bcrypt = Bcrypt()

UPLOAD_FOLDER = 'static'  # Upload directory, place the image under /static
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Allowed file types

# Make sure that the upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# The location where the logs are stored
GUNICORN_ACCESS_LOG = "logs/gunicorn_access.log"
GUNICORN_ERROR_LOG = "logs/gunicorn_error.log"


@admin_bp.route('/addHerb', methods=['POST'])
def add_herb():
    data = request.get_json()
    standardAction = data.get('action')
    id = data.get('id')
    name_en = data.get('name_en')
    name_zh = data.get('name_zh')
    category_en = data.get('category_en')
    category_zh = data.get('category_zh')
    origin_en = data.get('origin_en')
    origin_zh = data.get('origin_zh')
    production_regions_en = data.get('production_regions_en')
    production_regions_zh = data.get('production_regions_zh')
    properties_en = data.get('properties_en')
    properties_zh = data.get('properties_zh')
    functions_en = data.get('functions_en')
    functions_zh = data.get('functions_zh')
    image_en = data.get('image_en')
    image_zh = data.get('image_zh')
    classification_en = data.get('classification_en')
    classification_zh = data.get('classification_zh')

    prescriptions_en = Prescription.query.all()
    relate_en = []
    for prescription in prescriptions_en:
        cons = prescription.constitute
        result = cons.split(';')
        stander_result = [item.strip().lower() for item in result]
        stander_name = name_en.strip().lower()
        if stander_name in stander_result:
            relate_en.append(prescription.id)
    relate_json_en = json.dumps(relate_en)

    prescriptions_zh = ChinesePrescription.query.all()
    relate_zh = []
    for prescription in prescriptions_zh:
        cons = prescription.constitute
        result = cons.split(';')
        stander_result = [item.strip().lower() for item in result]
        stander_name = name_zh.strip().lower()

        # Fuzzy matching
        for item in stander_result:
            similarity = fuzz.ratio(stander_name, item)
            if similarity >= 80:
                relate_zh.append(prescription.id)
                break

    relate_json_zh = json.dumps(relate_zh)

    if standardAction == 1:
        herb = Herb(name=name_en, category=category_en, origin=origin_en, production_regions=production_regions_en,
                    properties=properties_en, functions=functions_en, image=image_en, classification=classification_en,
                    relate_prescription=relate_json_en)
        cHerb = ChineseHerb(name=name_zh, category=category_zh, origin=origin_zh,
                            production_regions=production_regions_zh,
                            properties=properties_zh, functions=functions_zh, image=image_zh,
                            classification=classification_zh, relate_prescription=relate_json_zh)
        db.session.add(herb)
        db.session.add(cHerb)
    else:
        herb = Herb.query.filter_by(id=id).first()
        cHerb = ChineseHerb.query.filter_by(id=id).first()

        herb.name = name_en
        herb.category = category_en
        herb.origin = origin_en
        herb.production_regions = production_regions_en
        herb.properties = properties_en
        herb.functions = functions_en
        herb.image_en = image_en
        herb.classification = classification_en
        herb.relate_prescription = relate_json_en

        cHerb.name = name_zh
        cHerb.category = category_zh
        cHerb.origin = origin_zh
        cHerb.production_regions = production_regions_zh
        cHerb.properties = properties_zh
        cHerb.functions = functions_zh
        cHerb.image_en = image_zh
        cHerb.classification = classification_zh
        cHerb.relate_prescription = relate_json_zh

    db.session.commit()
    return jsonify({'message': 'Success!'})


@admin_bp.route('/deleteHerb', methods=['DELETE'])
def delete_herb():
    data = request.get_json()
    id = data.get('id')
    herb = Herb.query.filter_by(id=id).first()
    cHerb = ChineseHerb.query.filter_by(id=id).first()
    db.session.delete(herb)
    db.session.delete(cHerb)
    db.session.commit()
    return jsonify({
        'code': 0,
        'message': 'Success!',
        'data': None
    })


@admin_bp.route('/addPrescription', methods=['POST'])
def add_prescription():
    data = request.get_json()
    standardAction = data.get('action')
    id = data.get('id')
    name_en = data.get('name_en')
    name_zh = data.get('name_zh')
    constitute_en = data.get('constitute_en')
    constitute_zh = data.get('constitute_zh')
    action_en = data.get('action_en')
    action_zh = data.get('action_zh')
    indication_en = data.get('indication_en')
    indication_zh = data.get('indication_zh')

    if standardAction == 1:
        constituteNumber = len(constitute_en.split(';'))
        pre = Prescription(name=name_en, constitute=constitute_en, action=action_en, indication=indication_en,
                           constituteNumber=constituteNumber)
        constituteNumber = len(constitute_zh.split(';'))
        cPre = ChinesePrescription(name=name_zh, constitute=constitute_zh, action=action_zh, indication=indication_zh,
                                   constituteNumber=constituteNumber)
        db.session.add(pre)
        db.session.add(cPre)
    else:
        pre = Prescription.query.filter_by(id=id).first()
        cPre = ChinesePrescription.query.filter_by(id=id).first()
        constituteNumber = len(constitute_en.split(';'))
        pre.name = name_en
        pre.constitute = constitute_en
        pre.action = action_en
        pre.indication = indication_en
        pre.constituteNumber = constituteNumber
        constituteNumber = len(constitute_zh.split(';'))
        cPre.name = name_zh
        cPre.constitute = constitute_zh
        cPre.action = action_zh
        cPre.indication = indication_zh
        cPre.constituteNumber = constituteNumber
    db.session.commit()
    return jsonify({'message': 'Success!'})


@admin_bp.route('/getHerbDetails/<int:id>', methods=['GET'])
def get_herb_detail(id):
    herb = Herb.query.filter_by(id=id).first()
    cHerb = ChineseHerb.query.filter_by(id=id).first()
    return jsonify({
        'id': id,
        'name_en': herb.name,
        'name_zh': cHerb.name,
        "category_en": herb.category,
        "origin_en": herb.origin,
        "production_regions_en": herb.production_regions,
        "properties_en": herb.properties,
        "functions_en": herb.functions,
        "image_en": herb.image,
        "classification_en": herb.classification,
        "category_zh": cHerb.category,
        "origin_zh": cHerb.origin,
        "production_regions_zh": cHerb.production_regions,
        "properties_zh": cHerb.properties,
        "functions_zh": cHerb.functions,
        "image_zh": cHerb.image,
        "classification_zh": cHerb.classification,
    })


@admin_bp.route('/getPrescriptionDetails/<int:id>', methods=['GET'])
def get_prescription_details(id):
    prescription = Prescription.query.filter_by(id=id).first()
    cPrescription = ChinesePrescription.query.filter_by(id=id).first()
    return jsonify({
        'id': id,
        'name_en': prescription.name,
        'name_zh': cPrescription.name,
        "constitute_en": prescription.constitute,
        "action_en": prescription.action,
        "indication_en": prescription.indication,
        "constitute_zh": cPrescription.constitute,
        "action_zh": cPrescription.action,
        "indication_zh": cPrescription.indication,
    })


@admin_bp.route('/deletePrescription', methods=['DELETE'])
def delete_prescription_group():
    data = request.get_json()
    id = data.get('id', 1)

    # Look for both Chinese and English records
    pre_en = Prescription.query.filter_by(id=id).first()
    pre_zh = ChinesePrescription.query.filter_by(id=id).first()

    if not pre_en and not pre_zh:
        return jsonify({'error': 'Neither prescription found'}), 404

    deleted_ids = []
    if pre_en:
        deleted_ids.append(pre_en.id)
        db.session.delete(pre_en)
        db.session.commit()
    if pre_zh:
        deleted_ids.append(pre_zh.id)
        db.session.delete(pre_zh)
        db.session.commit()

    # Update the relate_prescription field for all Herbs
    herbs = Herb.query.all()
    for herb in herbs:
        try:
            relate_ids = json.loads(herb.relate_prescription)
        except:
            relate_ids = []
        print(relate_ids)
        original_len = len(relate_ids)
        relate_ids = [id for id in relate_ids if id not in deleted_ids]

        if len(relate_ids) != original_len:
            herb.relate_prescription = json.dumps(relate_ids)
            db.session.commit()

    herbs = ChineseHerb.query.all()
    for herb in herbs:
        try:
            relate_ids = json.loads(herb.relate_prescription)
        except:
            relate_ids = []

        original_len = len(relate_ids)
        relate_ids = [id for id in relate_ids if id not in deleted_ids]

        if len(relate_ids) != original_len:
            herb.relate_prescription = json.dumps(relate_ids)
            db.session.commit()

    return jsonify({'message': 'Prescription group and related herb links deleted successfully!'})


@admin_bp.route('/deleteUser', methods=['DELETE'])
def delete_user():
    data = request.get_json()
    id = data.get('id')
    user = User.query.filter_by(id=id).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully!'})


@admin_bp.route('/updateUser', methods=['PUT'])
def update_user():
    data = request.get_json()
    id = data.get('id')
    username = data.get('username')
    password = data.get('password')
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    height = data.get('height')
    weight = data.get('weight')
    age = data.get('age')
    role = data.get('role')
    user = User.query.filter_by(id=id).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    user.username = username
    if user.password != password:
        user.password = hashed_password
    user.height = height
    user.weight = weight
    user.age = age
    user.role = role
    db.session.commit()
    return jsonify({'message': 'User updated successfully!'})


@admin_bp.route('/getAllUsers', methods=['GET'])
def get_all_user():
    users = User.query.all()
    result = []
    for user in users:
        result.append({
            'id': user.id,
            'username': user.username,
            'password': user.password,
            'height': user.height,
            'weight': user.weight,
            'age': user.age,
            'role': user.role,
            'avatar': user.avatar
        })
    return jsonify({
        'code': 0,
        'data': result
    })


@admin_bp.route('/addUser', methods=['POST'])
def add_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    height = data.get('height')
    weight = data.get('weight')
    age = data.get('age')
    role = data.get('role')
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    try:
        user = User(username=username, password=hashed_password, height=height, weight=weight, age=age, role=role)
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': 'The Username may duplicate'
        }), 404
    return jsonify({'message': 'User added successfully!'})


@admin_bp.route('/addMainImage', methods=['POST'])
def add_main_image():
    data = request.get_json()
    imageUrl_en = data.get('imageUrl_en')
    imageUrl_zh = data.get('imageUrl_zh')
    new_image = Image(imageUrl_en=imageUrl_en, imageUrl_zh=imageUrl_zh)
    try:
        db.session.add(new_image)
        db.session.commit()
        return jsonify({'message': 'Image added successfully!'})
    except:
        return jsonify({'message': 'Something went wrong!'}), 500


@admin_bp.route('/deleteMainImage', methods=['POST'])
def delete_main_image():
    data = request.get_json()
    image_id = data.get('image_id')
    image = Image.query.filter_by(id=image_id).first()
    try:
        db.session.delete(image)
        db.session.commit()
        return jsonify({'message': 'Image deleted successfully!'})
    except:
        return jsonify({'message': 'Something went wrong!'}), 500


@admin_bp.route('/uploadImages', methods=['POST'])
def upload_banner():
    if 'image_en' not in request.files or 'image_zh' not in request.files:
        return jsonify({'error': 'No file found!'}), 400

    file_en = request.files['image_en']
    file_zh = request.files['image_zh']
    if file_en.filename == '' or file_zh.filename == '':
        return jsonify({'error': 'No file selected!'}), 400
    if file_en and allowed_file(file_en.filename) and file_zh and allowed_file(file_zh.filename):
        filename_en = secure_filename(file_en.filename)
        filename_zh = secure_filename(file_zh.filename)

        # Add timestamps to prevent duplicate names
        unique_filename_en = f"{int(time.time())}_{filename_en}"
        unique_filename_zh = f"{int(time.time()) + 1}_{filename_zh}"
        filepath_en = os.path.join(UPLOAD_FOLDER, unique_filename_en)
        filepath_zh = os.path.join(UPLOAD_FOLDER, unique_filename_zh)
        file_en.save(filepath_en)
        file_zh.save(filepath_zh)

        # Save the file path to the database
        new_image = Image(imageUrl_en='/' + UPLOAD_FOLDER + '/' + unique_filename_en,
                          imageUrl_zh='/' + UPLOAD_FOLDER + '/' + unique_filename_zh)
        db.session.add(new_image)
        db.session.commit()

        return jsonify({
            'message': 'File uploaded successfully',
            'filename': unique_filename_en,
            'path': filepath_en
        }), 200

    return jsonify({'error': 'File type not allowed'}), 400


@admin_bp.route('/changeUserAvatar/<int:userId>', methods=['POST'])
def change_user_avatar(userId):
    uName = ''
    if 'avatar' not in request.files:
        return jsonify({'error': 'No file found!'}), 400
    avatar = request.files['avatar']

    if avatar.filename == '':
        return jsonify({'error': 'No file selected!'}), 400

    if avatar and allowed_file(avatar.filename):
        avatarName = secure_filename(avatar.filename)
        uName = f"{int(time.time())}_{avatarName}"
        user = User.query.filter_by(id=userId).first()
        filepath = os.path.join(UPLOAD_FOLDER, uName)
        avatar.save(filepath)
        user.avatar = '/' + UPLOAD_FOLDER + '/' + uName
        db.session.commit()
        return jsonify({
            'message': 'File uploaded successfully',
        }), 200
    return jsonify({'error': 'File type not allowed'}), 400


@admin_bp.route('/log', methods=['POST'])
def show_log():
    try:
        with open(GUNICORN_ACCESS_LOG, 'r') as f:
            lines = f.readlines()[-1000:]
            Alogs = ''.join(lines)

        with open(GUNICORN_ERROR_LOG, 'r') as f:
            lines = f.readlines()[-1000:]
            Elogs = ''.join(lines)

        return jsonify({
            'status': 'success',
            'Alogs': Alogs,
            'Elogs': Elogs
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to read logs: {str(e)}'
        }), 500

@admin_bp.route('/analyze-logs', methods=['GET'])
def analyze_logs():
    # Log file path
    log_file_path = "logs/gunicorn_access.log"

    # Define regular expressions
    url_pattern = re.compile(r'"([^"]+)"\s+\d+\s+\d+\s+"([^"]*)"')

    # Create a dictionary that counts the number of visits to each URL
    url_count = defaultdict(int)

    # Open and read the log file
    with open(log_file_path, "r") as log_file:
        for line in log_file:
            # Use regular expressions to find matching URLs
            match = url_pattern.search(line)
            verification = match.group(1)
            url = match.group(2)
            if match:
                # Make sure it's the user's request
                if verification.split(" ")[1].startswith("/api"):
                    # Story mode needs to be handled separately
                    if verification.split(" ")[1].startswith("/api/story"):
                        if verification.split(" ")[1].startswith("/api/story/1"):
                            url_count['http://csi6220-1-vm3.ucd.ie/story'] += 1
                    # Herb Wiki needs to be handled separately
                    elif verification.split(" ")[1].startswith("/api/herbs") or verification.split(" ")[1].startswith("/api/areas/herb"):
                        url_count['http://csi6220-1-vm3.ucd.ie/herb'] += 1
                    # Prescription Wiki needs to be handled separately
                    elif verification.split(" ")[1].startswith("/api/prescriptions"):
                        url_count['http://csi6220-1-vm3.ucd.ie/prescription'] += 1
                    else:
                        if url == 'http://csi6220-1-vm3.ucd.ie/zh/story/1':
                            print(verification.split(" ")[1])
                        if url != '-':
                            if not url.startswith('http://csi6220-1-vm3.ucd.ie/zh/story'):
                                url_count[url] += 1  # Count the number of visits to the URL
    # Returns the statistical results in JSON format
    return jsonify(dict(url_count))