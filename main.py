from fastapi import FastAPI
from controllers.hotel_controller import router as hotel_router
from controllers.chambre_controller import router as chambre_router
from controllers.client_controller import router as client_router
from controllers.reservation_controller import router as reservation_router

app = FastAPI()
app.include_router(hotel_router)
app.include_router(chambre_router)
app.include_router(client_router)
app.include_router(reservation_router)

@app.get("/")
def racine():
    return {"message": "API de gestion d'hôtel opérationnelle."}
