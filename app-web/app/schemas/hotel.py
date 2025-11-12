from pydantic import BaseModel

class HotelBase(BaseModel):
    nom: str
    adresse: str

class HotelCreate(HotelBase):
    pass

class HotelRead(HotelBase):
    id: int
    class Config:
        orm_mode = True

