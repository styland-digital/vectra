# ADR-011: Service d'Envoi d'Emails (Resend)

### Statut: APPROUVÉ

### Date: 15 Janvier 2026

### Décideurs: Tech Lead

### Contexte

Vectra nécessite l'envoi d'emails transactionnels:

- Vérification d'email lors de l'inscription
- Réinitialisation de mot de passe (futur)
- Notifications (futur)
- Emails de prospection générés par l'agent Scheduler (Phase 2)

Besoins:

- Fiabilité de livraison
- Templates HTML
- Tracking (ouvertures, clics)
- Coût compatible bootstrap
- API simple et moderne

### Options Considérées

#### Option A: Resend

- **Pour:** API moderne, excellent deliverability, templates React, coût $20/mois (100k emails), SDK Python simple
- **Contre:** Plus récent que SendGrid (moins de track record), moins de features avancées
- **Effort:** 2-3h d'intégration
- **Coût:** Free tier (3k emails/mois), puis $20/mois (100k emails)

#### Option B: SendGrid (déjà mentionné dans ADR)

- **Pour:** Mature, feature-rich, bonne deliverability
- **Contre:** API plus complexe, coût plus élevé ($19.95/mois pour 50k emails), SDK moins moderne
- **Effort:** 3-4h d'intégration
- **Coût:** Free tier (100 emails/jour), puis $19.95/mois

#### Option C: Postmark

- **Pour:** Excellent deliverability, spécialisé transactionnel
- **Contre:** Plus cher, moins connu
- **Coût:** $15/mois (10k emails)

#### Option D: AWS SES

- **Pour:** Très bon marché, scalable
- **Contre:** Configuration plus complexe, moins user-friendly
- **Coût:** $0.10 pour 1000 emails

### Décision

**Resend** est retenu comme service d'envoi d'emails pour les emails transactionnels (vérification, notifications).

**SendGrid** reste une option pour les emails de prospection (Phase 2) si besoin de features avancées.

### Justification

1. **Modernité:** API REST simple, SDK Python clair, templates React supportés
2. **Deliverability:** Excellent taux de livraison pour emails transactionnels
3. **Coût:** Free tier (3k emails/mois) suffisant pour début, puis $20/mois scalable
4. **Simplicité:** Moins de boilerplate que SendGrid
5. **Bootstrap-friendly:** Compatible avec stratégie de coûts réduits

### Architecture

**Séparation des responsabilités:**

```
Frontend (Next.js)
    ↓ (peut personnaliser le contenu via paramètres)
Backend Service (email_verification.py)
    ↓ (construit le template HTML)
Service Resend (resend.py)
    ↓ (envoie via API Resend)
Resend API
```

**Règle importante:** Le contenu de l'email est construit côté **backend** pour la sécurité. Le frontend peut fournir des paramètres de personnalisation (nom utilisateur, etc.), mais le template et l'envoi sont gérés par le backend.

### Implémentation

**Structure des fichiers:**

- `backend/app/services/resend.py` - Service Resend wrapper
- `backend/app/templates/emails/verify-email.html` - Template HTML
- `backend/app/services/email_verification.py` - Utilise Resend service

**Variables d'environnement:**

```bash
RESEND_API_KEY=re_xxxxx
RESEND_FROM_EMAIL=noreply@vectra.io  # Doit être vérifié dans Resend
```

### Conséquences

**Positives:**

- Code simple et maintenable
- Excellent taux de livraison
- Coût maîtrisé pour bootstrap
- Templates HTML flexibles

**Négatives:**

- Nouvelle dépendance externe
- Moins de track record que SendGrid
- Limite free tier: 3k emails/mois

### Risques et Mitigations

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| Rate limiting Resend | 20% | Moyen | Monitoring, retry logic, fallback SendGrid si nécessaire |
| Délivrabilité insuffisante | 10% | Moyen | Vérification domaine, SPF/DKIM/DMARC configurés |
| Coûts à l'échelle | 30% | Faible | Migration vers AWS SES si volume très élevé |

### Métriques de Succès

- Taux de livraison > 99%
- Temps d'envoi < 500ms (P99)
- Taux d'ouverture emails vérification > 60%

### Date de Revue: Mois 3 (Avril 2026)

---

*ADR-011 - 15 Janvier 2026*
