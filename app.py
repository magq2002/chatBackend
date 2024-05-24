import os

from flask import Flask
from flask_cors import CORS

from blueprints.controllers.TextMessageController import textMessage_bp
from blueprints.controllers.AudioMessageController import audioMessage_bp

app = Flask(__name__)

app.register_blueprint(textMessage_bp)
app.register_blueprint(audioMessage_bp)

CORS(app)

UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def hello_world():
    return 'Server active'


if __name__ == '__main__':
    app.run(debug=True)
