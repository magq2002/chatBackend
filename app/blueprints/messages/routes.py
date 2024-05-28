from flask_cors import cross_origin

from app.models.chatbotResponse import chatbot_text_response
from app.models.message import MessageModel
from pydantic import ValidationError
from bson.objectid import ObjectId

from flask import Blueprint, jsonify, request


messages_bp = Blueprint('messages_bp', __name__)


@messages_bp.route('', methods=['POST'])
@cross_origin(origins='http://localhost:4200')
def postMessageText():
    try:
        text = request.json['text']
        user = request.json['user']

        response = chatbot_text_response(text, user)

        return response

    except ValidationError as e:
        return jsonify({'error': e}), 400


@messages_bp.route('/<message_id>/<messageChat_id>', methods=['GET'])
@cross_origin(origins='http://localhost:4200')
def get_voice_message(message_id, messageChat_id):
    message = MessageModel.find_by_id(message_id)
    messageChat = MessageModel.find_by_id(messageChat_id)
    if not message:
        return jsonify({'error': 'Message not found'}), 404

    response = {
        "message": message.to_dict(),
        "messageChat": messageChat.to_dict()
    }
    return jsonify(response)


@messages_bp.route('/', methods=['GET'])
@cross_origin(origins='http://localhost:4200')
def get_all_voice_messages():
    messages = MessageModel.find_all()
    messages_data = [message.to_dict() for message in messages]
    return jsonify(messages_data)