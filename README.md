# TP Hôtel – SI conteneurisé

Projet DevOps de conteneurisation d'un système d'information métier pour une chaîne hôtelière fictive.

## 🚀 Démarrage rapide

### Prérequis

- **Docker** et **Docker Compose** installés
- Ports libres : `8004`, `8085`, `8090`, `8080`, `9090`, `3000`

### Installation et lancement

1. **Cloner le dépôt**
   ```bash
   git clone <url-du-repo>
   cd tphotel
   ```

2. **Créer le fichier d'environnement** (optionnel, des valeurs par défaut sont définies)
   ```bash
   cp .env.example .env
   ```

3. **Lancer l'application**
   ```bash
   docker compose up -d --build
   ```

   ⏱️ La première fois, cela peut prendre quelques minutes (téléchargement des images et construction).

4. **Vérifier que tout fonctionne**
   ```bash
   docker compose ps
   ```
   Tous les services doivent être `Up` et `healthy` (ou `started`).

## 🌐 Accès aux services

Une fois les conteneurs démarrés, les services sont accessibles via :

| Service | URL | Description |
|---------|-----|-------------|
| **API métier** | http://localhost:8004/docs | Interface Swagger de l'API de gestion hôtelière |
| **API externe (météo)** | http://localhost:8085/docs | Documentation de l'API météo simulée |
| **Console d'administration** | http://localhost:8090/ | Tableau de bord avec statistiques |
| **Reverse proxy** | http://localhost:8080 | Point d'entrée unique : `/app/`, `/api/`, `/admin/` |
| **Prometheus** | http://localhost:9090 | Interface de monitoring |
| **Grafana** | http://localhost:3000 | Dashboards (login: `admin` / mdp: `admin`) |

## 📋 Services disponibles

- **`app-web`** : API FastAPI pour gérer hôtels, chambres, clients et réservations
- **`db`** : Base de données MySQL 8 (initialisée automatiquement avec `db/init.sql`)
- **`api-externe`** : Service REST simulé fournissant des prévisions météo
- **`admin-console`** : Tableau de bord web affichant les statistiques
- **`proxy-nginx`** : Reverse proxy exposant tous les services sur le port 8080
- **`prometheus`** + **`grafana`** : Stack de monitoring (bonus)

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
