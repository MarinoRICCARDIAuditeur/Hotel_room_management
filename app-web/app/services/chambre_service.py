from sqlalchemy.orm import Session
from app.models.chambre import Chambre, EtatChambre, TypeChambre
from app.schemas.chambre import ChambreCreate
from app.models.reservation import Reservation, StatusReservation
from datetime import date

def get_chambres_by_hotel(db: Session, hotel_id: int):
    return db.query(Chambre).filter(Chambre.hotel_id == hotel_id).all()

def create_chambre(db: Session, hotel_id: int, chambre: ChambreCreate):
    # Conversion des strings en enums
    ctype = TypeChambre[chambre.type] if isinstance(chambre.type, str) else chambre.type
    cetat = EtatChambre[chambre.etat] if isinstance(chambre.etat, str) else chambre.etat
    db_chambre = Chambre(
        numero=chambre.numero,
        type=ctype,
        prix=chambre.prix,
        etat=cetat,
        hotel_id=hotel_id
    )
    db.add(db_chambre)
    db.commit()
    db.refresh(db_chambre)
    return db_chambre

def update_chambre(db: Session, id: int, chambre: ChambreCreate):
    db_chambre = db.query(Chambre).filter(Chambre.id == id).first()
    if not db_chambre:
        return None
    db_chambre.numero = chambre.numero
    db_chambre.type = TypeChambre[chambre.type] if isinstance(chambre.type, str) else chambre.type
    db_chambre.prix = chambre.prix
    db_chambre.etat = EtatChambre[chambre.etat] if isinstance(chambre.etat, str) else chambre.etat
    db.commit()
    db.refresh(db_chambre)
    return db_chambre

def get_disponibilite_chambre(db: Session, chambre_id: int):
    chambre = db.query(Chambre).filter(Chambre.id == chambre_id).first()
    if not chambre:
        return False
    today = date.today()
    reservations = db.query(Reservation).filter(
        Reservation.chambre_id == chambre_id,
        Reservation.status == StatusReservation.confirmee,
        Reservation.date_fin >= today
    ).all()
    return chambre.etat == EtatChambre.libre and len(reservations) == 0
