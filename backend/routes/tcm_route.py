import json
import random

from flask import Blueprint, jsonify, request
from database import db, Prescription, Herb, ChineseHerb, ChinesePrescription, Rank, Score, User

tcm_bp = Blueprint('tcm_dp', __name__, url_prefix='/api/tcm')

@tcm_bp.route('/getFuzzyPrescription', methods=['POST'])
def getFuzzyPrescription():
    data = request.get_json()
    herbs_id = data.get('herbs', [])
    lang = data.get('lang')
    prescriptions_id = []
    fuzzyResult = []
    precisionResult = []

    if lang == 'en':
        prescriptions = Prescription.query.all()
    else:
        prescriptions = ChinesePrescription.query.all()
    for prescription in prescriptions:
        cons = prescription.constitute
        cons_list = cons.split('; ')
        isPrecision = True
        if len(cons_list) != len(herbs_id):
            isPrecision = False
        else:
            for herbId in herbs_id:
                if lang == 'en':
                    herb = Herb.query.filter_by(id=herbId).first()
                else:
                    herb = ChineseHerb.query.filter_by(id=herbId).first()
                if herb.name not in cons_list:
                    isPrecision = False
                    break
        if isPrecision:
            precisionResult.append({
                'id': prescription.id,
                'name': prescription.name,
            })

    for hid in herbs_id:
        if lang == 'en':
            herb = Herb.query.filter_by(id=hid).first()
        else:
            herb = ChineseHerb.query.filter_by(id=hid).first()
        pre_ids = json.loads(herb.relate_prescription)
        for pid in pre_ids:
            if lang == 'en':
                p = Prescription.query.filter_by(id=pid).first()
            else:
                p = ChinesePrescription.query.filter_by(id=pid).first()
            pid = p.id
            pName = p.name
            if pid not in prescriptions_id:
                prescriptions_id.append(pid)
                fuzzyResult.append({
                    'id': pid,
                    'name': pName
                })

    if len(fuzzyResult) <= 5:
        guess = fuzzyResult
    else:
        guess = random.sample(fuzzyResult, 5)
    return jsonify({
        'precisionResult': precisionResult,
        'guessResult': guess
    })

@tcm_bp.route('/checkHerbSelection', methods=['POST'])
def checkHerbSelection():
    data = request.get_json()  # Get the request body
    lang = data.get('lang')
    prescription_id = data.get('prescriptionId')  # Get the prescription ID
    selected_herbs = data.get('selectedHerbs', [])  # Gets an array of herb IDs selected by the user
    if lang == 'en':
        prescription = Prescription.query.filter_by(id=prescription_id).first()
    else:
        prescription = ChinesePrescription.query.filter_by(id=prescription_id).first()
    cons = prescription.constitute
    cons_array = cons.split(';')
    stander_cons = []
    for constitute in cons_array:
        if constitute.startswith(" "):
            c = constitute[1:]
            stander_cons.append(c)
        else:
            stander_cons.append(constitute)
    herbs_name = []
    for hid in selected_herbs:
        if lang == 'en':
            herb = Herb.query.filter_by(id=hid).first()
        else:
            herb = ChineseHerb.query.filter_by(id=hid).first()
        hName = herb.name
        if hName not in herbs_name:
            herbs_name.append(hName)
    miss = set(stander_cons) - set(herbs_name)
    extra = set(herbs_name) - set(stander_cons)
    if len(miss) == 0 and len(extra) == 0:
        if lang == 'zh':
            return jsonify({
                'result': 'success',
                'message': '恭喜你，选择正确',
                'lack': [],
                'extra': []
            })
        else:
            return jsonify({
                'result': 'success',
                'message': 'Congratulations！You are right！',
                'lack': [],
                'extra': []
            })
    elif len(miss) > 0 and len(extra) == 0:
        lack_id = []
        for m in miss:
            if lang == 'en':
                herb = Herb.query.filter_by(name=m).first()
            else:
                herb = ChineseHerb.query.filter_by(name=m).first()
            try:
                lack_id.append(herb.id)
            except:
                lack_id.append(-1)
        if lang == 'zh':
            return jsonify({
                'result': 'failure',
                'message': f'缺少药材{miss}',
                'lack': lack_id,
                'extra': []
            })
        else:
            return jsonify({
                'result': 'failure',
                'message': f'Lack of herbs: {miss}',
                'lack': lack_id,
                'extra': []
            })
    elif len(miss) == 0 and len(extra) > 0:
        extra_id = []
        for e in extra:
            if lang == 'en':
                herb = Herb.query.filter_by(name=e).first()
            else:
                herb = ChineseHerb.query.filter_by(name=e).first()
            try:
                extra_id.append(herb.id)
            except:
                extra_id.append(-1)
        if lang == 'zh':
            return jsonify({
                'result': 'failure',
                'message': f'药材{extra}是多余的',
                'extra': extra_id,
                'lack': []
            })
        else:
            return jsonify({
                'result': 'failure',
                'message': f'Herbs: {extra} are additional',
                'extra': extra_id,
                'lack': []
            })
    else:
        lack_id = []
        for m in miss:
            if lang == 'en':
                herb = Herb.query.filter_by(name=m).first()
            else:
                herb = ChineseHerb.query.filter_by(name=m).first()
            try:
                lack_id.append(herb.id)
            except:
                lack_id.append(-1)
        extra_id = []
        for e in extra:
            if lang == 'en':
                herb = Herb.query.filter_by(name=e).first()
            else:
                herb = ChineseHerb.query.filter_by(name=e).first()
            try:
                extra_id.append(herb.id)
            except:
                extra_id.append(-1)
        if lang == 'zh':
            return jsonify({
                'result': 'failure',
                'message': f'药材{extra}是多余的并且缺少药材{miss}',
                'extra': extra_id,
                'lack': lack_id
            })
        else:
            return jsonify({
                'result': 'failure',
                'message': f'Herbs: {extra} are additional, and lack of herbs: {miss}',
                'extra': extra_id,
                'lack': lack_id
            })

