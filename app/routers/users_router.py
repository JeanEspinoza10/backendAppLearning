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

@user_ns.route("/all")
@user_ns.doc(security="Bearer")
class Users(Resource):
    @jwt_required()
    @role_required(rol_id=1)
    def get(self):
        ''' List all users'''
        controller = UsersController()
        return controller.all()

@user_ns.route("/<int:id>")
@user_ns.doc(security="Bearer")
class UserById(Resource):
    @jwt_required()
    @role_required(rol_id=1)
    def delete(self, id):
        ''' Delete user by id'''
        controller = UsersController()
        return controller.delete(id)