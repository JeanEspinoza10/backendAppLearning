import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")
class GeneretaImg:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_KEY)
    def generate_img(self,prompt):
        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            image_url = response.data[0].url
            return image_url
        except Exception as err:
            raise Exception("Mistake in phrases generate: ",err)