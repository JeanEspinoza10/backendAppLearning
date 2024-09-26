from app import db
from app.models.users_model import UserModel
from app.utils.response import Response
from flask_jwt_extended import create_access_token, create_refresh_token
from secrets import token_hex



class AuthController:
    def __init__(self):
        self.model = UserModel
        self.rol_id = 2
        self.response = Response

    def signIn(self, data):
        try:
            if data:
                email = data['email']
                password = data['password']
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
                            'access_token': access_token,
                            'refresh_token': refresh_token
                        }]
                        return self.response.code200(message="User SignIn", data= data)
                    else:
                        raise Exception('Password incorrect')
                raise Exception('Not found in email')
            else:
                return self.response.code404(message="Email or password was not sent")
        except Exception as e:
            return self.response.code500(message=f"An error occurred: {e}")
        
    def signUp(self, data):
        try:
             # Ingresar o insertar el rol_id
            data['rol_id'] = self.rol_id
            new_record = self.model.create(**data)
            new_record.hashPassword()
            db.session.add(new_record)
            db.session.commit()
            return self.response.code200(message="User created successfully")
        except Exception as e:
            self.response.code500(message=f"An error occurred: {e}")

    def refreshToken(self, identity):
        try:
            access_token = create_access_token(identity=identity)
            return self.response.code200(message="Token refreshed successfully", data=[{"access_token": access_token}])
        except Exception as e:
            return  self.response.code500(message=f"An error occurred: {e}")

    def resetPassword(self, data, identity):
        try:
            email = data['email']
            record = self.model.where(email=email).first()
            if record and record.id == identity:
                new_password = token_hex(5)
                record.password = new_password
                record.hashPassword()
                db.session.add(record)
                db.session.commit()
                return self.response.code200(message="Password reset successfully", data=[{
                    "name": record.name,
                    "email": record.email,
                    "new_password": new_password}
                    ])
            return self.response.code404(message="Email not found or not the same user")
        except Exception as e:
            db.session.rollback()
            return self.response.code500(message=f"An error occurred: {e}")