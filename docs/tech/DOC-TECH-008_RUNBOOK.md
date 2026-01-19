# VECTRA - RUNBOOK OPÉRATIONNEL
## Procédures d'Exploitation et de Gestion des Incidents
### Version 1.0 | 14 Janvier 2026

---

**Document:** DOC-009  
**Statut:** APPROUVÉ  
**Audience:** Équipe technique, DevOps, Support niveau 2-3  

---

## 1. INFORMATIONS GÉNÉRALES

### 1.1 Environnements

| Env | URL | Provider |
|-----|-----|----------|
| Production | app.vectra.io | Render |
| Staging | staging.vectra.io | Render |
| API Prod | api.vectra.io | Render |

### 1.2 SLA Cibles

| Métrique | Cible | Critique |
|----------|-------|----------|
| Uptime | 99.5% | < 99% |
| API Latency P50 | < 200ms | > 500ms |
| API Latency P99 | < 1s | > 3s |
| Error Rate | < 1% | > 5% |

---

## 2. MONITORING ET ALERTES

### 2.1 Alertes Configurées

| Alerte | Condition | Sévérité |
|--------|-----------|----------|
| API Down | Health check fail 3x | CRITICAL |
| High Error Rate | > 5% sur 5min | HIGH |
| High Latency | P99 > 3s | HIGH |
| Queue Depth | > 1000 jobs | MEDIUM |
| Disk Space | > 85% | MEDIUM |

### 2.2 Health Checks

```bash
# Backend
curl https://api.vectra.io/health
# Expected: {"status": "healthy"}

# Database
psql "postgres://..." -c "SELECT 1;"
```

---

## 3. PROCÉDURES DE DÉPLOIEMENT

### 3.1 Déploiement Standard

```
Push sur develop → Deploy Staging (auto)
Push sur main    → Deploy Production (auto)
```

### 3.2 Rollback

1. Render Dashboard > Service > Deploys
2. Trouver le déploiement précédent
3. Click "Rollback"

### 3.3 Checklist Post-Déploiement

- [ ] Health check OK
- [ ] Logs sans erreurs
- [ ] Métriques stables
- [ ] Test smoke manuel

---

## 4. GESTION DES INCIDENTS

### 4.1 Niveaux de Sévérité

| Niveau | Critères | Réponse |
|--------|----------|---------|
| SEV1 | Service down | 15 min |
| SEV2 | Feature majeure KO | 30 min |
| SEV3 | Feature mineure KO | 2h |
| SEV4 | Bug non bloquant | 24h |

### 4.2 Processus

```
1. DÉTECTION → Alerte ou rapport
2. TRIAGE → Évaluer sévérité
3. COMMUNICATION → Status page + Slack
4. INVESTIGATION → Logs, métriques
5. RÉSOLUTION → Fix + deploy
6. POST-MORTEM → Documentation
```

---

## 5. RUNBOOKS PAR INCIDENT

### INCIDENT: API Non Disponible

**Investigation:**
```bash
curl -I https://api.vectra.io/health
# Vérifier logs Render Dashboard
# Vérifier métriques (CPU, RAM)
```

**Résolution:**
1. Si crash → Redémarrer service
2. Si OOM → Augmenter RAM
3. Si bug → Rollback

---

### INCIDENT: Base de Données Lente

**Investigation:**
```sql
-- Connexions actives
SELECT count(*) FROM pg_stat_activity;

-- Requêtes lentes
SELECT pid, now() - query_start AS duration, query
FROM pg_stat_activity WHERE state != 'idle'
ORDER BY duration DESC;
```

**Résolution:**
```sql
-- Tuer connexions idle
SELECT pg_terminate_backend(pid) 
FROM pg_stat_activity 
WHERE state = 'idle' 
AND query_start < now() - interval '10 min';
```

---

### INCIDENT: Queue Celery Bloquée

**Investigation:**
```bash
celery -A app.worker inspect active
redis-cli LLEN celery
```

**Résolution:**
```bash
# Redémarrer workers
# Ou purger queue (DANGER)
celery -A app.worker purge
```

---

### INCIDENT: Emails Non Envoyés

**Investigation:**
- Dashboard SendGrid > Activity
- Logs: `grep "sendgrid" logs.txt`

**Résolution:**
1. Quota dépassé → Attendre/upgrader
2. API Key invalide → Régénérer
3. Bug → Rollback

---

## 6. BACKUP ET RESTORE

### 6.1 Backups

- Automatiques: Quotidien (Render)
- Rétention: 7 jours

### 6.2 Restore

```bash
# Via Render Dashboard
PostgreSQL > Backups > Select > Restore

# Manuel
pg_dump "postgres://..." > backup.sql
psql "postgres://..." < backup.sql
```

---

## 7. MAINTENANCE

### Quotidienne (Auto)
- 02:00 UTC: Backup DB
- 03:00 UTC: Log rotation

### Hebdomadaire
- Dimanche: VACUUM ANALYZE
- Lundi: Revue alertes

### Mensuelle
- Revue des accès
- Test de restore
- Mise à jour dépendances

---

## 8. CONTACTS ET ESCALADE

### Équipe

| Rôle | Contact |
|------|---------|
| On-Call Primary | PagerDuty |
| Tech Lead | tech-lead@vectra.io |
| CTO | cto@vectra.io |

### Escalade

| Temps | Action |
|-------|--------|
| T+0 | Primary On-Call |
| T+15min | Secondary On-Call |
| T+30min | Tech Lead |
| T+1h | CTO |

### Services Externes

| Service | Support |
|---------|---------|
| Render | support@render.com |
| Vercel | support@vercel.com |
| SendGrid | support.sendgrid.com |

---

## COMMANDES UTILES

### Database
```bash
# Connexion
psql "postgres://user:pass@host:port/db"

# Taille tables
SELECT relname, pg_size_pretty(pg_total_relation_size(relid))
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC;
```

### Redis
```bash
redis-cli INFO memory
redis-cli LLEN celery
```

### Celery
```bash
celery -A app.worker inspect active
celery -A app.worker inspect stats
```

---

**- FIN DU DOCUMENT -**

*14 Janvier 2026*
