# API RESTful de gestion de chambres d'hôtel

## Présentation
Dans le cadre d'une agence fictive de gestion d'hôtels, cette application fournit une API REST (FastAPI + MySQL) pour gérer :
- Hôtels
- Chambres
- Clients
- Réservations

Le tout dans une architecture  conteneurisée avec Docker.

---

## Prérequis
- **Docker**, **docker-compose** et **python** installés

---

## Lancement du projet

Se rendre dans le dossier *hotel* et exécuter :

```bash
docker compose up --build
```
*(Il faut accepter l'avertissement sur la clé `version` du compose)*

L'API sera ensuite disponible via l'adresse suivante :
- **http://localhost:8004/docs** (interface Swagger)

---

## Initialisation de la base de données
La première fois, il faut créer les tables dans MySQL. Pour cela, il suffit de :

1. Rentrer dans le conteneur API :
   ```bash
   docker compose exec api bash
   ```
2. Lancer Python :
   ```bash
   python
   ```
3. Taper dans le shell python les commandes suivantes, une par une :
   ```python
   import models.hotel, models.chambre, models.client, models.reservation
   from database import Base, engine
   Base.metadata.create_all(bind=engine)
   exit()
   ```
4. Sortir du conteneur :
   ```bash
   exit
   ```

---

## Utilisation : exemples de tests

Il est possible de tester les routes directement depuis l'interface Swagger, à l'adresse suivante :
**http://localhost:8004/docs**

Exemples de séquence possible :
1. Créer un hôtel (`POST /hotels`)
2. Ajouter une chambre à l'hôtel (`POST /hotels/{id}/chambres`)
3. Créer un client (`POST /clients`)
4. Faire une réservation (`POST /reservations`)
5. Lister des réservations (`GET /reservations`)
6. Vérifier la disponibilité d'une chambre (`GET /chambres/{id}/disponibilite`)

Chaque endpoint est testable en direct via l'interface Swagger !

---

## Configuration personnalisée

- Pour changer le port HTTP (par défaut :8004), il faut le modifier le port dans le fichier hotel/docker-compose.yml :
```yaml
  api:
    ...
    ports:
      - "8004:8000"
```

- Les identifiants MySQL sont configurés dans `docker-compose.yml`.

---

## Remarques
- Le projet utilise FastAPI, SQLAlchemy, pymysql et cryptography (attention : si besoin de rebuild, garder cryptography dans requirements.txt)
- Le code est découpé en modèles (`models`), schémas (`schemas`), services et contrôleurs (`controllers`)
- Possibilité d'ajouter de nouvelles routes facilement !
---


                         ### ENGLISH VERSION ###

# RESTful API for Hotel Room Management

## Overview
This application provides a REST API (FastAPI + MySQL) to manage :
- Hotels
- Rooms
- Clients
- Reservations

All built with a containerized architecture using Docker.

---

# Prerequisites
- *docker*, *docker-compose* and *python*  must be installed

---

## Lancement du projet

In the *hotel* folder :

```bash
docker compose up --build
```
*(You can safely ignore the warning about the `version` key in the compose file - it has no impact.)*

The API will be available at :
- **http://localhost:8004/docs** (interface Swagger)

---

## Database initialization
The first time you run de project, you'll need to create the MySQL tables :
1. Enter the API container :
```bash
docker compose exec api bash
```

2. Start Python :
```bash
python
```

3. In the Python shell, type :
```python
import models.hotel, models.chambre, models.client, models.reservation
from database import Base, engine
Base.metadata.create_all(bind=engine)
exit()
```

4. Then, exit the container :
```bash
exit()
```

---

## Usage : Example test

You can test all routes directly from
**http://localhost:8004/docs**

Example sequence:

1. Create a hotel (`POST /hotels`)
2. Add a room to the hotel (`POST /hotels/{id}/chambres`)
3. Create a client (`POST /clients`)
4. Make a reservation (`POST /reservations`)
5. List reservation (`GET /reservations`)
6. Check a room's availability (`GET /chambres/{id}/disponibilite`)

Each endpoint can be testes directly through the Swagger UI !

---

## Custom configuration

- To change the HTTP port (default:8004), edit the following in :
```yaml
  api:
    ...
    ports:
      - "8004:8000"
````

- MySQL credentials are configured in the `docker-compose.yml` file.

---

## Notes
- The project use **FastAPI**, **SQLAlchemy**, **pymysql** and **cryptography** (Important: if you want to rebuild, make sure `cryptography` stays in ``requirements.txt`)
- The codebase is organized into **models**, **schemlas**, **services** and **controllers**.
- You can easily add new routes as needed !
---


