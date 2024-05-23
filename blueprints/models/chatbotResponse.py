from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

from blueprints.models.saveFile import upload_file
from blueprints.models.bot import Bot

chatbotResponse_bp = Blueprint('chatbotResponse', __name__)

chatbot = Bot(r'static/corpus_deporte.txt')


@chatbotResponse_bp.route('/chatbot', methods=["POST", "GET"])
@cross_origin(origins='http://localhost:4200')
def chatbot_response():

    if request.method == "POST":
        if 'file' in request.files:
            upload_file(request.files['file'])

        user_response = request.json.get("message")
        if user_response:
            user_response = user_response.lower()

            if user_response in ['salir', 'gracias', 'muchas gracias']:
                return jsonify(
                    {"response": "Gusto atenderte, Cuídate" if user_response == 'salir' else "No hay de qué"})

            saludo_res = chatbot.saludos(user_response)
            if saludo_res is not None:
                return jsonify({"response": saludo_res})
            return jsonify({"response": chatbot.response(user_response)})

    return jsonify({"error": "Invalid request"})
