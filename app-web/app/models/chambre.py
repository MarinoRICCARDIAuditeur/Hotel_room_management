from sqlalchemy import Column, Integer, String, DECIMAL, Enum, ForeignKey
from app.database import Base
import enum

class TypeChambre(enum.Enum):
    simple = "simple"
    double = "double"
    suite = "suite"

class EtatChambre(enum.Enum):
    libre = "libre"
    occupee = "occupee"
    maintenance = "maintenance"

class Chambre(Base):
    __tablename__ = 'chambre'
    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String(20))
    type = Column(Enum(TypeChambre))
    prix = Column(DECIMAL(10,2))
    etat = Column(Enum(EtatChambre), default=EtatChambre.libre)
    hotel_id = Column(Integer, ForeignKey("hotel.id"))
