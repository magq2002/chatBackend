import speech_recognition as sr
import pyttsx3
import tempfile
import os
from app.services.s3_service import upload_file_to_s3
from werkzeug.datastructures import FileStorage


def convert_audio_to_text(file_path):
    r = sr.Recognizer()
    audio_file = sr.AudioFile(file_path)

    with audio_file as source:
        r.adjust_for_ambient_noise(source)
        audio = r.record(source)

    return (r.recognize_google(audio, language='es-Es'))

def convert_text_to_audio(text):
    engine = pyttsx3.init()

    engine.setProperty('rate', 150)
    engine.setProperty('voice', 'spanish')

    output_path = 'static/uploads/test.wav'
    engine.save_to_file(text, output_path)
    engine.runAndWait()

    with open(output_path, 'rb') as f:
        file = FileStorage(f)
        file.filename = output_path.split('/')[-1]
        name_file = upload_file_to_s3(file)
        os.remove(output_path)
        return name_file
