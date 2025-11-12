import os
from typing import Any, Dict

import httpx

EXTERNAL_API_URL = os.getenv("EXTERNAL_API_URL", "http://api-externe:8080")


class ExternalServiceError(Exception):
    """Erreur levée lorsqu'un appel au service externe échoue."""


async def fetch_weather_for_city(city: str) -> Dict[str, Any]:
    url = f"{EXTERNAL_API_URL}/meteo"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params={"ville": city}, timeout=10)
            response.raise_for_status()
        except httpx.HTTPError as exc:  # pragma: no cover - diagnostic
            raise ExternalServiceError(f"Échec de la récupération météo: {exc}") from exc
    data = response.json()
    if not isinstance(data, dict):
        raise ExternalServiceError("Réponse inattendue du service externe")
    return data
