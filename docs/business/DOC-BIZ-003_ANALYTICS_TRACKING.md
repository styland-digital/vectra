# VECTRA - ANALYTICS & TRACKING PLAN
## Data-Driven Product Development
### Version 1.0 | 14 Janvier 2026

---

**Document:** DOC-BIZ-003  
**Statut:** ESSENTIEL - DECISION MAKING  
**Objectif:** Ne jamais naviguer à l'aveugle  

---

## TABLE DES MATIÈRES

1. Philosophie Analytics
2. Stack Analytics
3. Event Taxonomy
4. Tracking Plan Complet
5. Funnels Critiques
6. Dashboards & Reports
7. Alertes Automatiques
8. Implémentation Technique

---

## 1. PHILOSOPHIE ANALYTICS

### 1.1 Principe Fondamental

```
MESURER pour COMPRENDRE
COMPRENDRE pour AMÉLIORER
AMÉLIORER pour CROÎTRE

Sans data → Opinions
Avec data → Décisions
```

### 1.2 Les 3 Questions Avant Chaque Feature

1. **Comment saurons-nous si ça marche ?** → Métrique de succès
2. **Quel comportement voulons-nous encourager ?** → Events à tracker
3. **Quel est le seuil de succès/échec ?** → Targets

### 1.3 Framework AARRR (Pirate Metrics)

| Niveau | Question | Métriques |
|--------|----------|-----------|
| **Acquisition** | D'où viennent-ils ? | Traffic, Sources, Landing |
| **Activation** | Voient-ils la valeur ? | Onboarding, Time-to-value |
| **Retention** | Reviennent-ils ? | DAU/MAU, Churn |
| **Revenue** | Paient-ils ? | Conversion, ARPU, LTV |
| **Referral** | Recommandent-ils ? | NPS, Viral coefficient |

---

## 2. STACK ANALYTICS

### 2.1 Stack Recommandé (Bootstrap)

| Besoin | Outil | Pricing | Pourquoi |
|--------|-------|---------|----------|
| CDP | **Segment** | Free < 1K MTU | Standard industrie |
| Product Analytics | **PostHog** | Free < 1M events | Open-source, replays |
| BI / Reports | **Metabase** | Free self-hosted | SQL-friendly |
| Error Tracking | **Sentry** | Free < 5K errors | Indispensable |

### 2.2 Architecture

```
Frontend (Segment) ──┬──> PostHog (Product Analytics)
                     ├──> Intercom (Support)
                     └──> Metabase (BI)

Backend ─────────────────> PostgreSQL (Events table)
                            └──> Metabase (Reports)
```

---

## 3. EVENT TAXONOMY

### 3.1 Convention de Nommage

```typescript
// Format: object_action
// ✅ Bon
track('campaign_created', { campaign_id, campaign_name });
track('email_approved', { email_id, time_to_approve });

// ❌ Mauvais
track('user clicked button');  // Trop verbeux
track('create');               // Pas spécifique
```

### 3.2 Catégories

```
ACCOUNT (account_*)     → Lifecycle compte
ONBOARDING (onboarding_*) → Activation
CAMPAIGN (campaign_*)   → Campagnes
LEAD (lead_*)           → Leads
EMAIL (email_*)         → Emails
MEETING (meeting_*)     → RDV
BILLING (billing_*)     → Paiement
```

---

## 4. TRACKING PLAN COMPLET

### 4.1 Account Events

| Event | Trigger | Properties |
|-------|---------|------------|
| `account_created` | Signup | `source`, `referrer`, `utm_*` |
| `account_verified` | Email vérifié | `time_to_verify` |
| `account_upgraded` | Upgrade | `from_plan`, `to_plan`, `mrr_change` |
| `account_downgraded` | Downgrade | `from_plan`, `to_plan` |
| `account_deleted` | Suppression | `reason`, `feedback` |

### 4.2 Onboarding Events

| Event | Trigger | Properties |
|-------|---------|------------|
| `onboarding_started` | Début wizard | `entry_point` |
| `onboarding_step_completed` | Étape faite | `step_number`, `duration_seconds` |
| `onboarding_completed` | Wizard terminé | `total_duration`, `steps_skipped` |
| `onboarding_abandoned` | Abandon | `last_step`, `time_spent` |
| `activation_achieved` | 3 critères | `days_to_activation` |

