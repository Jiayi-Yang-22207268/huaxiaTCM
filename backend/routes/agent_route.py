import json
from flask import Blueprint, jsonify, request
from cozepy import COZE_CN_BASE_URL, OAuthToken
from cozepy import Coze, TokenAuth, Message, ChatStatus, MessageContentType, ChatEventType
from typing import Optional
import time
import os
from cozepy import COZE_CN_BASE_URL, Coze, TokenAuth, WebOAuthApp

from flask import Blueprint, jsonify
from service.coze_client import coze_client
from config import config

agent_bp = Blueprint('agent', __name__, url_prefix='/api/agent')

@agent_bp.route('/<string:message>', methods=['GET'])
def chat_with_agent(message):
    if not message:
        return jsonify({'error': 'Message required'}), 400
    
    try:
        response = coze_client.safe_chat(message)
        return jsonify({'message': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# @agent_bp.route('/<string:message>', methods=['GET'])
# def chatWithAgent(message):
#     if not message:
#         return jsonify({'error': 'No message provided'}), 400
    
#     chat_poll = coze.chat.create_and_poll(
#         bot_id=bot_id,
#         user_id=user_id,
#         additional_messages=[
#             Message.build_user_question_text(message)
#         ],
#     )
#     for msg in chat_poll.messages:
#         # print("------------------------------------------------------------------------------------------------------")
#         # print(msg, end="", flush=True)
#         if (msg.type == 'answer'):
#             print(msg.content)
#             return jsonify({'message': msg.content})
    
#     return jsonify({'message': "Please try later"})
    