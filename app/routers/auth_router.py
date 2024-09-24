from app import api
from flask_restx import Resource
from flask import request
from app.controllers.auth_controller import AuthController
from flask_jwt_extended import jwt_required, get_jwt_identity


auth_ns = api.namespace(
    name='Autenticación',
    description='Routers for authentication',
    path='/auth'
)



@auth_ns.route('/signup')
class SignUp(Resource):
    def post(self):
        ''' Registro de usuario '''
        controller = AuthController()
        return controller.signUp(request.json)
