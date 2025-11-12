from sqlalchemy.orm import Session
from app.models.reservation import Reservation, StatusReservation
from app.schemas.reservation import ReservationCreate
from app.models.chambre import Chambre, EtatChambre
from datetime import date

def create_reservation(db: Session, resa: ReservationCreate):
    query = db.query(Reservation).filter(
        Reservation.chambre_id == resa.chambre_id,
        Reservation.status == StatusReservation.confirmee,
        Reservation.date_fin >= resa.date_debut,
        Reservation.date_debut <= resa.date_fin
    )
    if query.first():
        raise ValueError("Chambre déjà réservée sur cette période")
    chambre = db.query(Chambre).filter(Chambre.id == resa.chambre_id).first()
    if not chambre:
        raise ValueError("Chambre inconnue")
    if chambre.etat != EtatChambre.libre:
        raise ValueError("Chambre non disponible")
    db_resa = Reservation(
        client_id=resa.client_id,
        chambre_id=resa.chambre_id,
        date_debut=resa.date_debut,
        date_fin=resa.date_fin,
        status=StatusReservation.confirmee
    )
    chambre.etat = EtatChambre.occupee
    db.add(db_resa)
    db.commit()
    db.refresh(db_resa)
    return db_resa

def annuler_reservation(db: Session, resa_id: int):
    resa = db.query(Reservation).filter(Reservation.id == resa_id).first()
    if not resa:
        return False
    resa.status = StatusReservation.annulee
    chambre = db.query(Chambre).filter(Chambre.id == resa.chambre_id).first()
    if chambre:
        chambre.etat = EtatChambre.libre
    db.commit()
    return True

def get_reservations(db: Session):
    return db.query(Reservation).all()
