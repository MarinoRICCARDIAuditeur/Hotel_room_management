from pydantic import BaseModel
from enum import Enum
from datetime import date

class StatusReservation(str, Enum):
    confirmee = "confirmee"
    annulee = "annulee"

class ReservationBase(BaseModel):
    client_id: int
    chambre_id: int
    date_debut: date
    date_fin: date
    status: StatusReservation

class ReservationCreate(ReservationBase):
    pass

class ReservationRead(ReservationBase):
    id: int

    model_config = {
        "from_attributes": True
    }

