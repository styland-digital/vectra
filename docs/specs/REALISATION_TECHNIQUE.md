# RÉALISATION TECHNIQUE + DESIGN UX + MVP SCOPE

## Transformation de la Théorie en Réalité

### 06 Janvier 2026 - Implementation Blueprint Finale

---

## PARTIE 1: RÉALISATION TECHNIQUE

### Vision Simplifiée: 3 Blocs Fonctionnels

---

### BLOC 1: LE MOTEUR DE PROSPECT (Agent Prospector)

**Quoi**: Cherche les leads en permanence
**D'où**: Internet (RocketReach, LinkedIn)
**Comment**: Par créneau horaire (ex: 100 prospects/jour)
**Exécution**: ASYNCHRONE (toujours en arrière-plan)
**Résultat**: Liste de "prospects possibles" classée

**Responsabilités précises:**

1. Chercher les prospects (métiers ciblés + géo + taille)
2. Enrichir les données (emails, tél, entreprise)
3. Vérifier doublons (pas 2x la même personne)
4. Ranger par priorité (firmographique + démographique)
5. Transmettre au bloc suivant

**Ce qu'on NE fait PAS:**

- Contacter directement
- Décider s'il faut contacter
- Persister en base de données

**Où l'humain intervient:**

- Sélection des critères de recherche (config au début)
- Consultation du résultat (dashboard en temps réel)
- Lancer/arrêter manuellement

---

### BLOC 2: LE QUALIFIEUR (Agent BANT)

**Quoi**: Dit "oui" ou "non" pour contacter
**Quand**: Dès qu'on a un prospect
**Comment**: Évalue BANT (Budget, Authority, Need, Timeline)
**Exécution**: SYNCHRONE (réponse en <30 sec par prospect)
**Résultat**: "Oui, on le contacte" ou "Non, pas bon"

**Responsabilités précises:**

1. Analyser le profil LinkedIn (si disponible)
2. Vérifier BANT:
   - BUDGET: Taille entreprise > 50 personnes?
   - AUTHORITY: Manager/VP ou j'ai la bonne personne?
   - NEED: Indices entreprise (ex: croissance)
   - TIMELINE: Activité récente (post, website update)?
3. Donner un score 0-100
4. Décider: Contacter si score > 60
5. Créer "tâche de contact"

**Ce qu'on NE fait PAS:**

- Contacter directement
- Sauvegarder le lead (juste la tâche)
- Faire 2 fois le même prospect

**Où l'humain intervient:**

- Définir le seuil (60? 70?)
- Revoir des cas douteux (manuel)
- Ajuster les critères BANT en temps réel

---

### BLOC 3: LE CONTACTEUR (Agent Meeting Scheduler)

**Quoi**: Envoie un message et fixe un appel
**Quand**: Si le qualifieur dit oui (score > 60)
**Comment**: Email personnalisé + invitation Calendly
**Exécution**: ASYNCHRONE (envoie puis attend)
**Résultat**: Email envoyé + lien de réservation disponible

**Responsabilités précises:**

1. Générer email personnalisé (sujet + corps):
   - Contexte personnel (entreprise, rôle, activité)
   - Value prop claire en 1 ligne
   - CTA: "30 min demo mercredi?"
2. Envoyer via SendGrid
3. Créer le lien Calendly (pré-rempli)
4. Logger l'envoi (timestamp, email, sujet)
5. Attendre la réponse

**Ce qu'on NE fait PAS:**

- Relancer (c'est l'humain qui décide)
- Modifier email si réponse
- Mapper manuellement les dispo (Calendly auto)

**Où l'humain intervient:**

- Valider l'email avant envoi (jour 1)
- Relancer manuellement si pas réponse
- Confirmer les RDVs (validation finale)
- Suivre les conversations (sales rep)

---

## FLOW COMPLET: J1 À J30

### J1 (Setup)

- [ ] User logged in, crée sa 1ère "campaign"
- [ ] Define search criteria (job titles, industries, geo, company size)
- [ ] Set meeting preferences (available time slots)
- [ ] Review + approve email template
- [ ] Human valide: "c'est bon, lance"

### J2-J4 (Prospecting)

- [ ] Agent Prospector: Lance
- [ ] Cherche 300 prospects (100/jour)
- [ ] Enrichit avec RocketReach
- [ ] Dashboard montre: "102 prospects trouvés, enrichissement en cours"
- [ ] Human consulte: "OK, ils valent quelque chose ceux-là?"

### J5-J7 (Qualification)

- [ ] Agent BANT: Commence
- [ ] Évalue les 102 prospects
- [ ] Score: "45 sont bons (score > 60)"
- [ ] Human voit: "45 leads prêts à contacter"
- [ ] Peut ajuster seuil si trop/trop peu

### J8-J30 (Outreach)

- [ ] Agent Contacteur: Envoie
- [ ] 1 email/jour par prospect (pacing)
- [ ] Chaque jour: 1-5 emails envoyés
- [ ] Human voit en dashboard:
  - Emails envoyés: 35
  - Ouvertures: 12 (34%)
  - Clics Calendly: 8 (23%)
  - RDVs confirmés: 3
- [ ] Human: "Good, 3 demos cette semaine"
- [ ] Dans les autres outils CRM/calendar (sync automatisée)

---

## SYNCHRONE vs ASYNCHRONE

| Synchrone (<1 sec) | Asynchrone (minutes/heures) |
|--------------------|----------------------------|
| BANT qualification | Prospect search (RocketReach) |
| Lead deduplication | Email enrichment |
| Dashboard metrics | Email sending (rate-limited) |
| Email personalization (basic) | Follow-up sequencing |
| | Report generation |

