# Setup Ollama Cloud API

## Vue d'ensemble

Ollama Cloud permet d'utiliser des modèles LLM sans avoir besoin d'une machine locale puissante. Les modèles sont exécutés sur les serveurs d'Ollama via leur API cloud.

## Prérequis

1. Compte Ollama créé sur [ollama.com](https://ollama.com)
2. API Key Ollama générée depuis votre compte

## 1. Créer une API Key

1. Connectez-vous à [ollama.com](https://ollama.com)
2. Allez dans **Settings** > **API Keys**
3. Cliquez sur **Create API Key**
4. Copiez la clé API générée

## 2. Configuration locale

### Variables d'environnement

Ajoutez dans votre `.env` ou `.env.local`:

```env
# LLM Configuration
LLM_PROVIDER=ollama
OLLAMA_API_KEY=your_api_key_here
OLLAMA_CLOUD_HOST=https://ollama.com
OLLAMA_MODEL=llama2:7b
```

**Note:** `OLLAMA_BASE_URL` n'est pas nécessaire pour l'API cloud (uniquement pour Ollama local/remote).

### Configuration dans config.py

Les variables sont déjà configurées dans `backend/app/core/config.py`:

- `OLLAMA_API_KEY`: Clé API Ollama (optionnelle, priorité si définie)
- `OLLAMA_CLOUD_HOST`: URL de l'API cloud (`https://ollama.com`)
- `OLLAMA_MODEL`: Modèle à utiliser (par défaut `llama2:7b`)
- `OLLAMA_BASE_URL`: URL pour Ollama local/remote (utilisé si `OLLAMA_API_KEY` n'est pas défini)

## 3. Priorité de configuration

Le système utilise la configuration suivante (dans l'ordre de priorité):

1. **Ollama Cloud API** - Si `OLLAMA_API_KEY` est défini
2. **Ollama Local/Remote** - Si `OLLAMA_BASE_URL` est défini
3. **Claude API** - Fallback si Ollama n'est pas disponible

## 4. Modèles disponibles

### Modèles cloud supportés

Pour voir les modèles disponibles via l'API cloud:

```bash
curl https://ollama.com/api/tags \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Modèles recommandés

- `llama2:7b` - Léger, rapide (~4GB RAM)
- `llama2:13b` - Équilibre performance/taille
- `llama2:70b` - Plus puissant (~40GB RAM)

## 5. Utilisation avec CrewAI

CrewAI détecte automatiquement la configuration Ollama Cloud via les variables d'environnement:

```python
# Dans backend/app/agents/crew.py
# La fonction get_llm() configure automatiquement:
# - OLLAMA_API_KEY
# - OLLAMA_HOST (pointant vers OLLAMA_CLOUD_HOST)
# - OLLAMA_MODEL
```

## 6. Test de connexion

### Test via Python

```python
from ollama import Client
import os

client = Client(
    host="https://ollama.com",
    headers={'Authorization': 'Bearer ' + os.environ.get('OLLAMA_API_KEY')}
)

response = client.chat(
    'llama2:7b',
    messages=[{'role': 'user', 'content': 'Hello!'}]
)
print(response['message']['content'])
```

### Test via cURL

```bash
curl https://ollama.com/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "model": "llama2:7b",
    "messages": [
      {
        "role": "user",
        "content": "Why is the sky blue?"
      }
    ],
    "stream": false
  }'
```

## 7. Vérification dans l'application

Lors du démarrage de l'application, vous devriez voir dans les logs:

```
INFO: LLM configured: Ollama Cloud llama2:7b at https://ollama.com
```

## 8. Documentation officielle

- [Ollama Cloud Documentation](https://docs.ollama.com/cloud)
- [Ollama Python SDK](https://github.com/ollama/ollama-python)

## 9. Troubleshooting

### Erreur: "API key not found"

- Vérifiez que `OLLAMA_API_KEY` est bien défini dans `.env`
- Redémarrez l'application après modification de `.env`

### Erreur: "Model not found"

- Vérifiez que le modèle est disponible via l'API cloud
- Utilisez `llama2:7b` par défaut si le modèle n'est pas disponible

### Fallback vers Claude

- Si Ollama Cloud échoue, le système utilisera automatiquement Claude API (si configuré)
- Vérifiez les logs pour voir quel LLM est utilisé

---

*Dernière mise à jour: 15 Janvier 2026*
