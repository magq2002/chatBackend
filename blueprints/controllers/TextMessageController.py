from flask import Blueprint
from flask_cors import cross_origin

textMessage_bp = Blueprint('textMessage', __name__)


@textMessage_bp.route('/post-text-message', methods=['POST'])
@cross_origin(origins='http://localhost:4200')
def post_text_message():

    print("hello world")
    return "Posted text message"


@textMessage_bp.route('/get-text-message', methods=['GET'])
@cross_origin(origins='http://localhost:4200')
def get_text_message():

    print("hello world")
    return "Text message"


@textMessage_bp.route('/get-all-text-messages', methods=['GET'])
@cross_origin(origins='http://localhost:4200')
def get_all_text_messages():

    print("hello world")
    return "All text messages"
