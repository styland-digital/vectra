import Link from 'next/link'
import { cn } from '@/lib/utils'

interface ProjectCardProps {
  title: string
  description: string
  stack: string[]
  demoUrl?: string
  repoUrl: string
  slug: string
  category: string
}

export default function ProjectCard({
  title,
  description,
  stack,
  demoUrl,
  repoUrl,
  slug,
  category,
}: ProjectCardProps) {
  return (
    <div
      className={cn(
        'group relative flex flex-col gap-4 p-6 rounded-xl card-bg border-glow',
        'transition-all duration-300 hover:-translate-y-1'
      )}
    >
      <div className="flex items-start justify-between gap-4">
        <div className="flex flex-col gap-1">
          <span className="text-xs font-medium text-[#6366f1] uppercase tracking-wider">
            {category}
          </span>
          <h3 className="text-lg font-bold font-syne text-[#f5f5f5] group-hover:text-[#6366f1] transition-colors duration-200">
            {title}
          </h3>
        </div>
        <div className="flex items-center gap-2 shrink-0">
          {demoUrl && (
            <a
              href={demoUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="p-2 rounded-md text-[#71717a] hover:text-[#6366f1] hover:bg-[#1a1a1a] transition-colors duration-200"
              aria-label={`View ${title} demo`}
              onClick={(e) => e.stopPropagation()}
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                <path d="M15 3h6v6" />
                <path d="M10 14 21 3" />
                <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
              </svg>
            </a>
          )}
          <a
            href={repoUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="p-2 rounded-md text-[#71717a] hover:text-[#6366f1] hover:bg-[#1a1a1a] transition-colors duration-200"
            aria-label={`View ${title} repository`}
            onClick={(e) => e.stopPropagation()}
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0 1 12 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z" />
            </svg>
          </a>
        </div>
      </div>

      <p className="text-sm text-[#a1a1aa] leading-relaxed flex-1">{description}</p>

      <div className="flex flex-wrap gap-2">
        {stack.slice(0, 5).map((tech) => (
          <span
            key={tech}
            className="px-2 py-0.5 text-xs font-medium bg-[#1a1a1a] border border-[#27272a] text-[#a1a1aa] rounded-md"
          >
            {tech}
          </span>
        ))}
        {stack.length > 5 && (
          <span className="px-2 py-0.5 text-xs font-medium text-[#71717a]">
            +{stack.length - 5} more
          </span>
        )}
      </div>

      <Link
        href={`/projects/${slug}`}
        className="inline-flex items-center gap-1.5 text-xs font-medium text-[#6366f1] hover:gap-2.5 transition-all duration-200"
      >
        Read case study
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
          <path d="M5 12h14" />
          <path d="m12 5 7 7-7 7" />
        </svg>
      </Link>
    </div>
  )
}
