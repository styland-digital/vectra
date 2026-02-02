# VECTRA - CUSTOMER SUCCESS PLAYBOOK
## Maximiser la Rétention et l'Expansion
### Version 1.0 | 14 Janvier 2026

---

**Document:** DOC-BIZ-004  
**Statut:** ESSENTIEL - LTV MAXIMIZATION  
**Objectif:** NRR > 100%, Churn < 3%  

---

## TABLE DES MATIÈRES

1. Philosophie Customer Success
2. Health Score Framework
3. Segmentation Clients
4. Playbooks par Segment
5. Triggers d'Intervention
6. Processus d'Expansion
7. Prévention du Churn
8. Métriques CS
9. Outils & Automatisation

---

## 1. PHILOSOPHIE CUSTOMER SUCCESS

### 1.1 Principe Fondamental

```
Le Customer Success n'est pas du Support.

Support = Réactif (le client a un problème)
CS = Proactif (on anticipe avant le problème)

Objectif CS : Le client RÉUSSIT avec notre produit
             → Il reste
             → Il paie plus
             → Il recommande
```

### 1.2 Équation de la Rétention

```
RÉTENTION = Valeur Perçue × Engagement × Qualité Relation
            ─────────────────────────────────────────────
                     Effort × Alternatives

Pour maximiser la rétention :
✓ Augmenter la valeur perçue (résultats visibles)
✓ Maximiser l'engagement (usage régulier)
✓ Construire la relation (touchpoints humains)
✗ Réduire l'effort (simplifier)
✗ Réduire les alternatives (lock-in = mauvaise stratégie)
```

### 1.3 Moments de Vérité

Les moments où le client décide de rester ou partir :

| Moment | Timing | Ce qui compte |
|--------|--------|---------------|
| **First Value** | J1-J7 | Voir un résultat concret |
| **First Win** | J7-J30 | Premier RDV qualifié |
| **First Renewal** | M1 | ROI vs attentes |
| **Quarterly Review** | M3, M6, M9 | Progression mesurable |
| **Annual Decision** | M11-M12 | Business case pour renouveler |

---

## 2. HEALTH SCORE FRAMEWORK

### 2.1 Qu'est-ce que le Health Score ?

```
Score 0-100 qui prédit la probabilité qu'un client :
- Churn (score < 40)
- Reste stable (40-70)
- Expand (> 70)

Mis à jour quotidiennement, automatiquement.
```

### 2.2 Composantes du Health Score

```
┌─────────────────────────────────────────────────────────────┐
│ HEALTH SCORE = 100 points                                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ 1. USAGE (30 points)                                        │
│    └─ Logins mensuels (0-10)                               │
│    └─ Features utilisées (0-10)                            │
│    └─ Campagnes actives (0-10)                             │
│                                                             │
│ 2. RÉSULTATS (30 points)                                    │
│    └─ Leads générés vs quota (0-10)                        │
│    └─ Meetings bookés (0-10)                               │
│    └─ Progression MoM (0-10)                               │
│                                                             │
│ 3. ENGAGEMENT (20 points)                                   │
│    └─ Emails ouverts de notre part (0-5)                   │
│    └─ Participation aux calls (0-5)                        │
│    └─ Support tickets résolus (0-5)                        │
│    └─ NPS/Feedback (0-5)                                   │
│                                                             │
│ 4. FINANCIER (20 points)                                    │
│    └─ Paiements à jour (0-10)                              │
│    └─ Plan vs usage (0-5)                                  │
│    └─ Contrat durée restante (0-5)                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2.3 Calcul Détaillé

```typescript
interface HealthScoreComponents {
  usage: {
    logins_monthly: number;        // 0-10: <5=0, 5-10=5, 10-20=8, >20=10
    features_used: number;         // 0-10: <3=0, 3-5=5, 5-8=8, >8=10
    campaigns_active: number;      // 0-10: 0=0, 1=5, 2-3=8, >3=10
  };
  results: {
    leads_vs_quota: number;        // 0-10: <50%=0, 50-80%=5, 80-100%=8, >100%=10
    meetings_booked: number;       // 0-10: 0=0, 1-2=5, 3-5=8, >5=10
    mom_growth: number;            // 0-10: negative=0, 0-10%=5, 10-25%=8, >25%=10
  };
  engagement: {
    emails_opened: number;         // 0-5: 0%=0, 1-25%=2, 25-50%=3, >50%=5
    calls_attended: number;        // 0-5: 0=0, 1=3, 2+=5
    tickets_resolved: number;      // 0-5: pending=-2, resolved=+3, no tickets=5
    nps_score: number;             // 0-5: detractor=-5, passive=0, promoter=5
  };
  financial: {
    payment_status: number;        // 0-10: failed=-5, past_due=0, current=10
    plan_fit: number;              // 0-5: underusing=3, right-sized=5, hitting_limits=4
    contract_remaining: number;    // 0-5: <30d=1, 30-90d=3, >90d=5
  };
}

