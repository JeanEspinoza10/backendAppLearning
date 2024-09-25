from app import api
from flask_restx import Resource
from app.controllers.users_controller import UsersController
from flask_jwt_extended import jwt_required
from app.utils.decorators import role_required

user_ns = api.namespace(
    name = "User",
    description = "Routers for users",
    path = "/users"
)

@user_ns.route("/<int:id>")
@user_ns.doc(security="Bearer")
class UserById(Resource):
    @jwt_required()
    @role_required(rol_id=1)
    def get(self, id):
        ''' Obtener un usuario por el ID '''
        controller = UsersController()
        return controller.getById(id)