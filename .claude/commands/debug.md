## 6. debug.md

```markdown
# Aide au Debugging

## Usage
```
/debug <type>
```

Types:
- `api` - Problème API/Backend
- `db` - Problème base de données
- `agent` - Problème agent IA
- `celery` - Problème queue/workers
- `frontend` - Problème UI

## Debug API

### Vérifier les logs
```bash
# Local
docker-compose logs -f backend

# Production
# Render Dashboard > Service > Logs
```

### Tester un endpoint
```bash
# Obtenir un token
TOKEN=$(curl -s -X POST http://localhost:8000/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@vectra-demo.com","password":"demo123"}' \
  | jq -r '.data.access_token')

# Appeler l'endpoint
curl -X GET http://localhost:8000/v1/campaigns \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" | jq
```

## Debug Database

### Connexion
```bash
docker exec -it vectra-postgres psql -U vectra
```

### Requêtes utiles
```sql
-- Voir les connexions actives
SELECT count(*), state FROM pg_stat_activity GROUP BY state;

-- Requêtes lentes
SELECT pid, now() - query_start AS duration, query
FROM pg_stat_activity WHERE state != 'idle'
ORDER BY duration DESC LIMIT 10;

-- Taille des tables
SELECT relname, pg_size_pretty(pg_total_relation_size(relid))
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC;
```

## Debug Agent

### Logs agent
```bash
grep "agent" logs/app.log | tail -100
```

### Tester un agent manuellement
```python
# Dans un shell Python
from app.agents.bant import BANTAgent

agent = BANTAgent()
result = await agent.execute({
    "lead": {"job_title": "VP Sales", "company_size": "100-500"}
})
print(result)
```

## Debug Celery

### Voir les workers
```bash
celery -A app.tasks.celery_app inspect active
```

### Voir la queue
```bash
celery -A app.tasks.celery_app inspect reserved
redis-cli LLEN celery
```

### Flower dashboard
```bash
celery -A app.tasks.celery_app flower
# Ouvrir http://localhost:5555
```

## Debug Frontend

### Console browser
F12 > Console > Chercher les erreurs rouges

### Network
F12 > Network > Vérifier les requêtes API qui échouent

### React DevTools
Installer l'extension et inspecter les composants/state
```

---