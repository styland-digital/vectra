# VECTRA - BILLING & SUBSCRIPTION SPECIFICATION
## Monétisation, Plans, et Infrastructure de Paiement
### Version 1.0 | 14 Janvier 2026

---

**Document:** DOC-BIZ-002  
**Statut:** CRITIQUE - REVENUE READY  
**Objectif:** Infrastructure de facturation robuste et prévisible  

---

## TABLE DES MATIÈRES

1. Stratégie de Monétisation
2. Structure des Plans
3. Limites & Quotas Techniques
4. Intégration Stripe
5. Gestion du Lifecycle Abonnement
6. Dunning & Recovery
7. Métriques Revenue
8. Implémentation Technique

---

## 1. STRATÉGIE DE MONÉTISATION

### 1.1 Modèle de Pricing

```
MODÈLE HYBRIDE :
Base mensuelle fixe + Usage variable (leads)

Pourquoi :
- Base fixe → Revenu prévisible (MRR stable)
- Variable → Aligne nos intérêts avec le client (plus de leads = plus de valeur)
```

### 1.2 Principes de Pricing

| Principe | Application |
|----------|-------------|
| Value-based | Prix basé sur la valeur (RDV générés), pas sur les coûts |
| Transparent | Pas de frais cachés, tout est visible |
| Scalable | Le client peut upgrader/downgrader sans friction |
| Fair | Pas de lock-in, export des données gratuit |

### 1.3 Positionnement Marché

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  Outreach.io     ████████████████████████████  $100-150/user│
│  Salesloft       ██████████████████████████    $75-125/user │
│  Apollo.io       ██████████████                $49-99/user  │
│  VECTRA          █████████████                 $99-299 flat │
│                                                             │
│  Notre avantage : Prix FLAT, pas par utilisateur            │
│                   ROI visible en < 30 jours                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. STRUCTURE DES PLANS

### 2.1 Les 3 Plans

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   STARTER              GROWTH                 SCALE                 │
│   Pour tester          Pour croître           Pour dominer          │
│                                                                     │
│   99€/mois             299€/mois              799€/mois             │
│   (ou 990€/an)         (ou 2 990€/an)         (ou 7 990€/an)        │
│   = 2 mois gratuits    = 2 mois gratuits      = 2 mois gratuits     │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   LEADS/MOIS                                                        │
│   500                  2 000                  10 000                │
│                                                                     │
│   CAMPAGNES ACTIVES                                                 │
│   2                    5                      Illimitées            │
│                                                                     │
│   UTILISATEURS                                                      │
│   2                    5                      15                    │
│                                                                     │
│   INTÉGRATIONS                                                      │
│   HubSpot              + Salesforce           + Custom API          │
│   Calendly             + Pipedrive            + Webhooks            │
│                                                                     │
│   SUPPORT                                                           │
│   Email                Email + Chat           + Dédié               │
│   48h                  24h                    4h                    │
│                                                                     │
│   FONCTIONNALITÉS                                                   │
│   ✓ 3 Agents IA        ✓ 3 Agents IA          ✓ 3 Agents IA         │
│   ✓ BANT Scoring       ✓ BANT Scoring         ✓ BANT Scoring        │
│   ✓ Email Generation   ✓ Email Generation     ✓ Email Generation    │
│   ✓ Basic Analytics    ✓ Advanced Analytics   ✓ Custom Reports      │
│   ✗ A/B Testing        ✓ A/B Testing          ✓ A/B Testing         │
│   ✗ API Access         ✗ API Access           ✓ API Access          │
│   ✗ White Label        ✗ White Label          ✓ White Label         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.2 Plan Détaillé

#### STARTER - 99€/mois

```yaml
name: starter
price_monthly: 99
price_yearly: 990
currency: EUR

limits:
  leads_per_month: 500
  campaigns_active: 2
  users: 2
  emails_per_day: 50
  
features:
  agents:
    prospector: true
    bant_qualifier: true
    meeting_scheduler: true
  integrations:
    hubspot: true
    calendly: true
    salesforce: false
    pipedrive: false
    custom_api: false
    webhooks: false
  analytics:
    basic_dashboard: true
    advanced_reports: false
    custom_reports: false
    export_csv: true
    export_api: false
  automation:
    ab_testing: false
    auto_approve: false
    custom_scoring: false
  support:
    email: true
    chat: false
    dedicated: false
    sla_hours: 48

ideal_for: "Startups et PME testant l'automatisation"
```

