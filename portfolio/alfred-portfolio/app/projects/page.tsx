'use client'

import { useState } from 'react'
import ProjectCard from '@/components/ProjectCard'
import { projects, getProjectsByCategory } from '@/lib/projects'

const categories = ['All', 'SaaS', 'Fintech', 'Healthcare', 'Civic Tech', 'AI']

export default function ProjectsPage() {
  const [activeCategory, setActiveCategory] = useState('All')

  const filtered = getProjectsByCategory(activeCategory)

  return (
    <div className="min-h-screen pt-24 pb-16 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto">

        <header className="mb-12">
          <p className="text-xs font-semibold text-[#6366f1] uppercase tracking-widest mb-4">
            Work
          </p>
          <h1 className="text-4xl sm:text-5xl font-bold font-syne text-[#f5f5f5] mb-4">
            Projects
          </h1>
          <p className="text-[#a1a1aa] text-lg max-w-xl">
            A selection of SaaS products and side projects I&apos;ve built — from idea to production.
          </p>
        </header>

        <div className="flex flex-wrap gap-2 mb-10">
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setActiveCategory(cat)}
              className={`px-4 py-1.5 rounded-full text-sm font-medium transition-all duration-200 ${
                activeCategory === cat
                  ? 'bg-[#6366f1] text-white'
                  : 'bg-[#111111] border border-[#27272a] text-[#a1a1aa] hover:border-[#6366f1]/50 hover:text-[#f5f5f5]'
              }`}
            >
              {cat}
              {cat === 'All' && (
                <span className="ml-2 text-xs opacity-60">{projects.length}</span>
              )}
            </button>
          ))}
        </div>

        {filtered.length === 0 ? (
          <div className="text-center py-20">
            <p className="text-[#71717a] text-lg">No projects in this category yet.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filtered.map((project) => (
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
        )}

      </div>
    </div>
  )
}
