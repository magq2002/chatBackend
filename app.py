import os

from flask import Flask, request, jsonify
from flask_cors import CORS
from blueprints.models.bot import Bot

from blueprints.models.chatbotResponse import chatbotResponse_bp;

app = Flask(__name__)
app.register_blueprint(chatbotResponse_bp)

CORS(app)

UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# chatbot = Bot(r'static/corpus_deporte.txt')


@app.route('/')
def hello_world():
    return 'Hello World!'
#
#
# @app.route('/chatbot', methods=["POST", "GET"])
# @cross_origin(origins='http://localhost:4200')
# def chatbot_response():
#     if request.method == "POST":
#         if 'file' not in request.files:
#             return jsonify({'error': 'No file part'}), 400
#         file = request.files['file']
#         if file.filename == '':
#             return jsonify({'error': 'No selected file'}), 400
#
#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#         file.save(file_path)
#
#         return jsonify({'message': "File uploaded"}), 200
#
#     user_response = request.json.get("message")
#     user_response = user_response.lower()
#
#     if user_response in ['salir', 'gracias', 'muchas gracias']:
#         return jsonify({"response": "Gusto atenderte, Cuidate" if user_response == 'salir' else "No hay de qué"})
#
#     saludo_res = chatbot.saludos(user_response)
#     if saludo_res is not None:
#         return jsonify({"response": saludo_res})
#     return jsonify({"response": chatbot.response(user_response)})


if __name__ == '__main__':
    app.run(debug=True)