function calculateHealthScore(c: HealthScoreComponents): number {
  const usage = c.usage.logins_monthly + c.usage.features_used + c.usage.campaigns_active;
  const results = c.results.leads_vs_quota + c.results.meetings_booked + c.results.mom_growth;
  const engagement = c.engagement.emails_opened + c.engagement.calls_attended + 
                     c.engagement.tickets_resolved + c.engagement.nps_score;
  const financial = c.financial.payment_status + c.financial.plan_fit + c.financial.contract_remaining;
  
  return Math.max(0, Math.min(100, usage + results + engagement + financial));
}
```

### 2.4 Interprétation du Score

| Score | Statut | Couleur | Action |
|-------|--------|---------|--------|
| 80-100 | Champion | 🟢 Vert | Expansion, Referral |
| 60-79 | Healthy | 🟢 Vert | Maintenir, Nurture |
| 40-59 | At Risk | 🟡 Jaune | Intervention CS |
| 20-39 | Critical | 🟠 Orange | Escalade Manager |
| 0-19 | Churn Imminent | 🔴 Rouge | Escalade Direction |

---

## 3. SEGMENTATION CLIENTS

### 3.1 Segments par Valeur

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  ENTERPRISE (Scale plan)                     15% clients    │
│  MRR: €799+                                  45% revenue    │
│  Touch: High-touch, CSM dédié                              │
│  Cadence: Weekly calls, QBRs                               │
│                                                             │
│  MID-MARKET (Growth plan)                    35% clients    │
│  MRR: €299-€798                              40% revenue    │
│  Touch: Medium-touch, CSM partagé                          │
│  Cadence: Bi-weekly calls, QBRs                            │
│                                                             │
│  SMB (Starter plan)                          50% clients    │
│  MRR: €99-€298                               15% revenue    │
│  Touch: Tech-touch, automatisé                             │
│  Cadence: Monthly emails, self-serve                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Allocation des Ressources

| Segment | Ratio CSM:Clients | Temps/Client/Mois |
|---------|-------------------|-------------------|
| Enterprise | 1:10 | 8-12h |
| Mid-Market | 1:30 | 2-4h |
| SMB | 1:100 (automatisé) | 30min (si besoin) |

---

## 4. PLAYBOOKS PAR SEGMENT

### 4.1 Playbook Enterprise (High-Touch)

#### Onboarding (J1-J30)

```
J0  │ Welcome call (30min)
    │ → Présentation équipe
    │ → Découverte objectifs business
    │ → Timeline d'implémentation
    │
J1  │ Kick-off technique (1h)
    │ → Configuration compte
    │ → Intégrations CRM
    │ → Formation admin
    │
J3  │ Formation utilisateurs (1h)
    │ → Création première campagne
    │ → Workflow quotidien
    │ → Q&A
    │
J7  │ Check-in (30min)
    │ → Revue premiers résultats
    │ → Ajustements critères
    │ → Blockers?
    │
J14 │ Review (30min)
    │ → Métriques vs objectifs
    │ → Optimisations
    │ → Plan pour J30
    │