@tcm_bp.route('/herb-ids', methods=['GET'])
def getHerbIds():
    herb_ids = []
    while len(herb_ids) < 5:
        num = random.randint(1, 217)
        if num not in herb_ids:
            herb_ids.append(num)
    return jsonify({
        'ids': herb_ids
    })

@tcm_bp.route('/herb-detail/<int:id>', methods=['GET'])
def getHerbDetail(id):
    lang = request.args.get('lang', 'zh')
    option_id = []
    option_name = []
    position = random.randint(1, 4)
    while len(option_id) < 4:
        if len(option_id) == position - 1:
            option_id.append(id)
        else:
            num = random.randint(1, 217)
            if num not in option_id:
                option_id.append(num)

    if lang == 'en':
        herb = Herb.query.filter_by(id=id).first()
        for oid in option_id:
            option_name.append(Herb.query.filter_by(id=oid).first().name)
    else:
        herb = ChineseHerb.query.filter_by(id=id).first()
        for oid in option_id:
            option_name.append(ChineseHerb.query.filter_by(id=oid).first().name)

    return jsonify({
        'imageUrl': herb.image,
        'name': herb.name,
        'options': option_name
    })

@tcm_bp.route('/quiz-result', methods=['POST'])
def quizResultInput():
    data = request.get_json()
    username = data.get('username')
    if not username:
        return jsonify({'message': 'No available user'})
    accuracy = data.get('accuracy')
    totalTime = data.get('totalTime')
    rank = Rank.query.filter_by(username=username).first()
    if not rank:
        new_rank = Rank(username=username, accuracy=accuracy, time=1, totalTime=totalTime)
        db.session.add(new_rank)
    else:
        accuracy = (rank.accuracy * rank.time + accuracy) / (rank.time + 1)
        totalTime = (rank.totalTime * rank.time + totalTime) / (rank.time + 1)
        rank.time += 1
        if accuracy < 0:
            accuracy = 0
        rank.accuracy = accuracy
        rank.totalTime = totalTime
    db.session.commit()
    return jsonify({'message': 'Input succeed'})

@tcm_bp.route('/ranking', methods=['GET'])
def getRanking():
    ranks = Rank.query.order_by((Rank.accuracy - 0.03 * Rank.totalTime).desc()).all()
    data = []
    for i in range(0, 10):
        if len(ranks) >= i + 1:
            if int(ranks[i].accuracy - 0.03 * ranks[i].totalTime) < 0:
                data.append({
                    "username": ranks[i].username,
                    "avatar": User.query.filter_by(username=ranks[i].username).first().avatar,
                    "accuracy": int(ranks[i].accuracy),
                    "score": 0
                })
            else:
                data.append({
                    "username": ranks[i].username,
                    "avatar": User.query.filter_by(username=ranks[i].username).first().avatar,
                    "accuracy": int(ranks[i].accuracy),
                    "score": int(ranks[i].accuracy - 0.03 * ranks[i].totalTime)
                })
        i += 1
    return jsonify({
        "status": "success",
        "data": data
    })

