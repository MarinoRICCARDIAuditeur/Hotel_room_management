from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.hotel import HotelCreate, HotelRead
from services.hotel_service import get_hotels, get_hotel, create_hotel
from database import get_db
from typing import List

router = APIRouter()

@router.get("/hotels", response_model=List[HotelRead])
def lister_hotels(db: Session = Depends(get_db)):
    return get_hotels(db)

@router.get("/hotels/{hotel_id}", response_model=HotelRead)
def detail_hotel(hotel_id: int, db: Session = Depends(get_db)):
    hotel = get_hotel(db, hotel_id)
    if hotel is None:
        raise HTTPException(status_code=404, detail="Hôtel non trouvé")
    return hotel

@router.post("/hotels", response_model=HotelRead)
def creer_hotel(hotel: HotelCreate, db: Session = Depends(get_db)):
    return create_hotel(db, hotel)
