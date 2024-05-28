from flask import Blueprint, request, jsonify
from flask_cors import cross_origin

from app.models.chatbotResponse import chatbot_audio_response
from app.models.message import MessageModel

import os

voice_messages_bp = Blueprint('voice_messages_bp', __name__)


@voice_messages_bp.route('/', methods=['POST'])
@cross_origin(origins='http://localhost:4200')
def post_voice_message():
    if 'audio' in request.files:
        audio = request.files['audio']
        user = int(request.form.get('user'))

        response = chatbot_audio_response(audio, user)
        return response
    else:
        return jsonify({'error': 'No audio file found'}), 400


@voice_messages_bp.route('/<message_id>', methods=['GET'])
def get_voice_message(message_id):
    message = MessageModel.find_by_id(message_id)
    if not message:
        return jsonify({'error': 'Message not found'}), 404
    return jsonify(message.to_dict())


@voice_messages_bp.route('/', methods=['GET'])
def get_all_voice_messages():
    messages = MessageModel.find_all()
    messages_data = [message.to_dict() for message in messages]
    return jsonify(messages_data)
