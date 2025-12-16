# Configuration du Reverse Proxy Nginx

Ce reverse proxy expose tous les services via un seul point d'entrée sur le port 8080 (configurable via `PROXY_PORT` dans `.env`).

## Authentification Basic Auth (optionnel)

Pour activer l'authentification Basic Auth sur les endpoints protégés :

1. **Générer un fichier htpasswd** (nécessite le package `apache2-utils` ou `htpasswd`) :
   ```bash
   htpasswd -c .htpasswd admin
   # Entrez le mot de passe lorsque demandé
   ```

2. **Décommenter les lignes d'authentification** dans `nginx.conf` :
   - Décommentez les lignes `auth_basic` et `auth_basic_user_file` pour les sections désirées (`/app/`, `/api/`, `/admin/`)

3. **Monter le fichier htpasswd dans le conteneur** :
   Modifiez `docker-compose.yml` pour ajouter le volume :
   ```yaml
   proxy-nginx:
     volumes:
       - ./proxy-nginx/.htpasswd:/etc/nginx/.htpasswd:ro
   ```

## Authentification par API Key (alternative)

Pour une authentification par API Key, vous pouvez :
- Ajouter un middleware dans les applications FastAPI qui vérifie un header `X-API-Key`
- Ou utiliser Nginx avec un module Lua pour vérifier le header avant de proxyfier la requête

## Accès aux services

- **Application métier** : `http://localhost:8080/app/`
- **API externe** : `http://localhost:8080/api/`
- **Console d'administration** : `http://localhost:8080/admin/`
- **Métriques** : `http://localhost:8080/metrics/{service}`

