# Medigest — Hospital Management SaaS

> Full-stack SaaS platform for hospital management with AI-powered decision dashboard — streamlining patient flows, medical records, appointments, and operational analytics.

[![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Next.js](https://img.shields.io/badge/Next.js_14-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)](https://nextjs.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![AI Powered](https://img.shields.io/badge/AI_Powered-blueviolet?style=for-the-badge)](https://openai.com/)

---

## Overview

Healthcare facilities in Central Africa face massive operational inefficiencies: paper-based patient records, no appointment systems, zero visibility on bed occupancy or staff productivity. Medigest digitalizes and centralizes all hospital operations into a single, intuitive SaaS platform — with an AI decision layer that surfaces actionable insights to administrators.

From patient admission to discharge, every step is tracked, measured, and optimized.

---

## Key Features

- **Patient Management** — Digital records, medical history, admission/discharge flows
- **Appointment Scheduling** — Online booking with doctor availability management
- **Bed & Ward Management** — Real-time occupancy tracking across departments
- **Staff Management** — Shifts, performance metrics, role-based access
- **AI Decision Dashboard** — Predictive analytics on patient flows, resource usage, peak periods
- **Billing & Invoicing** — Automated invoice generation with payment tracking
- **Multi-tenant** — Each hospital = isolated data environment
- **Mobile-first** — Designed for nurses and doctors on tablets/phones

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14 (App Router) + React 18 |
| Language | TypeScript |
| Styling | Tailwind CSS + Shadcn/ui |
| Backend | Node.js + Express.js (API) |
| Database | PostgreSQL |
| ORM | Prisma |
| AI Layer | OpenAI API / Local LLM |
| Auth | JWT + Role-based access |
| Charts | Recharts / Chart.js |

---

## Architecture

```
medigest/
├── app/                    # Next.js 14 App Router
│   ├── (auth)/             # Authentication
│   ├── (dashboard)/
│   │   ├── patients/       # Patient management
│   │   ├── appointments/   # Scheduling
│   │   ├── wards/          # Bed management
│   │   ├── staff/          # HR management
│   │   ├── billing/        # Finance
│   │   └── analytics/      # AI Dashboard
│   └── api/                # API routes
├── components/
│   ├── ui/                 # Shadcn/ui components
│   ├── forms/              # Patient, appointment forms
│   └── charts/             # Analytics widgets
├── lib/
│   ├── db/                 # Prisma client
│   ├── auth/               # NextAuth or custom JWT
│   └── ai/                 # AI integration
└── prisma/
    └── schema.prisma
```

---

## Getting Started

### Prerequisites

- Node.js 20+
- PostgreSQL 15+
- npm or pnpm

### Installation

```bash
git clone https://github.com/styland-digital/medigest.git
cd medigest
npm install

# Database setup
cp .env.example .env
# Edit .env with your PostgreSQL connection string

npx prisma migrate dev
npx prisma db seed

# Start
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Environment Variables

```env
DATABASE_URL=postgresql://user:password@localhost:5432/medigest
NEXTAUTH_SECRET=your-secret
NEXTAUTH_URL=http://localhost:3000
OPENAI_API_KEY=your-openai-key   # optional, for AI features
```

---

## Roadmap

- [x] Patient management & medical records
- [x] Appointment scheduling
- [x] Bed/ward management
- [x] Staff & role management
- [x] Billing & invoicing
- [x] AI analytics dashboard
- [ ] Mobile app (React Native)
- [ ] HL7 FHIR compliance
- [ ] Insurance integration

---

## Author

**Alfred Landry Talom** — Full Stack Developer & Product Designer

[![Dribbble](https://img.shields.io/badge/Dribbble-EA4C89?style=flat-square&logo=dribbble&logoColor=white)](https://dribbble.com/TFAL237)
[![Email](https://img.shields.io/badge/Email-D14836?style=flat-square&logo=gmail&logoColor=white)](mailto:alfredlandrytalom2004@gmail.com)

---

## License

MIT © 2026 Alfred Landry Talom
