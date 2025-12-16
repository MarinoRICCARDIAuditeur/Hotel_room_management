from prometheus_client import Counter, Gauge
from sqlalchemy.orm import Session

from app.models.chambre import Chambre, EtatChambre
from app.models.reservation import Reservation, StatusReservation
from app.schemas.reservation import ReservationCreate

RESERVATIONS_CREATED_TOTAL = Counter(
    "tphotel_reservations_created_total",
    "Nombre total de réservations confirmées créées.",
)
RESERVATIONS_CANCELLED_TOTAL = Counter(
    "tphotel_reservations_cancelled_total",
    "Nombre total de réservations annulées.",
)
RESERVATIONS_ACTIVE = Gauge(
    "tphotel_reservations_active",
    "Nombre de réservations confirmées actives.",
)
ROOMS_OCCUPIED = Gauge(
    "tphotel_rooms_occupied",
    "Nombre de chambres actuellement occupées.",
)
ROOMS_AVAILABLE = Gauge(
    "tphotel_rooms_available",
    "Nombre de chambres disponibles.",
)
ROOM_OCCUPANCY_RATE = Gauge(
    "tphotel_room_occupancy_rate",
    "Taux d'occupation global des chambres.",
)


def _update_room_metrics(db: Session):
    chambres_total = db.query(Chambre).count()
    chambres_occupees = db.query(Chambre).filter(Chambre.etat == EtatChambre.occupee).count()
    chambres_disponibles = max(chambres_total - chambres_occupees, 0)

    ROOMS_OCCUPIED.set(chambres_occupees)
    ROOMS_AVAILABLE.set(chambres_disponibles)
    ROOM_OCCUPANCY_RATE.set(chambres_occupees / chambres_total if chambres_total else 0)


def _update_reservation_metrics(db: Session):
    reservations_actives = (
        db.query(Reservation)
        .filter(Reservation.status == StatusReservation.confirmee)
        .count()
    )
    RESERVATIONS_ACTIVE.set(reservations_actives)
    _update_room_metrics(db)

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
    RESERVATIONS_CREATED_TOTAL.inc()
    _update_reservation_metrics(db)
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
    RESERVATIONS_CANCELLED_TOTAL.inc()
    _update_reservation_metrics(db)
    return True

def get_reservations(db: Session):
    return db.query(Reservation).all()
