from flask import Blueprint, request, jsonify
from flask_cors import cross_origin

from app.models.message import MessageModel
from pydantic import ValidationError
from bson.objectid import ObjectId


messages_bp = Blueprint('messages_bp', __name__)


@messages_bp.route('', methods=['POST'])
@cross_origin(origins='http://localhost:4200')
def postMessageText():
    try:
        text = request.json['text']
        user = request.json['user']
        new_message = MessageModel(text=text, is_audio=False, user=user)
        message_id = new_message.save()
        return jsonify({'_id': message_id}), 200
    except ValidationError as e:
        return jsonify({'error': e}), 400


@messages_bp.route('/<message_id>', methods=['GET'])
@cross_origin(origins='http://localhost:4200')
def get_voice_message(message_id):
    message = MessageModel.find_by_id(message_id)
    if not message:
        return jsonify({'error': 'Message not found'}), 404
    return jsonify(message.to_dict())


@messages_bp.route('/', methods=['GET'])
@cross_origin(origins='http://localhost:4200')
def get_all_voice_messages():
    messages = MessageModel.find_all()
    messages_data = [message.to_dict() for message in messages]
    return jsonify(messages_data)