### 4.3 Campaign Events

| Event | Trigger | Properties |
|-------|---------|------------|
| `campaign_created` | Nouvelle | `campaign_id`, `target_criteria` |
| `campaign_launched` | Lancement | `campaign_id`, `target_leads` |
| `campaign_paused` | Pause | `campaign_id`, `reason` |
| `campaign_completed` | Fin | `total_leads`, `total_meetings`, `roi` |

### 4.4 Lead Events

| Event | Trigger | Properties |
|-------|---------|------------|
| `lead_found` | Trouvé | `lead_id`, `campaign_id`, `source` |
| `lead_enriched` | Enrichi | `lead_id`, `fields_added` |
| `lead_scored` | Score BANT | `bant_score`, `breakdown` |
| `lead_qualified` | Score >= 60 | `bant_score`, `time_to_qualify` |
| `lead_exported` | Export CRM | `destination_crm` |

### 4.5 Email Events

| Event | Trigger | Properties |
|-------|---------|------------|
| `email_generated` | Créé par IA | `email_id`, `generation_time` |
| `email_approved` | Approbation | `time_to_approve`, `was_edited` |
| `email_rejected` | Rejet | `rejection_reason` |
| `email_sent` | Envoyé | `email_id`, `lead_id` |
| `email_opened` | Ouvert | `open_count`, `device` |
| `email_clicked` | Clic | `link_url` |
| `email_replied` | Réponse | `reply_sentiment` |
| `email_bounced` | Bounce | `bounce_type` |

### 4.6 Meeting Events

| Event | Trigger | Properties |
|-------|---------|------------|
| `meeting_scheduled` | Booké | `meeting_id`, `lead_id` |
| `meeting_completed` | Terminé | `duration`, `outcome` |
| `meeting_no_show` | No-show | `follow_up_action` |
| `meeting_canceled` | Annulé | `canceled_by`, `reason` |

### 4.7 Billing Events

| Event | Trigger | Properties |
|-------|---------|------------|
| `checkout_started` | Début | `plan`, `billing_cycle` |
| `checkout_completed` | Succès | `plan`, `amount` |
| `checkout_abandoned` | Abandon | `abandonment_step` |
| `subscription_started` | Début abo | `plan`, `mrr` |
| `subscription_canceled` | Annulation | `reason`, `mrr_lost` |
| `payment_failed` | Échec | `failure_reason` |
| `payment_recovered` | Récupéré | `recovery_attempt` |

### 4.8 Properties Standards

```typescript
// Toujours inclus automatiquement
interface StandardProperties {
  user_id: string;
  organization_id: string;
  plan: 'trial' | 'starter' | 'growth' | 'scale';
  subscription_status: string;
  timestamp: string;
  session_id: string;
  device_type: 'desktop' | 'tablet' | 'mobile';
}
```

---

## 5. FUNNELS CRITIQUES

### 5.1 Funnel Signup → Activated

```
Landing Page Visit     100% (10,000)
        ↓
Signup Started         15% (1,500)
        ↓
Signup Completed       80% (1,200)
        ↓
Onboarding Completed   70% (840)
        ↓
First Campaign         85% (714)
        ↓
Integration Connected  60% (428)
        ↓
Email Approved         80% (343)
        ↓
ACTIVATED              3.4% of visitors, 29% of signups
```

**Cibles:** Signup > 15% | Onboarding > 70% | Activation > 30%

### 5.2 Funnel Campaign → Meeting

```
Campaign Created       100% (100)
        ↓
Leads Found (>10)      95% (95)
        ↓
Leads Qualified (>5)   80% (76)
        ↓
Emails Sent (>3)       90% (68)
        ↓
Emails Opened (>1)     75% (51)
        ↓
Replies (>0)           30% (15)
        ↓
Meeting Booked         60% (9)
        ↓
9% of campaigns → 1+ meeting
```

**Cibles:** Open rate > 35% | Reply rate > 8% | Show rate > 85%

### 5.3 Funnel Trial → Paid

```
Trial Started          100% (1,000)
        ↓
Activated              40% (400)
        ↓
Value Seen (1+ meeting) 30% (120)
        ↓
Pricing Viewed         80% (96)
        ↓
Checkout Started       50% (48)
        ↓
PAID                   75% (36)

3.6% trial-to-paid overall
30% value-seen-to-paid
```

