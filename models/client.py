from sqlalchemy import Column, Integer, String
from database import Base

class Client(Base):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255))
    email = Column(String(255))
    tel = Column(String(20))
