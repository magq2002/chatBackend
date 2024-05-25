import speech_recognition as sr
import pyttsx3
import tempfile
import os
from app.services.s3_service import upload_file_to_s3

def convert_audio_to_text(audio_data):
    r = sr.Recognizer()
    with sr.AudioData(audio_data) as source:
        text = r.recognize_google(source, language='es-ES')
    return text
    '''
    r = sr.Recognizer()
    audio_file = sr.AudioFile(audio_path)

    with audio_file as source:
        r.adjust_for_ambient_noise(source)
        audio = r.record(source)

    return (r.recognize_google(audio, language='es-Es'))
    '''
def convert_text_to_audio(text):
    engine = pyttsx3.init()

    engine.setProperty('rate', 150)

    engine.setProperty('voice', 'spanish')
    ##engine.say(text)
    temp_audio_file = tempfile.NamedTemporaryFile(delete=False)
    temp_audio_path = temp_audio_file.name
    engine.save_to_file(text, temp_audio_path)
    engine.runAndWait()

    upload_file_to_s3(temp_audio_file)
    os.unlink(temp_audio_path)


