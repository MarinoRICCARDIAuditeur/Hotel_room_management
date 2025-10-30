from sqlalchemy import Column, Integer, Date, ForeignKey, Enum
from database import Base
import enum

class StatusReservation(enum.Enum):
    confirmee = "confirmee"
    annulee = "annulee"

class Reservation(Base):
    __tablename__ = 'reservation'
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey('client.id'))
    chambre_id = Column(Integer, ForeignKey('chambre.id'))
    date_debut = Column(Date)
    date_fin = Column(Date)
    status = Column(Enum(StatusReservation))
