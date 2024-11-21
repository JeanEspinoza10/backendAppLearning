from app import api
from flask import  request
from flask_restx import Resource
from app.controllers.services_controller import ServiceController

service_ns = api.namespace(
    name='Services',
    description='Routers for Services',
    path='/services'
)


@service_ns.route('/free/phrases')
class DataFree(Resource):
    def get(self):
        try:
            '''
            End point that returns data of phrases
            '''
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
        try:
            '''
            End point that returns sounds
            '''
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
        try:
            '''
            End point that returns sounds
            '''
            controller = ServiceController()
            return controller.download_free(id=id,valueItem="img_url")
        except Exception as err:    
            return {
                "messge": f"Mistakes in consult: {err}",
                "code":500,
            },500
            
@service_ns.route('/free/create')
class CreateFree(Resource):
    def get(self):
        # Intentar obtener la IP del encabezado X-Forwarded-For
        client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        return f"La IP del cliente es: {client_ip}"
    