from flask import Blueprint
from flask_cors import cross_origin

audioMessage_bp = Blueprint('audioMessage', __name__)


@audioMessage_bp.route('/post-audio-message', methods=['POST'])
@cross_origin(origins='http://localhost:4200')
def post_audio_message():

    print("hello world")


@audioMessage_bp.route('/get-audio-message', methods=['GET'])
@cross_origin(origins='http://localhost:4200')
def get_audio_message():

    print("hello world")


@audioMessage_bp.route('/get-all-audio-messages', methods=['GET'])
@cross_origin(origins='http://localhost:4200')
def get_all_audio_messages():

    print("hello world")