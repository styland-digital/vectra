# Case Study — Medigest: Hospital Management SaaS with AI

**Role:** Full Stack Developer & Product Designer  
**Stack:** Next.js 14 · TypeScript · Node.js · PostgreSQL · AI/LLM  
**Timeline:** 4 months (Feb – May 2026)  
**Status:** Active development (MVP deployed)

---

## Context & Problem

Most private clinics and hospitals in Cameroon run on a combination of paper records, personal spreadsheets, and WhatsApp groups. The consequences are severe: lost patient records, double-booked appointments, no bed visibility, and zero data for management decisions.

One clinic director described the problem: **"On a bad day, I don't know how many patients are admitted, which doctors are on duty, or if we have the equipment a patient needs — until a nurse physically walks through every ward."**

The opportunity: digitalize hospital operations with an affordable, easy-to-use SaaS that works on African infrastructure (unreliable internet, older devices).

---

## Target Users

| User | Role | Primary Need |
|------|------|-------------|
| **Hospital Director** | Executive | Real-time operational overview, KPIs |
| **Reception Staff** | Operator | Fast patient admission, appointment booking |
| **Doctor/Nurse** | Clinical | Quick access to patient records |
| **Administrator** | Finance | Billing, insurance claims, reports |
| **IT Manager** | Technical | Simple deployment, minimal maintenance |

---

## Constraints

- **Technical:** Must work with intermittent connectivity (offline-first for critical flows)
- **Security:** Patient data = highly sensitive (HIPAA-equivalent compliance goal)
- **Budget:** SaaS model — pricing must be accessible to small clinics (starting 50,000 FCFA/month)
- **Timeline:** Working MVP in 8 weeks for pilot clinic
- **Legacy:** Some staff with zero digital literacy — UX must be trainable in <1 hour

---

## Process

### Discovery
Spent 2 weeks embedded at a 40-bed private clinic in Douala:
- Shadowed reception staff during morning rush (7-10am peak)
- Interviewed 3 doctors, 5 nurses, 2 administrators
- Mapped every paper form currently in use (14 distinct forms identified)

Key insight: **The biggest pain wasn't the data capture — it was the retrieval.** Finding a patient's history from 6 months ago took 15-20 minutes of archive digging.

### Information Architecture
Designed the IA around 5 core objects: Patient · Appointment · Admission · Prescription · Invoice

Each object has a complete lifecycle view and cross-references.

### Wireframes → Prototypes
- V1 wireframes: paper sketches (rapid, cheap to discard)
- V2 digital wireframes: Figma low-fidelity (tested with 4 reception staff)
- V3 high-fidelity: Figma prototype with real data shapes (tested with director)

### AI Decision Dashboard
The AI layer was added in month 3 based on director feedback: *"I have all the data now, but I still don't know what to do with it."*

Implemented:
- **Predictive bed occupancy** — 7-day forecast based on historical admission patterns
- **Staff scheduling recommendations** — Suggests optimal shift assignments based on predicted patient load
- **Anomaly detection** — Flags unusual billing patterns, missed appointments spikes

---

## Key Architecture Decisions

**1. Multi-tenant with data isolation**
Each hospital = isolated PostgreSQL schema. No cross-contamination of patient data between clients.

**2. Offline-first for reception flows**
Patient check-in and appointment creation work without internet. Data syncs automatically when connection restores. Used service workers + IndexedDB for client-side persistence.

**3. Audit trail for every record change**
Medical records are legally immutable. Every edit creates a new version with timestamp and user attribution. Previous versions accessible to authorized staff.

**4. Progressive AI adoption**
AI features are optional add-ons. Clinics can start with basic management (no AI), and activate the decision dashboard as they become comfortable with data-driven operations.

---

## Results & Impact

- **Pilot clinic:** 40-bed private clinic, Douala (deployed April 2026)
- **Patient lookup time:** 15-20 min (paper) → under 10 seconds
- **Appointment no-shows:** Reduced by ~35% after SMS reminders activated
- **Director daily check:** Now takes 3 minutes via the AI dashboard
- **Staff adoption:** 100% in 2 weeks (doctors were the fastest adopters — surprising)
- **Open issues resolved in sprint:** 15 features shipped in final sprint (May 2026)

---

## Lessons Learned

1. **Offline-first is mandatory** — The pilot clinic had 3 internet outages in the first 2 weeks of deployment. Offline-first wasn't a nice-to-have; it was survival.
2. **Doctors care about speed above all** — A doctor will abandon any tool that takes more than 2 clicks to find what they need. Every flow was optimized for under 3 clicks.
3. **The AI dashboard needs explanation** — Doctors and administrators wanted to know "how does it know this?" — added explainability tooltips to all AI recommendations.
4. **Billing is the killer feature** — Expected clinical features to drive adoption; reality: the billing module saved so much time that it became the primary driver of renewals.

---

## Author

**Alfred Landry Talom** — [dribbble.com/TFAL237](https://dribbble.com/TFAL237) · [alfredlandrytalom2004@gmail.com](mailto:alfredlandrytalom2004@gmail.com)
