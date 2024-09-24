from app import db
from app.models.roles_model import RoleModel

class RolesController:
    def __init__(self):
        self.model = RoleModel
    
    def all(self):
        try:
            records =  self.model.where(status=True).order_by("id")
            if records:
                records_list = [record.to_dict() for record in records]
                return {
                    "message":"Roles found",
                    "code":200,
                    "data": records_list,
                },200
            return {
                "message": "Not found roles",
                "code": 404,
                "data": [],
            }
        except Exception as e:
            return {
                "message": "An error occurred",
                "mistake": str(e)
            },500