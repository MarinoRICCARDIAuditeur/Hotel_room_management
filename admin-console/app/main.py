import os
from typing import Any, Dict, List, Optional

import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from prometheus_fastapi_instrumentator import Instrumentator

APP_API_URL = os.getenv("APP_WEB_URL", "http://app-web:8000")
EXTERNAL_API_URL = os.getenv("EXTERNAL_API_URL", "http://api-externe:8080")

app = FastAPI(title="Console d'administration hôtel")
Instrumentator().instrument(app).expose(app, include_in_schema=False)

templates = Jinja2Templates(directory="app/templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def fetch_json(client: httpx.AsyncClient, url: str, **kwargs: Any) -> Dict[str, Any]:
    response = await client.get(url, timeout=10, **kwargs)
    response.raise_for_status()
    data = response.json()
    if not isinstance(data, dict):
        raise HTTPException(status_code=500, detail="Réponse inattendue du service distant")
    return data


async def fetch_list(client: httpx.AsyncClient, url: str, **kwargs: Any) -> List[Dict[str, Any]]:
    response = await client.get(url, timeout=10, **kwargs)
    response.raise_for_status()
    data = response.json()
    if not isinstance(data, list):
        raise HTTPException(status_code=500, detail="Réponse inattendue du service app-web")
    return data


@app.get("/status")
async def status() -> Dict[str, Any]:
    async with httpx.AsyncClient() as client:
        try:
            app_status = await fetch_json(client, f"{APP_API_URL}/")
        except Exception as exc:  # pragma: no cover - diagnostic
            raise HTTPException(status_code=503, detail=f"app-web indisponible: {exc}") from exc
        try:
            external_status = await fetch_json(client, f"{EXTERNAL_API_URL}/status")
        except Exception as exc:  # pragma: no cover - diagnostic
            raise HTTPException(status_code=503, detail=f"api-externe indisponible: {exc}") from exc
    return {"app_web": app_status, "api_externe": external_status}


async def collect_metrics(client: httpx.AsyncClient) -> Dict[str, Any]:
    hotels = await fetch_list(client, f"{APP_API_URL}/hotels")
    reservations = await fetch_list(client, f"{APP_API_URL}/reservations")
    chambres_total = 0
    chambres_libres = 0

    for hotel in hotels:
        chambres = await fetch_list(client, f"{APP_API_URL}/hotels/{hotel['id']}/chambres")
        chambres_total += len(chambres)
        chambres_libres += sum(1 for chambre in chambres if chambre.get("etat") == "libre")

    meteo: Optional[Dict[str, Any]] = None
    try:
        ville = hotels[0]["nom"] if hotels else "Paris"
        meteo = await fetch_json(client, f"{EXTERNAL_API_URL}/meteo", params={"ville": ville})
    except Exception:
        meteo = None

    return {
        "hotels": hotels,
        "reservations": reservations,
        "chambres_total": chambres_total,
        "chambres_libres": chambres_libres,
        "meteo": meteo,
    }


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    async with httpx.AsyncClient() as client:
        metrics = await collect_metrics(client)
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "hotels": metrics["hotels"],
            "reservations": metrics["reservations"],
            "chambres_total": metrics["chambres_total"],
            "chambres_libres": metrics["chambres_libres"],
            "meteo": metrics["meteo"],
            "app_url": APP_API_URL,
            "api_url": EXTERNAL_API_URL,
        },
    )


@app.get("/api/dashboard", response_class=JSONResponse)
async def dashboard_api():
    async with httpx.AsyncClient() as client:
        metrics = await collect_metrics(client)
    return metrics
