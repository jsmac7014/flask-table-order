import boto3
from dotenv import load_dotenv
import os

from flask import jsonify

load_dotenv()

def connect():
    s3 = boto3.client("s3",
                      endpoint_url=os.getenv('S3_ENDPOINT_URL'),
                      aws_access_key_id=os.getenv("S3_ACCESS_KEY_ID"),
                      aws_secret_access_key=os.getenv("S3_SECRET_ACCESS_KEY"),
                      region_name=os.getenv("S3_REGION_NAME")
                      )
    return s3


def upload_file(file,  key):
    s3 = connect()
    try:
        filename = _create_random_filename(key)
        image_dir = "food-images/" + filename + "/"
        s3.upload_fileobj(file, 'table-order', image_dir)
        return jsonify({"url": f"https://image.jungwoo.xyz/{image_dir}"})
    except Exception as e:
        print(e)
        return False

def _create_random_filename(filename):
    import uuid
    return str(uuid.uuid4()) + '.' + filename.split('.')[-1]