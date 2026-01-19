# VECTRA - ONBOARDING & ACTIVATION SPECIFICATION
## First-Time User Experience (FTUE) & Activation Framework
### Version 1.0 | 14 Janvier 2026

---

**Document:** DOC-BIZ-001  
**Statut:** CRITIQUE - BUSINESS READY  
**Objectif:** Maximiser l'activation et réduire le churn J1-J7  

---

## TABLE DES MATIÈRES

1. Philosophie d'Onboarding
2. Définition de l'Activation
3. Parcours Onboarding Détaillé
4. Empty States Stratégiques
5. Emails Lifecycle
6. Métriques & Monitoring
7. Implémentation Technique

---

## 1. PHILOSOPHIE D'ONBOARDING

### 1.1 Principe Fondamental

```
L'utilisateur doit voir de la VALEUR en < 5 minutes.

Pas comprendre le produit.
Pas configurer le produit.
VOIR DE LA VALEUR.
```

### 1.2 Les 3 Erreurs Fatales à Éviter

| Erreur | Conséquence | Notre Approche |
|--------|-------------|----------------|
| Tour produit de 10 slides | 70% abandon | Zéro tour, action immédiate |
| Demander trop d'infos au signup | Friction = churn | 3 champs max (email, password, company) |
| Dashboard vide au premier login | "C'est quoi ce truc?" | Données de démo pré-remplies |

### 1.3 Time-to-Value Cibles

| Milestone | Temps Cible | Définition |
|-----------|-------------|------------|
| First Value | < 5 min | Voir un lead qualifié (même fictif) |
| Aha Moment | < 15 min | Première campagne créée |
| Habit Moment | < 48h | Revenir vérifier les résultats |

---

## 2. DÉFINITION DE L'ACTIVATION

### 2.1 Qu'est-ce qu'un Utilisateur "Activé" ?

Un utilisateur est **ACTIVÉ** quand il a complété ces 3 actions :

```
✅ Action 1 : Créé sa première campagne
✅ Action 2 : Connecté une intégration (HubSpot OU Calendly)
✅ Action 3 : Approuvé au moins 1 email généré

Délai cible : < 7 jours après signup
```

### 2.2 Pourquoi Ces 3 Actions ?

| Action | Signal Business | Corrélation Rétention |
|--------|-----------------|----------------------|
| Campagne créée | A compris le produit | +45% rétention M1 |
| Intégration connectée | Investissement technique | +65% rétention M1 |
| Email approuvé | A vu la valeur IA | +80% rétention M1 |

### 2.3 Segmentation par Activation

```
┌─────────────────────────────────────────────────────────────┐
│ SEGMENT           │ DÉFINITION        │ ACTION REQUISE      │
├───────────────────┼───────────────────┼─────────────────────┤
│ 🔴 À risque       │ 0 action en 3j    │ Email + Call urgent │
│ 🟠 En cours       │ 1-2 actions en 7j │ Nudge in-app        │
│ 🟢 Activé         │ 3 actions en 7j   │ Upsell ready        │
│ ⭐ Power User     │ 3 actions en 24h  │ Case study prospect │
└───────────────────┴───────────────────┴─────────────────────┘
```

---

## 3. PARCOURS ONBOARDING DÉTAILLÉ

### 3.1 Vue d'Ensemble du Flow

```
Signup (30 sec)
    │
    ▼
Welcome Screen (10 sec)
    │
    ▼
Quick Setup Wizard (3 min)
    │
    ├─ Step 1: Company Info (30 sec)
    ├─ Step 2: Connect Integration (1 min)
    └─ Step 3: Create First Campaign (1.5 min)
    │
    ▼
Dashboard avec Données Démo
    │
    ▼
Checklist Flottante (guide les 7 premiers jours)
```

### 3.2 Étape 0 : Signup

**URL:** `/signup`

**Champs (3 maximum):**
```
- Email professionnel *
- Mot de passe *
- Nom de l'entreprise *
```

