import base64
from app.core.aws import AWS
from app.core.phrases import Phrases
from app.core.sounds import Sounds
from app.models.phrases_model import PhrasesModel
from app.utils.response import Response
from flask_jwt_extended import current_user
from app.core.generate_img import GeneretaImg
from datetime import date
from app import db

class PhrasesController:
    def __init__(self):
        self.phrasesModel = PhrasesModel
        self.aws = AWS()
        self.generatePhrases = Phrases()
        self.generateSounds = Sounds()
        self.response = Response
        self.current_user = current_user
        self.generateImg = GeneretaImg()

    def validateQuantity(self,user_id):
        try:
            records = self.phrasesModel.where(user_id=user_id).order_by('id')
            date_today = date.today()
            quantity = 0
            for record in records:
                if record.created_at.date() == date_today:
                    quantity += 1
            if quantity >= 3:
                raise Exception('You can not create more than 3 phrases per day')
            else:
                return True
        except Exception as e:
            raise Exception(f"{e}")
    
    def getAll(self):
        try:
            user_id = int(self.current_user.id)
            records = self.phrasesModel.where(user_id=user_id, status=True).order_by('id').all()
            data = []
            if records:
                for record in records:
                    record_dict = {
                        'id': record.id,
                        'title': record.title,
                        'sound_url': record.sound_url,
                        'description': record.description,
                        'translation':record.translation,
                        'img_url':record.img_url
                    }
                    data.append(record_dict)
                return self.response.code200(message="Phrases found", data=data)
            return self.response.code404(message="Phrases not found for users")
        except Exception as e:
            return self.response.code400(message=f"An error occurred: {e}")
        
    def create(self, data, user_id=0):
        try:
            prompt = data['phrase']
            if len(prompt) > 80:
                raise Exception('Phrases must be less than 80 characters')
            if user_id != 0:
                user_id = user_id
            else:
                user_id = self.current_user.id
            
            quantity = self.validateQuantity(user_id=user_id)
            if quantity:
                title = self.generatePhrases.generate_phrases(prompt=prompt)
                sound_url = self.generateSounds.text_to_speech_file_OpenAI(text=title)
                img_url = self.generateImg.generate_img(prompt=title,user_id=user_id)
                translation = prompt
                description = self.generatePhrases.generate_description(prompt=title)
                data_record = {
                    'title': title,
                    'sound_url': sound_url,
                    'description': description,
                    'translation': translation,
                    'img_url': img_url,
                    'user_id': user_id,
                }
                record = self.phrasesModel.create(**data_record)
                db.session.add(record)
                db.session.commit()
                return self.response.code200(message="Create phrases correct.",data=data_record)
        except Exception as e:
            return self.response.code400(message=f"An error occurred:{e}")
        
    def update(self, data):
        try:
            user_id = self.current_user.id
            id = int(data['id'])
            record = self.phrasesModel.where(id=id,user_id=user_id).first()
            if record:
                data_record = {
                    'status': data["status"]
                }
                record.update(**data_record)
                db.session.add(record)
                db.session.commit()
                return self.response.code200(message="Update phrases correct.")
            return self.response.code404(message="Phrases not found")
        except Exception as e:
            message=f"An error occurred:{e}"
            return self.response.code400(message=message)
    
    def download(self,id,valueItem):
        try:
            user_id = self.current_user.id
            record_phrase = self.phrasesModel.query.filter(self.phrasesModel.id == id, user_id == user_id).first()
            if record_phrase.user_id == user_id:
                file_sound = self.aws.download_file(getattr(record_phrase, valueItem, None))
                file_content = file_sound.read()
                encoded_content = base64.b64encode(file_content).decode('utf-8')
                response = {
                    'file_name': getattr(record_phrase, valueItem, None),
                    'file_content_base64': encoded_content
                }
                return self.response.code200(message="Content of file sound",data=response)
            else:
                return self.response.code404(message="Not have permission for record")                
        except Exception as e:
            message=f"An error occurred:{e}"
            return self.response.code400(message=message)