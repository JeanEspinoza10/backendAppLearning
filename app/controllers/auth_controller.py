from app import db
from app.models.users_model import UserModel
from ..utils.response import Response
from flask_jwt_extended import create_access_token, create_refresh_token
from secrets import token_hex



class AuthController:
    def __init__(self):
        self.model = UserModel
        self.response = Response

    def signUp(self, data):
        try:
            if data:
                email = data['email']
                password = data['password']

                # 1ª Validar que el usuario exista y no este inhabilitado
                record = self.model.where(email=email, status=True).first()
                if record:
                    # 2ª Validar que la contraseña sea correcta
                    if record.checkPassword(password):
                        # 3º Creación de JWT (Access Token y Refresh Token)
                        user_id = record.id
                        access_token = create_access_token(identity=user_id)
                        refresh_token = create_refresh_token(identity=user_id)
                        data = [{
                            'access_token': access_token,
                            'refresh_token': refresh_token
                        }]
                        return self.response.code200(message="User SignUP", data= data)
                    else:
                        raise Exception('Password incorrect')

                raise Exception('Not found in email')
            else:
                return self.response.code404(message="Email or password was not sent")
        except Exception as e:
            return {
                'message': 'An error occurred',
                'error': str(e)
            }, 500