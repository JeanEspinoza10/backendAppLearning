import os
import json
from ..utils.const import data_phrases
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")

class Phrases():
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_KEY)
    def generate_phrases_free(self):
        try:
            completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo", 
            messages=[
                {"role": "user", "content": "Give me 10 phrases in english."}
            ],
            max_tokens=30
            )
            response = completion.choices[0].message.content
            return response
        except Exception as err:
            raise Exception("Mistake in phrases generate free: ",err)
        
    def generate_localhost(self):
        try:
            data = data_phrases
            return data
        except Exception as err:
            raise Exception("Mistake in phrases generate free localhost:",err)