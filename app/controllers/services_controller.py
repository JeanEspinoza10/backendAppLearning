import base64
from ..utils.phrases import Phrases
from ..utils.sounds import Sounds
from app import db
from app.models.roles_model import RoleModel
from app.models.users_model import UserModel
from app.models.phrases_model import PhrasesModel


class ServiceController:
    def __init__(self):
        self.userModel = UserModel
        self.rolModel = RoleModel
        self.phrasesModel = PhrasesModel
        self.generatePhrases = Phrases()
        self.generateSounds = Sounds()
    def free(self):
        try:
            records_phrases = self.phrasesModel.query.filter(self.phrasesModel.user_id == None).all()
            if not records_phrases:
                data = self.generatePhrases.generate_localhost()
                for element in data['phrases']:
                    sound_url = self.generateSounds.text_to_speech_file(element["phrase"])
                    record = self.phrasesModel.create(
                        title= element["phrase"],
                        sound_url =sound_url,
                        description = element["description"],
                        translation = element["translation"],
                    )
                    db.session.add(record)
                    db.session.commit()
                return {
                    'message':'Phrases not found',
                    'code':404,
                    'data':[],
                    },404
            # Become response a JSON
            response = []
            for record in records_phrases:
                record_dict = {
                    'id': record.id,
                    'title': record.title,
                    'sound_url': record.sound_url,
                    'description': record.description,
                    'translation':record.translation
                }
                response.append(record_dict)
            return {
                'message':'List of Phrases',
                'code':200,
                'data':response,
            },200
        except Exception as e:
            return {
                "message":str(e),
                "code":500,
                "data":[],
            },500
        
    
    def download_free(self,id:int):
        try:
            record_phrase = self.phrasesModel.query.filter(self.phrasesModel.id == id).first()
            if record_phrase.user_id:
                return {
                        'message':'Not have permission for record',
                        'code':401,
                        'data':[],
                    },401
            else:
                file_sound = self.generateSounds.download_file(record_phrase.sound_url)
                file_content = file_sound.read()
                encoded_content = base64.b64encode(file_content).decode('utf-8')
                response = {
                    'file_name': record_phrase.sound_url,
                    'file_content_base64': encoded_content
                }
                return {
                    'message':'Content of file sound',
                    'code':200,
                    'data':[response],
                },200
        except Exception as err:
            return {
                "message":str(err),
                "code": 500,
                "data":[]
            },500