import json

from flask import Blueprint, jsonify, request
from database import Herb, Prescription, ChinesePrescription, ChineseHerb

herb_bp = Blueprint('herb', __name__, url_prefix='/api/herbs')

@herb_bp.route('/', methods=['GET'])
def get_herbs():
    lang = request.args.get('lang', 'zh')
    result = []
    if lang == 'en':
        herbs = Herb.query.all()
    else:
        herbs = ChineseHerb.query.all()
    for herb in herbs:
        result.append({
            'id': herb.id,
            'name': herb.name,
            'image': herb.image
        })
    return jsonify(result)


@herb_bp.route('/usefulHerbs', methods=['POST'])
def get_useful_herbs():
    lang = request.args.get('lang', 'zh')  # Default is 'zh' if lang parameter is not provided
    print(lang)

    # Get a list of herbs
    if lang == 'en':
        herbs = Herb.query.limit(20).all()
    else:
        herbs = ChineseHerb.query.limit(20).all()

    result = []
    for herb in herbs:
        result.append({
            'id': herb.id,
            'name': herb.name,
            'image': herb.image
        })

    return jsonify(result)

@herb_bp.route('/<string:category>', methods=['GET'])
def get_herbs_by_category(category):
    lang = request.args.get('lang', 'zh')
    result = []
    if lang == 'en':
        herbs = Herb.query.filter_by(category=category).all()
    else:
        herbs = ChineseHerb.query.filter_by(category=category).all()
    if not herbs:
        return jsonify({'error': 'No herbs found with category {}'.format(category)})
    for herb in herbs:
        result.append({
            'id': herb.id,
            'name': herb.name,
            'image': herb.image
        })
    return jsonify(result)

@herb_bp.route('/classification/<string:classification>', methods=['GET'])
def get_herbs_by_classification(classification):
    lang = request.args.get('lang', 'zh')
    result = []
    if lang == 'en':
        herbs = Herb.query.filter_by(classification=classification).all()
    else:
        herbs = ChineseHerb.query.filter_by(classification=classification).all()
    if not herbs:
        return jsonify({'error': 'No herbs found with category {}'.format(classification)})
    for herb in herbs:
        result.append({
            'id': herb.id,
            'name': herb.name,
            'image': herb.image
        })
    return jsonify(result)

@herb_bp.route('/<int:id>', methods=['GET'])
def get_herb(id):
    lang = request.args.get('lang', 'zh')
    if lang == 'en':
        herb = Herb.query.filter_by(id=id).first()
    else:
        herb = ChineseHerb.query.filter_by(id=id).first()
    if not herb:
        return jsonify({'error': 'No prescription found'}), 404

    relate_prescription_id = json.loads(herb.relate_prescription)
    relate_prescription_name = []
    for pid in relate_prescription_id:
        if lang == 'en':
            pre = Prescription.query.filter_by(id=pid).first()
        else:
            pre = ChinesePrescription.query.filter_by(id=pid).first()
        relate_prescription_name.append(pre.name)

    return jsonify({
        "id": herb.id,
        "name": herb.name,
        'cnName': ChineseHerb.query.filter_by(id=herb.id).first().name,
        "category": herb.category,
        "origin": herb.origin,
        "production_regions": herb.production_regions,
        "properties": herb.properties,
        "functions": herb.functions,
        "image": herb.image,
        "relate_prescription": relate_prescription_name,
        'relate_prescription_id': relate_prescription_id,
        "classification": herb.classification,
    })

@herb_bp.route('/categories', methods=['GET'])
def get_category():
    lang = request.args.get('lang', 'zh')
    if lang == 'en':
        herbs = Herb.query.all()
    else:
        herbs = ChineseHerb.query.all()
    categories = []
    for herb in herbs:
        if herb.category not in categories and len(herb.category) > 1:
            categories.append(herb.category)
    result = json.dumps(categories)
    return result

@herb_bp.route('/classifications', methods=['GET'])
def get_classification():
    lang = request.args.get('lang', 'zh')
    if lang == 'en':
        herbs = Herb.query.all()
    else:
        herbs = ChineseHerb.query.all()
    classifications = []
    for herb in herbs:
        if herb.classification not in classifications and len(herb.classification) > 1:
            classifications.append(herb.classification)
    result = json.dumps(classifications)
    return result

@herb_bp.route('/search', methods=['GET'])
def get_herb_by_name():
    lang = request.args.get('lang', 'zh')
    name = request.args.get("name", "").strip()
    if not name:
        return jsonify({'error': 'No name provided'}), 400
    try:
        EN_herbs = Herb.query.filter(Herb.name.ilike(f'%{name}%')).all()
        CN_herbs = ChineseHerb.query.filter(ChineseHerb.name.ilike(f'%{name}%')).all()
        herbIds = []
        if not EN_herbs:
            for herb in CN_herbs:
                herbIds.append(herb.id)
        else:
            for herb in EN_herbs:
                herbIds.append(herb.id)

        result = []
        for hid in herbIds:
            if lang == 'en':
                herb = Herb.query.filter_by(id=hid).first()
            else:
                herb = ChineseHerb.query.filter_by(id=hid).first()
            result.append({"id": herb.id, "name": herb.name, "image": herb.image})

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@herb_bp.route('/batchNames', methods=['POST'])
def get_herb_names_batch():
    try:
        data = request.get_json()
        ids = data.get('ids', [])
        lang = data.get('lang', 'zh')
        if not isinstance(ids, list) or not ids:
            return jsonify({'error': 'No ids provided'}), 400

        result = []
        Model = Herb if lang == 'en' else ChineseHerb
        herbs = Model.query.filter(Model.id.in_(ids)).all()
        herb_dict = {herb.id: herb.name for herb in herbs}
        # Ensure the order matches the request
        for hid in ids:
            if hid in herb_dict:
                result.append({'id': hid, 'name': herb_dict[hid]})
        return jsonify(result)
    except Exception as e:
        print(f"Failed to batch get herb names: {e}")
        return jsonify(None)