J30 │ Success review (1h)
    │ → Bilan premier mois
    │ → ROI démontré
    │ → Plan trimestre
```

#### Ongoing (Monthly)

```
SEMAINE 1 │ Weekly sync (30min)
          │ → Métriques semaine
          │ → Prochaines actions
          │
SEMAINE 2 │ Async check-in (email)
          │ → Progression
          │ → Questions?
          │
SEMAINE 3 │ Weekly sync (30min)
          │ → Deep dive feature
          │ → Best practices
          │
SEMAINE 4 │ Monthly review (1h)
          │ → KPIs du mois
          │ → Planning mois suivant
          │ → Feedback produit
```

#### Quarterly Business Review (QBR)

```
DURÉE: 1h30

AGENDA:
1. Executive Summary (10min)
   - Highlights du trimestre
   - ROI démontré
   
2. Performance Review (20min)
   - Métriques vs objectifs
   - Comparaison trimestre précédent
   - Benchmark industrie
   
3. Success Stories (10min)
   - Best performing campaigns
   - Wins notables
   
4. Challenges & Solutions (15min)
   - Obstacles rencontrés
   - Plan d'action
   
5. Product Roadmap (15min)
   - Features à venir
   - Input client
   
6. Next Quarter Planning (15min)
   - Objectifs Q+1
   - Actions clés
   
7. Q&A (5min)

PARTICIPANTS:
- Côté client: Sponsor exec + User lead
- Côté Vectra: CSM + Account Exec (si expansion)
```

### 4.2 Playbook Mid-Market (Medium-Touch)

#### Onboarding (J1-J14)

```
J0  │ Welcome email automatique
    │ + Calendly pour kick-off call
    │
J1  │ Kick-off call (45min)
    │ → Configuration + formation
    │ → Objectifs
    │
J7  │ Check-in call (20min)
    │ → Premiers résultats
    │ → Questions
    │
J14 │ Success review email
    │ + Loom vidéo personnalisée
    │ → Bilan + prochaines étapes
```

#### Ongoing (Bi-Weekly/Monthly)

```
SEMAINE 1  │ Call bi-weekly (20min)
SEMAINE 2  │ Email async check-in
SEMAINE 3  │ Call bi-weekly (20min)
SEMAINE 4  │ Monthly email report
           │ + QBR simplifié (trimestriel)
```

### 4.3 Playbook SMB (Tech-Touch)

#### Onboarding (Automatisé)

```
J0  │ Welcome email + Checklist interactive
J1  │ Email "Getting started" + vidéos
J3  │ Email si onboarding incomplet
J7  │ Email "Your first week results"
J14 │ Email "Tips for success"
J30 │ Email "Your first month report"
```

#### Ongoing (Automatisé)

```
HEBDO     │ Email digest automatique (si actif)
MENSUEL   │ Performance report email
TRIGGER   │ Email si health score < 50
TRIGGER   │ Email si hitting limits (upsell)
```

---

## 5. TRIGGERS D'INTERVENTION

### 5.1 Triggers Automatiques

```typescript
const INTERVENTION_TRIGGERS = {
  // Usage drops
  'usage_drop_50': {
    condition: 'usage_this_week < usage_last_week * 0.5',
    action: 'send_email_check_in',
    escalate_after: '3_days',
    severity: 'medium',
  },
  
  // No login
  'no_login_7_days': {
    condition: 'last_login > 7_days_ago',
    action: 'send_email_miss_you',
    escalate_after: '3_days',
    severity: 'medium',
  },
  
  'no_login_14_days': {
    condition: 'last_login > 14_days_ago',
    action: 'cs_call_outreach',
    escalate_after: '3_days',
    severity: 'high',
  },
  
  // Results
  'no_meetings_30_days': {
    condition: 'meetings_last_30_days = 0 AND campaigns_active > 0',
    action: 'send_email_optimization_tips',
    escalate_after: '7_days',
    severity: 'medium',
  },
  
  // Health score
  'health_critical': {
    condition: 'health_score < 40',
    action: 'cs_immediate_outreach',
    escalate_after: '1_day',
    severity: 'critical',
  },
  
  // Payment
  'payment_failed': {
    condition: 'payment_status = failed',
    action: 'send_dunning_sequence',
    escalate_after: '3_days',
    severity: 'critical',
  },
  
  // Positive triggers
  'hitting_limits': {
    condition: 'usage > plan_limit * 0.8',
    action: 'send_upsell_email',
    severity: 'opportunity',
  },
  
  'big_win': {
    condition: 'meetings_this_week >= 5',
    action: 'send_congratulations + ask_testimonial',
    severity: 'opportunity',
  },
};
```

### 5.2 Matrice d'Escalade

```
┌─────────────────────────────────────────────────────────────┐
│ NIVEAU 1: CSM                                               │
│ → Usage drop, no login, optimisation                       │
│ → Response time: 24h                                        │
│                                                             │
│ NIVEAU 2: CS Manager                                        │
│ → Health < 40, churn signals, complaints                   │
│ → Response time: 4h                                         │
│                                                             │
│ NIVEAU 3: Head of CS + Account Exec                        │
│ → Health < 20, Enterprise at risk                          │
│ → Response time: 1h                                         │
│                                                             │
│ NIVEAU 4: CEO                                               │
│ → Top 10 clients at risk, PR risk                          │
│ → Response time: immediate                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 6. PROCESSUS D'EXPANSION

