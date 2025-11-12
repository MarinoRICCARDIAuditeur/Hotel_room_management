from sqlalchemy.orm import Session
from app.models.hotel import Hotel
from app.schemas.hotel import HotelCreate

def get_hotels(db: Session):
    return db.query(Hotel).all()

def get_hotel(db: Session, hotel_id: int):
    return db.query(Hotel).filter(Hotel.id == hotel_id).first()

def create_hotel(db: Session, hotel: HotelCreate):
    db_hotel = Hotel(nom=hotel.nom, adresse=hotel.adresse)
    db.add(db_hotel)
    db.commit()
    db.refresh(db_hotel)
    return db_hotel
