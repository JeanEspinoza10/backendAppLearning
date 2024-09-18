
import os
import uuid
from dotenv import load_dotenv
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from io import BytesIO
import boto3

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
REGION_NAME = os.getenv("REGION_NAME")
BUCCKET_NAME = os.getenv("BUCCKET_NAME")



class Sounds():
    def __init__(self):
        self.client_ElevenLabs = ElevenLabs(api_key=ELEVENLABS_API_KEY,)
        
        self.session_aws = boto3.session.Session(aws_access_key_id=AWS_ACCESS_KEY_ID,
                                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                        region_name=REGION_NAME)

    def text_to_speech_file(self,text):
        try:
            # Calling the text_to_speech conversion API with detailed parameters
            response = self.client_ElevenLabs.text_to_speech.convert(
                voice_id="pNInz6obpgDQGcFmaJgB",
                output_format="mp3_22050_32",
                text=text,
                model_id="eleven_turbo_v2_5",
                voice_settings=VoiceSettings(
                    stability=0.0,
                    similarity_boost=1.0,
                    style=0.0,
                    use_speaker_boost=True,
                ),
            )
            # Create a BytesIO object to hold the file in memory
            file_stream = BytesIO()
            # Write the response content to the BytesIO stream
            for chunk in response:
                if chunk:
                    file_stream.write(chunk)
            # Reset the stream position to the beginning
            file_stream.seek(0)
            # Generate a unique file name for the output MP3 file
            file_name = f"{uuid.uuid4()}.mp3"
            # Upload the file directly to S3
            s3_client = self.session_aws.client('s3')
            s3_client.upload_fileobj(file_stream, BUCCKET_NAME, file_name)
            return file_name
        except Exception as err:
            raise Exception("Mistake in function for save text in respository:",err)
        
    
    def download_file(self,file_name):
        try:
            s3 = self.session_aws.client('s3')
            file_stream = BytesIO()
            s3.download_fileobj('appingles', file_name, file_stream)
            file_stream.seek(0)
            return file_stream
        except Exception as err:
            raise Exception("Mistake in function download file from repository:",err)