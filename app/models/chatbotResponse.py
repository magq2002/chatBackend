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

    UPLOAD_FOLDER = 'static/uploads'
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    file_path = os.path.join(UPLOAD_FOLDER, audio.filename)
    with open(file_path, 'wb') as f:
        f.write(audio_stream)

    user_text=request_audio_to_text(file_path, audio, user)
    user_message_id = save_user_audio(file_path, audio, user, user_text)

    # Obtener la respuesta del chatbot
    chatbot = Bot(os.path.join('static', 'corpus_deporte.txt'))
    bot_response = chatbot.response(user_text)
    # chatbot = BotBert(os.path.join('train', 'trained_model'), os.path.join('static', 'corpus_deporte.json'))
    # bot_response = chatbot.response(user_text)

    chatbot_message_id=response_text_to_audio(bot_response)

    return jsonify({'_id': user_message_id, '_idChat': chatbot_message_id})


def chatbot_text_response(text, user):

    new_message = MessageModel(text=text, is_audio=False, user=user)
    message_id = new_message.save()

    # Obtener la respuesta del chatbot
    chatbot = Bot(os.path.join('static', 'corpus_deporte.txt'))
    bot_response = chatbot.response(text)
    # chatbot = BotBert(os.path.join('train', 'trained_model'), os.path.join('static', 'corpus_deporte.json'))
    # bot_response = chatbot.response(text)

    answer_message = MessageModel(is_audio=False, user=2, text=bot_response)
    chatbot_message_id = answer_message.save()
    
    return jsonify({'_id': message_id, '_idChat': chatbot_message_id})


def save_audio_to_s3(audio):
    return upload_file_to_s3(audio)


def request_audio_to_text(file_path, audio, user):

    try:
        user_text = convert_audio_to_text(file_path)
        return user_text
    except Exception as e:
        user_text = 'No fui capaz de entenderte, podrías volver a intentarlo'
        new_message = MessageModel(text=user_text, is_audio=False, user=2)
        chatbot_message_id = new_message.save()

        os.remove(file_path)
        user_audio = save_audio_to_s3(audio)

        question_message = MessageModel(name_audio=user_audio, is_audio=True, user=user, text=user_text)
        message_id = question_message.save()

        return jsonify({'_id': message_id, '_idChat': chatbot_message_id})


def save_user_audio(file_path, audio, user, user_text):
    
    os.remove(file_path)
    user_audio = save_audio_to_s3(audio)

    question_message = MessageModel(name_audio=user_audio, is_audio=True, user=user, text=user_text)
    user_message_id = question_message.save()
    return user_message_id


def response_text_to_audio(bot_response):
    try:
        chatbot_audio = convert_text_to_audio(bot_response)
        answer_message = MessageModel(name_audio=chatbot_audio, is_audio=True, user=2, text=bot_response)
        chatbot_message_id = answer_message.save()
        return chatbot_message_id
    except Exception as e:
        error_message = 'Error al convertir la respuesta a audio. Por favor, intenta nuevamente.'
        error_message_model = MessageModel(text=error_message, is_audio=False, user=2)
        error_message_id = error_message_model.save()
        return jsonify({'_id': error_message_id})