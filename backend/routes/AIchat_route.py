import os, time
from pathlib import Path
from flask import current_app as app, Blueprint, jsonify, request, redirect
from service.coze_client import coze_client, NeedReauthorize
from config import config

aichat_bp = Blueprint('aichat', __name__, url_prefix='/api/chat')


# @aichat_bp.route('', methods=['GET'])
# def chat():
#     user_id = request.args.get('user_id', None)
#     new_message = request.args.get('new_message', None)

#     if not user_id:
#         return jsonify({'error': 'No user id provided'}), 400
#     if not new_message:
#         return jsonify({'error': 'No new message provided'}), 400

#     chatHistory = ChatHistory.query.filter_by(user_id=user_id).order_by(ChatHistory.created_at).all()
#     messages = []
#     for chat in chatHistory:
#         messages.append({
#             "role": chat.role,
#             "content": chat.content
#         })
#     messages.append({
#         "role": "user",
#         "content": new_message
#     })
#     new_chat_record = ChatHistory(user_id=user_id, content=new_message, role="user")
#     db.session.add(new_chat_record)
#     db.session.commit()

#     response = client.chat.completions.create(
#         model="deepseek-chat",
#         messages=messages
#     )
#     response_message = ChatHistory(user_id=user_id, content=response.choices[0].message.content, role=response.choices[0].message.role)
#     db.session.add(response_message)
#     db.session.commit()
#     return jsonify({'message': response.choices[0].message.content}), 200

# @aichat_bp.route('/auth-url', methods=['GET'])
# def get_auth_url():
#     """
#     返回当前最新的 OAuth 授权链接，前端可用来跳转。
#     """
#     url = coze_client.oauth_app.get_oauth_url(
#         redirect_uri=config.REDIRECT_URI
#     )
#     return jsonify({ "auth_url": url }), 200

@aichat_bp.route('/auth-url', methods=['GET'])
def get_auth_url():
    """
    浏览器访问此路由时，直接跳到 Coze 授权页。
    """
    auth_url = coze_client.oauth_app.get_oauth_url(
        redirect_uri=config.COZE_REDIRECT_URI
    )
    return redirect(auth_url)

# @aichat_bp.route('/oauth/callback', methods=['GET'])
# def oauth_callback():
#     code = request.args.get('code')
#     if not code:
#         return jsonify({"error": "code missing"}), 400
#
#     try:
#         app.logger.info(f"OAuth callback received code={code}")
#         coze_client.authorize_with_code(code)
#         app.logger.info("authorize_with_code succeeded")
#         return jsonify({"status": "ok"}), 200
#
#     except Exception as e:
#         # 打印完整堆栈到控制台/日志
#         app.logger.exception("Error in oauth_callback")
#         # 把错误信息也返回给前端（仅测试阶段，生产可删）
#         return jsonify({
#             "error": "authorize failed",
#             "detail": str(e)
#         }), 500

@aichat_bp.route('/oauth/callback', methods=['GET'])
def oauth_callback():
    code = request.args.get('code')
    if not code:
        return "Missing code", 400

    try:
        coze_client.authorize_with_code(code)
    except Exception as e:
        app.logger.exception("authorize_with_code failed")
        return f"Authorize failed: {e}", 500

    # 授权、换 token 都成功后，302 跳回前端聊天页
    return redirect(config.COZE_SUCCESS_REDIRECT_URI)

@aichat_bp.route('/BianQue', methods=['POST'])
def BianQue():
    """
    现有的聊天接口，支持自动刷新或重授权
    """
    data = request.get_json()
    question = data.get('question')
    if not question:
        return jsonify({'error': 'Message required'}), 400

    try:
        answer = coze_client.safe_chat(question)
        return jsonify({'message': answer}), 200

    except NeedReauthorize:
        # 直接返回 401，不再返回 JSON 链接，前端拦截后打开 /auth-url
        return '', 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # try:
    #     answer = coze_client.safe_chat(question)
    #     return jsonify({'message': answer}), 200
    #
    # except NeedReauthorize:
    #     # Refresh Token 已过期，需要重新授权
    #     auth_url = coze_client.oauth_app.get_oauth_url(
    #         redirect_uri=config.COZE_REDIRECT_URI
    #     )
    #     return jsonify({
    #         'error': 'need_reauthorize',
    #         'auth_url': auth_url
    #     }), 401
    #
    # except Exception as e:
    #     return jsonify({'error': str(e)}), 500