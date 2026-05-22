import Link from 'next/link'

const socialLinks = [
  {
    label: 'GitHub',
    href: 'https://github.com/styland-digital',
    icon: (
      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
        <path d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0 1 12 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z" />
      </svg>
    ),
  },
  {
    label: 'Dribbble',
    href: 'https://dribbble.com/styland-digital',
    icon: (
      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
        <path d="M12 24C5.385 24 0 18.615 0 12S5.385 0 12 0s12 5.385 12 12-5.385 12-12 12zm10.12-10.358c-.35-.11-3.17-.953-6.384-.438 1.34 3.684 1.887 6.684 1.992 7.308 2.3-1.555 3.936-4.02 4.395-6.87zm-6.115 7.808c-.153-.9-.75-4.032-2.19-7.77l-.066.02c-5.79 2.015-7.86 6.025-8.048 6.379 1.73 1.35 3.92 2.165 6.298 2.165 1.42 0 2.77-.29 4.006-.794zm-9.84-2.58c.25-.445 3.182-5.197 8.409-6.9a19.88 19.88 0 0 0-.518-1.09c-4.986 1.49-9.83 1.43-10.275 1.42a10.05 10.05 0 0 0 2.385 6.57zm-2.645-8.97c.453.006 4.562 0 9.284-1.22A58.63 58.63 0 0 0 10 5.5c-2.13 3.21-4.46 5.58-4.69 5.81a10.07 10.07 0 0 1-.79-1.01zM7.37 4.33a54.04 54.04 0 0 1 2.823 3.26C12.944 6.5 15.4 4.89 16.132 4.4c-1.29-1.02-2.9-1.65-4.66-1.65-1.46 0-2.84.39-4.1 1.08zm9.98 1.38c-.822.58-3.397 2.29-6.238 3.42.2.411.39.835.56 1.263.06.15.12.3.17.45 3.37-.424 6.72.27 7.065.336a9.993 9.993 0 0 0-1.557-5.469z" />
      </svg>
    ),
  },
  {
    label: 'Email',
    href: 'mailto:alfredlandrytalom2004@gmail.com',
    icon: (
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
        <rect width="20" height="16" x="2" y="4" rx="2" />
        <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7" />
      </svg>
    ),
  },
]

export default function Footer() {
  return (
    <footer className="border-t border-[#27272a] py-8 mt-16">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-[#a1a1aa] text-sm">
            &copy; {new Date().getFullYear()}{' '}
            <span className="text-[#6366f1] font-medium">Alfred Landry Talom</span>
            {' '}— styland-digital
          </p>

          <div className="flex items-center gap-5">
            {socialLinks.map((link) => (
              <a
                key={link.label}
                href={link.href}
                target={link.href.startsWith('mailto') ? undefined : '_blank'}
                rel={link.href.startsWith('mailto') ? undefined : 'noopener noreferrer'}
                className="text-[#a1a1aa] hover:text-[#6366f1] transition-colors duration-200"
                aria-label={link.label}
              >
                {link.icon}
              </a>
            ))}
          </div>
        </div>
      </div>
    </footer>
  )
}
