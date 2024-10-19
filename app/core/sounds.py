
from dotenv import load_dotenv
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from io import BytesIO
from app.core.aws import AWS
from openai import OpenAI
import os
import uuid

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
REGION_NAME = os.getenv("REGION_NAME")
BUCCKET_NAME = os.getenv("BUCCKET_NAME")
OPENAI_KEY = os.getenv("OPENAI_KEY")


class Sounds():
    def __init__(self):
        self.client_ElevenLabs = ElevenLabs(api_key=ELEVENLABS_API_KEY,)
        self.clientOPENAI = OpenAI(api_key=OPENAI_KEY)
        self.aws = AWS()

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
            self.aws.upload_file(file_name,file_stream)
            return file_name
        except Exception as err:
            raise Exception("Mistake in function generate sound:",err)
    
    def text_to_speech_file_OpenAI(self,text):
        try:
            response = self.clientOPENAI.audio.speech.create(
                    model="tts-1",
                    voice="alloy",
                    input=text,
                )
            audio_content = response.content
            file_stream = BytesIO(audio_content) 
            file_stream.seek(0)
            file_name = f"{uuid.uuid4()}.mp3"
            self.aws.upload_file(file_name,file_stream)
            return file_name
        except Exception as err:
            raise Exception("Mistake in function generate sound:",err)