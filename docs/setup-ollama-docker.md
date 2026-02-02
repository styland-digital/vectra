# Setup Ollama avec Docker

## Option 1: Docker Compose (Recommandé)

### 1. Créer le fichier `docker-compose.ollama.yml`

Un fichier `docker-compose.ollama.yml` a été créé à la racine du projet.

### 2. Démarrer Ollama

```bash
# Créer le réseau si nécessaire
docker network create vectra-network

# Démarrer Ollama
docker-compose -f docker-compose.ollama.yml up -d

# Vérifier que Ollama tourne
docker ps | grep ollama
```

### 3. Télécharger le modèle Llama 2 70B

```bash
# Se connecter au conteneur
docker exec -it vectra-ollama ollama pull llama2:70b

# Ou depuis l'hôte si ollama CLI installé localement
ollama pull llama2:70b
```

### 4. Configurer l'environnement

Dans `.env`:

```env
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=https://api.ollama.com
OLLAMA_MODEL=llama2:70b
```

Si Ollama est dans un autre conteneur Docker:

```env
OLLAMA_BASE_URL=http://ollama:11434
```

### 5. Tester la connexion

```bash
curl https://api.ollama.com/api/tags
```

## Option 2: Docker Run (Simple)

```bash
# Lancer Ollama
docker run -d \
  --name vectra-ollama \
  -p 11434:11434 \
  -v ollama_data:/root/.ollama \
  ollama/ollama:latest

# Télécharger le modèle
docker exec -it vectra-ollama ollama pull llama2:70b
```

## Option 3: Intégrer dans docker-compose.yml principal

Ajouter dans `docker-compose.yml`:

```yaml
services:
  ollama:
    image: ollama/ollama:latest
    container_name: vectra-ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    networks:
      - vectra-network
    healthcheck:
      test: ["CMD", "curl", "-f", "https://api.ollama.com/api/tags"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  ollama_data:
```

## Notes

- **Modèle recommandé**: `llama2:70b` (nécessite ~40GB RAM)
- **Alternative plus légère**: `llama2:7b` (~4GB RAM)
- **API**: Ollama expose une API REST sur `https://api.ollama.com`
- **CrewAI**: Détecte automatiquement Ollama via `OLLAMA_BASE_URL` et `OLLAMA_MODEL`

## Vérification

```bash
# Vérifier les modèles téléchargés
docker exec -it vectra-ollama ollama list

# Tester un prompt
curl https://api.ollama.com/api/generate -d '{
  "model": "llama2:70b",
  "prompt": "Bonjour, comment allez-vous?",
  "stream": false
}'
```
