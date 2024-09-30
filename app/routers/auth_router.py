from app import api
from flask_restx import Resource
from flask import request
from app.controllers.auth_controller import AuthController
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.schemas.auth_schemas import AuthRequestSchema
from app.utils.decorators import role_required
auth_ns = api.namespace(
    name='Autenticación',
    description='Routers for authentication',
    path='/auth'
)

request_schema = AuthRequestSchema(auth_ns)

@auth_ns.route('/signup')
class SignUp(Resource):
    @auth_ns.expect(request_schema.signup(), validate=True)
    def post(self):
        '''Users Registration'''
        controller = AuthController()
        return controller.signUp(request.json)
@auth_ns.route('/signin')
class SignIn(Resource):
    @auth_ns.expect(request_schema.signin(), validate=True)
    def post(self):
        '''Users Sign In'''
        controller = AuthController()
        return controller.signIn(request.json)
    
@auth_ns.route('/token/refresh')
class RefreshToken(Resource):
    @jwt_required(refresh=True)
    @auth_ns.expect(request_schema.refreshToken(), validate=True)
    def post(self):
        '''Refresh Token'''
        identity = get_jwt_identity()
        controller = AuthController()
        return controller.refreshToken(identity)

@auth_ns.route('/token/validate')
@auth_ns.doc(security="Bearer")
class ValidateToken(Resource):
    @jwt_required()
    def get(self):
        '''Validate Token'''
        controller = AuthController()
        return controller.validateToken()

@auth_ns.route('/reset_password')
@auth_ns.doc(security="Bearer")
class ResetPassword(Resource):
    @auth_ns.expect(request_schema.resetPassword(), validate=True)
    @jwt_required()
    def post(self):
        '''Reset Password'''
        identity = get_jwt_identity()
        data = request.json
        controller = AuthController()
        return controller.resetPassword(data, identity)
    
