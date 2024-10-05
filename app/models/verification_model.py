from app.models.base import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey,Text,DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class VerificationModel(BaseModel):
    __tablename__ = 'verification'

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    user_id = Column(Integer, ForeignKey('users.id'))
    users = relationship('UserModel', uselist=False, back_populates='usersVerification')

    status = Column(Boolean, default=True)
    email = Column(String(140))
    code = Column(String(6))
    date_verification = Column(DateTime, server_default=func.now(), nullable=False)