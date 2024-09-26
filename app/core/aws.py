import os
from dotenv import load_dotenv
from io import BytesIO
import boto3

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
REGION_NAME = os.getenv("REGION_NAME")
BUCCKET_NAME = os.getenv("BUCCKET_NAME")

class AWS():
    def __init__(self):
        self.session_aws = boto3.session.Session(aws_access_key_id=AWS_ACCESS_KEY_ID,
                                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                        region_name=REGION_NAME)
    def upload_file(self,file_name,file_content):
        try:
            s3_client = self.session_aws.client('s3')
            s3_client.upload_fileobj(file_content, BUCCKET_NAME, file_name)
            return file_name
        except Exception as err:
            raise Exception("Mistake in function for upload file in respository:",err)
        
    def download_file(self,file_name):
        try:
            s3 = self.session_aws.client('s3')
            file_stream = BytesIO()
            s3.download_fileobj('appingles', file_name, file_stream)
            file_stream.seek(0)
            return file_stream
        except Exception as err:
            raise Exception("Mistake in function download file from repository:",err)