# TP Hôtel – SI conteneurisé

Projet DevOps de conteneurisation d'un système d'information métier pour une chaîne hôtelière fictive.

## 🚀 Démarrage rapide

### Prérequis

- **Docker** et **Docker Compose** installés
- Ports libres : `8004`, `8085`, `8090`, `8080` (proxy principal), `9090`, `3000`

### Installation et lancement

1. **Cloner le dépôt**
   ```bash
   git clone https://github.com/MarinoRICCARDIAuditeur/Hotel_room_management
   cd Hotel_room_management
   ```

2. **Créer le fichier d'environnement** (optionnel, des valeurs par défaut sont définies)
   ```bash
   cp .env.example .env
   ```

3. **Déclarer le nom de domaine local**
   ```bash
   echo "127.0.0.1 hotelmanagement" | sudo tee -a /etc/hosts
   ```
   > Remarque : sur Windows, ajoutez `127.0.0.1 hotelmanagement` dans `C:\Windows\System32\drivers\etc\hosts`.

4. **Lancer l'application**
   ```bash
   docker compose up -d --build
   ```

   ⏱️ La première fois, cela peut prendre quelques minutes (téléchargement des images et construction).

5. **Vérifier que tout fonctionne**
   ```bash
   docker compose ps
   ```
   Tous les services doivent être `Up` et `healthy` (ou `started`).

## 🌐 Accès aux services

Une fois les conteneurs démarrés, ouvrez `http://localhost:8080/` : la page d'accueil centralise des boutons vers tous les services. Les URLs directes restent disponibles :

| Service | URL | Description |
|---------|-----|-------------|
| **Portail central** | http://localhost:8080/ | Hub avec boutons vers l'ensemble des services |
| **API métier** | http://localhost:8080/app/docs | Interface Swagger de l'API de gestion hôtelière |
| **API externe (météo)** | http://localhost:8080/api/docs | Documentation de l'API météo simulée |
| **Console d'administration** | http://localhost:8080/admin/ | Tableau de bord avec statistiques |
| **Reverse proxy** | http://localhost:8080/ | Point d'entrée unique : `/app/`, `/api/`, `/admin/`, `/metrics/...` |
| **Prometheus** | http://localhost:9090 | Interface de monitoring |
| **Grafana** | http://localhost:3000 | Dashboards (login: `admin` / mdp: `admin`) |

## 📋 Services disponibles

- **`app-web`** : API FastAPI pour gérer hôtels, chambres, clients et réservations
- **`db`** : Base de données MySQL 8 (initialisée automatiquement avec `db/init.sql`)
- **`api-externe`** : Service REST simulé fournissant des prévisions météo
- **`admin-console`** : Tableau de bord web affichant les statistiques
- **`proxy-nginx`** : Reverse proxy exposant tous les services sur le port 8080 (`http://localhost:8080`)
- **`prometheus`** + **`grafana`** : Stack de monitoring (bonus)

## 📈 Supervision (Prometheus & Grafana)

La stack d'observabilité est packagée dans `docker-compose.yml`. Lancez-la (ainsi que les applications) avec :

```bash
docker compose up -d --build app-web api-externe admin-console proxy-nginx db prometheus grafana mysqld-exporter
```

### Prometheus

- Configuration centralisée dans `monitoring/prometheus.yml`.
- Scrape des endpoints `/metrics` exposés par `app-web`, `api-externe`, `admin-console`.
- Exporter MySQL (`mysqld-exporter` sur le port `9104`) pour disposer de métriques de base de données (`mysql_global_status_*`).
- Auto-surveillance de Prometheus (`job_name: prometheus`).

### Métriques métiers ajoutées

- `tphotel_reservations_created_total` / `tphotel_reservations_cancelled_total`
- `tphotel_reservations_active`, `tphotel_rooms_available`, `tphotel_rooms_occupied`, `tphotel_room_occupancy_rate`
- `tphotel_meteo_requests_total{ville=...}` et histogramme `tphotel_meteo_requested_days`

Ces métriques sont générées directement par les services FastAPI (voir `app-web/app/services/reservation_service.py` et `api-externe/app/main.py`).

### Grafana

- Provisioning automatisé (`monitoring/grafana/provisioning`).
- Datasource Prometheus pré-définie (`uid: Prometheus`).
- Dashboard prêt à l'emploi : `TPHotel - Vue d'ensemble` (`monitoring/grafana/provisioning/dashboards/tphotel-overview.json`).
  - Suivi du débit HTTP, erreurs 5xx et latence P95 par service.
  - Visibilité sur l'occupation des chambres / réservations.
  - Statistiques MySQL (threads, requêtes/s) et top 5 des villes interrogées.

Connexion : http://localhost:3000 (admin / admin). Les dashboards se mettent à jour automatiquement toutes les 30 secondes.

## 🛠️ Commandes utiles

```bash
# Arrêter l'application
docker compose down

# Voir les logs
docker compose logs -f

# Redémarrer un service spécifique
docker compose restart app-web

# Supprimer tout (volumes inclus) pour repartir de zéro
docker compose down -v
```

## ⚠️ Dépannage

**MySQL ne démarre pas / erreur "No space left on device"**
- Vérifier l'espace disque disponible : `df -h`
- Libérer de l'espace si nécessaire
- Supprimer le volume MySQL : `docker compose down && docker volume rm tphotel_db_data`
- Relancer : `docker compose up -d --build`

## 📚 Documentation complémentaire

- `docs/api-externe.md` : Documentation détaillée de l'API météo
- `db/init.sql` : Schéma de base de données et données de démonstration
