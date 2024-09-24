from app import api
from flask_restx import Resource
from app.controllers.users_controller import UsersController
from flask_jwt_extended import jwt_required

user_ns = api.namespace(
    name = "User",
    description = "Routers for users",
    path = "/users"
)

@user_ns.route("/<int:id>")
class UserById(Resource):
    @jwt_required()
    def get(self, id):
        ''' Obtener un usuario por el ID '''
        controller = UsersController()
        return controller.getById(id)