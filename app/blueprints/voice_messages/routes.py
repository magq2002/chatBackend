from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from app.models.message import MessageModel
from app.services.s3_service import upload_file_to_s3
from app.services.conversion_service import convert_audio_to_text
import os

voice_messages_bp = Blueprint('voice_messages_bp', __name__)


@voice_messages_bp.route('/', methods=['POST'])
@cross_origin(origins='http://localhost:4200')
def post_voice_message():
    if 'audio' in request.files:
        audio = request.files['audio']
        user = int(request.form.get('user'))

        audio_stream = audio.stream.read()
        audio.stream.seek(0)

        UPLOAD_FOLDER = 'static/uploads'
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        file_path = os.path.join(UPLOAD_FOLDER, audio.filename)
        with open(file_path, 'wb') as f:
            f.write(audio_stream)

        try:
            text=convert_audio_to_text(file_path)
        except Exception as e:
            os.remove(file_path)
            text = 'No fui capaz de entenderte, podrias volver a intentarlo'
            new_message = MessageModel(text=text, is_audio=False, user=2)
            message_id = new_message.save()
            return jsonify({'_id': message_id}), 200

        os.remove(file_path)
        name_audio = save_audio_to_s3(audio)


        new_message = MessageModel(name_audio=name_audio, is_audio=True, user=user, text=text)
        message_id = new_message.save()
        return jsonify({'_id': message_id}), 200
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