#### GROWTH - 299€/mois

```yaml
name: growth
price_monthly: 299
price_yearly: 2990
currency: EUR

limits:
  leads_per_month: 2000
  campaigns_active: 5
  users: 5
  emails_per_day: 200
  
features:
  agents:
    prospector: true
    bant_qualifier: true
    meeting_scheduler: true
  integrations:
    hubspot: true
    calendly: true
    salesforce: true
    pipedrive: true
    custom_api: false
    webhooks: true
  analytics:
    basic_dashboard: true
    advanced_reports: true
    custom_reports: false
    export_csv: true
    export_api: false
  automation:
    ab_testing: true
    auto_approve: true
    custom_scoring: true
  support:
    email: true
    chat: true
    dedicated: false
    sla_hours: 24

ideal_for: "Équipes commerciales en croissance"
```

#### SCALE - 799€/mois

```yaml
name: scale
price_monthly: 799
price_yearly: 7990
currency: EUR

limits:
  leads_per_month: 10000
  campaigns_active: -1  # unlimited
  users: 15
  emails_per_day: 500
  
features:
  agents:
    prospector: true
    bant_qualifier: true
    meeting_scheduler: true
  integrations:
    hubspot: true
    calendly: true
    salesforce: true
    pipedrive: true
    custom_api: true
    webhooks: true
  analytics:
    basic_dashboard: true
    advanced_reports: true
    custom_reports: true
    export_csv: true
    export_api: true
  automation:
    ab_testing: true
    auto_approve: true
    custom_scoring: true
  support:
    email: true
    chat: true
    dedicated: true
    sla_hours: 4

ideal_for: "Entreprises avec équipes commerciales importantes"
```

### 2.3 Add-ons & Overages

```yaml
addons:
  extra_leads_pack:
    name: "Pack 500 leads supplémentaires"
    price: 49
    leads: 500
    
  extra_user:
    name: "Utilisateur supplémentaire"
    price: 29
    per: "month"
    
  priority_support:
    name: "Support prioritaire"
    price: 99
    per: "month"
    sla_hours: 4
    
  api_access:
    name: "Accès API"
    price: 199
    per: "month"
    note: "Inclus dans Scale"

overages:
  leads:
    price_per_unit: 0.15  # €0.15 par lead au-delà du quota
    billing: "end_of_month"
    cap: 2x  # Max 2x le quota avant blocage
```

### 2.4 Trial & Freemium

```yaml
trial:
  duration_days: 14
  plan: "growth"  # Full Growth features pendant trial
  credit_card_required: false
  limits:
    leads: 100  # Limité pendant trial
    campaigns: 1
    emails: 20
  conversion_prompt:
    day_7: true
    day_10: true
    day_13: true
    day_14: true

# Pas de plan freemium (décision stratégique)
# Raison: Coût LLM trop élevé, focus sur clients payants
```

---

## 3. LIMITES & QUOTAS TECHNIQUES

### 3.1 Rate Limiting par Plan

```typescript
const RATE_LIMITS = {
  starter: {
    api_requests_per_minute: 60,
    leads_per_day: 50,
    emails_per_hour: 10,
    campaigns_concurrent: 2,
  },
  growth: {
    api_requests_per_minute: 300,
    leads_per_day: 200,
    emails_per_hour: 50,
    campaigns_concurrent: 5,
  },
  scale: {
    api_requests_per_minute: 1000,
    leads_per_day: 1000,
    emails_per_hour: 100,
    campaigns_concurrent: -1, // unlimited
  },
};
```

### 3.2 Soft Limits vs Hard Limits

```
SOFT LIMITS (avertissement, pas blocage):
- 80% du quota leads → Notification in-app + email
- 90% du quota leads → Warning prominent
- 100% du quota → Propose upgrade OU pack leads

HARD LIMITS (blocage):
- 120% du quota leads → Blocage création campagne
- Rate limit API dépassé → 429 Too Many Requests
- Users max atteints → Impossible d'inviter
```