### 6.1 Signals d'Expansion

| Signal | Score | Action |
|--------|-------|--------|
| Hitting lead quota > 80% | +20 | Upsell email |
| Users at limit | +15 | Upsell call |
| Requesting features du plan supérieur | +25 | Demo upgrade |
| Multiple positive feedbacks | +10 | Expansion conversation |
| New team members mentioned | +15 | Proactive call |
| Health score > 80 pendant 60j | +30 | Strategic review |

### 6.2 Expansion Playbook

```
PHASE 1: IDENTIFICATION
├─ Signal détecté
├─ Score expansion calculé
└─ Qualification (> 50 points = qualified)

PHASE 2: PRÉPARATION
├─ Analyse usage actuel
├─ Calcul ROI avec upgrade
├─ Identification features désirées
└─ Préparation business case

PHASE 3: CONVERSATION
├─ Scheduling call (CSM)
├─ Discovery: besoins évolutifs?
├─ Présentation options upgrade
└─ Discussion ROI

PHASE 4: PROPOSITION
├─ Custom quote si besoin
├─ Timeline d'upgrade
├─ Incentive si annuel
└─ Simplifier le process

PHASE 5: CLOSE
├─ Signature upgrade
├─ Activation nouvelles features
├─ Formation si nécessaire
└─ Celebration avec client
```

### 6.3 Templates Expansion

#### Email Upsell (Hitting Limits)

```
Sujet: 🚀 {company_name} is growing!

Bonjour {first_name},

Great news - your team has generated {leads_count} leads this month,
which means you're at {usage_percent}% of your current plan.

Based on your growth trajectory, upgrading to {next_plan} would give you:
• {new_limit} leads/month (vs {current_limit})
• {additional_features}
• Priority support

The ROI math:
• Current cost per meeting: €{current_cpm}
• With upgrade: €{new_cpm} (saved: €{savings}/meeting)

Want to discuss? I have 15 minutes Tuesday or Thursday.
→ {calendly_link}

Best,
{csm_name}
```

---

## 7. PRÉVENTION DU CHURN

### 7.1 Early Warning Signals

| Signal | Lag Time | Severity |
|--------|----------|----------|
| Health score drop > 20 points | 30-60 jours | 🟡 |
| No login 14+ jours | 30-45 jours | 🟠 |
| Support tickets négatifs | 30-45 jours | 🟠 |
| Demande export données | 7-14 jours | 🔴 |
| Question sur annulation | 3-7 jours | 🔴 |
| Contact concurrent | 14-30 jours | 🔴 |

### 7.2 Save Playbook

