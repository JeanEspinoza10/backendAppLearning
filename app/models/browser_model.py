from app.models.base import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey,DateTime,func
from sqlalchemy.orm import relationship

class BrowserModel(BaseModel):
    __tablename__ = 'browsers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String(15))
    count = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    
    browsersPhrases = relationship('PhrasesModel', uselist=True, back_populates='browsers')
    