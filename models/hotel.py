from sqlalchemy import Column, Integer, String, Text
from database import Base

class Hotel(Base):
    __tablename__ = 'hotel'
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255))
    adresse = Column(Text)