```
NIVEAU 1: PROACTIVE (Health 40-59)
├─ Email check-in personnalisé
├─ Call CSM sous 48h
├─ Identify root cause
└─ Plan d'action 14 jours

NIVEAU 2: RESCUE (Health 20-39)
├─ Call CSM immediate
├─ Escalade CS Manager
├─ Offre: consultation gratuite
├─ Plan de recovery personnalisé
└─ Executive sponsor impliqué

NIVEAU 3: EMERGENCY (Health < 20 ou demande annulation)
├─ Call immediate (dans l'heure)
├─ Escalade Head CS + AE
├─ Discovery approfondie
├─ Options sur table:
│   ├─ Discount temporaire
│   ├─ Pause abonnement
│   ├─ Plan downgrade
│   └─ Services additionnels gratuits
└─ Documentation pour feedback produit
```

### 7.3 Exit Interview

Toujours faire quand un client part :

```
QUESTIONS:
1. Quelle est la principale raison de votre départ?
   □ Prix trop élevé
   □ Pas assez de valeur/résultats
   □ Manque de features
   □ Mauvaise expérience support
   □ Changement interne (budget, équipe)
   □ Choix d'un concurrent
   □ Autre: _____

2. Qu'aurions-nous pu faire différemment?

3. Recommanderiez-vous Vectra malgré tout? (1-10)

4. Y a-t-il une chance de vous revoir dans le futur?

5. Pouvons-nous vous recontacter dans 6 mois?

ACTIONS POST-EXIT:
├─ Logger dans CRM
├─ Partager feedback avec Product
├─ Ajouter à séquence win-back (6 mois)
└─ Analyser pattern si récurrent
```

---

## 8. MÉTRIQUES CS

### 8.1 KPIs Principaux

| Métrique | Définition | Cible |
|----------|------------|-------|
| **NRR** | Net Revenue Retention | > 105% |
| **Gross Churn** | MRR perdu / MRR début | < 3% mensuel |
| **Logo Churn** | Clients perdus / Total | < 5% mensuel |
| **Expansion Rate** | Expansion MRR / MRR début | > 5% mensuel |
| **Time to Value** | Jours jusqu'au 1er meeting | < 14 jours |
| **Health Score Avg** | Moyenne tous clients | > 65 |

### 8.2 Dashboard CS

```
┌──────────────────────────────────────────────────────────┐
│ CUSTOMER SUCCESS DASHBOARD                               │
├──────────────────────────────────────────────────────────┤
│                                                          │
│ HEALTH DISTRIBUTION                                      │
│ ┌──────────────────────────────────────────────────────┐│
│ │ 🟢 Champion (80+)    ████████████       28 (31%)    ││
│ │ 🟢 Healthy (60-79)   ██████████████████ 38 (43%)    ││
│ │ 🟡 At Risk (40-59)   ████████           15 (17%)    ││
│ │ 🟠 Critical (20-39)  ███                 6 (7%)     ││
│ │ 🔴 Churn Risk (<20)  █                   2 (2%)     ││
│ └──────────────────────────────────────────────────────┘│
│                                                          │
│ THIS MONTH                                               │
│ NRR: 108%  │  Churn: 2.1%  │  Expansion: 6.2%          │
│                                                          │
│ ACTIONS NEEDED                                           │
│ ⚠️ 8 clients need intervention today                    │
│ 📞 12 calls scheduled this week                         │
│ 📧 23 check-in emails to send                           │
│                                                          │
│ EXPANSION PIPELINE                                       │
│ €4,200 MRR in qualified expansion opportunities         │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### 8.3 Reporting Cadence

| Report | Audience | Fréquence |
|--------|----------|-----------|
| Health Score Alert | CSM | Real-time |
| Daily Digest | CS Team | Daily |
| CS Dashboard | CS Manager | Daily |
| Churn Analysis | Leadership | Weekly |
| NRR Report | Exec | Monthly |
| Customer Health Review | Board | Quarterly |

---

## 9. OUTILS & AUTOMATISATION

### 9.1 Stack CS Recommandé

| Besoin | Outil | Pourquoi |
|--------|-------|----------|
| CRM + CS Platform | HubSpot Service Hub | All-in-one |
| In-app messaging | Intercom | Onboarding + Support |
| Health Score | Custom (Metabase) | Flexibilité |
| Email automation | Customer.io | Behavioral triggers |
| Call scheduling | Calendly | Self-service |
| Video messaging | Loom | Async communication |
| Feedback | Typeform | NPS, surveys |

### 9.2 Automations Clés

```typescript
// Automation: Onboarding incomplete J3
{
  trigger: 'signup_date = NOW() - 3 days AND onboarding_completed = false',
  action: 'send_email',
  template: 'onboarding_reminder',
  segment: 'all',
}

