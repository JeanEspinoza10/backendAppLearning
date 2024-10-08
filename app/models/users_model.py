from app.models.base import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from bcrypt import hashpw, gensalt, checkpw

class UserModel(BaseModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80))
    status = Column(Boolean, default=True)

    email = Column(String(140), unique=True)
    password = Column(String(120), nullable=False)

    rol_id = Column(Integer, ForeignKey('roles.id'))
    role = relationship('RoleModel', uselist=False, back_populates='users')

    usersPhrases = relationship('PhrasesModel', uselist=True, back_populates='users')
    usersVerification = relationship('VerificationModel', uselist=True, back_populates='users')

    def hashPassword(self):
        pwd_encode = self.password.encode('utf-8')
        pwd_hash = hashpw(pwd_encode, gensalt(rounds=10))
        self.password = pwd_hash.decode('utf-8')

    def checkPassword(self, password):
        return checkpw(
            password.encode('utf-8'),
            self.password.encode('utf-8')
        )