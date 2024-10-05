
from app import db
from app.models.verification_model import VerificationModel
from app.utils.sendmail import SendMail
from app.utils.response import Response
import random

class VerificationController:
    def __init__(self):
        self.model = VerificationModel
        self.sendMail = SendMail()
        self.response = Response
        self.random = random

    def create(self,user_id,email):
        try:
            data = {
                'user_id': user_id,
                'email': email,
                'code': self.random.randint(1000,9999)
            }
            # Update or Create code
            record = self.model.where(email=email).first()
            if record:
                record.update(**data)
            else:
                record = self.model.create(**data)
                db.session.add(record)
                db.session.commit()
            self.sendMail.send(to=email, subject="Verification code", message=f"Your verification code is {record.code}")
            return self.response.code200(message="Verification code created successfully")
        except Exception as e :
            return self.response.code400(message=f"An error occurred: {e}")
        
    def verifyCode(self,email,code):
        try:
            record = self.model.where(email = email, status=True).first()
            if record and record.code == code:
                record.status = False
                db.session.add(record)
                db.session.commit()
                return True
            else:
                raise Exception('Verification code incorrect')
        except Exception as e:
            raise Exception(f"{e}")
        
    def verifyUserStatus(self,email):
        try:
            record = self.model.where(email=email, status=True).all()
            if record:
                raise Exception('User needs to verify their code')
            else:
                return True
        except Exception as e:
            raise Exception(f"{e}")