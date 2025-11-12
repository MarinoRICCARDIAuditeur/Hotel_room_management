from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.hotel import HotelCreate, HotelRead
from app.services.external_api_service import (
    ExternalServiceError,
    fetch_weather_for_city,
)
from app.services.hotel_service import create_hotel, get_hotel, get_hotels

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


@router.get("/hotels/{hotel_id}/meteo")
async def meteo_hotel(hotel_id: int, db: Session = Depends(get_db)):
    hotel = get_hotel(db, hotel_id)
    if hotel is None:
        raise HTTPException(status_code=404, detail="Hôtel non trouvé")
    try:
        meteo = await fetch_weather_for_city(hotel.nom)
    except ExternalServiceError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    return {
        "hotel": {"id": hotel.id, "nom": hotel.nom, "adresse": hotel.adresse},
        "meteo": meteo,
    }
