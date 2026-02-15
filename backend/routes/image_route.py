from flask import Blueprint, jsonify, request
from database import Image

image_bp = Blueprint('image', __name__, url_prefix='/api/mainImage')

@image_bp.route('/banner', methods=['GET'])
def getAllBenners():
    lang = request.args.get('lang', 'zh')
    images = Image.query.all()
    result = []
    for image in images:
        if lang == 'zh':
            result.append({
                "imageUrl": image.imageUrl_zh,
                "id": image.id,
            })
        else:
            result.append({
                "imageUrl": image.imageUrl_en,
                "id": image.id,
            })
    return jsonify({
        "code": 0,
        "data": result,
        "message": "Success"
    })