@tcm_bp.route('/ranking/prescription', methods=['GET'])
def getRankingPrescription():
    scores = Score.query.order_by((Score.accuracy - 0.03 * Score.totalTime).desc()).all()
    data = []
    for i in range(0, 10):
        if len(scores) >= i + 1:
            if int(scores[i].accuracy - 0.03 * scores[i].totalTime) < 0:
                data.append({
                    "username": scores[i].username,
                    "avatar": User.query.filter_by(username=scores[i].username).first().avatar,
                    "accuracy": int(scores[i].accuracy),
                    "score": 0
                })
            else:
                data.append({
                    "username": scores[i].username,
                    "avatar": User.query.filter_by(username=scores[i].username).first().avatar,
                    "accuracy": int(scores[i].accuracy),
                    "score": int(scores[i].accuracy - 0.03 * scores[i].totalTime)
                })
        i += 1
    return jsonify({
        "status": "success",
        "data": data
    })

@tcm_bp.route('/prescriptionQuiz/question', methods=['GET'])
def getQuizQuestion():
    lang = request.args.get('lang', 'zh')
    difficulty = request.args.get('difficulty')
    print(difficulty)
    doneQuestionIds = []
    print(request.args.get('doneQuestionIds'))
    if request.args.get('doneQuestionIds') != '':
        for id in request.args.get('doneQuestionIds').split(','):
            if id.startswith(" "):
                sid = int(id[1:])
            else:
                sid = int(id)
            doneQuestionIds.append(sid)
            print(doneQuestionIds)

    if lang == 'en':
        difficulty_rank = Prescription.query.order_by(Prescription.constituteNumber).all()
    else:
        difficulty_rank = ChinesePrescription.query.order_by(ChinesePrescription.constituteNumber).all()

    questions_1 = difficulty_rank[1:len(difficulty_rank)//3]
    questions_2 = difficulty_rank[len(difficulty_rank)//3: 2 * len(difficulty_rank)//3]
    questions_3 = difficulty_rank[2 * len(difficulty_rank)//3:]

    if difficulty == '1':
        num = random.randint(1, len(questions_1))
        while num in doneQuestionIds or ifQuestionValue(questions_1[num].id, lang) == False:
            num = random.randint(1, len(questions_1))
        question = questions_1[num]
    elif difficulty == '2':
        num = random.randint(1, len(questions_2))
        while num in doneQuestionIds or ifQuestionValue(questions_1[num].id, lang) == False:
            num = random.randint(1, len(questions_2))
        question = questions_2[num]
    else:
        num = random.randint(1, len(questions_3))
        while num in doneQuestionIds or ifQuestionValue(questions_1[num].id, lang) == False:
            num = random.randint(1, len(questions_3))
        question = questions_3[num]
    pid = question.id
    prescriptionName = question.name
    constituteList = question.constitute.split(';')
    stander_cons = []
    for constitute in constituteList:
        if constitute.startswith(" "):
            c = constitute[1:]
            stander_cons.append(c)
        else:
            stander_cons.append(constitute)
    stander_cons_ids = []
    for sc in stander_cons:
        if lang == 'en':
            herb = Herb.query.filter_by(name=sc).first()
        else:
            herb = ChineseHerb.query.filter_by(name=sc).first()
        stander_cons_ids.append(herb.id)

    return jsonify({
        "id": pid,
        "prescriptionName": prescriptionName,
        "correctHerbIds": stander_cons_ids,
        "correctHerbNames": stander_cons,
        "difficulty": difficulty
    })

def ifQuestionValue(id, lang):
    if lang == 'en':
        pre = Prescription.query.filter_by(id=id).first()
    else:
        pre = ChinesePrescription.query.filter_by(id=id).first()
    constituteList = pre.constitute.split('; ')
    value = True
    for cons in constituteList:
        if lang == 'en':
            herb = Herb.query.filter_by(name=cons).first()
        else:
            herb = ChineseHerb.query.filter_by(name=cons).first()
        if herb is None:
            value = False
            return value
    return value

@tcm_bp.route('/score', methods=['POST'])
def prescriptionScore():
    data = request.get_json()
    username = data.get('username')
    if not username:
        return jsonify({'message': 'No available user'})
    accuracy = data.get('accuracy')
    totalTime = data.get('totalTime')
    score = Score.query.filter_by(username=username).first()
    if not score:
        new_score = Score(username=username, accuracy=accuracy, time=1, totalTime=totalTime)
        db.session.add(new_score)
    else:
        accuracy = (score.accuracy * score.time + accuracy) / (score.time + 1)
        totalTime = (score.totalTime * score.time + totalTime) / (score.time + 1)
        score.time += 1
        if accuracy < 0:
            accuracy = 0
        score.accuracy = accuracy
        score.totalTime = totalTime
    db.session.commit()
    return jsonify({'message': 'Input succeed'})



