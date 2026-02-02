# Configuration Resend - Variables d'Environnement

## Backend Configuration

### Fichier: `backend/.env` ou `backend/.env.local`

Ajoutez ces variables pour configurer Resend:

```bash
# Resend API Configuration
RESEND_API_KEY=re_xxxxx  # Votre clé API Resend (obtenue depuis https://resend.com/api-keys)
RESEND_FROM_EMAIL=noreply@vectra.io  # Email expéditeur (doit être vérifié dans Resend)
APP_URL=http://localhost:3000  # URL frontend pour les liens dans les emails
```

### Exemple complet `.env.local` backend

```bash
# Application
ENVIRONMENT=development
DEBUG=true
APP_URL=http://localhost:3000

# Database
DATABASE_URL=postgresql+psycopg://vectra:vectra@localhost:5432/vectra

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT
JWT_SECRET=your-jwt-secret-key
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=15
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Resend Email Service
RESEND_API_KEY=re_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
RESEND_FROM_EMAIL=noreply@vectra.io

# ... autres variables
```

## Frontend Configuration

**Note:** Le frontend n'a pas besoin de configuration Resend car les emails sont envoyés uniquement par le backend.

Le frontend peut recevoir des paramètres pour personnaliser les emails (via l'API), mais l'envoi se fait côté backend.

### Fichier: `frontend/.env.local`

```bash
# Frontend n'a pas besoin de RESEND_API_KEY
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

## Obtenir une Clé API Resend

1. **Créer un compte:** <https://resend.com>
2. **Vérifier votre domaine** (optionnel mais recommandé):
   - Allez dans "Domains" dans le dashboard
   - Ajoutez votre domaine (ex: `vectra.io`)
   - Configurez les enregistrements DNS (SPF, DKIM, DMARC)
3. **Créer une API Key:**
   - Allez dans "API Keys"
   - Cliquez "Create API Key"
   - Nommez-la (ex: "Vectra Production")
   - Copiez la clé (commence par `re_...`)
   - ⚠️ **Important:** La clé n'est affichée qu'une seule fois

## Configuration Domaine (Production)

Pour envoyer des emails depuis votre domaine personnalisé:

1. **Dans Resend Dashboard > Domains:**
   - Ajoutez votre domaine (ex: `vectra.io`)

2. **Configurez DNS:**

   ```
   Type: TXT
   Name: @
   Value: [SPF record fourni par Resend]
   
   Type: CNAME
   Name: [DKIM record name]
   Value: [DKIM value fourni par Resend]
   ```

3. **Attendez la vérification** (peut prendre quelques minutes)

4. **Mettez à jour `.env`:**

   ```bash
   RESEND_FROM_EMAIL=noreply@vectra.io  # Utilise votre domaine vérifié
   ```

## Test en Développement

**Sans API Key:**

- Les emails sont loggés dans les logs backend
- Aucun email réel n'est envoyé
- Parfait pour tests sans coût

**Avec API Key:**

- Les emails sont envoyés via Resend API
- Free tier: 3,000 emails/mois
- Dashboard Resend pour tracking

## Vérification Setup

Pour vérifier que Resend est correctement configuré:

```bash
# Backend
cd backend
python -c "from app.core.config import settings; print(f'Resend API Key: {settings.RESEND_API_KEY[:10] if settings.RESEND_API_KEY else None}...'); print(f'From Email: {settings.RESEND_FROM_EMAIL}')"
```

Si `RESEND_API_KEY` est `None` ou vide, les emails seront loggés mais pas envoyés.

---

*Configuration Resend - 15 Janvier 2026*
