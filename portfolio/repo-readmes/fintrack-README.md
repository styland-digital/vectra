# FinTrack — Financial Dashboard SaaS

> Multi-agency financial transfer platform with real-time dashboard for monitoring transactions, cash flows, and inter-agency operations — built for African fintech.

[![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Next.js](https://img.shields.io/badge/Next.js_14-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)](https://nextjs.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Vercel](https://img.shields.io/badge/Deployed_on_Vercel-000?style=for-the-badge&logo=vercel&logoColor=white)](https://fintrack-cyan-nine.vercel.app)

**[Live Demo →](https://fintrack-cyan-nine.vercel.app)**

---

## Overview

FinTrack addresses a critical operational challenge for financial agencies in Cameroon and sub-Saharan Africa: the lack of unified visibility over inter-agency cash flows and transaction volumes. Agency managers needed real-time data to make decisions on liquidity, detect anomalies, and track operator performance.

This platform provides a centralized dashboard where finance directors can monitor all agency activity, transfer volumes, and financial KPIs from a single interface.

---

## Key Features

- **Real-time Dashboard** — Live KPIs: transfer volumes, cash balances, transaction counts
- **Multi-Agency Management** — Hierarchical view: network → agency → operator
- **Transaction Tracking** — Full history with status (pending, validated, cancelled)
- **Role-Based Access** — Director / Manager / Operator with scoped permissions
- **Financial Reporting** — Daily/weekly/monthly reports exportable to PDF
- **Anomaly Alerts** — Threshold-based notifications for unusual activity
- **Responsive UI** — Mobile-first design for field operators

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14 (App Router) + React 18 |
| Language | TypeScript |
| Styling | Tailwind CSS + Shadcn/ui |
| Backend | Node.js + Express.js |
| Database | PostgreSQL |
| ORM | Prisma |
| Auth | JWT + Refresh tokens |
| Deploy | Vercel (frontend) |

---

## Architecture

```
fintrack/
├── frontend/           # Next.js 14 App Router
│   ├── app/
│   │   ├── (auth)/     # Login, register
│   │   ├── dashboard/  # Main KPI dashboard
│   │   ├── agencies/   # Agency management
│   │   ├── transactions/ # Transaction history
│   │   └── reports/    # Financial reports
│   └── components/
├── backend/            # Node.js + Express API
│   ├── routes/
│   ├── controllers/
│   ├── middlewares/
│   └── prisma/         # DB schema
└── docs/
```

---

## Getting Started

### Prerequisites

- Node.js 20+
- PostgreSQL 15+
- npm or pnpm

### Installation

```bash
git clone https://github.com/styland-digital/fintrack.git
cd fintrack

# Frontend
cd frontend
npm install
cp .env.example .env.local
# Edit .env.local with your values

# Backend
cd ../backend
npm install
cp .env.example .env
# Edit .env with your database URL

# Run migrations
npx prisma migrate dev

# Start development
npm run dev
```

### Environment Variables

```env
# Frontend (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:3001

# Backend (.env)
DATABASE_URL=postgresql://user:password@localhost:5432/fintrack
JWT_SECRET=your-secret-key
JWT_REFRESH_SECRET=your-refresh-secret
```

---

## Demo

**Live:** [fintrack-cyan-nine.vercel.app](https://fintrack-cyan-nine.vercel.app)

Test credentials:
```
Email: demo@fintrack.cm
Password: Demo@2026
```

---

## Author

**Alfred Landry Talom** — Full Stack Developer & Product Designer

[![Dribbble](https://img.shields.io/badge/Dribbble-EA4C89?style=flat-square&logo=dribbble&logoColor=white)](https://dribbble.com/TFAL237)
[![Email](https://img.shields.io/badge/Email-D14836?style=flat-square&logo=gmail&logoColor=white)](mailto:alfredlandrytalom2004@gmail.com)

---

## License

MIT © 2026 Alfred Landry Talom