// Automation: Usage drop
{
  trigger: 'weekly_logins < last_week_logins * 0.5',
  action: 'create_task_for_csm',
  task: 'Check in with {customer_name} - usage dropped 50%',
  priority: 'high',
  segment: ['enterprise', 'mid-market'],
}

// Automation: Hitting limits
{
  trigger: 'leads_used > leads_limit * 0.8',
  action: 'send_email',
  template: 'upsell_hitting_limits',
  segment: 'all',
}

// Automation: Champion program
{
  trigger: 'health_score > 80 AND customer_tenure > 90 days',
  action: 'add_to_list',
  list: 'champion_candidates',
  notify: 'cs_manager',
}

// Automation: Churn prevention
{
  trigger: 'health_score < 40',
  action: 'create_urgent_task',
  task: 'URGENT: {customer_name} health critical - immediate outreach',
  notify: ['csm', 'cs_manager'],
  escalate_after: '24h',
}
```

### 9.3 Schema Base de Données CS

```sql
-- Customer Health History
CREATE TABLE customer_health (
    id UUID PRIMARY KEY,
    organization_id UUID REFERENCES organizations(id),
    score INTEGER NOT NULL,
    components JSONB NOT NULL,
    calculated_at TIMESTAMP DEFAULT NOW()
);

-- CS Activities
CREATE TABLE cs_activities (
    id UUID PRIMARY KEY,
    organization_id UUID REFERENCES organizations(id),
    csm_id UUID REFERENCES users(id),
    activity_type VARCHAR(50),  -- 'call', 'email', 'meeting', 'note'
    description TEXT,
    outcome VARCHAR(50),
    next_action TEXT,
    next_action_date DATE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Expansion Opportunities
CREATE TABLE expansion_opportunities (
    id UUID PRIMARY KEY,
    organization_id UUID REFERENCES organizations(id),
    current_plan VARCHAR(50),
    target_plan VARCHAR(50),
    mrr_increase INTEGER,
    signals JSONB,
    status VARCHAR(50),  -- 'identified', 'qualified', 'proposed', 'won', 'lost'
    created_at TIMESTAMP DEFAULT NOW(),
    closed_at TIMESTAMP
);

-- Churn Risk Log
CREATE TABLE churn_risk_log (
    id UUID PRIMARY KEY,
    organization_id UUID REFERENCES organizations(id),
    risk_level VARCHAR(20),
    signals JSONB,
    intervention_taken TEXT,
    outcome VARCHAR(50),  -- 'saved', 'churned', 'pending'
    created_at TIMESTAMP DEFAULT NOW(),
    resolved_at TIMESTAMP
);
```

---

## CHECKLIST PRE-LAUNCH CS

### Process
- [ ] Health Score défini et calculé
- [ ] Playbooks documentés par segment
- [ ] Templates emails prêts
- [ ] Escalade process défini

### Tools
- [ ] CRM configuré avec health score
- [ ] Email automation setup
- [ ] Calendly pour tous les CSMs
- [ ] Dashboard CS créé

### Team
- [ ] CSM roles définis
- [ ] Training completé
- [ ] Quotas/targets assignés
- [ ] Compensation plan clair

### Metrics
- [ ] NRR tracking
- [ ] Churn tracking
- [ ] Health score monitoring
- [ ] Alertes configurées

---

**- FIN DU DOCUMENT -**

*Customer Success Playbook - Vectra v1.0*
*14 Janvier 2026*
