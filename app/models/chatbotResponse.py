import os

from flask import jsonify

from app.models.ChatBotBert import BotBert
from app.models.ChatBotCorpus import Bot
from app.models.message import MessageModel
from app.services.conversion_service import convert_audio_to_text, convert_text_to_audio
from app.services.s3_service import upload_file_to_s3


def chatbot_audio_response(audio, user):
    audio_stream = audio.stream.read()
    audio.stream.seek(0)

    # Save audio in folder
    UPLOAD_FOLDER = 'static/uploads'
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    file_path = os.path.join(UPLOAD_FOLDER, audio.filename)
    with open(file_path, 'wb') as f:
        f.write(audio_stream)

    try:
        user_text = convert_audio_to_text(file_path)
    except Exception as e:
        os.remove(file_path)
        user_text = 'No fui capaz de entenderte, podrías volver a intentarlo'
        new_message = MessageModel(text=user_text, is_audio=False, user=2)
        message_id = new_message.save()
        return jsonify({'_id': message_id}), 200

    os.remove(file_path)
    user_audio = save_audio_to_s3(audio)

    # Guarda el mensaje de voz y su transcripción
    question_message = MessageModel(name_audio=user_audio, is_audio=True, user=user, text=user_text)
    user_message_id = question_message.save()

    # Obtén la respuesta del chatbot
    print(user_text)
    chatbot = Bot(os.path.join('static', 'corpus_deporte.txt'))
    bot_response = chatbot.response(user_text)
    # chatbot = BotBert(os.path.join('train', 'trained_model'), os.path.join('static', 'corpus_deporte.json'))
    # bot_response = chatbot.response(user_text)
    print(bot_response)

    # Pasar respuesta de texto a audio
    try:
        chatbot_audio = convert_text_to_audio(bot_response)
        answer_message = MessageModel(name_audio=chatbot_audio, is_audio=True, user=2, text=bot_response)
        chatbot_message_id = answer_message.save()
    except Exception as e:
        error_message = 'Error al convertir la respuesta a audio. Por favor, intenta nuevamente.'
        error_message_model = MessageModel(text=error_message, is_audio=False, user=2)
        error_message_id = error_message_model.save()
        return jsonify({'_id': error_message_id}), 200

    return jsonify({'_id': user_message_id}, {'_id': chatbot_message_id}), 200


def chatbot_text_response(text, user):

    new_message = MessageModel(text=text, is_audio=False, user=user)
    message_id = new_message.save()

    # Obtén la respuesta del chatbot
    print(text)
    chatbot = Bot(os.path.join('static', 'corpus_deporte.txt'))
    bot_response = chatbot.response(text)
    # chatbot = BotBert(os.path.join('train', 'trained_model'), os.path.join('static', 'corpus_deporte.json'))
    # bot_response = chatbot.response(text)
    print(bot_response)

    answer_message = MessageModel(is_audio=False, user=2, text=bot_response)
    chatbot_message_id = answer_message.save()
    return jsonify({'_id': message_id}, {'_id': chatbot_message_id}), 200


def save_audio_to_s3(audio):
    return upload_file_to_s3(audio)
