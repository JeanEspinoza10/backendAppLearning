from app import api
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
            }

@service_ns.route('/free/sound/<int:id>')
class SoundFree(Resource):
    def get(self,id):
        try:
            '''
            End point that returns sounds
            '''
            controller = ServiceController()
            return controller.download_free(id=id)
        except Exception as err:
            return {
                "messge": f"Mistakes in consult: {err}",
                "code":500,
            }