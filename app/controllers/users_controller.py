from app import db
from app.models.users_model import UserModel


class UsersController:
    def __init__(self):
        self.model = UserModel

    def getById(self,id):
        try:
            pass
        except Exception as e :
            pass