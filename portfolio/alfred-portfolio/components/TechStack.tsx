interface TechItem {
  name: string
  emoji: string
}

interface TechCategory {
  label: string
  items: TechItem[]
}

const techCategories: TechCategory[] = [
  {
    label: 'Frontend',
    items: [
      { name: 'Next.js', emoji: '▲' },
      { name: 'React', emoji: '⚛' },
      { name: 'TypeScript', emoji: '🔷' },
      { name: 'Tailwind CSS', emoji: '🎨' },
    ],
  },
  {
    label: 'Backend',
    items: [
      { name: 'Node.js', emoji: '🟢' },
      { name: 'Python', emoji: '🐍' },
      { name: 'FastAPI', emoji: '⚡' },
      { name: 'Express.js', emoji: '🚂' },
    ],
  },
  {
    label: 'Database',
    items: [
      { name: 'PostgreSQL', emoji: '🐘' },
      { name: 'Redis', emoji: '🔴' },
      { name: 'Prisma', emoji: '◆' },
    ],
  },
  {
    label: 'Design',
    items: [
      { name: 'Figma', emoji: '🖌' },
      { name: 'Photoshop', emoji: '🖼' },
      { name: 'After Effects', emoji: '✨' },
    ],
  },
  {
    label: 'DevOps',
    items: [
      { name: 'Docker', emoji: '🐳' },
      { name: 'Git', emoji: '🌿' },
      { name: 'Vercel', emoji: '▲' },
      { name: 'GitHub Actions', emoji: '⚙' },
    ],
  },
]

export default function TechStack() {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      {techCategories.map((category) => (
        <div
          key={category.label}
          className="p-5 rounded-xl card-bg"
        >
          <h3 className="text-xs font-semibold text-[#6366f1] uppercase tracking-wider mb-4">
            {category.label}
          </h3>
          <div className="flex flex-wrap gap-2">
            {category.items.map((item) => (
              <span
                key={item.name}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-[#1a1a1a] border border-[#27272a] rounded-lg text-sm text-[#d4d4d8] hover:border-[#6366f1]/40 hover:text-[#f5f5f5] transition-colors duration-200"
              >
                <span
                  className="text-base leading-none"
                  role="img"
                  aria-hidden="true"
                >
                  {item.emoji}
                </span>
                {item.name}
              </span>
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}