---

## 6. DASHBOARDS & REPORTS

### 6.1 Executive Dashboard (Weekly)

```
┌──────────────────────────────────────────────────────────┐
│ KEY METRICS                                              │
│ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐            │
│ │ €24.5K │ │   89   │ │  42%   │ │  3.2%  │            │
│ │  MRR   │ │Clients │ │Activ.  │ │ Churn  │            │
│ │ +8.2%  │ │  +6    │ │  +3%   │ │ -0.5%  │            │
│ └────────┘ └────────┘ └────────┘ └────────┘            │
│                                                          │
│ FUNNEL: Visitors → Signups → Activated → Paid           │
│         5,234   →  312(6%) →   89(29%) →  12(13%)      │
└──────────────────────────────────────────────────────────┘
```

### 6.2 Product Dashboard (Daily)

```
┌──────────────────────────────────────────────────────────┐
│ DAU: 234 │ 7-day avg: 198 │ Trend: +18%                 │
│                                                          │
│ FEATURE USAGE TODAY                                      │
│ Dashboard viewed    ████████████████████  234            │
│ Campaigns viewed    ████████████████      156            │
│ Leads viewed        ██████████████        134            │
│ Emails approved     ████████               67            │
│ Campaign created    ███                    23            │
│                                                          │
│ ENGAGEMENT: 1 action 40% │ 2-5: 35% │ 6+: 25%          │
└──────────────────────────────────────────────────────────┘
```

### 6.3 Revenue Dashboard (Monthly)

```
┌──────────────────────────────────────────────────────────┐
│ MRR MOVEMENT                                             │
│ Starting MRR           €21,200                           │
│ + New MRR              +€3,800                           │
│ + Expansion            +€1,200                           │
│ - Contraction            -€400                           │
│ - Churned              -€1,300                           │
│ ───────────────────────────────                          │
│ Ending MRR             €24,500                           │
│ Net New MRR            +€3,300 (+15.6%)                  │
│                                                          │
│ RATIOS                                                   │
│ ARPU: €275 │ LTV: €8,250 │ NRR: 104% │ Quick: 2.5      │
└──────────────────────────────────────────────────────────┘
```

### 6.4 Cohort Retention

```
Cohort   │ M0   │ M1   │ M2   │ M3   │ M4   │ M5   │
─────────┼──────┼──────┼──────┼──────┼──────┼──────┤
Sep 2025 │ 100% │ 78%  │ 71%  │ 67%  │ 64%  │ 62%  │
Oct 2025 │ 100% │ 80%  │ 74%  │ 70%  │ 67%  │  --  │
Nov 2025 │ 100% │ 82%  │ 76%  │ 72%  │  --  │  --  │
Dec 2025 │ 100% │ 84%  │ 78%  │  --  │  --  │  --  │
Jan 2026 │ 100% │ 86%  │  --  │  --  │  --  │  --  │

Trend: M1 retention +8% over 5 months ✓
```

---

## 7. ALERTES AUTOMATIQUES

### 7.1 Alertes Critiques (Immediate)

| Alerte | Condition | Action |
|--------|-----------|--------|
| 🔴 Signup spike | > 2x moyenne | Vérifier source |
| 🔴 Signup drop | < 50% moyenne | Check landing |
| 🔴 Payment failures | > 5 en 1h | Vérifier Stripe |
| 🔴 Error rate | > 1% requests | Investigate |
| 🔴 Agent down | No response 5min | Restart |

### 7.2 Alertes Business (Daily)

| Alerte | Condition | Priority |
|--------|-----------|----------|
| 🟠 Activation drop | < 30% semaine | High |
| 🟠 Churn spike | > 5% mois | High |
| 🟠 Open rate low | < 30% 7j | Medium |
| 🟠 No-show high | > 20% semaine | Medium |

### 7.3 Alertes Customer (Per-Account)

| Alerte | Condition | Action |
|--------|-----------|--------|
| At-risk | No login 14j | CS outreach |
| Power user | > 2x average | Upsell |
| Expansion | Hitting limits | Upgrade nudge |
| Churn signal | -30% usage | Retention call |

---

