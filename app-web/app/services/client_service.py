from sqlalchemy.orm import Session
from app.models.client import Client
from app.schemas.client import ClientCreate

def create_client(db: Session, client: ClientCreate):
    db_client = Client(nom=client.nom, email=client.email, tel=client.tel)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def get_client(db: Session, client_id: int):
    return db.query(Client).filter(Client.id == client_id).first()
