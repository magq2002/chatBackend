import os
from flask import request, jsonify, current_app


class SaveFile:

    @staticmethod
    def upload_file(file):
        if 'file' not in request.files:
            return jsonify({'error': 'No selected file'}), 400

        # file = request.files['file']
        # if file.filename == '':
        #     return jsonify({'error': 'No selected file'}), 400

        if file.mimetype.startswith('audio/'):
            upload_folder = current_app.config['UPLOAD_FOLDER']
            file_path = os.path.join(upload_folder, file.filename)
            file.save(file_path)
            return jsonify({'message': "File uploaded"}), 200
        else:
            return jsonify({'error': 'Unsupported file type'}), 415
