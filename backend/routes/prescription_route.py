from flask import Blueprint, jsonify, request
from database import Prescription, ChinesePrescription, Herb, ChineseHerb

prescription_bp = Blueprint('prescription', __name__, url_prefix='/api/prescriptions')

@prescription_bp.route('', methods=['GET'])
def get_prescriptions():
    lang = request.args.get('lang', 'zh')
    result = []
    if lang == 'en':
        prescriptions = Prescription.query.all()
    else:
        prescriptions = ChinesePrescription.query.all()
    for p in prescriptions:
        result.append({
            "id": p.id,
            "name": p.name,
        })
    return jsonify(result)

@prescription_bp.route('/<int:id>', methods=['GET'])
def get_prescription(id):
    lang = request.args.get('lang', 'zh')
    if lang == 'en':
        prescription = Prescription.query.filter_by(id=id).first()
    else:
        prescription = ChinesePrescription.query.filter_by(id=id).first()
    if not prescription:
        return jsonify({'error': 'No prescription found'}), 404
    constitutes_name = prescription.constitute
    constitutes_name_list = constitutes_name.split('; ')
    constitutes_id = []
    for constitute_name in constitutes_name_list:
        if lang == 'en':
            herb = Herb.query.filter_by(name=constitute_name).first()
        else:
            herb = ChineseHerb.query.filter_by(name=constitute_name).first()
        try:
            constitutes_id.append(herb.id)
        except:
            constitutes_id.append(-1)

    return jsonify({
        "id": prescription.id,
        "name": prescription.name,
        "cnName": ChinesePrescription.query.filter_by(id=prescription.id).first().name,
        "constitute": prescription.constitute,
        "action": prescription.action,
        "indication": prescription.indication,
        "constituteId": constitutes_id,
    })

@prescription_bp.route('/search', methods=['GET'])
def get_prescription_by_name():
    name = request.args.get('name', '').strip()
    lang = request.args.get('lang', 'zh')  # 默认中文

    if not name:
        return jsonify({'error': 'No name provided'}), 400

    try:
        EN_Prescription = Prescription.query.filter(Prescription.name.ilike(f'%{name}%')).all()
        CN_Prescription = ChinesePrescription.query.filter(ChinesePrescription.name.ilike(f'%{name}%')).all()
        prescriptionIds = []
        if not EN_Prescription:
            for prescription in CN_Prescription:
                prescriptionIds.append(prescription.id)
        else:
            for prescription in EN_Prescription:
                prescriptionIds.append(prescription.id)

        result = []
        for pid in prescriptionIds:
            if lang == 'en':
                prescription = Prescription.query.filter_by(id=pid).first()
            else:
                prescription = ChinesePrescription.query.filter_by(id=pid).first()
            result.append({"id": prescription.id, "name": prescription.name})

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500