from flask import Blueprint, request, jsonify
from flask_cors import cross_origin

from app.models.message import MessageModel
from pydantic import ValidationError
from bson.objectid import ObjectId


messages_bp = Blueprint('messages_bp', __name__)

@messages_bp.route('/messages', methods=['POST'])
@cross_origin(origins='http://localhost:4200')
def saveMessage():
    return "hola"

@messages_bp.route('/<message_id>', methods=['GET'])
@cross_origin(origins='http://localhost:4200')
def get_message(message_id):
    return "hola"

@messages_bp.route('/', methods=['GET'])
@cross_origin(origins='http://localhost:4200')
def get_all_messages():
    messages = MessageModel.find_all()
    messages_data = [message.to_dict() for message in messages]
    return jsonify(messages_data)