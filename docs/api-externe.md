# Documentation de l'API externe simulée

L'API externe fournit des prévisions météo fictives pour différentes villes afin de simuler la dépendance à un service tiers.

## Base URL

- Interne au réseau Docker : `http://api-externe:8080`
- Via Docker Compose (port mappé) : `http://localhost:8085`
- Via le reverse proxy Nginx : `http://localhost:8080/api/`

## Endpoints

### `GET /status`

Vérifie la disponibilité du service.

**Réponse 200**
```json
{
  "status": "ok",
  "timestamp": "2025-11-12T09:15:23.456Z"
}
```

### `GET /meteo`

Retourne entre 1 et 7 jours de prévisions météo pour une ville connue.

| Paramètre | Type | Obligatoire | Description |
|-----------|------|-------------|-------------|
| `ville`   | string | Oui | Nom de la ville (non sensible à la casse). |
| `jours`   | entier | Non (défaut 3) | Nombre de jours souhaités (1 à 7). |

**Réponse 200**
```json
{
  "ville": "Paris",
  "pays": "France",
  "jours": [
    {
      "date": "2025-11-12T09:15:23.456Z",
      "condition": "Ensoleillé",
      "temperature_min": 12.4,
      "temperature_max": 18.7
    },
    {
      "date": "2025-11-13T09:15:23.456Z",
      "condition": "Nuageux",
      "temperature_min": 10.2,
      "temperature_max": 15.5
    }
  ]
}
```

**Codes d'erreur possibles**

- `404` : ville inconnue (base de démonstration limitée).
- `422` : paramètres invalides.

## Liste des villes supportées

`Paris`, `Lyon`, `Marseille`, `Lille`, `Nantes`, `Bordeaux`, `Toulouse`, `Londres`, `New York`, `Tokyo`.

## Observabilité

- Les métriques Prometheus sont exposées via `GET /metrics`.
- Voir le tableau de bord Grafana préconfiguré pour visualiser les requêtes reçues.
