from app.models.base import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey,Text,DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class PhrasesModel(BaseModel):
    __tablename__ = 'phrases'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(220))
    img_url = Column(Text())
    sound_url = Column(Text())
    description = Column(Text())
    translation = Column(Text())
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'))
    users = relationship('UserModel', uselist=False, back_populates='usersPhrases')
    
    browsers_id = Column(Integer, ForeignKey('browsers.id'))
    browsers = relationship('BrowserModel', uselist=False, back_populates='browsersPhrases')

    status = Column(Boolean, default=True)