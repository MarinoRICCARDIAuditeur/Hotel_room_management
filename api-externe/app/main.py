from datetime import datetime, timedelta
from random import randint
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="API Météo Simulée", description="Service externe fictif fournissant une météo quotidienne pour une ville donnée.")
Instrumentator().instrument(app).expose(app, include_in_schema=False)

class MeteoJour(BaseModel):
    date: datetime
    condition: str
    temperature_min: float
    temperature_max: float

class MeteoResponse(BaseModel):
    ville: str
    pays: str
    jours: list[MeteoJour]

_CONDITIONS = [
    "Ensoleillé",
    "Nuageux",
    "Pluie légère",
    "Orages",
    "Averses",
    "Vent fort",
    "Brume",
]

_PAYS_VILLE = {
    "paris": "France",
    "lyon": "France",
    "marseille": "France",
    "lille": "France",
    "nantes": "France",
    "bordeaux": "France",
    "lyon": "France",
    "toulouse": "France",
    "londres": "Royaume-Uni",
    "new york": "États-Unis",
    "tokyo": "Japon",
}

@app.get("/status")
def status():
    return {"status": "ok", "timestamp": datetime.utcnow()}

@app.get("/meteo", response_model=MeteoResponse)
def meteo(ville: str = Query(..., min_length=2, description="Nom de la ville"), jours: int = Query(3, ge=1, le=7, description="Nombre de jours de prévision")):
    ville_norm = ville.strip().lower()
    pays = _PAYS_VILLE.get(ville_norm)
    if not pays:
        raise HTTPException(status_code=404, detail="Ville inconnue dans la base de démonstration")
    base_temp = randint(5, 25)
    previsions = []
    for i in range(jours):
        condition = _CONDITIONS[randint(0, len(_CONDITIONS) - 1)]
        delta = randint(-3, 3)
        temp_min = base_temp + delta - 3
        temp_max = base_temp + delta + 3
        previsions.append(
            MeteoJour(
                date=datetime.utcnow() + timedelta(days=i),
                condition=condition,
                temperature_min=round(temp_min + randint(-10, 10) * 0.1, 1),
                temperature_max=round(temp_max + randint(-10, 10) * 0.1, 1),
            )
        )
    return MeteoResponse(ville=ville.title(), pays=pays, jours=previsions)
