import os
from flask import Blueprint, request, jsonify, current_app

saveFile_bp = Blueprint('saveFile', __name__)


@saveFile_bp.route('/upload', methods=['POST'])
def upload_file(file):
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    upload_folder = current_app.config['UPLOAD_FOLDER']
    file_path = os.path.join(upload_folder, file.filename)
    file.save(file_path)

    return jsonify({'message': "File uploaded"}), 200
