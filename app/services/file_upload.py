import boto3
import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)


def upload_file_to_s3(file, filename):
    try:
        filename = secure_filename(filename)
        
        unique_key = f"{uuid.uuid4()}_{filename}"
        
        bucket_name = os.getenv("AWS_S3_BUCKET_NAME")

        s3_client.put_object(
            Bucket=bucket_name, 
            Key=unique_key, 
            Body=file, 
            ContentType=file.content_type
        )
        
        file_url = f"https://{bucket_name}.s3.{os.getenv('AWS_REGION')}.amazonaws.com/{unique_key}"
        
        return file_url

    except Exception as e:
        raise Exception(f"Error uploading file to S3: {e}")