### 3.3 Quota Reset

```
Période: Mois calendaire
Reset: 1er du mois à 00:00 UTC
Rollover: Non (leads non utilisés perdus)
Prorata: Oui au premier mois (upgrade mid-month)
```

### 3.4 Usage Tracking

```sql
-- Table: organization_usage
CREATE TABLE organization_usage (
    id UUID PRIMARY KEY,
    organization_id UUID REFERENCES organizations(id),
    period_start DATE,
    period_end DATE,
    
    -- Counters
    leads_used INTEGER DEFAULT 0,
    leads_limit INTEGER,
    emails_sent INTEGER DEFAULT 0,
    emails_limit INTEGER,
    api_calls INTEGER DEFAULT 0,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(organization_id, period_start)
);

-- Index pour query rapide
CREATE INDEX idx_usage_current ON organization_usage 
(organization_id, period_start DESC);
```

---

## 4. INTÉGRATION STRIPE

### 4.1 Architecture Stripe

```
┌─────────────────────────────────────────────────────────────┐
│                        STRIPE                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Products                                                   │
│  ├─ prod_starter     → Vectra Starter                      │
│  ├─ prod_growth      → Vectra Growth                       │
│  └─ prod_scale       → Vectra Scale                        │
│                                                             │
│  Prices (par Product)                                       │
│  ├─ price_starter_monthly   → 99€/mois                     │
│  ├─ price_starter_yearly    → 990€/an                      │
│  ├─ price_growth_monthly    → 299€/mois                    │
│  ├─ price_growth_yearly     → 2990€/an                     │
│  ├─ price_scale_monthly     → 799€/mois                    │
│  └─ price_scale_yearly      → 7990€/an                     │
│                                                             │
│  Customers                                                  │
│  └─ 1 Customer = 1 Organization                            │
│                                                             │
│  Subscriptions                                              │
│  └─ 1 Subscription = 1 Plan actif                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Stripe Webhook Events

```typescript
// Événements à gérer
const STRIPE_EVENTS = {
  // Subscription lifecycle
  'customer.subscription.created': handleSubscriptionCreated,
  'customer.subscription.updated': handleSubscriptionUpdated,
  'customer.subscription.deleted': handleSubscriptionDeleted,
  
  // Paiements
  'invoice.paid': handleInvoicePaid,
  'invoice.payment_failed': handlePaymentFailed,
  'invoice.upcoming': handleUpcomingInvoice,
  
  // Customer
  'customer.updated': handleCustomerUpdated,
  'customer.deleted': handleCustomerDeleted,
  
  // Checkout
  'checkout.session.completed': handleCheckoutCompleted,
};
```

### 4.3 Mapping Stripe ↔ Vectra

```sql
-- Table: stripe_customers
CREATE TABLE stripe_customers (
    id UUID PRIMARY KEY,
    organization_id UUID UNIQUE REFERENCES organizations(id),
    stripe_customer_id VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Table: subscriptions
CREATE TABLE subscriptions (
    id UUID PRIMARY KEY,
    organization_id UUID REFERENCES organizations(id),
    stripe_subscription_id VARCHAR(255) UNIQUE,
    stripe_price_id VARCHAR(255),
    
    -- Plan info
    plan VARCHAR(50) NOT NULL,  -- 'starter', 'growth', 'scale'
    billing_cycle VARCHAR(20),   -- 'monthly', 'yearly'
    
    -- Status
    status VARCHAR(50) NOT NULL,  -- 'active', 'past_due', 'canceled', 'trialing'
    
    -- Dates
    current_period_start TIMESTAMP,
    current_period_end TIMESTAMP,
    trial_end TIMESTAMP,
    canceled_at TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### 4.4 Checkout Flow

```typescript
// 1. Créer une session Checkout
async function createCheckoutSession(
  organizationId: string,
  priceId: string,
  successUrl: string,
  cancelUrl: string
) {
  // Récupérer ou créer le customer Stripe
  const customer = await getOrCreateStripeCustomer(organizationId);
  
  // Créer la session
  const session = await stripe.checkout.sessions.create({
    customer: customer.id,
    mode: 'subscription',
    payment_method_types: ['card'],
    line_items: [{ price: priceId, quantity: 1 }],
    success_url: successUrl,
    cancel_url: cancelUrl,
    allow_promotion_codes: true,
    billing_address_collection: 'required',
    tax_id_collection: { enabled: true },
    metadata: {
      organization_id: organizationId,
    },
  });
  
  return session;
}

// 2. Rediriger vers Stripe
// Frontend: window.location.href = session.url

// 3. Webhook: checkout.session.completed
async function handleCheckoutCompleted(event: Stripe.Event) {
  const session = event.data.object as Stripe.Checkout.Session;
  const organizationId = session.metadata?.organization_id;
  
  // Activer l'abonnement côté Vectra
  await activateSubscription(organizationId, session.subscription as string);
}
```

### 4.5 Customer Portal

```typescript
// Permettre au client de gérer son abonnement
async function createBillingPortalSession(organizationId: string) {
  const customer = await getStripeCustomer(organizationId);
  
  const session = await stripe.billingPortal.sessions.create({
    customer: customer.stripe_customer_id,
    return_url: `${APP_URL}/settings/billing`,
  });
  
  return session.url;
}

// Configuration du portal dans Stripe Dashboard:
// - Autoriser upgrade/downgrade
// - Autoriser annulation
// - Autoriser mise à jour paiement
// - Historique des factures
```

---

## 5. GESTION DU LIFECYCLE ABONNEMENT

### 5.1 États de l'Abonnement

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  ┌─────────┐     ┌─────────┐     ┌─────────┐              │
│  │TRIALING │────▶│ ACTIVE  │────▶│CANCELED │              │
│  └─────────┘     └─────────┘     └─────────┘              │
│       │               │               │                    │
│       │               ▼               │                    │
│       │         ┌─────────┐          │                    │
│       └────────▶│PAST_DUE │──────────┘                    │
│                 └─────────┘                                │
│                      │                                     │
│                      ▼                                     │
│                 ┌─────────┐                                │
│                 │UNPAID   │                                │
│                 └─────────┘                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 Transitions d'État

```typescript
const SUBSCRIPTION_TRANSITIONS = {
  trialing: {
    on_trial_end: 'active',      // Si paiement OK
    on_payment_failed: 'past_due',
    on_cancel: 'canceled',
  },
  active: {
    on_payment_failed: 'past_due',
    on_cancel: 'canceled',
  },
  past_due: {
    on_payment_success: 'active',
    on_max_retries: 'unpaid',
    on_cancel: 'canceled',
  },
  unpaid: {
    on_payment_success: 'active',
    on_grace_period_end: 'canceled',
  },
  canceled: {
    on_resubscribe: 'active',
  },
};
```

### 5.3 Actions par État

```typescript
const STATE_ACTIONS = {
  trialing: {
    access: 'full',
    limits: 'trial_limits',
    notifications: ['trial_ending_soon'],
  },
  active: {
    access: 'full',
    limits: 'plan_limits',
    notifications: [],
  },
  past_due: {
    access: 'full',           // Continue l'accès pendant 7 jours
    limits: 'plan_limits',
    notifications: ['payment_failed', 'update_payment'],
    grace_period_days: 7,
  },
  unpaid: {
    access: 'read_only',      // Peut voir mais pas créer
    limits: 'none',
    notifications: ['account_suspended'],
    grace_period_days: 14,
  },
  canceled: {
    access: 'export_only',    // Peut exporter ses données
    limits: 'none',
    data_retention_days: 30,
  },
};
```

### 5.4 Upgrade / Downgrade

```typescript
// Upgrade immédiat avec prorata
async function upgradeSubscription(
  organizationId: string,
  newPriceId: string
) {
  const subscription = await getSubscription(organizationId);
  
  await stripe.subscriptions.update(subscription.stripe_subscription_id, {
    items: [{
      id: subscription.items[0].id,
      price: newPriceId,
    }],
    proration_behavior: 'create_prorations',  // Facture la différence
  });
  
  // Mettre à jour les limites immédiatement
  await updateOrganizationLimits(organizationId, newPriceId);
}

// Downgrade à la fin de la période
async function downgradeSubscription(
  organizationId: string,
  newPriceId: string
) {
  const subscription = await getSubscription(organizationId);
  
  await stripe.subscriptions.update(subscription.stripe_subscription_id, {
    items: [{
      id: subscription.items[0].id,
      price: newPriceId,
    }],
    proration_behavior: 'none',  // Pas de remboursement
    billing_cycle_anchor: 'unchanged',  // Change au prochain cycle
  });
  
  // Programmer le changement de limites
  await scheduleLimit Change(organizationId, newPriceId, subscription.current_period_end);
}
```

### 5.5 Cancellation Flow

```typescript
async function cancelSubscription(
  organizationId: string,
  reason: string,
  feedback?: string
) {
  const subscription = await getSubscription(organizationId);
  
  // 1. Annuler à la fin de la période (pas immédiatement)
  await stripe.subscriptions.update(subscription.stripe_subscription_id, {
    cancel_at_period_end: true,
  });
  
  // 2. Logger la raison
  await logCancellation(organizationId, reason, feedback);
  
  // 3. Déclencher séquence win-back
  await triggerWinBackSequence(organizationId);
  
  // 4. Notification
  await sendEmail(organizationId, 'subscription_canceled', {
    end_date: subscription.current_period_end,
    export_link: generateExportLink(organizationId),
  });
}
```

---

## 6. DUNNING & RECOVERY

### 6.1 Stratégie de Dunning

```
OBJECTIF: Récupérer 60%+ des paiements échoués

┌─────────────────────────────────────────────────────────────┐
│ TIMELINE DUNNING                                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ J0   Paiement échoué                                       │
│      → Email automatique "Paiement échoué"                 │
│      → Retry automatique Stripe                            │
│                                                             │
│ J1   1er retry Stripe (automatique)                        │
│                                                             │
│ J3   2ème retry + Email "Action requise"                   │
│      → Lien direct mise à jour carte                       │
│                                                             │
│ J5   3ème retry + Email "Compte à risque"                  │
│      → Warning in-app                                      │
│                                                             │
│ J7   Passage en "past_due"                                 │
│      → Email CEO/Owner                                     │
│      → Accès maintenu mais warning permanent               │
│                                                             │
│ J10  Email "Dernière chance"                               │
│      → Offre: -20% si régularisation dans 48h              │
│                                                             │
│ J14  Passage en "unpaid"                                   │
│      → Accès read-only                                     │
│      → Email suspension                                    │
│                                                             │
│ J21  Dernier email avant suppression                       │
│      → Export données disponible                           │
│                                                             │
│ J30  Annulation définitive                                 │
│      → Données conservées 30j supplémentaires              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 Templates Emails Dunning

#### Email J0 : Paiement échoué

```
Sujet: ⚠️ Votre paiement Vectra a échoué

---

Bonjour {first_name},

Nous n'avons pas pu débiter votre carte pour votre 
abonnement Vectra ({plan_name} - {amount}€).

Raison probable : {failure_reason}

→ Mettre à jour ma carte
  {update_payment_link}

Votre accès reste actif. Nous réessaierons automatiquement 
dans 3 jours.

Si vous avez des questions, répondez à cet email.

L'équipe Vectra
```

#### Email J7 : Compte à risque

```
Sujet: 🚨 Action requise : votre compte Vectra

---

Bonjour {first_name},

Malgré plusieurs tentatives, nous n'avons pas pu 
encaisser votre paiement de {amount}€.

⏰ Votre accès sera limité dans 7 jours si le 
   paiement n'est pas régularisé.

Ce qui se passera :
- Vos campagnes seront mises en pause
- Vous ne pourrez plus créer de nouveaux leads
- Vos données resteront accessibles en lecture

→ Régulariser maintenant
  {update_payment_link}

Besoin d'aide ? Contactez-nous : support@vectra.io

L'équipe Vectra
```

#### Email J10 : Dernière chance avec offre

```
Sujet: Offre spéciale : -20% pour régulariser votre compte

---

Bonjour {first_name},

Nous comprenons que des imprévus arrivent.

Pour vous aider à maintenir votre compte actif, 
nous vous offrons 20% de réduction sur votre 
prochain mois si vous régularisez dans les 48h.

Au lieu de {amount}€, vous ne paierez que {discounted_amount}€.

→ Profiter de l'offre
  {special_offer_link}

Cette offre expire le {expiry_date}.

L'équipe Vectra
```

### 6.3 Configuration Stripe Dunning

```javascript
// Configuration via Stripe Dashboard ou API
const dunningConfig = {
  // Retry schedule
  smart_retries: true,  // Stripe choisit le meilleur moment
  
  // Ou custom schedule
  retry_schedule: [
    { days_after_failure: 1 },
    { days_after_failure: 3 },
    { days_after_failure: 5 },
  ],
  
  // Emails Stripe (en plus des nôtres)
  send_invoice_emails: true,
  
  // Quand marquer comme impayé
  days_until_due: 7,
};
```

### 6.4 Métriques Dunning

| Métrique | Définition | Cible |
|----------|------------|-------|
| Recovery Rate | % paiements récupérés | > 60% |
| Voluntary Churn | Annulations volontaires | < 3% |
| Involuntary Churn | Churn paiement échoué | < 1% |
| Time to Recovery | Jours moyen pour récupérer | < 5 jours |

---

## 7. MÉTRIQUES REVENUE

### 7.1 Dashboard Revenue

```
┌─────────────────────────────────────────────────────────────┐
│ REVENUE DASHBOARD                                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  MRR          │  ARR          │  Customers    │  ARPU       │
│  €24,500      │  €294,000     │  89           │  €275       │
│  +12.5% ▲     │               │  +8 ce mois   │  +€15 ▲     │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  MRR BREAKDOWN                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ New MRR         ████████████           €3,200       │   │
│  │ Expansion MRR   ██████                 €1,500       │   │
│  │ Contraction     ██                     -€400        │   │
│  │ Churned MRR     ███                    -€800        │   │
│  │ ─────────────────────────────────────────────────   │   │
│  │ Net New MRR                            €3,500       │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  PLAN DISTRIBUTION                                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Starter (99€)   ████████████████████   45 (51%)     │   │
│  │ Growth (299€)   ████████████           32 (36%)     │   │
│  │ Scale (799€)    █████                  12 (13%)     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  REVENUE BY PLAN                                            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Starter         ████████               €4,455 (18%) │   │
│  │ Growth          ████████████████       €9,568 (39%) │   │
│  │ Scale           ████████████████████   €9,588 (43%) │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 7.2 KPIs à Suivre

```typescript
interface RevenueMetrics {
  // MRR Metrics
  mrr: number;
  mrr_new: number;
  mrr_expansion: number;
  mrr_contraction: number;
  mrr_churned: number;
  mrr_net_new: number;
  mrr_growth_rate: number;
  
  // ARR
  arr: number;
  
  // Customer Metrics
  total_customers: number;
  new_customers: number;
  churned_customers: number;
  
  // Unit Economics
  arpu: number;  // Average Revenue Per User
  ltv: number;   // Lifetime Value
  cac: number;   // Customer Acquisition Cost
  ltv_cac_ratio: number;
  
  // Churn
  gross_churn_rate: number;
  net_churn_rate: number;
  revenue_churn_rate: number;
  
  // Expansion
  expansion_rate: number;
  nrr: number;  // Net Revenue Retention
}
```

### 7.3 Calculs

```typescript
// MRR
const mrr = subscriptions
  .filter(s => s.status === 'active')
  .reduce((sum, s) => sum + s.monthly_amount, 0);

// Net New MRR
const netNewMRR = newMRR + expansionMRR - contractionMRR - churnedMRR;

// ARPU (Average Revenue Per User)
const arpu = mrr / activeCustomers;

// LTV (Lifetime Value)
const avgLifetimeMonths = 1 / monthlyChurnRate;
const ltv = arpu * avgLifetimeMonths * grossMargin;

// Net Revenue Retention (NRR)
const nrr = ((startingMRR + expansion - contraction - churn) / startingMRR) * 100;
// Target: > 100% (expansion > churn)

// Quick Ratio (SaaS health)
const quickRatio = (newMRR + expansionMRR) / (contractionMRR + churnedMRR);
// Target: > 4 (excellent), > 2 (bon), < 1 (problème)
```

---

## 8. IMPLÉMENTATION TECHNIQUE

### 8.1 Schema Base de Données

```sql
-- Plans disponibles
CREATE TABLE plans (
    id UUID PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,  -- 'starter', 'growth', 'scale'
    display_name VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- Pricing
    price_monthly INTEGER NOT NULL,  -- En centimes
    price_yearly INTEGER NOT NULL,
    currency VARCHAR(3) DEFAULT 'EUR',
    
    -- Stripe IDs
    stripe_product_id VARCHAR(255),
    stripe_price_monthly_id VARCHAR(255),
    stripe_price_yearly_id VARCHAR(255),
    
    -- Limites
    limits JSONB NOT NULL,
    features JSONB NOT NULL,
    
    -- Status
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Abonnements
CREATE TABLE subscriptions (
    id UUID PRIMARY KEY,
    organization_id UUID UNIQUE REFERENCES organizations(id),
    plan_id UUID REFERENCES plans(id),
    
    -- Stripe
    stripe_customer_id VARCHAR(255),
    stripe_subscription_id VARCHAR(255),
    stripe_price_id VARCHAR(255),
    
    -- Status
    status VARCHAR(50) NOT NULL,
    billing_cycle VARCHAR(20),  -- 'monthly', 'yearly'
    
    -- Période
    current_period_start TIMESTAMP,
    current_period_end TIMESTAMP,
    trial_end TIMESTAMP,
    
    -- Annulation
    cancel_at_period_end BOOLEAN DEFAULT false,
    canceled_at TIMESTAMP,
    cancellation_reason TEXT,
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Factures
CREATE TABLE invoices (
    id UUID PRIMARY KEY,
    organization_id UUID REFERENCES organizations(id),
    subscription_id UUID REFERENCES subscriptions(id),
    stripe_invoice_id VARCHAR(255) UNIQUE,
    
    -- Montants
    amount_due INTEGER NOT NULL,
    amount_paid INTEGER,
    currency VARCHAR(3) DEFAULT 'EUR',
    
    -- Status
    status VARCHAR(50) NOT NULL,  -- 'draft', 'open', 'paid', 'void', 'uncollectible'
    
    -- Dates
    due_date TIMESTAMP,
    paid_at TIMESTAMP,
    
    -- PDF
    invoice_pdf_url TEXT,
    
    created_at TIMESTAMP DEFAULT NOW()
);

-- Usage mensuel
CREATE TABLE usage_records (
    id UUID PRIMARY KEY,
    organization_id UUID REFERENCES organizations(id),
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    
    -- Compteurs
    leads_used INTEGER DEFAULT 0,
    emails_sent INTEGER DEFAULT 0,
    api_calls INTEGER DEFAULT 0,
    
    -- Limites du plan
    leads_limit INTEGER,
    emails_limit INTEGER,
    
    UNIQUE(organization_id, period_start)
);
```

### 8.2 API Endpoints Billing

```
# Plans
GET  /api/v1/plans                    # Liste des plans
GET  /api/v1/plans/:id                # Détail d'un plan

# Subscription
GET  /api/v1/subscription             # Abonnement actuel
POST /api/v1/subscription/checkout    # Créer session checkout
POST /api/v1/subscription/upgrade     # Upgrade plan
POST /api/v1/subscription/downgrade   # Downgrade plan
POST /api/v1/subscription/cancel      # Annuler
POST /api/v1/subscription/reactivate  # Réactiver

# Billing Portal
POST /api/v1/billing/portal           # Lien vers Stripe Portal

# Usage
GET  /api/v1/usage                    # Usage actuel
GET  /api/v1/usage/history            # Historique

# Invoices
GET  /api/v1/invoices                 # Liste des factures
GET  /api/v1/invoices/:id             # Détail + PDF

# Webhooks (internal)
POST /api/webhooks/stripe             # Webhook Stripe
```

### 8.3 Middleware de Vérification

```typescript
// middleware/subscription.ts
export async function requireActiveSubscription(
  req: Request,
  res: Response,
  next: NextFunction
) {
  const organization = req.organization;
  const subscription = await getSubscription(organization.id);
  
  if (!subscription) {
    return res.status(402).json({
      error: 'subscription_required',
      message: 'An active subscription is required',
      upgrade_url: '/settings/billing',
    });
  }
  
  if (subscription.status === 'unpaid') {
    return res.status(402).json({
      error: 'subscription_unpaid',
      message: 'Please update your payment method',
      update_url: '/settings/billing',
    });
  }
  
  if (subscription.status === 'canceled') {
    return res.status(402).json({
      error: 'subscription_canceled',
      message: 'Your subscription has been canceled',
      reactivate_url: '/settings/billing',
    });
  }
  
  req.subscription = subscription;
  next();
}

// middleware/quota.ts
export async function checkQuota(resource: 'leads' | 'emails' | 'api') {
  return async (req: Request, res: Response, next: NextFunction) => {
    const usage = await getCurrentUsage(req.organization.id);
    const limits = await getPlanLimits(req.subscription.plan_id);
    
    if (usage[resource] >= limits[resource]) {
      return res.status(429).json({
        error: 'quota_exceeded',
        resource,
        used: usage[resource],
        limit: limits[resource],
        upgrade_url: '/settings/billing',
      });
    }
    
    next();
  };
}
```

### 8.4 Composant Pricing Page

```tsx
// components/features/billing/pricing-table.tsx
export function PricingTable({
  currentPlan,
  onSelectPlan,
}: {
  currentPlan?: string;
  onSelectPlan: (planId: string, billingCycle: 'monthly' | 'yearly') => void;
}) {
  const [billingCycle, setBillingCycle] = useState<'monthly' | 'yearly'>('monthly');
  const plans = usePlans();

  return (
    <div className="space-y-8">
      {/* Toggle Monthly/Yearly */}
      <div className="flex justify-center">
        <div className="inline-flex items-center p-1 bg-surface-secondary rounded-lg">
          <button
            className={cn(
              'px-4 py-2 text-sm font-medium rounded-md transition-colors',
              billingCycle === 'monthly'
                ? 'bg-surface-primary text-text-primary shadow'
                : 'text-text-secondary'
            )}
            onClick={() => setBillingCycle('monthly')}
          >
            Mensuel
          </button>
          <button
            className={cn(
              'px-4 py-2 text-sm font-medium rounded-md transition-colors',
              billingCycle === 'yearly'
                ? 'bg-surface-primary text-text-primary shadow'
                : 'text-text-secondary'
            )}
            onClick={() => setBillingCycle('yearly')}
          >
            Annuel
            <Badge variant="success" className="ml-2">-17%</Badge>
          </button>
        </div>
      </div>

      {/* Plans Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {plans.map((plan) => (
          <PlanCard
            key={plan.id}
            plan={plan}
            billingCycle={billingCycle}
            isCurrent={currentPlan === plan.name}
            onSelect={() => onSelectPlan(plan.id, billingCycle)}
          />
        ))}
      </div>
    </div>
  );
}
```

---

## CHECKLIST PRE-LAUNCH BILLING

### Configuration Stripe

- [ ] Compte Stripe créé et vérifié
- [ ] Products créés (Starter, Growth, Scale)
- [ ] Prices créés (monthly + yearly pour chaque)
- [ ] Webhooks configurés
- [ ] Customer Portal activé
- [ ] Dunning settings configurés
- [ ] Tax settings (TVA) configurés

### Backend

- [ ] Tables DB créées
- [ ] Webhook handler implémenté
- [ ] Middleware subscription
- [ ] Middleware quota
- [ ] API endpoints billing

### Frontend

- [ ] Pricing page
- [ ] Checkout flow
- [ ] Settings > Billing page
- [ ] Usage display
- [ ] Upgrade/downgrade modals
- [ ] Payment failed banner

### Tests

- [ ] Test achat subscription
- [ ] Test upgrade
- [ ] Test downgrade
- [ ] Test cancellation
- [ ] Test webhook (toutes les events)
- [ ] Test dunning (mode test)
- [ ] Test quota enforcement

---

**- FIN DU DOCUMENT -**

*Billing & Subscription Spec - Vectra v1.0*
*14 Janvier 2026*
