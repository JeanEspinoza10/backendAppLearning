import base64
from app.core.aws import AWS
from app.core.phrases import Phrases
from app.core.sounds import Sounds
from app import db
from app.models.roles_model import RoleModel
from app.models.users_model import UserModel
from app.models.phrases_model import PhrasesModel
from app.models.browser_model import BrowserModel
from app.core.generate_img import GeneretaImg

class ServiceController:
    def __init__(self):
        self.userModel = UserModel
        self.rolModel = RoleModel
        self.phrasesModel = PhrasesModel
        self.browserModel = BrowserModel
        self.generatePhrases = Phrases()
        self.generateSounds = Sounds()
        self.generateImg = GeneretaImg()
        self.aws = AWS()
    def free(self):
        try:
            records_phrases = self.phrasesModel.query.filter(self.phrasesModel.user_id == None).all()
            if not records_phrases:
                data = self.generatePhrases.generate_localhost()
                for element in data['phrases']:
                    sound_url = self.generateSounds.text_to_speech_file_OpenAI(element["phrase"])
                    img_url = self.generateImg.generate_img(prompt=element["phrase"])
                    record = self.phrasesModel.create(
                        title= element["phrase"],
                        sound_url =sound_url,
                        description = element["description"],
                        translation = element["translation"],
                        img_url = img_url,
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
                    'translation':record.translation,
                    'img_url':record.img_url
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
        
    
    def download_free(self,id,valueItem):
        try:
            record_phrase = self.phrasesModel.query.filter(self.phrasesModel.id == id).first()
            if record_phrase.user_id:
                return {
                        'message':'Not have permission for record',
                        'code':401,
                        'data':[],
                    },401
            else:
                file_sound = self.aws.download_file(getattr(record_phrase, valueItem, None))
                file_content = file_sound.read()
                encoded_content = base64.b64encode(file_content).decode('utf-8')
                response = {
                    'file_name': getattr(record_phrase, valueItem, None),
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
    
    def free_create(self,request):
        try:
            data = request.json
            browser_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
            # Getting quantity of browsers
            record_browser = self.browserModel.where(ip= browser_ip).first()
            if record_browser:
                quantity = record_browser.count
                if quantity >= 3:
                    return {
                        'message':'You can not create more than 3 phrases',
                        'code':401,
                        'data':[],
                    },401
            else:
                record_browser = self.browserModel.create(
                    ip=browser_ip
                )
                db.session.add(record_browser)
                db.session.commit()
            
            prompt = data['phrase']
            if len(prompt) > 80:
                raise Exception('Phrases must be less than 80 characters')
            
            title = self.generatePhrases.generate_phrases(prompt=prompt)
            sound_url = self.generateSounds.text_to_speech_file_OpenAI(text=title)
            img_url = self.generateImg.generate_img(prompt=title,user_id=browser_ip)
            translation = prompt
            description = self.generatePhrases.generate_description(prompt=title)
            data_record = {
                'title': title,
                'sound_url': sound_url,
                'description': description,
                'translation': translation,
                'img_url': img_url,
                'browsers_id': record_browser.id,
                'user_id': 1,
            }
            record = self.phrasesModel.create(**data_record)
            if record:
                record_browser.count += 1
            db.session.add(record)
            db.session.commit()
            return {
                'message':'Phrases created',
                'code':200,
                'data':data_record,
            },200            
        except Exception as err:
            return {
                "message":str(err),
                "code": 500,
                "data":[]
            },500
    
    def free_browsersAll(self, request):
        try:
            ip = request.headers.get('X-Forwarded-For', request.remote_addr)
            record_browser = self.browserModel.where(ip=ip).first()
            if not record_browser:
                return {
                    'message':'No browser found, please create is phrases',
                    'code':404,
                    'data':[],
                },404
                
            records_phrases = self.phrasesModel.where(browsers_id=record_browser.id).all()
            if records_phrases:
                # Become response a JSON
                response = []
                for record in records_phrases:
                    record_dict = {
                        'id': record.id,
                        'title': record.title,
                        'sound_url': record.sound_url,
                        'description': record.description,
                        'translation':record.translation,
                        'img_url':record.img_url
                    }
                    response.append(record_dict)
                return {
                    'message':'List of Phrases',
                    'code':200,
                    'data':response,
                },200
            else:
                return {
                    'message':'No phrases found',
                    'code':404,
                    'data':[],
                },404
                        
        except Exception as err:
            return {
                "message":str(err),
                "code": 500,
                "data":[]
            },500