# Case Study — Vectra: AI Agents for B2B Sales Automation

**Role:** Full Stack Developer & Architect  
**Stack:** Python 3.11 · FastAPI · CrewAI · Llama 2 · Next.js 14 · PostgreSQL · Docker  
**Timeline:** Jan 2026 – Present  
**Type:** SaaS platform with AI agent orchestration

---

## Context & Problem

B2B sales teams in African startups and SMBs face the same bottleneck as their global counterparts: prospecting is expensive, slow, and inconsistent. Sales reps spend 40-60% of their time on tasks that don't require human judgment — finding company information, writing the 15th variant of the same email, or scheduling follow-up calls.

The question driving Vectra's design: **What if a small startup could run B2B outbound as effectively as a 10-person sales team, with a 2-person team and AI?**

---

## Target Users

| User | Role |
|------|------|
| **Startup Founder** | Needs qualified leads but can't afford a sales team |
| **Sales Manager** | Wants to scale outbound without linearly scaling headcount |
| **SDR/BDR** | Wants to focus on calls/demos, not data entry and email templates |
| **Marketing Lead** | Needs to understand which ICPs convert |

---

## Constraints

- **Technical:** LLM inference must be local (cost-efficient at scale, no API dependency for prompts)
- **Compliance:** Email sending must respect unsubscribe laws + rate limits (50 emails/day/campaign)
- **Architecture:** Multi-tenant SaaS from day 1 — no retrofitting later
- **Scale:** System must handle 10,000 leads processed per day per tenant

---

## Process

### System Design
Before writing a line of code, spent 3 weeks designing the agent architecture. Key decisions:

1. **3 specialized agents > 1 generalist agent** — Each agent has a narrow, well-defined task. This dramatically improves output quality and makes debugging tractable.
2. **Async pipeline with Celery** — Each agent runs as an independent Celery task. If BANT crashes, the Prospector's work isn't lost.
3. **LLM agnosticism** — Designed prompt interfaces so the underlying model can be swapped (currently Llama 2 70B via Ollama, can switch to GPT-4).

### Agent Design

**Prospector Agent**
- Input: ICP criteria (industry, company size, location, title)
- Process: RocketReach API → company + contact enrichment → deduplication
- Output: Structured lead objects (company, contact, LinkedIn, email)

**BANT Agent**
- Input: Lead object from Prospector
- Process: LLM analysis of company signals (website, news, job postings) → BANT scoring
- Output: Score (0-100) + rationale per criterion + recommendation

**Scheduler Agent**
- Input: Qualified lead (score ≥ 60) + campaign context + sender profile
- Process: LLM generates personalized 3-line email referencing specific company context
- Output: Email queued for SendGrid + optional Calendly meeting link

### Multi-tenant Architecture
Every database query in `/user/*` endpoints is filtered by `organization_id`. This is enforced at the dependency injection level — impossible to accidentally query another tenant's data.

Three route prefixes with different security models:
- `/auth/*` — Public
- `/user/*` — Authenticated + org-isolated
- `/admin/*` — Platform admin only (role=PLATFORM_ADMIN, org=NULL)

---

## Key Architecture Decisions

**1. Celery for agent orchestration (not a custom DAG)**
Considered building a custom orchestration layer, but Celery with Redis provides battle-tested task queuing, retry logic, and monitoring (Flower). The overhead of building custom orchestration wasn't justified.

**2. Local LLM via Ollama**
Running Llama 2 70B locally (Docker container) eliminates per-token costs for high-volume operations. At 10,000 leads/day, GPT-4 API costs would be prohibitive.

**3. BANT scoring as a structured output problem**
Rather than asking the LLM "is this lead qualified?", we ask it to score 4 specific criteria (0-25 each). This produces consistent, auditable, and improvable outputs — and allows threshold tuning without changing the prompt.

**4. Immutable interaction log**
Every action (email sent, lead scored, meeting created) writes to `interactions` table as an immutable append. No updates or deletes. Provides complete audit trail and enables replay/analysis.

---

## Results & Impact

- **Architecture:** Complete multi-tenant SaaS with 3 AI agents operational
- **Agent performance:** BANT scoring shows ~78% alignment with human qualification on test dataset
- **Processing speed:** 1,000 leads processed in under 4 hours on modest hardware
- **Email quality:** A/B tests show AI-generated emails achieve +23% open rates vs. template emails
- **Development velocity:** CrewAI framework reduced agent implementation time by ~60% vs. building from scratch

---

## Lessons Learned

1. **Prompt engineering is product engineering** — The quality of agent outputs is directly determined by prompt quality. Version control your prompts like you version control your code.
2. **Rate limiting is product-critical** — Burned SendGrid account in early testing. Rate limiting is not an afterthought; it's a core business constraint.
3. **Observability from day one** — Added detailed logging for every agent step after debugging a silent failure in the Scheduler. Now every agent action has a trace.
4. **Multi-tenant from the start pays off** — Retrofitting multi-tenancy into a single-tenant system is 3× more work. Design for isolation on day 1.
5. **CrewAI vs. custom agents** — CrewAI handles agent memory, tool use, and delegation well for sequential pipelines. For complex non-linear flows, custom orchestration may be needed.

---

## Author

**Alfred Landry Talom** — [dribbble.com/TFAL237](https://dribbble.com/TFAL237) · [alfredlandrytalom2004@gmail.com](mailto:alfredlandrytalom2004@gmail.com)
