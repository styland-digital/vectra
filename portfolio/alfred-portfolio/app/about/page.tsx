import type { Metadata } from 'next'
import Link from 'next/link'
import TechStack from '@/components/TechStack'

export const metadata: Metadata = {
  title: 'About — Alfred Landry Talom',
  description:
    'Full Stack Developer & Product Designer based in Douala, Cameroon. Background, experience, skills, and the way I work.',
}

const timeline = [
  {
    type: 'work',
    period: 'Aug 2025 – Feb 2026',
    role: 'UI/UX Designer',
    org: 'Katika Web3',
    description:
      'Designed and shipped visual acquisition assets for a Web3 money transfer application targeting the African diaspora. Led end-to-end UX for onboarding flows, wallet interfaces, and marketing pages.',
  },
  {
    type: 'work',
    period: 'May 2024 – present',
    role: 'Freelance Full Stack Developer',
    org: 'styland-digital',
    description:
      'Built FinTrack (multi-agency financial SaaS), Medigest (hospital management + AI), Vectra (AI prospecting agents), and Trash Mboa (civic tech). Working with clients across Cameroon and the diaspora.',
  },
  {
    type: 'education',
    period: '2025',
    role: 'Licence Pro Génie Logiciel',
    org: 'IUT de Douala',
    description:
      'Advanced software engineering program covering distributed systems, software architecture, project management, and applied AI.',
  },
  {
    type: 'education',
    period: '2024',
    role: 'DUT Génie Informatique',
    org: 'IUT de Douala',
    description:
      'Foundational computer science: algorithms, data structures, systems programming, databases, and software development methodology.',
  },
]

const skills = [
  {
    category: 'Frontend',
    items: ['Next.js', 'React', 'TypeScript', 'JavaScript', 'Tailwind CSS', 'Framer Motion', 'Shadcn/ui'],
  },
  {
    category: 'Backend',
    items: ['Node.js', 'Python', 'FastAPI', 'Express.js', 'REST APIs', 'WebSockets', 'Celery'],
  },
  {
    category: 'Database',
    items: ['PostgreSQL', 'Redis', 'Prisma ORM', 'SQLAlchemy', 'Supabase'],
  },
  {
    category: 'Design',
    items: ['Figma', 'Adobe Photoshop', 'After Effects', 'Design Systems', 'UX Research', 'Prototyping'],
  },
  {
    category: 'DevOps & Tools',
    items: ['Docker', 'Git', 'GitHub Actions', 'Vercel', 'Railway', 'CI/CD'],
  },
  {
    category: 'AI & Agents',
    items: ['CrewAI', 'Llama 2', 'LLM Integration', 'Prompt Engineering', 'RAG'],
  },
]

