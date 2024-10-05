from app import db
from app.models.users_model import UserModel
from app.utils.response import Response
from app.controllers.phrases_controller import PhrasesController
from app.controllers.verification_controller import VerificationController
from app.utils.sendmail import SendMail
from flask_jwt_extended import create_access_token, create_refresh_token, current_user
from secrets import token_hex



class AuthController:
    def __init__(self):
        self.model = UserModel
        self.rol_id = 2
        self.response = Response
        self.current_user = current_user
        self.phrasesController = PhrasesController()
        self.verificationController = VerificationController()
        self.sendMail = SendMail()

    def signIn(self, data):
        try:
            if data:
                email = data['email']
                password = data['password']
                # Validate code
                record_verification = self.verificationController.verifyUserStatus(email=email)
                # 1st Validate that the user exists and is not disabled
                record = self.model.where(email=email, status=True).first()
                if record:
                    # 2. Validate that the password is correct
                    if record.checkPassword(password):
                        # 3rd Creation of JWT (Access Token and Refresh Token)
                        user_id = record.id
                        access_token = create_access_token(identity=user_id)
                        refresh_token = create_refresh_token(identity=user_id)
                        data = [{
                            'name': record.name,
                            'access_token': access_token,
                            'refresh_token': refresh_token,
                            'verification': record_verification,
                        }]
                        return self.response.code200(message="User SignIn", data= data)
                    else:
                        raise Exception('Password incorrect')
                raise Exception('Not found in email')
            else:
                return self.response.code404(message="Email or password was not sent")
        except Exception as e:
            return self.response.code400(message=f"An error occurred: {e}")
        
    def signUp(self, data):
        try:
             # Ingresar o insertar el rol_id
            data['rol_id'] = self.rol_id
            new_record = self.model.create(**data)
            new_record.hashPassword()
            # Generar Phrases for deafult
            phrase_default = {
                'phrase': "Bienvenido",
            }
            response = self.phrasesController.create(data=phrase_default,user_id=new_record.id)
            response_verification = self.verificationController.create(user_id=new_record.id,email=data['email'])
            # Response
            response_data = {
                
            }
            db.session.add(new_record)
            db.session.commit()
            return self.response.code200(message="User created successfully",data=response_data)
        except Exception as e:
            return self.response.code400(message=f"An error occurred: {e}")

    def refreshToken(self, identity):
        try:
            access_token = create_access_token(identity=identity)
            refresh_token = create_refresh_token(identity=identity)
            return self.response.code200(message="Token refreshed successfully", data=[{
                "access_token": access_token,
                "refresh_token": refresh_token
                }])
        except Exception as e:
            return self.response.code400(message=f"An error occurred: {e}")

    def resetPassword(self, data):
        try:
            email = data['email']
            record = self.model.where(email=email).first()
            if record:
                new_password = token_hex(5)
                record.password = new_password
                record.hashPassword()
                db.session.add(record)
                db.session.commit()
                self.sendMail.send(to=email, subject="Password reset", message=f"The new password is:: {new_password}")
                return self.response.code200(message="Password reset successfully")
            return self.response.code404(message="Email not found or not the same user")
        except Exception as e:
            db.session.rollback()
            return self.response.code400(message=f"An error occurred: {e}")
        
    def resetPasswordAfterVerification(self,data):
        try:
            email = data['email']
            password = data['password']
            record = self.model.where(email=email).first()
            if record:
                record.password = password
                record.hashPassword()
                db.session.add(record)
                db.session.commit()
                self.sendMail.send(to=email, subject="Password reset", message=f"A change has been made to your password.")
                return self.response.code200(message="Password reset successfully")
            else:
                return self.response.code404(message="Email not found or not the same user")
        except Exception as e:
            db.session.rollback()
            return self.response.code400(message=f"An error occurred: {e}")
        
    def validateToken(self):
        try:
            user_id = self.current_user.id
            record = self.model.where(id=user_id).first()
            if record:
                return self.response.code200(message="Token validated successfully")
        except Exception as e:
            return  self.response.code400(message=f"An error occurred: {e}")
        
    def validateCodeVerification(self,data):
        try:
            email = data['email']
            code = data['code']
            record = self.verificationController.verifyCode(email=email,code=code)
            if record:
                return self.response.code200(message="Code verification correct")
        except Exception as e:
            return self.response.code400(message=f"An error occurred: {e}")
        
    def newCode(self,data):
        try:
            email = data['email']
            record = self.model.where(email=email).first()
            return self.verificationController.create(user_id=record.id,email=data['email'])
        except Exception as e:
            return self.response.code400(message=f"An error occurred: {e}")