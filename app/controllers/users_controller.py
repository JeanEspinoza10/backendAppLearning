from app import db
from app.models.users_model import UserModel


class UsersController:
    def __init__(self):
        self.model = UserModel

    def all(self):
        try:
            records =  self.model.where(status=True).order_by("id")
            if records:
                records_list = [{"id": record.id, "name": record.name, "email": record.email} for record in records]
                return {
                    "message":"Users found",
                    "code":200,
                    "data": records_list,
                },200
            return {
                "message": "Not found users",
                "code": 404,
                "data": [],
            },404
        except Exception as e:
            return {
                "message": "An error occurred",
                "mistake": str(e)
            },500
        
    def delete(self,id):
        try:
            record = self.model.where(id=id).first()
            if record:
                record.status = False
                db.session.add(record)
                db.session.commit()
                return {
                    "message": "User deleted successfully",
                    "code": 200,
                    "data": [],
                },200
            return {
                "message": "Not found user",
                "code": 404,
                "data": [],
            },404
        except Exception as e:
            return {
                "message": "An error occurred",
                "mistake": str(e)
            },