export default function AboutPage() {
  return (
    <div className="min-h-screen pt-24 pb-16 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">

        <header className="mb-16">
          <p className="text-xs font-semibold text-[#6366f1] uppercase tracking-widest mb-4">
            About
          </p>
          <h1 className="text-4xl sm:text-5xl font-bold font-syne text-[#f5f5f5] mb-4 leading-tight">
            Alfred Landry Talom
          </h1>
          <p className="text-xl text-[#a1a1aa] font-medium">
            Full Stack Developer & Product Designer based in Douala, Cameroon.
            Building SaaS products from zero to one.
          </p>
        </header>

        <section className="mb-20">
          <div className="prose prose-invert max-w-none">
            <p className="text-base text-[#d4d4d8] leading-relaxed mb-4">
              I&apos;m a software developer and product designer who builds full-stack SaaS applications — from the database schema to the pixel-perfect UI. My work lives at the intersection of solid engineering and thoughtful design, and I believe the best products are ones where neither discipline compromises the other.
            </p>
            <p className="text-base text-[#d4d4d8] leading-relaxed mb-4">
              I studied computer science at IUT de Douala, where I developed strong foundations in software architecture, algorithms, and systems programming. Since then, I&apos;ve been building independently under the{' '}
              <span className="text-[#6366f1] font-medium">styland-digital</span>{' '}
              brand — shipping products in fintech, healthcare, AI, and civic tech.
            </p>
            <p className="text-base text-[#d4d4d8] leading-relaxed mb-4">
              My philosophy is simple: ship fast, measure, and iterate. I prefer small, focused teams where engineers take ownership of problems end-to-end. I&apos;m comfortable going from a napkin sketch to a deployed production API in the same week.
            </p>
            <p className="text-base text-[#d4d4d8] leading-relaxed">
              Outside of code, I&apos;m deeply interested in the African tech ecosystem and how software can solve real problems for communities that have historically been underserved by technology. Trash Mboa is a direct expression of that — and just the beginning.
            </p>
          </div>
        </section>

        <section className="mb-20">
          <h2 className="text-2xl font-bold font-syne text-[#f5f5f5] mb-10">
            Experience & Education
          </h2>

          <div className="relative">
            <div className="absolute left-4 top-0 bottom-0 w-px bg-[#27272a]" aria-hidden="true" />

            <div className="flex flex-col gap-8">
              {timeline.map((item, i) => (
                <div key={i} className="relative pl-12">
                  <div
                    className={`absolute left-2.5 top-1 w-3 h-3 rounded-full border-2 -translate-x-1/2 ${
                      item.type === 'work'
                        ? 'bg-[#6366f1] border-[#6366f1]'
                        : 'bg-[#0a0a0a] border-[#6366f1]'
                    }`}
                    aria-hidden="true"
                  />
                  <div className="flex flex-col sm:flex-row sm:items-center gap-1 sm:gap-4 mb-2">
                    <span className="text-xs font-medium text-[#6366f1] bg-[#6366f1]/10 px-2.5 py-1 rounded-full w-fit">
                      {item.period}
                    </span>
                    <span className="text-xs font-medium text-[#71717a] uppercase tracking-wider">
                      {item.type === 'work' ? 'Work' : 'Education'}
                    </span>
                  </div>
                  <h3 className="text-base font-bold font-syne text-[#f5f5f5] mb-0.5">
                    {item.role}
                  </h3>
                  <p className="text-sm font-medium text-[#6366f1] mb-2">{item.org}</p>
                  <p className="text-sm text-[#a1a1aa] leading-relaxed">{item.description}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="mb-20">
          <h2 className="text-2xl font-bold font-syne text-[#f5f5f5] mb-4">
            Skills & Technologies
          </h2>
          <p className="text-[#a1a1aa] text-sm mb-10">
            Full-stack coverage from design to DevOps.
          </p>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-12">
            {skills.map((skill) => (
              <div key={skill.category} className="p-5 rounded-xl card-bg">
                <h3 className="text-xs font-semibold text-[#6366f1] uppercase tracking-wider mb-3">
                  {skill.category}
                </h3>
                <div className="flex flex-wrap gap-2">
                  {skill.items.map((item) => (
                    <span
                      key={item}
                      className="px-2.5 py-1 text-xs font-medium bg-[#1a1a1a] border border-[#27272a] text-[#d4d4d8] rounded-md"
                    >
                      {item}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>

          <div className="mt-4">
            <p className="text-xs font-semibold text-[#6366f1] uppercase tracking-widest mb-6">
              Tech Stack Overview
            </p>
            <TechStack />
          </div>
        </section>

        <section>
          <div className="p-8 rounded-xl card-bg flex flex-col sm:flex-row items-center justify-between gap-6">
            <div>
              <h2 className="text-xl font-bold font-syne text-[#f5f5f5] mb-2">
                Want the full details?
              </h2>
              <p className="text-sm text-[#a1a1aa]">
                Download my CV for a complete overview of my experience and skills.
              </p>
            </div>
            <div className="flex items-center gap-4 shrink-0">
              <a
                href="/cv-developer.pdf"
                download
                className="inline-flex items-center gap-2 px-5 py-2.5 bg-[#6366f1] text-white font-semibold rounded-lg hover:bg-[#5558e8] transition-colors duration-200 text-sm"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                  <polyline points="7 10 12 15 17 10" />
                  <line x1="12" x2="12" y1="15" y2="3" />
                </svg>
                Download CV
              </a>
              <Link
                href="/contact"
                className="inline-flex items-center gap-2 px-5 py-2.5 border border-[#27272a] text-[#f5f5f5] font-semibold rounded-lg hover:border-[#6366f1] hover:text-[#6366f1] transition-colors duration-200 text-sm"
              >
                Contact me
              </Link>
            </div>
          </div>
        </section>

      </div>
    </div>
  )
}
