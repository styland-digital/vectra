import Link from 'next/link'
import Hero from '@/components/Hero'
import ProjectCard from '@/components/ProjectCard'
import TechStack from '@/components/TechStack'
import { getFeaturedProjects } from '@/lib/projects'

const services = [
  {
    icon: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
        <polyline points="16 18 22 12 16 6" />
        <polyline points="8 6 2 12 8 18" />
      </svg>
    ),
    title: 'Frontend Development',
    description:
      'Pixel-perfect UIs built with Next.js, React, and Tailwind CSS. Fast, accessible, and mobile-first by default.',
  },
  {
    icon: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
        <rect width="20" height="8" x="2" y="2" rx="2" ry="2" />
        <rect width="20" height="8" x="2" y="14" rx="2" ry="2" />
        <line x1="6" x2="6.01" y1="6" y2="6" />
        <line x1="6" x2="6.01" y1="18" y2="18" />
      </svg>
    ),
    title: 'Backend Development',
    description:
      'Robust APIs with Node.js, Python, FastAPI, or Express. Multi-tenant architecture, authentication, and PostgreSQL.',
  },
  {
    icon: (
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
        <path d="M12 20h9" />
        <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z" />
      </svg>
    ),
    title: 'Product Design',
    description:
      'UX research, wireframing, and high-fidelity Figma prototypes. Design systems that scale and delight users.',
  },
]

export default function HomePage() {
  const featuredProjects = getFeaturedProjects()

  return (
    <>
      <Hero />

      <section className="py-24 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <p className="text-xs font-semibold text-[#6366f1] uppercase tracking-widest mb-3">
              Services
            </p>
            <h2 className="text-3xl sm:text-4xl font-bold font-syne text-[#f5f5f5]">
              What I do
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {services.map((service) => (
              <div
                key={service.title}
                className="flex flex-col gap-4 p-6 rounded-xl card-bg hover:border-[#6366f1]/30 transition-all duration-300"
              >
                <div className="w-10 h-10 flex items-center justify-center rounded-lg bg-[#6366f1]/10 text-[#6366f1]">
                  {service.icon}
                </div>
                <h3 className="text-base font-bold font-syne text-[#f5f5f5]">
                  {service.title}
                </h3>
                <p className="text-sm text-[#a1a1aa] leading-relaxed">
                  {service.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="py-24 px-4 sm:px-6 lg:px-8 bg-[#0d0d0d]">
        <div className="max-w-6xl mx-auto">
          <div className="flex items-end justify-between mb-16">
            <div>
              <p className="text-xs font-semibold text-[#6366f1] uppercase tracking-widest mb-3">
                Work
              </p>
              <h2 className="text-3xl sm:text-4xl font-bold font-syne text-[#f5f5f5]">
                Featured Projects
              </h2>
            </div>
            <Link
              href="/projects"
              className="hidden sm:inline-flex items-center gap-2 text-sm font-medium text-[#a1a1aa] hover:text-[#6366f1] transition-colors duration-200"
            >
              View all
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                <path d="M5 12h14" />
                <path d="m12 5 7 7-7 7" />
              </svg>
            </Link>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {featuredProjects.map((project) => (
              <ProjectCard
                key={project.slug}
                title={project.title}
                description={project.description}
                stack={project.stack}
                demoUrl={project.demoUrl}
                repoUrl={project.repoUrl}
                slug={project.slug}
                category={project.category[0]}
              />
            ))}
          </div>

          <div className="mt-8 sm:hidden text-center">
            <Link
              href="/projects"
              className="inline-flex items-center gap-2 text-sm font-medium text-[#6366f1] hover:text-[#5558e8] transition-colors duration-200"
            >
              View all projects
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                <path d="M5 12h14" />
                <path d="m12 5 7 7-7 7" />
              </svg>
            </Link>
          </div>
        </div>
      </section>

      <section className="py-24 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <p className="text-xs font-semibold text-[#6366f1] uppercase tracking-widest mb-3">
              Stack
            </p>
            <h2 className="text-3xl sm:text-4xl font-bold font-syne text-[#f5f5f5]">
              Technologies I work with
            </h2>
          </div>
          <TechStack />
        </div>
      </section>

      <section className="py-24 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          <div className="relative overflow-hidden rounded-2xl p-8 sm:p-12 text-center" style={{ background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)' }}>
            <div
              className="absolute inset-0 opacity-30"
              style={{
                background: 'radial-gradient(ellipse at center, rgba(99,102,241,0.4) 0%, transparent 70%)',
              }}
            />
            <div className="relative z-10">
              <h2 className="text-3xl sm:text-4xl font-bold font-syne text-[#f5f5f5] mb-4">
                Let&apos;s build something together
              </h2>
              <p className="text-[#a1a1aa] mb-8 max-w-lg mx-auto text-base">
                Available for CDI positions and remote freelance projects. Let&apos;s talk about how I can help bring your product to life.
              </p>
              <Link
                href="/contact"
                className="inline-flex items-center gap-2 px-8 py-3.5 bg-[#6366f1] text-white font-semibold rounded-lg hover:bg-[#5558e8] transition-colors duration-200"
              >
                Get in touch
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                  <path d="M5 12h14" />
                  <path d="m12 5 7 7-7 7" />
                </svg>
              </Link>
            </div>
          </div>
        </div>
      </section>
    </>
  )
}
