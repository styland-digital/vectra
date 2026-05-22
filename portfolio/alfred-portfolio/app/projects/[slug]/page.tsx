import type { Metadata } from 'next'
import { notFound } from 'next/navigation'
import Link from 'next/link'
import { getProjectBySlug, projects } from '@/lib/projects'

interface PageProps {
  params: { slug: string }
}

export async function generateStaticParams() {
  return projects.map((p) => ({ slug: p.slug }))
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const project = getProjectBySlug(params.slug)
  if (!project) return {}

  return {
    title: `${project.title} — Alfred Landry Talom`,
    description: project.description,
  }
}

function renderLongDescription(text: string) {
  const paragraphs = text.split('\n\n').filter(Boolean)

  return paragraphs.map((para, i) => {
    if (para.startsWith('**') && para.endsWith('**')) {
      return (
        <h3 key={i} className="text-lg font-bold font-syne text-[#f5f5f5] mt-8 mb-3">
          {para.replace(/\*\*/g, '')}
        </h3>
      )
    }

    if (para.startsWith('- ')) {
      const items = para
        .split('\n')
        .filter((l) => l.startsWith('- '))
        .map((l) => l.slice(2))
      return (
        <ul key={i} className="list-none flex flex-col gap-2 my-4">
          {items.map((item, j) => {
            const cleaned = item.replace(/\*\*(.*?)\*\*/g, '$1')
            return (
              <li key={j} className="flex items-start gap-2 text-[#a1a1aa] text-sm leading-relaxed">
                <span className="text-[#6366f1] mt-0.5 shrink-0">▸</span>
                {cleaned}
              </li>
            )
          })}
        </ul>
      )
    }

    const formattedPara = para.replace(/\*\*(.*?)\*\*/g, '<strong class="text-[#f5f5f5]">$1</strong>')
    return (
      <p
        key={i}
        className="text-[#a1a1aa] text-base leading-relaxed mb-4"
        dangerouslySetInnerHTML={{ __html: formattedPara }}
      />
    )
  })
}

export default function ProjectDetailPage({ params }: PageProps) {
  const project = getProjectBySlug(params.slug)
  if (!project) notFound()

  const currentIndex = projects.findIndex((p) => p.slug === params.slug)
  const prevProject = currentIndex > 0 ? projects[currentIndex - 1] : null
  const nextProject = currentIndex < projects.length - 1 ? projects[currentIndex + 1] : null

  return (
    <div className="min-h-screen pt-24 pb-16 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">

        <div className="mb-8">
          <Link
            href="/projects"
            className="inline-flex items-center gap-2 text-sm text-[#71717a] hover:text-[#6366f1] transition-colors duration-200"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
              <path d="m15 18-6-6 6-6" />
            </svg>
            Back to projects
          </Link>
        </div>

        <header className="mb-12">
          <div className="flex flex-wrap gap-2 mb-4">
            {project.category.map((cat) => (
              <span
                key={cat}
                className="px-3 py-1 text-xs font-semibold bg-[#6366f1]/10 text-[#6366f1] rounded-full"
              >
                {cat}
              </span>
            ))}
          </div>

          <h1 className="text-4xl sm:text-5xl font-bold font-syne text-[#f5f5f5] mb-4">
            {project.title}
          </h1>

          <p className="text-lg text-[#a1a1aa] leading-relaxed mb-6">
            {project.description}
          </p>

          <div className="flex flex-wrap gap-3">
            {project.demoUrl && (
              <a
                href={project.demoUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 px-5 py-2.5 bg-[#6366f1] text-white font-semibold rounded-lg hover:bg-[#5558e8] transition-colors duration-200 text-sm"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                  <path d="M15 3h6v6" />
                  <path d="M10 14 21 3" />
                  <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
                </svg>
                Live Demo
              </a>
            )}
            <a
              href={project.repoUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 px-5 py-2.5 border border-[#27272a] text-[#f5f5f5] font-semibold rounded-lg hover:border-[#6366f1] hover:text-[#6366f1] transition-colors duration-200 text-sm"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                <path d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0 1 12 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z" />
              </svg>
              View Source
            </a>
          </div>
        </header>

        <div className="mb-10 p-5 rounded-xl card-bg">
          <h2 className="text-xs font-semibold text-[#6366f1] uppercase tracking-wider mb-3">
            Tech Stack
          </h2>
          <div className="flex flex-wrap gap-2">
            {project.stack.map((tech) => (
              <span
                key={tech}
                className="px-3 py-1.5 text-sm font-medium bg-[#1a1a1a] border border-[#27272a] text-[#d4d4d8] rounded-lg"
              >
                {tech}
              </span>
            ))}
          </div>
        </div>

        <article className="mb-16">
          <div className="prose-section">
            {renderLongDescription(project.longDescription)}
          </div>
        </article>

        <nav
          className="border-t border-[#27272a] pt-8 grid grid-cols-2 gap-4"
          aria-label="Project navigation"
        >
          {prevProject ? (
            <Link
              href={`/projects/${prevProject.slug}`}
              className="flex flex-col gap-1 p-4 rounded-lg card-bg hover:border-[#6366f1]/30 transition-all duration-200 group"
            >
              <span className="text-xs text-[#71717a] flex items-center gap-1">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                  <path d="m15 18-6-6 6-6" />
                </svg>
                Previous
              </span>
              <span className="text-sm font-semibold text-[#f5f5f5] group-hover:text-[#6366f1] transition-colors duration-200">
                {prevProject.title}
              </span>
            </Link>
          ) : (
            <div />
          )}

          {nextProject ? (
            <Link
              href={`/projects/${nextProject.slug}`}
              className="flex flex-col gap-1 p-4 rounded-lg card-bg hover:border-[#6366f1]/30 transition-all duration-200 text-right group"
            >
              <span className="text-xs text-[#71717a] flex items-center justify-end gap-1">
                Next
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                  <path d="m9 18 6-6-6-6" />
                </svg>
              </span>
              <span className="text-sm font-semibold text-[#f5f5f5] group-hover:text-[#6366f1] transition-colors duration-200">
                {nextProject.title}
              </span>
            </Link>
          ) : (
            <div />
          )}
        </nav>

      </div>
    </div>
  )
}
