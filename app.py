from flask import Flask, request, jsonify
from models.bot import Bot
import nltk

app = Flask(__name__)
chatbot = Bot(r'static/corpus_deporte.txt')

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/chatbot', methods=["POST", "GET"])
def chatbot_response():
    user_response = request.json.get("message")
    user_response = user_response.lower()

    if user_response in ['salir', 'gracias', 'muchas gracias']:
        return jsonify({"response": "Gusto atenderte, Cuidate" if user_response == 'salir' else "No hay de qué"})

    saludo_res = chatbot.saludos(user_response)
    if saludo_res is not None:
        return jsonify({"response": saludo_res})
    return jsonify({"response": chatbot.response(user_response)})

if __name__ == '__main__':
    app.run(debug=True)
