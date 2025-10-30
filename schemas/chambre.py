from pydantic import BaseModel
from typing import Literal

class ChambreBase(BaseModel):
    numero: str
    type: Literal['simple', 'double', 'suite']
    prix: float
    etat: Literal['libre', 'occupee', 'maintenance']

class ChambreCreate(ChambreBase):
    pass

class ChambreRead(BaseModel):
    id: int
    numero: str
    type: str
    prix: float
    etat: str
    hotel_id: int

    class Config:
        orm_mode = True
