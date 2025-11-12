# Cahier des charges – Validation

| Exigence | Implémentation |
|----------|----------------|
| Conteneurisation Docker + Docker Compose | `docker-compose.yml` orchestrant 7 services, réseaux dédiés, volumes nommés. |
| Réseaux personnalisés | Réseaux `backend` (API ↔ DB) et `frontend` (exposition). |
| Volumes persistants | `db_data`, `prometheus_data`, `grafana_data`. |
| Fichiers Dockerfile dédiés | `app-web/Dockerfile`, `api-externe/Dockerfile`, `admin-console/Dockerfile`. |
| Variables d'environnement externalisées | `.env` / `.env.example`. |
| Base de données relationnelle sécurisée | MySQL 8 (`db`), non exposée hors réseau `backend`, script `db/init.sql`. |
| Application métier | `app-web` (FastAPI + SQLAlchemy) – gestion hôtels/chambres/clients/réservations. |
| Intégration service externe | Endpoint `GET /hotels/{id}/meteo` appellera `api-externe`. |
| Service externe simulé | `api-externe` (FastAPI météo) + documentation `docs/api-externe.md`. |
| Administration / supervision | `admin-console` (tableau de bord) + stack Prometheus/Grafana. |
| Reverse proxy (bonus) | `proxy-nginx` exposant `/app`, `/api`, `/admin`, `/metrics`. |
| Monitoring (bonus) | `prometheus` + `grafana` avec métriques `/metrics`. |
| Documentation projet | `README.md`, `docs/` (API externe, cahier des charges). |
| Données d'initialisation | `db/init.sql`. |
| Capture d'écran | Prévoir ajout dans `docs/captures/` (à compléter). |
