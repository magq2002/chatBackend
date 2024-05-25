from flask import Blueprint, request, jsonify
from app.models.message import MessageModel
from app.services.s3_service import upload_file_to_s3
from app.services.conversion_service import convert_audio_to_text

voice_messages_bp = Blueprint('voice_messages_bp', __name__)


@voice_messages_bp.route('/', methods=['POST'])
def post_voice_message():
    if 'audio' in request.files:
        audio = request.files['audio']
        user = request.form.get('user_id')
        #, text=convert_audio_to_text(audio)
        new_message = MessageModel(name_audio=save_audio_to_s3(audio), is_audio=True, user=user)
        message_id = new_message.save()
        return jsonify({'message_id': message_id}), 200
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


def save_audio_to_s3(audio):
    return upload_file_to_s3(audio)
