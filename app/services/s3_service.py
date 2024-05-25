import boto3
import uuid
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from flask import current_app

def upload_file_to_s3(file):
    new_filename = uuid.uuid4().hex + '.' + file.filename.rsplit('.', 1)[1].lower()

    s3 = boto3.client(
        's3',
        aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'],
        region_name=current_app.config['AWS_S3_REGION']
    )
    bucket_name = "chatbotplnflask"
##    s3.Bucket(bucket_name).upload_fileobj(file, new_filename)
    s3.upload_fileobj(file, current_app.config['AWS_S3_BUCKET'], new_filename)

    return new_filename
