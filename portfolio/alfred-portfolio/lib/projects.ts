export type Project = {
  slug: string
  title: string
  description: string
  longDescription: string
  stack: string[]
  category: string[]
  demoUrl?: string
  repoUrl: string
  featured: boolean
}

export const projects: Project[] = [
  {
    slug: 'fintrack',
    title: 'FinTrack',
    description: 'Multi-agency financial dashboard SaaS for real-time transaction monitoring.',
    longDescription: `FinTrack is a multi-tenant financial dashboard SaaS platform designed for agencies that need to monitor and manage transactions across multiple clients in real time.

The platform provides a centralized hub where finance teams can track transaction flows, flag anomalies, generate reports, and manage accounts across different organizations — all from a single interface.

**Key challenges solved:**
The core technical challenge was building a rock-solid multi-tenant architecture where each agency's data is fully isolated while sharing the same infrastructure. I implemented row-level security in PostgreSQL combined with JWT-based organization scoping at the API layer.

**Technical highlights:**
- Real-time transaction updates via WebSocket connections
- Role-based access control (Owner, Admin, Analyst, Viewer)
- CSV/Excel export for audit and reporting workflows
- Responsive dashboard built with Tailwind CSS and Recharts
- Deployed on Vercel (frontend) + Railway (backend + DB)

**Stack:** Next.js, TypeScript, Node.js, PostgreSQL, Tailwind CSS, Recharts, Prisma ORM`,
    stack: ['Next.js', 'TypeScript', 'Node.js', 'PostgreSQL', 'Tailwind CSS'],
    category: ['SaaS', 'Fintech'],
    demoUrl: 'https://fintrack-cyan-nine.vercel.app',
    repoUrl: 'https://github.com/styland-digital/fintrack',
    featured: true,
  },
  {
    slug: 'medigest',
    title: 'Medigest',
    description: 'Hospital management SaaS with AI-powered decision dashboard.',
    longDescription: `Medigest is a hospital management platform that combines traditional healthcare administration with AI-powered clinical decision support.

Designed for mid-sized hospitals and clinics in francophone Africa, Medigest digitizes patient records, appointment scheduling, pharmacy inventory, and billing — while layering AI analytics on top to help doctors and administrators make faster, better-informed decisions.

**Key challenges solved:**
Healthcare data in many African hospitals is still paper-based. Medigest needed to handle both structured digital data and scanned/photographed legacy documents. I integrated an OCR pipeline to ingest historical records and normalize them into the database.

**Technical highlights:**
- AI dashboard surfacing patient risk scores, drug interaction alerts, and discharge predictions
- LLM-powered clinical notes summarization (using local Llama model)
- Multi-role system: Doctor, Nurse, Pharmacist, Admin, Billing
- FHIR-compatible data model for interoperability
- Offline-first architecture for unstable internet environments

**Stack:** Next.js, TypeScript, Node.js, PostgreSQL, AI/LLM, Prisma ORM`,
    stack: ['Next.js', 'TypeScript', 'Node.js', 'PostgreSQL', 'AI/LLM'],
    category: ['SaaS', 'Healthcare'],
    repoUrl: 'https://github.com/styland-digital/medigest',
    featured: true,
  },
  {
    slug: 'vectra',
    title: 'Vectra',
    description: 'AI agents platform for automated B2B sales prospecting and outreach.',
    longDescription: `Vectra is a SaaS platform that automates the entire B2B sales prospecting pipeline using a team of specialized AI agents — from finding leads to booking meetings.

The system orchestrates three agents: a Prospector agent that sources leads via RocketReach, a BANT qualification agent that scores each lead on Budget/Authority/Need/Timeline (0–100), and a Scheduler agent that writes personalized outreach emails and schedules Calendly meetings.

**Key challenges solved:**
Coordinating multiple AI agents in a reliable, auditable pipeline was the central challenge. I used CrewAI to manage agent orchestration with clear handoff points, while Celery handled async job queuing so long-running prospecting jobs don't block the API.

**Technical highlights:**
- Multi-agent system with CrewAI (Prospector → BANT → Scheduler)
- BANT scoring engine: 0–100 composite score with automated routing
- Celery task queue for async agent jobs with progress tracking
- Multi-tenant SaaS with strict organization data isolation
- Audit logging for every agent action (compliance-ready)
- Rate limiting on all external API calls (RocketReach, SendGrid)

**Stack:** Python, FastAPI, CrewAI, Next.js, Docker, PostgreSQL, Redis, Celery`,
    stack: ['Python', 'FastAPI', 'CrewAI', 'Next.js', 'Docker', 'PostgreSQL'],
    category: ['SaaS', 'AI'],
    repoUrl: 'https://github.com/styland-digital/vectra',
    featured: true,
  },
  {
    slug: 'trash-mboa',
    title: 'Trash Mboa',
    description: 'Civic-tech app for urban waste reporting and collection tracking in Douala.',
    longDescription: `Trash Mboa (Mboa means "my country" in Cameroonian slang) is a civic-tech application that empowers Douala residents to report illegal dumping sites, track garbage collection schedules, and hold local authorities accountable through data visualization.

The app was built in response to a real problem: Douala generates over 1,500 tonnes of waste daily, but collection infrastructure is fragmented and citizens have no way to report or track issues. Trash Mboa fills that gap with a lightweight, mobile-first reporting tool.

**Key challenges solved:**
Building for low-bandwidth environments in Cameroon required aggressive optimization. The app is a Progressive Web App (PWA) that works offline, uses compressed images, and syncs reports when connectivity is restored.

**Technical highlights:**
- Geolocated waste report submissions with photo upload
- Interactive map showing active dump sites and collection zones
- Public dashboard with city-wide waste metrics
- PWA with offline report queuing
- Anonymous reporting to protect civic reporters
- Multilingual: French + English

**Stack:** Next.js, TypeScript, Tailwind CSS, Mapbox GL, Supabase`,
    stack: ['Next.js', 'TypeScript', 'Tailwind CSS'],
    category: ['Civic Tech'],
    repoUrl: 'https://github.com/styland-digital/trash-mboa',
    featured: false,
  },
]

export function getProjectBySlug(slug: string): Project | undefined {
  return projects.find((p) => p.slug === slug)
}

export function getFeaturedProjects(): Project[] {
  return projects.filter((p) => p.featured)
}

export function getProjectsByCategory(category: string): Project[] {
  if (category === 'All') return projects
  return projects.filter((p) => p.category.includes(category))
}
