from app import api
from flask_restx import Resource
from app.schemas.phrases_schemas import PhrasesRequestSchema
from flask_jwt_extended import jwt_required
from app.controllers.phrases_controller import PhrasesController
from flask import request

phrases_ns = api.namespace(
    name='Phrases',
    description='Routers for phrases',
    path='/phrases'
)

request_schema = PhrasesRequestSchema(phrases_ns)

@phrases_ns.route('/all')
@phrases_ns.doc(security="Bearer")
class PhrasesAll(Resource):
    @jwt_required()
    def get(self):
        ''' List all phrases for user'''
        controller = PhrasesController()
        return controller.getAll()
    
@phrases_ns.route('/create')
@phrases_ns.doc(security="Bearer")
class PhrasesCreate(Resource):
    @jwt_required()
    @phrases_ns.expect(request_schema.create(), validate=True)
    def post(self):
        ''' Create phrases'''
        controller = PhrasesController()
        return controller.create(request.json)

@phrases_ns.route('/update')
@phrases_ns.doc(security="Bearer")
class PhrasesUpdate(Resource):
    @jwt_required()
    @phrases_ns.expect(request_schema.update(), validate=True)
    def post(self):
        ''' Update phrases only status'''
        controller = PhrasesController()
        return controller.update(request.json)

@phrases_ns.route('/img/<int:id>')
@phrases_ns.doc(security="Bearer")
class PhrasesImg(Resource):
    @jwt_required()
    def get(self,id):
        ''' Get phrases img'''
        controller = PhrasesController()
        return controller.download(id=id,valueItem="img_url")
    
@phrases_ns.route('/sound/<int:id>')
@phrases_ns.doc(security="Bearer")
class PhrasesSound(Resource):
    @jwt_required()
    def get(self,id):
        ''' Get phrases sound'''
        controller = PhrasesController()
        return controller.download(id=id,valueItem="sound_url")