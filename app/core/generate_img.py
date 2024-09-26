from openai import OpenAI
from dotenv import load_dotenv
from app.core.aws import AWS
from io import BytesIO
import requests
import uuid
import os
import json

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")
class GeneretaImg:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_KEY)
        self.aws = AWS()
    def generate_img(self,prompt,user_id=1):
        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            # Logic for save image in AWS
            image_url = response.data[0].url
            response_url = requests.get(image_url)
            img_data = BytesIO(response_url.content)
            img_data.seek(0)
            file_name = f"{user_id}{uuid.uuid4()}.jpg"
            self.aws.upload_file(file_name,file_content=img_data)
            return file_name
        except Exception as err:
            raise Exception("Mistake in phrases generate: ",err)
        

    