## 8. IMPLÉMENTATION TECHNIQUE

### 8.1 Client (Frontend)

```typescript
// lib/analytics.ts
import { AnalyticsBrowser } from '@segment/analytics-next';

let analytics: Analytics;

export async function initAnalytics() {
  const [response] = await AnalyticsBrowser.load({
    writeKey: process.env.NEXT_PUBLIC_SEGMENT_WRITE_KEY!,
  });
  analytics = response;
}

export function identify(userId: string, traits: Record<string, any>) {
  analytics?.identify(userId, traits);
}

export function track(event: string, properties?: Record<string, any>) {
  analytics?.track(event, {
    ...properties,
    timestamp: new Date().toISOString(),
  });
}

export function page(name?: string) {
  analytics?.page(name);
}
```

### 8.2 Hook React

```typescript
// hooks/use-track.ts
import { useCallback } from 'react';
import { track } from '@/lib/analytics';

export function useTrack() {
  return useCallback((event: string, properties?: Record<string, any>) => {
    track(event, properties);
  }, []);
}

// Usage
function CampaignButton() {
  const track = useTrack();
  
  const handleClick = () => {
    track('campaign_create_clicked', { source: 'dashboard' });
  };
  
  return <Button onClick={handleClick}>Create</Button>;
}
```

### 8.3 Backend (Python)

```python
# analytics/tracker.py
import segment.analytics as analytics

analytics.write_key = os.environ['SEGMENT_WRITE_KEY']

def track(user_id: str, event: str, properties: dict = None):
    analytics.track(
        user_id=user_id,
        event=event,
        properties=properties or {}
    )

# Usage
@router.post("/campaigns")
async def create_campaign(data: CampaignCreate, user: User):
    campaign = await service.create(data)
    
    track(str(user.id), 'campaign_created', {
        'campaign_id': str(campaign.id),
        'campaign_name': campaign.name,
    })
    
    return campaign
```

### 8.4 Schema PostgreSQL

```sql
CREATE TABLE analytics_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID,
    organization_id UUID,
    event_name VARCHAR(255) NOT NULL,
    properties JSONB DEFAULT '{}',
    timestamp TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_events_user ON analytics_events(user_id, timestamp DESC);
CREATE INDEX idx_events_name ON analytics_events(event_name, timestamp DESC);
```

### 8.5 Queries Utiles

```sql
-- Activation funnel 30 jours
SELECT 
    'signup' as step, COUNT(DISTINCT user_id) as users
FROM analytics_events WHERE event_name = 'account_created' 
    AND timestamp > NOW() - INTERVAL '30 days'
UNION ALL
SELECT 'onboarding', COUNT(DISTINCT user_id)
FROM analytics_events WHERE event_name = 'onboarding_completed'
    AND timestamp > NOW() - INTERVAL '30 days'
UNION ALL
SELECT 'activated', COUNT(DISTINCT user_id)
FROM analytics_events WHERE event_name = 'activation_achieved'
    AND timestamp > NOW() - INTERVAL '30 days';

-- DAU 30 jours
SELECT DATE(timestamp) as date, COUNT(DISTINCT user_id) as dau
FROM analytics_events
WHERE timestamp > NOW() - INTERVAL '30 days'
GROUP BY DATE(timestamp)
ORDER BY date;

-- Feature adoption
SELECT 
    event_name,
    COUNT(DISTINCT user_id) as users,
    COUNT(*) as total_uses
FROM analytics_events
WHERE event_name IN ('campaign_created', 'email_approved', 'lead_exported')
    AND timestamp > NOW() - INTERVAL '30 days'
GROUP BY event_name
ORDER BY users DESC;
```

---

## CHECKLIST PRE-LAUNCH

### Setup
- [ ] Segment account créé
- [ ] PostHog configuré
- [ ] Alertes Slack configurées

### Frontend
- [ ] Analytics initialisé
- [ ] Identify au login
- [ ] Events clés trackés
- [ ] Page views automatiques

### Backend
- [ ] Events serveur trackés
- [ ] Table events créée

### Dashboards
- [ ] Executive dashboard
- [ ] Product dashboard
- [ ] Alertes testées

---

**- FIN DU DOCUMENT -**

*Analytics & Tracking Plan - Vectra v1.0*
*14 Janvier 2026*
