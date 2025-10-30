from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.client import ClientCreate, ClientRead
from services.client_service import create_client, get_client
from database import get_db

router = APIRouter()

@router.post("/clients", response_model=ClientRead)
def creer_client(client: ClientCreate, db: Session = Depends(get_db)):
    return create_client(db, client)

@router.get("/clients/{id}", response_model=ClientRead)
def lire_client(id: int, db: Session = Depends(get_db)):
    client = get_client(db, id)
    if not client:
        raise HTTPException(status_code=404, detail="Client non trouvé")
    return client
