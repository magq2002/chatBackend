import os


class Config:
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/chatbot_db')

    # AWS S3 Configuration
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_S3_BUCKET = os.getenv('AWS_S3_BUCKET')
    AWS_S3_REGION = os.getenv('AWS_S3_REGION', 'us-west-2')
    AWS_S3_URL = f'https://{AWS_S3_BUCKET}.s3.{AWS_S3_REGION}.amazonaws.com'

    # Directory for storing audio files locally before upload
    AUDIO_UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    os.makedirs(AUDIO_UPLOAD_FOLDER, exist_ok=True)

