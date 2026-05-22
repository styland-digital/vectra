# Case Study — FinTrack: Multi-Agency Financial Dashboard

**Role:** Full Stack Developer & Product Designer  
**Stack:** Next.js 14 · TypeScript · Node.js · PostgreSQL · Tailwind CSS  
**Timeline:** 3 months (2026)  
**Live Demo:** [fintrack-cyan-nine.vercel.app](https://fintrack-cyan-nine.vercel.app)

---

## Context & Problem

Financial transfer agencies in Cameroon manage large volumes of cash transactions across multiple locations daily — but most operate with zero digital infrastructure. Agency directors had no way to monitor real-time cash balances, track operator performance, or detect fraudulent activity across their network.

The core problem: **a director managing 8 agencies across Douala had to call each agency individually every morning to get the day's opening balances — a 45-minute manual process with high error risk.**

---

## Target Users

| User | Pain Point |
|------|-----------|
| **Finance Director** | No consolidated view of the whole network |
| **Agency Manager** | Manual transaction logs, no performance tracking |
| **Operator/Cashier** | Paper-based recording, error-prone |
| **Auditor** | No digital audit trail |

---

## Constraints

- **Technical:** Must work on low-bandwidth mobile connections (Douala average: 3G)
- **Timeline:** MVP in 6 weeks for client pilot
- **Budget:** No third-party SaaS (cost-conscious client)
- **Accessibility:** Some users are not digital natives — UX must be extremely simple

---

## Process

### Discovery & Research
Conducted 4 interviews with agency directors and operators in Douala. Key findings:
- 100% used WhatsApp to communicate balances between agencies → needed a more structured but equally simple solution
- Directors checked their phone on average 12× per day for balance updates
- Biggest fear: unauthorized transactions not caught until end of day

### User Flows
Mapped 3 critical flows:
1. **Opening flow** — Operator records opening balance → Manager validates
2. **Transaction flow** — Each transfer logged with amount, sender, receiver, agency
3. **Reporting flow** — Director generates daily summary → exports PDF

### Wireframes → Design
Started with paper wireframes (3 iterations with client), then moved to Figma hi-fi mockups. Dark mode was specifically requested by users who work under direct sunlight.

Design principles applied:
- Large touch targets (operators use the app on budget Android phones)
- Color-coded status indicators (green/orange/red) — works without reading text
- Progressive disclosure: overview first, details on click

---

## Key Architecture Decisions

**1. Server-side rendering for the dashboard**
Chose Next.js App Router with server components for the main KPI page — ensures fast initial load on 3G and avoids blank screens while data fetches.

**2. Optimistic UI for transaction logging**
Operators log 50-200 transactions/day. Used optimistic updates to make the interface feel instant even on slow connections — with background sync to the server.

**3. Prisma + PostgreSQL for audit trail**
All transactions are append-only. Soft deletes only. Gives auditors a complete immutable history.

---

## Results & Impact

- **Pilot:** Deployed with 1 agency network (8 locations, 23 operators)
- **Time saved:** Director morning check reduced from 45 min → under 5 min
- **Error reduction:** Manual calculation errors dropped to near zero
- **Adoption:** 100% of operators using the app within 2 weeks (no training required)
- **Performance:** Lighthouse score 94 (Performance), 98 (Accessibility)

---

## Lessons Learned

1. **Mobile-first isn't optional in this market** — 80% of actual usage was on mobile, not desktop
2. **Offline capability would have been a game changer** — Multiple requests for offline transaction logging to handle connectivity drops
3. **Simple > powerful** — Removed several "advanced" features (forecasting, BI charts) from V1 after user testing showed they caused confusion
4. **PDF exports are critical** — Users wanted to print and sign reports; digital-only was a dealbreaker for some

---

## Author

**Alfred Landry Talom** — [dribbble.com/TFAL237](https://dribbble.com/TFAL237) · [alfredlandrytalom2004@gmail.com](mailto:alfredlandrytalom2004@gmail.com)
