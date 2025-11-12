from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from app.controllers.hotel_controller import router as hotel_router
from app.controllers.chambre_controller import router as chambre_router
from app.controllers.client_controller import router as client_router
from app.controllers.reservation_controller import router as reservation_router

app = FastAPI(title="TP Hôtel API", version="1.0.0")
Instrumentator().instrument(app).expose(app, include_in_schema=False)
app.include_router(hotel_router)
app.include_router(chambre_router)
app.include_router(client_router)
app.include_router(reservation_router)

@app.get("/")
def racine():
    return {"message": "API de gestion d'hôtel opérationnelle."}
