from flask_restx import fields
from flask_restx.reqparse import RequestParser


class AuthRequestSchema:
    def __init__(self, namespace):
        self.namespace = namespace

    def signin(self):
        return self.namespace.model('Auth SignIn', {
            'email': fields.String(required=True),
            'password': fields.String(required=True)
        })

    def signup(self):
        return self.namespace.model('Auth SignUp', {
            'name': fields.String(required=True, min_length=10, max_length=80),
            'password': fields.String(required=True, min_length=10, max_length=120),
            'email': fields.String(required=True, min_length=3, max_length=140)
        })

    def refreshToken(self):
        parser = RequestParser()
        parser.add_argument(
            'Authorization', type=str, location='headers',
            help='Ej: Bearer {refresh_token}'
        )
        return parser

    def resetPassword(self):
        return self.namespace.model('Auth Reset Password', {
            'email': fields.String(required=True)
        })
    
    def resetPasswordVerification(self):
        return self.namespace.model('Reset Password After Verification', {
            'email': fields.String(required=True),
            'password': fields.String(required=True,min_length=10, max_length=120)
        })
    
    def verificationCode(self):
        return self.namespace.model('Auth Verification', {
            'email': fields.String(required=True),
            'code': fields.String(required=True)
        })