**Ce qu'on NE demande PAS:**
- Prénom/Nom (récupéré plus tard)
- Téléphone (friction inutile)
- Taille entreprise (demandé dans wizard)
- Carte bancaire (jamais au signup)

**Post-Signup:**
```
1. Créer organization avec plan "trial"
2. Créer user avec rôle "owner"
3. Envoyer email de bienvenue
4. Redirect vers /onboarding
5. Tracker événement: user_signed_up
```

### 3.3 Étape 1 : Welcome Screen

**URL:** `/onboarding`

**Durée:** 10 secondes max

**Contenu:**
```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│                    👋 Bienvenue sur Vectra                  │
│                                                             │
│     Vous êtes à 3 minutes de votre première campagne        │
│     de prospection automatisée.                             │
│                                                             │
│                   [Commencer →]                             │
│                                                             │
│           ○ ○ ○  (3 étapes, ~3 min)                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Pas de:**
- Vidéo explicative
- Tour produit
- Liste de features

### 3.4 Étape 2 : Quick Setup Wizard

#### Step 1/3 : Company Info (30 sec)

```
┌─────────────────────────────────────────────────────────────┐
│ Étape 1/3 • Votre entreprise                               │
│ ═══════●○○                                                  │
│                                                             │
│ Secteur d'activité *                                       │
│ ┌─────────────────────────────────────────────────────────┐│
│ │ [SaaS / Technology ▼]                                   ││
│ └─────────────────────────────────────────────────────────┘│
│                                                             │
│ Taille de l'équipe commerciale *                           │
│ ┌─────────────────────────────────────────────────────────┐│
│ │ ○ 1-5    ○ 6-20    ○ 21-50    ○ 50+                    ││
│ └─────────────────────────────────────────────────────────┘│
│                                                             │
│ Votre rôle *                                               │
│ ┌─────────────────────────────────────────────────────────┐│
│ │ [Founder / CEO ▼]                                       ││
│ └─────────────────────────────────────────────────────────┘│
│                                                             │
│                                    [Continuer →]            │
└─────────────────────────────────────────────────────────────┘
```

**Pourquoi ces champs:**
- Secteur → Personnaliser les templates email
- Taille équipe → Déterminer le plan recommandé
- Rôle → Adapter le messaging

#### Step 2/3 : Connect Integration (1 min)

```
┌─────────────────────────────────────────────────────────────┐
│ Étape 2/3 • Connexion rapide                               │
│ ═══════════●○                                               │
│                                                             │
│ Connectez votre CRM pour synchroniser vos leads            │
│ (Vous pourrez le faire plus tard)                          │
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐│
│ │ [HubSpot Logo]  HubSpot                                 ││
│ │ Synchronisation bidirectionnelle          [Connecter]   ││
│ └─────────────────────────────────────────────────────────┘│
│                                                             │
│ ┌─────────────────────────────────────────────────────────┐│
│ │ [Calendly Logo]  Calendly                               ││
│ │ Booking automatique des RDV               [Connecter]   ││
│ └─────────────────────────────────────────────────────────┘│
│                                                             │
│ [Passer cette étape]               [Continuer →]           │
└─────────────────────────────────────────────────────────────┘
```

**Logique:**
- Si connecte HubSpot → Importer les contacts existants
- Si connecte Calendly → Récupérer les disponibilités
- Si skip → Rappeler dans la checklist

#### Step 3/3 : First Campaign (1.5 min)

```
┌─────────────────────────────────────────────────────────────┐
│ Étape 3/3 • Votre première campagne                        │
│ ═══════════════●                                            │
│                                                             │
│ Créons votre première campagne en 60 secondes              │
│                                                             │
│ Nom de la campagne                                         │
│ ┌─────────────────────────────────────────────────────────┐│
│ │ Q1 2026 - Prospection VP Sales                          ││
│ └─────────────────────────────────────────────────────────┘│
│                                                             │
│ Qui voulez-vous cibler ?                                   │
│ ┌─────────────────────────────────────────────────────────┐│
│ │ VP Sales ✕  Director Sales ✕  [+ Ajouter]              ││
│ └─────────────────────────────────────────────────────────┘│
│                                                             │
│ Géographie                                                 │
│ ┌─────────────────────────────────────────────────────────┐│
│ │ France ✕  Belgique ✕  [+ Ajouter]                      ││
│ └─────────────────────────────────────────────────────────┘│
│                                                             │
│              [Créer ma campagne et voir les résultats →]   │
└─────────────────────────────────────────────────────────────┘
```

**Ce qui se passe en arrière-plan:**
```python
# Pseudo-code
1. Créer campaign avec critères
2. Lancer Agent Prospector en mode "démo" (10 leads fictifs réalistes)
3. Afficher immédiatement le dashboard avec ces leads
4. Lancer la vraie prospection en background
```

### 3.5 Étape 3 : Dashboard avec Données Démo

**Premier affichage du Dashboard:**

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  🎉 Votre campagne est lancée !                            │
│                                                             │
│  Pendant que nos agents recherchent vos prospects,         │
│  voici un aperçu de ce que vous verrez :                   │
│                                                             │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐              │
│  │   10   │ │    4   │ │    0   │ │    0   │              │
│  │ Leads  │ │Qualif. │ │ Emails │ │Meetings│              │
│  │ (démo) │ │ (démo) │ │        │ │        │              │
│  └────────┘ └────────┘ └────────┘ └────────┘              │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Données de démonstration                       [✕]  │   │
│  │ Ces leads sont fictifs pour illustrer le produit.   │   │
│  │ Vos vrais prospects apparaîtront dans ~15 min.      │   │
│  │                                                     │   │
│  │ [Voir les leads de démo]  [Configurer mes critères] │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 3.6 Checklist Flottante (7 premiers jours)

**Widget fixe en bas à droite:**

```
┌───────────────────────────────────────┐
│ 🚀 Démarrage rapide            2/5   │
├───────────────────────────────────────┤
│ ✅ Créer votre compte                 │
│ ✅ Créer votre première campagne      │
│ ○  Connecter HubSpot ou Calendly      │
│ ○  Approuver votre premier email      │
│ ○  Obtenir votre premier RDV          │
├───────────────────────────────────────┤
│ [Besoin d'aide ? Parler à un expert]  │
└───────────────────────────────────────┘
```

**Comportement:**
- Apparaît après onboarding wizard
- Reste visible jusqu'à 5/5 complété
- Peut être minimisé mais pas fermé définitivement
- Chaque item cliquable → action correspondante

---

## 4. EMPTY STATES STRATÉGIQUES

### 4.1 Principe

```
Un empty state n'est pas un message d'erreur.
C'est une OPPORTUNITÉ de guider l'utilisateur.
```

### 4.2 Empty States par Page

#### Dashboard - Aucune campagne

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│                    📊                                       │
│                                                             │
│           Votre dashboard attend des données                │
│                                                             │
│    Créez votre première campagne pour commencer             │
│    à générer des leads qualifiés automatiquement.           │
│                                                             │
│              [Créer ma première campagne →]                 │
│                                                             │
│    💡 Astuce : La plupart de nos clients voient leurs      │
│       premiers leads qualifiés en moins de 24h.            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### Leads - Liste vide

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│                    👥                                       │
│                                                             │
│              Aucun lead pour le moment                      │
│                                                             │
│    Vos leads apparaîtront ici dès que nos agents           │
│    auront terminé leur recherche.                          │
│                                                             │
│    Temps estimé : ~15 minutes                              │
│                                                             │
│    ┌─────────────────────────────────────────────────┐     │
│    │ ████████████████░░░░ Recherche en cours... 65%  │     │
│    └─────────────────────────────────────────────────┘     │
│                                                             │
│    [Voir le statut des agents] [Ajuster mes critères]      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### Emails - Aucun email à approuver

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│                    ✅                                       │
│                                                             │
│              Tout est à jour !                              │
│                                                             │
│    Aucun email en attente d'approbation.                   │
│    Nous vous préviendrons dès qu'il y en aura.             │
│                                                             │
│    [Voir les emails envoyés] [Configurer l'auto-approve]   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### Meetings - Aucun RDV

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│                    📅                                       │
│                                                             │
│           Vos premiers RDV arrivent bientôt                │
│                                                             │
│    En moyenne, nos utilisateurs obtiennent leur            │
│    premier RDV qualifié en 5-7 jours.                      │
│                                                             │
│    Votre campagne est active depuis : 2 jours              │
│                                                             │
│    ┌─────────────────────────────────────────────────┐     │
│    │ 📈 Pipeline actuel                              │     │
│    │    342 prospects → 45 qualifiés → 12 contactés  │     │
│    └─────────────────────────────────────────────────┘     │
│                                                             │
│    [Voir les leads contactés] [Optimiser ma campagne]      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. EMAILS LIFECYCLE

### 5.1 Séquence d'Emails Onboarding

| J+ | Email | Objectif | Trigger |
|----|-------|----------|---------|
| J0 | Welcome | Confirmer inscription | Signup |
| J0+2h | Getting Started | Rappeler wizard si non complété | !wizard_completed |
| J1 | First Results | Montrer premiers leads | leads_found > 0 |
| J3 | Activation Nudge | Pousser vers activation | !activated |
| J5 | Success Story | Social proof | !activated |
| J7 | Last Chance | Urgence fin trial | !activated |

### 5.2 Templates Emails

#### Email J0 : Welcome

```
Sujet: Bienvenue sur Vectra, {first_name} 👋

---

Bonjour {first_name},

Votre compte Vectra est prêt.

Voici ce qui vous attend :
• Des leads qualifiés automatiquement
• Des emails personnalisés par l'IA
• Des RDV bookés sans effort

→ Créer ma première campagne
   {cta_link}

Vous avez 14 jours pour explorer Vectra gratuitement.

À très vite,
L'équipe Vectra

P.S. Une question ? Répondez simplement à cet email.
```

#### Email J3 : Activation Nudge

```
Sujet: {first_name}, vos premiers leads vous attendent

---

Bonjour {first_name},

Vous avez créé votre compte il y a 3 jours, 
mais vous n'avez pas encore lancé votre première campagne.

Nos utilisateurs qui lancent leur campagne dans les 3 premiers jours
obtiennent en moyenne 40% plus de RDV qualifiés.

Il vous reste 11 jours de trial.

→ Lancer ma campagne maintenant (2 min)
   {cta_link}

Besoin d'aide ? Réservez un appel de 15 min avec notre équipe :
→ {calendly_link}

Cordialement,
{sales_rep_name}
Customer Success, Vectra
```

#### Email J7 : Last Chance

```
Sujet: ⏰ Plus que 7 jours de trial, {first_name}

---

Bonjour {first_name},

Votre période d'essai se termine dans 7 jours.

Voici ce que vous manquez :
❌ {leads_count} leads potentiels non exploités
❌ Environ {estimated_meetings} RDV qualifiés
❌ ~{estimated_pipeline}€ de pipeline

Il n'est pas trop tard.

→ Activer ma campagne maintenant
   {cta_link}

Ou si Vectra ne correspond pas à vos besoins actuels,
dites-le nous : {feedback_link}

Cordialement,
L'équipe Vectra
```

---

## 6. MÉTRIQUES & MONITORING

### 6.1 KPIs Onboarding

| Métrique | Définition | Cible | Alerte |
|----------|------------|-------|--------|
| Signup → Wizard Start | % qui commencent le wizard | > 90% | < 80% |
| Wizard Completion | % qui finissent le wizard | > 70% | < 50% |
| Time to First Campaign | Temps médian | < 5 min | > 15 min |
| Activation Rate J7 | % activés en 7 jours | > 40% | < 25% |
| Activation Rate J14 | % activés en 14 jours | > 55% | < 40% |

### 6.2 Funnel d'Activation

```
Signup
  │ 100%
  ▼
Wizard Started
  │ 92% (cible)
  ▼
Wizard Completed
  │ 75% (cible)
  ▼
First Campaign Created
  │ 70% (cible)
  ▼
Integration Connected
  │ 50% (cible)
  ▼
First Email Approved
  │ 45% (cible)
  ▼
ACTIVATED
  │ 40% (cible)
```

### 6.3 Cohort Analysis

Suivre par cohorte hebdomadaire :
- Activation J7
- Activation J14
- Conversion Trial → Paid
- Churn M1

---

## 7. IMPLÉMENTATION TECHNIQUE

### 7.1 Événements à Tracker

```typescript
// Signup & Onboarding
track('user_signed_up', { source, referrer });
track('onboarding_started', {});
track('onboarding_step_completed', { step: 1|2|3 });
track('onboarding_completed', { duration_seconds });
track('onboarding_skipped', { at_step });

// Activation
track('campaign_created', { campaign_id, is_first: boolean });
track('integration_connected', { type: 'hubspot'|'calendly' });
track('email_approved', { email_id, is_first: boolean });
track('user_activated', { days_since_signup });

// Engagement
track('dashboard_viewed', {});
track('leads_list_viewed', {});
track('email_edited', { email_id });
track('checklist_item_clicked', { item });
```

### 7.2 Schema Base de Données

```sql
-- Table: user_onboarding
CREATE TABLE user_onboarding (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    organization_id UUID REFERENCES organizations(id),
    
    -- Progress
    wizard_started_at TIMESTAMP,
    wizard_completed_at TIMESTAMP,
    wizard_current_step INTEGER DEFAULT 0,
    
    -- Activation milestones
    first_campaign_at TIMESTAMP,
    first_integration_at TIMESTAMP,
    first_email_approved_at TIMESTAMP,
    activated_at TIMESTAMP,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Index pour queries fréquentes
CREATE INDEX idx_onboarding_not_activated 
ON user_onboarding (user_id) 
WHERE activated_at IS NULL;
```

### 7.3 API Endpoints

```
POST /api/v1/onboarding/start
POST /api/v1/onboarding/step/{step}/complete
POST /api/v1/onboarding/skip
GET  /api/v1/onboarding/status
POST /api/v1/onboarding/checklist/{item}/complete
```

### 7.4 Checklist Component

```tsx
// components/features/onboarding/activation-checklist.tsx
interface ChecklistItem {
  id: string;
  title: string;
  completed: boolean;
  href: string;
  action?: () => void;
}

const CHECKLIST_ITEMS: ChecklistItem[] = [
  {
    id: 'signup',
    title: 'Créer votre compte',
    completed: true, // Always true if they see this
    href: '#',
  },
  {
    id: 'campaign',
    title: 'Créer votre première campagne',
    completed: false,
    href: '/campaigns/new',
  },
  {
    id: 'integration',
    title: 'Connecter HubSpot ou Calendly',
    completed: false,
    href: '/settings/integrations',
  },
  {
    id: 'email',
    title: 'Approuver votre premier email',
    completed: false,
    href: '/emails?status=pending',
  },
  {
    id: 'meeting',
    title: 'Obtenir votre premier RDV',
    completed: false,
    href: '/meetings',
  },
];
```

---

## CHECKLIST PRE-LAUNCH

### Onboarding Ready

- [ ] Signup flow avec 3 champs max
- [ ] Wizard 3 steps implémenté
- [ ] Données démo générées
- [ ] Empty states pour toutes les pages
- [ ] Checklist flottante fonctionnelle
- [ ] Emails lifecycle configurés
- [ ] Events tracking implémenté
- [ ] Métriques dashboard Ops

### Tests à Faire

- [ ] Test complet signup → activation (< 5 min)
- [ ] Test abandon wizard (emails de relance)
- [ ] Test empty states sur mobile
- [ ] Test emails (tous les templates)
- [ ] Test cohort tracking

---

**- FIN DU DOCUMENT -**

*Onboarding & Activation Spec - Vectra v1.0*
*14 Janvier 2026*
