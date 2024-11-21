from app import api
from flask import  request
from flask_restx import Resource
from app.controllers.services_controller import ServiceController
from app.schemas.phrases_schemas import PhrasesRequestSchema

service_ns = api.namespace(
    name='Services',
    description='Routers for Services',
    path='/services'
)
request_schema = PhrasesRequestSchema(service_ns)

@service_ns.route('/free/phrases')
class DataFree(Resource):
    def get(self):
        '''
            End point that returns data of phrases
        '''
        try:
            controller = ServiceController()
            return controller.free()
        except Exception as err:
            return {
                "messge": f"Mistakes in consult : {err}",
                "code":500,
            },500

@service_ns.route('/free/sound/<int:id>')
class SoundFree(Resource):
    def get(self,id):
        '''
            End point that returns sounds
        '''
        try:            
            controller = ServiceController()
            return controller.download_free(id=id,valueItem="sound_url")
        except Exception as err:
            return {
                "messge": f"Mistakes in consult: {err}",
                "code":500,
            },500
        
@service_ns.route('/free/img/<int:id>')
class ImgFree(Resource):
    def get(self,id):
        '''
            End point that returns images
        '''
        try:
            controller = ServiceController()
            return controller.download_free(id=id,valueItem="img_url")
        except Exception as err:    
            return {
                "messge": f"Mistakes in consult: {err}",
                "code":500,
            },500
            
@service_ns.route('/free/create')
class CreateFree(Resource):
    @service_ns.expect(request_schema.create(), validate=True)
    def post(self):
        '''Create free phrases'''
        try:
            controller = ServiceController()
            return controller.free_create(request)
        except Exception as err:
            return {
                "messge": f"Mistakes in consult : {err}",
                "code":500,
            },500
@service_ns.route('/free/phrases/browsers')
class PhrasesFreeBrowsers(Resource):
    def get(self):
        '''
            End point that returns data of phrases for browsers
        '''
        try:
            controller = ServiceController()
            return controller.free_browsersAll(request)
        except Exception as err:
            return {
                "messge": f"Mistakes in consult : {err}",
                "code":500,
            },500