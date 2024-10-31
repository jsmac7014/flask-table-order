import boto3
from dotenv import load_dotenv
import os

load_dotenv()

def connect():
    s3 = boto3.client("s3",
                      endpoint_url=os.getenv('S3_ENDPOINT_URL'),
                      aws_access_key_id=os.getenv("S3_ACCESS_KEY_ID"),
                      aws_secret_access_key=os.getenv("S3_SECRET_ACCESS_KEY"),
                      region_name=os.getenv("S3_REGION_NAME")
                      )
    return s3