---

## PARTIE 2: DESIGN UI/UX

### Les 4 Écrans du MVP

#### ÉCRAN 1: DASHBOARD

- **Metrics bar**: Prospects found | Qualified (>60) | Emails sent | Responses
- **3 Cards**: Status, Quick Actions, Engagement Stats
- **User time**: 30 sec (check status)

#### ÉCRAN 2: CAMPAIGN SETUP (5 steps)

- Step 1: Name + Sector
- Step 2: Target Profile (director/VP/manager + size + geo)
- Step 3: Email Template Review (MUST approve)
- Step 4: Meeting Availability (days + times)
- Step 5: Review & Launch
- **User time**: 5 min (first time)

#### ÉCRAN 3: EMAIL REVIEW (day 8+)

- Agent drafted 10 emails
- User: Approve / Reject / Edit each
- **User time**: 2 min per 10 emails

#### ÉCRAN 4: PERFORMANCE TRACKER (daily)

- **Metrics**: Prospects found, qualified, sent, opens, clicks, meetings
- **Graphs**: Email volume, engagement rate, meetings booked
- **User time**: 1-2 min daily

---

### User Journey: J1 to J30

| Jour | Action |
|------|--------|
| J1 | Login → Create Campaign → Setup (5 min) → Launch |
| J2-4 | Check dashboard daily (prospects found) |
| J5-7 | Check dashboard (BANT scoring done) |
| J8 | Review emails (2 min) → Approve |
| J9-30 | Track metrics daily (opens, clicks, meetings) |

---

### Automated vs Manual

| Agent Does | Human Does |
|------------|------------|
| Find prospects | Define search criteria |
| Enrich data | Set meeting availability |
| Score BANT | Approve email template (day 1) |
| Draft emails | Approve individual emails (day 8+) |
| Send emails (rate-limited) | Manual follow-ups |
| Track metrics | CRM sync |
| | Take meetings |

---

## PARTIE 3: MVP SCOPE FINAL

### MUST HAVE (V1 go-live)

- [ ] Login / Auth (basic email pass)
- [ ] Create campaign (UI step 1-5)
- [ ] Prospect search (RocketReach API)
- [ ] BANT scoring (sync)
- [ ] Email draft generation (Llama 2)
- [ ] Email approval flow
- [ ] Email sending (SendGrid)
- [ ] Calendly integration
- [ ] Dashboard metrics
- [ ] Performance tracker
- [ ] Campaign pause/stop

### SHOULD HAVE (V1.1, 2 weeks after)

- [ ] HubSpot sync (bidirectional)
- [ ] LinkedIn enrichment
- [ ] Email template customization
- [ ] A/B testing (subject lines)
- [ ] Manual follow-ups
- [ ] CRM lead mapping
- [ ] Bulk campaign actions
- [ ] Email edit before send

### LATER (V2+, 3 months)

- [ ] Voice calling agent
- [ ] SMS outreach
- [ ] Multi-channel (LinkedIn msgs)
- [ ] Advanced AI personalization
- [ ] Salesforce sync
- [ ] Mobile app
- [ ] Team management
- [ ] Custom reporting

---

## CRITICAL DEPENDENCIES

### BLOCKER #1: BANT Qualification

- **Why**: Without it, we spam bad prospects
- **Must be**: Accurate + fast (<30sec per lead)
- **Dependency**: LLM quality (Llama 2)
- **Fallback**: Manual review first 20 (then auto)

### BLOCKER #2: Email Generation

- **Why**: Poor emails = no responses
- **Must be**: Personalized + not spammy
- **Dependency**: LLM quality + data enrichment
- **Fallback**: Use templates + light personalization

### BLOCKER #3: Calendly Integration

- **Why**: Users want meetings booked auto
- **Must be**: Pre-filled slots + no manual sync
- **Dependency**: Calendar API
- **Fallback**: Send Calendly link only

---

## GO-LIVE REQUIREMENTS

### V1 Minimum

- ✓ 3 agents working (Prospector, BANT, Contacteur)
- ✓ 100+ prospects found per campaign
- ✓ 50%+ BANT accuracy (human validation)
- ✓ Emails sending at 1-2/day pace
- ✓ Meetings booking in Calendly
- ✓ Dashboard showing real metrics
- ✓ Zero data duplication
- ✓ OWASP audit passed
- ✓ 10-15 beta users testing
- ✓ NPS target: >50

### NOT INCLUDED V1

- ✗ Multi-team support
- ✗ Custom AI models
- ✗ Voice integration
- ✗ Advanced analytics
- ✗ Webhooks/API

---

## DÉPENDANCES TECH

| Semaine | Must Complete | Blocks |
|---------|---------------|--------|
| 1-2 | Database schema, State machine, API contracts | Week 3+ |
| 3-4 | Prospector agent, RocketReach, Deduplication | Week 5+ |
| 5-6 | BANT agent, State machine tested, Llama fine-tuning | Week 7+ |
| 7-8 | Frontend MVP, Dashboard | Week 9+ |
| 9-10 | HubSpot sync, E2E testing, Security audit | Launch |

---

## MVP PERIMETER LOCKED

**STATUS: APPROVED**

- 26 user stories finalized
- 72 story points allocated
- 12 weeks timeline confirmed
- 2 devs + 1 PM team assigned
- CrewAI + Llama 2 tech stack approved
- Zero scope creep allowed

**NEXT PHASE**: Start Sprint 1 (Week 1-2)

- Architecture workshop (4 hours)
- Jira setup + story import
- Daily standups begin
- Risk monitoring starts

---

*Document approuvé - 06 Janvier 2026*
