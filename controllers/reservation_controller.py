from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.reservation import ReservationCreate, ReservationRead
from services.reservation_service import (
    create_reservation, annuler_reservation, get_reservations
)
from database import get_db
from typing import List

router = APIRouter()

@router.post("/reservations", response_model=ReservationRead)
def creer_reservation(resa: ReservationCreate, db: Session = Depends(get_db)):
    try:
        return create_reservation(db, resa)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/reservations/{id}")
def annuler_resa(id: int, db: Session = Depends(get_db)):
    if not annuler_reservation(db, id):
        raise HTTPException(status_code=404, detail="Réservation non trouvée")
    return {"message": "Réservation annulée"}

@router.get("/reservations", response_model=List[ReservationRead])
def lister_reservations(db: Session = Depends(get_db)):
    return get_reservations(db)
