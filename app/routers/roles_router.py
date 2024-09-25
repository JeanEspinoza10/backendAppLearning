from app import api
from flask_restx import Resource
from flask_jwt_extended import jwt_required
from app.controllers.roles_controller import RolesController
from app.utils.decorators import role_required

role_ns = api.namespace(
    name = "Rol",
    description = "Routers for Roles",
    path = "/roles"
)

@role_ns.route("")
@role_ns.doc(security="Bearer")
class Roles(Resource):
    @jwt_required()
    @role_required(rol_id=1)
    def get(self):
        ''' List all roles'''
        controller = RolesController()
        return controller.all()
