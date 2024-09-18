from app.models.base import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class UserModel(BaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80))
    status = Column(Boolean, default=True)

    rol_id = Column(Integer, ForeignKey('roles.id'))
    role = relationship('RoleModel', uselist=False, back_populates='users')

    usersPhrases = relationship('PhrasesModel', uselist=True, back_populates='users')
    