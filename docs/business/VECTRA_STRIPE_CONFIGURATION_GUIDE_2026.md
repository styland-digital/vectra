# VECTRA
## Guide de Configuration Stripe - Version 2026

*Powering your pipeline, simply.*

---

**Document Technique Détaillé**  
Configuration pas-à-pas pour intégration SaaS B2B  
Date: 02 Février 2026  
Status: Production Ready

---

## TABLE DES MATIÈRES

1. [Prérequis et Informations Essentielles](#1-prérequis-et-informations-essentielles)
2. [Configuration du Dashboard Stripe](#2-configuration-du-dashboard-stripe)
3. [Création des Produits et Prix](#3-création-des-produits-et-prix)
4. [Configuration des Webhooks](#4-configuration-des-webhooks)
5. [Configuration du Customer Portal](#5-configuration-du-customer-portal)
6. [Intégration Next.js - Code](#6-intégration-nextjs---code)
7. [Variables d'Environnement](#7-variables-denvironnement)
8. [Test et Validation](#8-test-et-validation)
9. [Passage en Production](#9-passage-en-production)
10. [Checklist Finale](#10-checklist-finale)

---

## 1. PRÉREQUIS ET INFORMATIONS ESSENTIELLES

### 1.1 Ce dont vous avez besoin

- ✓ Un compte Stripe actif (déjà créé)
- ✓ Accès au Dashboard Stripe
- ✓ Projet Next.js 14+ configuré
- ✓ Stripe CLI installé (pour tests locaux)

### 1.2 Structure Tarifaire Vectra

Basée sur le cahier des charges:

| Plan | Prix Mensuel | Prix Annuel | Commission |
|------|--------------|-------------|------------|
| **Starter** | €2,000/mois | €20,000/an | 8% du pipeline |
| **Growth** | €5,000/mois | €50,000/an | 10% du pipeline |
| **Scale** | Sur devis | Sur devis | 12% du pipeline |

### 1.3 URLs à Configurer

```
Success URL:           https://app.vectra.io/billing/success
Cancel URL:            https://app.vectra.io/billing/cancel
Webhook URL (prod):    https://app.vectra.io/api/webhooks/stripe
Customer Portal Return: https://app.vectra.io/settings/billing
```

---

## 2. CONFIGURATION DU DASHBOARD STRIPE

### 2.1 Accès au Dashboard

**ÉTAPE 1: Connexion**

→ Ouvrir votre navigateur  
→ Aller sur: `https://dashboard.stripe.com`  
→ Se connecter avec vos identifiants

> ⚠️ **ATTENTION:** Vérifiez que vous êtes en **MODE TEST** (bandeau orange en haut). Ne jamais configurer directement en production.

### 2.2 Configuration des Informations Business

**ÉTAPE 2: Paramètres du compte**

Cliquer: **"Settings"** (roue dentée en haut à droite)  
Cliquer: **"Business settings"**  
Cliquer: **"Public details"**

Remplir les champs:

| Champ | Valeur à saisir |
|-------|-----------------|
| Business name | `Vectra` |
| Statement descriptor | `VECTRA` |
| Shortened descriptor | `VECTRA` |
| Support email | `support@vectra.io` |
| Support phone | `+33 1 XX XX XX XX` |
| Support URL | `https://vectra.io/support` |

Cliquer: **"Save"**

### 2.3 Configuration du Branding

**ÉTAPE 3: Branding**

Cliquer: **"Settings"**  
Cliquer: **"Branding"**

| Élément | Valeur |
|---------|--------|
| Icon | Logo Vectra (512x512px, PNG) |
| Logo | Logo Vectra horizontal (PNG) |
| Brand color | `#2E5BFF` |
| Accent color | `#FF9F43` |

Cliquer: **"Save"**

> 📌 **NOTE:** Le branding s'applique à Checkout, Customer Portal et emails.

---

## 3. CRÉATION DES PRODUITS ET PRIX

### 3.1 Accès au Catalogue

**ÉTAPE 1: Navigation**

Cliquer: **"More"** (sidebar gauche)  
Cliquer: **"Product catalog"**  
Cliquer: **"+Add product"**

### 3.2 Produit 1: Plan Starter

**ÉTAPE 2: Créer le produit Starter**

| Champ | Valeur |
|-------|--------|
| Name | `Vectra Starter` |
| Description | `Plan idéal pour les équipes commerciales de 5-15 personnes. Inclut: 300 leads/mois, qualification BANT, intégration HubSpot.` |

**Prix mensuel:**

Cliquer: **"Add pricing"**

| Champ | Valeur |
|-------|--------|
| Price | `2000` |
| Currency | `EUR` |
| Type | ✓ **Recurring** |
| Billing period | `Monthly` |

Cliquer: **"Add price"**

**Prix annuel:**

Cliquer: **"Add another price"**

| Champ | Valeur |
|-------|--------|
| Price | `20000` |
| Currency | `EUR` |
| Type | ✓ **Recurring** |
| Billing period | `Yearly` |

Cliquer: **"Save product"**

> 📌 **NOTE:** Notez le Price ID (ex: `price_1Abc...`).

### 3.3 Produit 2: Plan Growth

**ÉTAPE 3: Créer le produit Growth**

Cliquer: **"+Add product"**

| Champ | Valeur |
|-------|--------|
| Name | `Vectra Growth` |
| Description | `Pour les équipes de 15-50 personnes. Inclut: 1000 leads/mois, agent Meeting Scheduler, A/B testing emails, analytics avancés.` |

**Prix mensuel:** `5000` EUR, Monthly  
**Prix annuel:** `50000` EUR, Yearly

Cliquer: **"Save product"**

### 3.4 Produit 3: Plan Scale

**ÉTAPE 4: Créer le produit Scale**

| Champ | Valeur |
|-------|--------|
| Name | `Vectra Scale` |
| Description | `Solution Enterprise sur mesure. Volume illimité, SLA garanti, support dédié, intégrations personnalisées.` |

**Prix indicatif:** `10000` EUR, Monthly

Cliquer: **"Save product"**

### 3.5 Récapitulatif des Price IDs

| Produit | Période | Price ID |
|---------|---------|----------|
| Starter | Mensuel | `price_starter_monthly_xxx` |
| Starter | Annuel | `price_starter_yearly_xxx` |
| Growth | Mensuel | `price_growth_monthly_xxx` |
| Growth | Annuel | `price_growth_yearly_xxx` |
| Scale | Mensuel | `price_scale_monthly_xxx` |

---

## 4. CONFIGURATION DES WEBHOOKS

### 4.1 Pourquoi les Webhooks?

- Paiement réussi → Activer l'abonnement
- Paiement échoué → Notifier le client
- Abonnement annulé → Désactiver l'accès
- Mise à jour → Ajuster les limites

### 4.2 Création du Webhook Endpoint

**ÉTAPE 1: Accéder aux Webhooks**

Cliquer: **"Developers"** (sidebar)  
Cliquer: **"Webhooks"**  
Cliquer: **"Add endpoint"**

**ÉTAPE 2: Configuration**

| Champ | Valeur |
|-------|--------|
| Endpoint URL | `https://app.vectra.io/api/webhooks/stripe` |
| Description | `Vectra Production Webhook` |

Cliquer: **"Select events"**

### 4.3 Événements requis (cocher)

| Événement | Usage |
|-----------|-------|
| `checkout.session.completed` | Nouveau client a payé |
| `customer.subscription.created` | Nouvel abonnement actif |
| `customer.subscription.updated` | Changement de plan |
| `customer.subscription.deleted` | Annulation |
| `invoice.paid` | Facture payée |
| `invoice.payment_failed` | Échec de paiement |
| `customer.updated` | Mise à jour infos client |

Cliquer: **"Add endpoint"**

**ÉTAPE 3: Récupérer le Webhook Secret**

→ Cliquer sur le webhook créé  
Cliquer: **"Reveal signing secret"**  
→ Copier le secret (`whsec_...`)

> ⚠️ **ATTENTION:** Secret CONFIDENTIEL. Utilisez des variables d'environnement.

### 4.4 Test Local avec Stripe CLI

**Installation:**

```bash
# macOS
brew install stripe/stripe-cli/stripe

# Windows (Scoop)
scoop install stripe
```

**Connexion et écoute:**

```bash
stripe login
stripe listen --forward-to localhost:3000/api/webhooks/stripe
```

---

## 5. CONFIGURATION DU CUSTOMER PORTAL

### 5.1 Accès aux paramètres

Cliquer: **"Settings"**  
Cliquer: **"Billing"**  
Cliquer: **"Customer portal"**  
Cliquer: **"Configure portal"**

### 5.2 Features à activer

- ✅ Allow customers to view their invoice history
- ✅ Allow customers to update payment methods
- ✅ Allow customers to update subscriptions
- ✅ Allow customers to cancel subscriptions

### 5.3 Configuration annulation

Dans 'Cancellation':

- ✅ Collect cancellation reason

Raisons à ajouter:
- Too expensive
- Missing features
- Switching to competitor
- No longer needed
- Other

### 5.4 URL de retour

| Champ | Valeur |
|-------|--------|
| Default return URL | `https://app.vectra.io/settings/billing` |

Cliquer: **"Save changes"**

---

## 6. INTÉGRATION NEXT.JS - CODE

### 6.1 Installation

```bash
npm install stripe @stripe/stripe-js
```

### 6.2 lib/stripe.ts

```typescript
import Stripe from 'stripe';
import { loadStripe } from '@stripe/stripe-js';

// Server-side
export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2025-01-28.acacia',
  typescript: true,
});

// Client-side
let stripePromise: Promise<Stripe | null>;

export const getStripe = () => {
  if (!stripePromise) {
    stripePromise = loadStripe(
      process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!
    );
  }
  return stripePromise;
};
```

### 6.3 app/api/stripe/checkout/route.ts

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { stripe } from '@/lib/stripe';

export async function POST(request: NextRequest) {
  try {
    const { priceId, organizationId, userId } = await request.json();

    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      line_items: [{ price: priceId, quantity: 1 }],
      mode: 'subscription',
      success_url: `${process.env.NEXT_PUBLIC_APP_URL}/billing/success?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${process.env.NEXT_PUBLIC_APP_URL}/billing/cancel`,
      metadata: { organizationId, userId },
      subscription_data: {
        metadata: { organizationId, userId },
      },
    });

    return NextResponse.json({ sessionId: session.id, url: session.url });
  } catch (error: any) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
```

### 6.4 app/api/webhooks/stripe/route.ts

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { headers } from 'next/headers';
import Stripe from 'stripe';
import { stripe } from '@/lib/stripe';

export async function POST(request: NextRequest) {
  const body = await request.text();
  const signature = headers().get('stripe-signature')!;

  let event: Stripe.Event;

  try {
    event = stripe.webhooks.constructEvent(
      body,
      signature,
      process.env.STRIPE_WEBHOOK_SECRET!
    );
  } catch (err: any) {
    console.error('Webhook signature verification failed:', err.message);
    return NextResponse.json(
      { error: 'Webhook signature verification failed' },
      { status: 400 }
    );
  }

  switch (event.type) {
    case 'checkout.session.completed':
      const session = event.data.object as Stripe.Checkout.Session;
      await handleCheckoutComplete(session);
      break;

    case 'customer.subscription.updated':
      const subscription = event.data.object as Stripe.Subscription;
      await handleSubscriptionUpdate(subscription);
      break;

    case 'customer.subscription.deleted':
      const deletedSub = event.data.object as Stripe.Subscription;
      await handleSubscriptionCancelled(deletedSub);
      break;

    case 'invoice.payment_failed':
      const invoice = event.data.object as Stripe.Invoice;
      await handlePaymentFailed(invoice);
      break;
  }

  return NextResponse.json({ received: true });
}

async function handleCheckoutComplete(session: Stripe.Checkout.Session) {
  const organizationId = session.metadata?.organizationId;
  // TODO: Activer l'abonnement dans votre DB
  console.log('Checkout completed for org:', organizationId);
}

async function handleSubscriptionUpdate(subscription: Stripe.Subscription) {
  // TODO: Mettre à jour le plan dans votre DB
  console.log('Subscription updated:', subscription.id);
}

async function handleSubscriptionCancelled(subscription: Stripe.Subscription) {
  // TODO: Désactiver l'accès
  console.log('Subscription cancelled:', subscription.id);
}

async function handlePaymentFailed(invoice: Stripe.Invoice) {
  // TODO: Notifier le client
  console.log('Payment failed for invoice:', invoice.id);
}
```

### 6.5 app/api/stripe/portal/route.ts

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { stripe } from '@/lib/stripe';

export async function POST(request: NextRequest) {
  try {
    const { customerId } = await request.json();

    const session = await stripe.billingPortal.sessions.create({
      customer: customerId,
      return_url: `${process.env.NEXT_PUBLIC_APP_URL}/settings/billing`,
    });

    return NextResponse.json({ url: session.url });
  } catch (error: any) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
```

### 6.6 components/SubscribeButton.tsx

```typescript
'use client';

import { useState } from 'react';

interface Props {
  priceId: string;
  organizationId: string;
  userId: string;
  planName: string;
}

export function SubscribeButton({ priceId, organizationId, userId, planName }: Props) {
  const [loading, setLoading] = useState(false);

  const handleSubscribe = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/stripe/checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ priceId, organizationId, userId }),
      });
      const { url } = await response.json();
      if (url) window.location.href = url;
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <button
      onClick={handleSubscribe}
      disabled={loading}
      className="bg-[#2E5BFF] hover:bg-[#4C7DFF] text-white px-6 py-3 rounded-lg"
    >
      {loading ? 'Chargement...' : `Souscrire à ${planName}`}
    </button>
  );
}
```

### 6.7 components/ManageBillingButton.tsx

```typescript
'use client';

import { useState } from 'react';

export function ManageBillingButton({ customerId }: { customerId: string }) {
  const [loading, setLoading] = useState(false);

  const handleClick = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/stripe/portal', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ customerId }),
      });
      const { url } = await response.json();
      if (url) window.location.href = url;
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <button
      onClick={handleClick}
      disabled={loading}
      className="border border-[#2E5BFF] text-[#2E5BFF] hover:bg-[#2E5BFF] hover:text-white px-6 py-3 rounded-lg"
    >
      {loading ? 'Chargement...' : 'Gérer mon abonnement'}
    </button>
  );
}
```

---

## 7. VARIABLES D'ENVIRONNEMENT

### 7.1 .env.local (développement)

```bash
# ===========================================
# STRIPE CONFIGURATION - TEST MODE
# ===========================================

# API Keys (Dashboard > Developers > API Keys)
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_xxxxxxxxxxxxxxxxxxxxxxxx
STRIPE_SECRET_KEY=sk_test_xxxxxxxxxxxxxxxxxxxxxxxx

# Webhook Secret (Dashboard > Webhooks > Endpoint)
STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxxxxxxxxxxxxx

# ===========================================
# APP CONFIGURATION
# ===========================================

NEXT_PUBLIC_APP_URL=http://localhost:3000

# ===========================================
# PRICE IDs (Test Mode)
# ===========================================

STRIPE_PRICE_STARTER_MONTHLY=price_xxxxxxxxxxxxxxxxxxxxxxxx
STRIPE_PRICE_STARTER_YEARLY=price_xxxxxxxxxxxxxxxxxxxxxxxx
STRIPE_PRICE_GROWTH_MONTHLY=price_xxxxxxxxxxxxxxxxxxxxxxxx
STRIPE_PRICE_GROWTH_YEARLY=price_xxxxxxxxxxxxxxxxxxxxxxxx
STRIPE_PRICE_SCALE_MONTHLY=price_xxxxxxxxxxxxxxxxxxxxxxxx
```

### 7.2 Où trouver les clés

| Variable | Source |
|----------|--------|
| `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` | Dashboard > Developers > API Keys |
| `STRIPE_SECRET_KEY` | Dashboard > Developers > API Keys |
| `STRIPE_WEBHOOK_SECRET` | Dashboard > Webhooks > Endpoint |

> ⚠️ **ATTENTION:** La Secret Key ne s'affiche qu'une fois. Copiez-la immédiatement.

> 📌 **NOTE:** `NEXT_PUBLIC_` expose la variable au navigateur. N'utilisez **JAMAIS** ce préfixe pour la Secret Key.

---

## 8. TEST ET VALIDATION

### 8.1 Cartes de Test

| Numéro | Résultat | Usage |
|--------|----------|-------|
| `4242 4242 4242 4242` | ✅ Succès | Test standard |
| `4000 0000 0000 0002` | ❌ Refusée | Test échec |
| `4000 0025 0000 3155` | 🔐 3D Secure | Test auth |
| `4000 0000 0000 9995` | 💸 Fonds insuffisants | Test erreur |

Pour toutes:
- Date: N'importe quelle date future (ex: `12/34`)
- CVC: N'importe quel code 3 chiffres (ex: `123`)
- Code postal: N'importe quel code (ex: `75001`)

### 8.2 Checklist de Test

1. ☐ Créer un abonnement Starter mensuel
2. ☐ Vérifier webhook `checkout.session.completed`
3. ☐ Accéder au Customer Portal
4. ☐ Changer de plan (Starter → Growth)
5. ☐ Annuler l'abonnement
6. ☐ Tester un paiement échoué
7. ☐ Vérifier les emails automatiques

### 8.3 Test Webhooks Local

```bash
# Terminal 1: App
npm run dev

# Terminal 2: Webhooks
stripe listen --forward-to localhost:3000/api/webhooks/stripe

# Terminal 3: Trigger event
stripe trigger checkout.session.completed
```

---

## 9. PASSAGE EN PRODUCTION

### 9.1 Activer le Mode Live

**ÉTAPE 1: Vérification**

Cliquer: **"Settings"**  
Cliquer: **"Business settings"**  
→ Compléter toutes les informations  
→ Vérifier l'identité (si demandé)  
→ Ajouter un compte bancaire

**ÉTAPE 2: Basculer**

→ En haut du Dashboard: **"Test mode"** → **"Live mode"**

> ⚠️ **ATTENTION:** En mode Live, les paiements sont RÉELS.

### 9.2 Migration

**ÉTAPE 3: Copier les produits**

→ Product catalog (mode Test)  
→ Ouvrir chaque produit  
Cliquer: **"Copy to live mode"**

**ÉTAPE 4: Webhook Live**

→ Developers > Webhooks (mode Live)  
Cliquer: **"Add endpoint"**  
→ Mêmes événements qu'en test  
→ Copier le nouveau signing secret

### 9.3 Mise à jour variables

| Variable | Nouvelle valeur |
|----------|-----------------|
| `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` | `pk_live_xxx` |
| `STRIPE_SECRET_KEY` | `sk_live_xxx` |
| `STRIPE_WEBHOOK_SECRET` | `whsec_xxx` (live) |
| Price IDs | `price_xxx` (live) |

---

## 10. CHECKLIST FINALE

### ✅ Dashboard

- [ ] Informations business complétées
- [ ] Branding configuré
- [ ] Produits créés (Starter, Growth, Scale)
- [ ] Prix configurés (mensuel + annuel)
- [ ] Webhook endpoint créé
- [ ] Événements sélectionnés
- [ ] Customer Portal configuré

### ✅ Code

- [ ] Packages installés
- [ ] `lib/stripe.ts` créé
- [ ] API checkout créée
- [ ] API webhook créée
- [ ] API portal créée
- [ ] Variables configurées

### ✅ Tests

- [ ] Paiement réussi
- [ ] Paiement échoué
- [ ] Changement de plan
- [ ] Annulation
- [ ] Webhooks (logs)
- [ ] Customer Portal

### ✅ Production

- [ ] Compte Stripe vérifié
- [ ] Produits copiés Live
- [ ] Webhook Live créé
- [ ] Variables Live
- [ ] Portal Live
- [ ] Premier paiement réel

---

## ANNEXE: Structure de Fichiers

```
vectra/
├── app/
│   ├── api/
│   │   ├── stripe/
│   │   │   ├── checkout/route.ts
│   │   │   └── portal/route.ts
│   │   └── webhooks/
│   │       └── stripe/route.ts
│   ├── billing/
│   │   ├── success/page.tsx
│   │   └── cancel/page.tsx
│   └── settings/billing/page.tsx
├── components/
│   ├── SubscribeButton.tsx
│   └── ManageBillingButton.tsx
├── lib/
│   └── stripe.ts
├── .env.local
└── package.json
```

---

## ANNEXE: Mapping Plans ↔ Prix

```typescript
// lib/stripe-plans.ts

export const STRIPE_PLANS = {
  starter: {
    name: 'Starter',
    monthlyPriceId: process.env.STRIPE_PRICE_STARTER_MONTHLY!,
    yearlyPriceId: process.env.STRIPE_PRICE_STARTER_YEARLY!,
    features: [
      '300 leads/mois',
      'Qualification BANT',
      'Intégration HubSpot',
      'Support email',
    ],
    limits: { leadsPerMonth: 300, campaigns: 3, users: 5 },
  },
  growth: {
    name: 'Growth',
    monthlyPriceId: process.env.STRIPE_PRICE_GROWTH_MONTHLY!,
    yearlyPriceId: process.env.STRIPE_PRICE_GROWTH_YEARLY!,
    features: [
      '1000 leads/mois',
      'Agent Meeting Scheduler',
      'A/B testing emails',
      'Analytics avancés',
      'Support prioritaire',
    ],
    limits: { leadsPerMonth: 1000, campaigns: 10, users: 20 },
  },
  scale: {
    name: 'Scale',
    monthlyPriceId: process.env.STRIPE_PRICE_SCALE_MONTHLY!,
    yearlyPriceId: null,
    features: [
      'Volume illimité',
      'SLA garanti',
      'Support dédié',
      'Intégrations personnalisées',
      'Account manager',
    ],
    limits: { leadsPerMonth: -1, campaigns: -1, users: -1 },
  },
} as const;

export type PlanType = keyof typeof STRIPE_PLANS;

export function getPlanFromPriceId(priceId: string): PlanType | null {
  for (const [planKey, plan] of Object.entries(STRIPE_PLANS)) {
    if (plan.monthlyPriceId === priceId || plan.yearlyPriceId === priceId) {
      return planKey as PlanType;
    }
  }
  return null;
}
```

---

## RÉSUMÉ EXÉCUTIF

| Élément | Action | Temps estimé |
|---------|--------|--------------|
| Dashboard | Business info + branding | 15 min |
| Produits | 3 produits × 2 prix | 20 min |
| Webhooks | 1 endpoint + 7 événements | 10 min |
| Portal | Configuration complète | 15 min |
| Code | 4 fichiers | 30 min |
| Tests | 7 scénarios | 45 min |
| Production | Migration | 30 min |

**Temps total estimé:** 2-3 heures

**Prochaine étape:** Commencer par la section 2.

---

**— FIN DU DOCUMENT —**

**VECTRA**  
*Powering your pipeline, simply.*

Document généré le 02 Février 2026  
Version 2026 - Production Ready
