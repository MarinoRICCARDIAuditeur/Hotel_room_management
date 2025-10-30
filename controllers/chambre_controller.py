from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.chambre import ChambreCreate, ChambreRead
from services.chambre_service import (
    get_chambres_by_hotel, create_chambre, update_chambre, get_disponibilite_chambre
)
from database import get_db
from typing import List

router = APIRouter()

@router.get("/hotels/{hotel_id}/chambres", response_model=List[ChambreRead])
def chambres_par_hotel(hotel_id: int, db: Session = Depends(get_db)):
    return get_chambres_by_hotel(db, hotel_id)

@router.post("/hotels/{hotel_id}/chambres", response_model=ChambreRead)
def ajouter_chambre(hotel_id: int, chambre: ChambreCreate, db: Session = Depends(get_db)):
    return create_chambre(db, hotel_id, chambre)

@router.put("/chambres/{id}", response_model=ChambreRead)
def modifier_chambre(id: int, chambre: ChambreCreate, db: Session = Depends(get_db)):
    return update_chambre(db, id, chambre)

@router.get("/chambres/{id}/disponibilite")
def disponibilite_chambre(id: int, db: Session = Depends(get_db)):
    dispo = get_disponibilite_chambre(db, id)
    return {"disponible": dispo}
