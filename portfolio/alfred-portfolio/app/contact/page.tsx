import type { Metadata } from 'next'
import ContactForm from '@/components/ContactForm'

export const metadata: Metadata = {
  title: 'Contact — Alfred Landry Talom',
  description:
    'Get in touch with Alfred Landry Talom. Available for CDI positions and remote freelance projects.',
}

const contactLinks = [
  {
    label: 'Email',
    value: 'alfredlandrytalom2004@gmail.com',
    href: 'mailto:alfredlandrytalom2004@gmail.com',
    icon: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
        <rect width="20" height="16" x="2" y="4" rx="2" />
        <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7" />
      </svg>
    ),
  },
  {
    label: 'GitHub',
    value: 'github.com/styland-digital',
    href: 'https://github.com/styland-digital',
    icon: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
        <path d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0 1 12 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z" />
      </svg>
    ),
  },
  {
    label: 'Dribbble',
    value: 'dribbble.com/styland-digital',
    href: 'https://dribbble.com/styland-digital',
    icon: (
      <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
        <path d="M12 24C5.385 24 0 18.615 0 12S5.385 0 12 0s12 5.385 12 12-5.385 12-12 12zm10.12-10.358c-.35-.11-3.17-.953-6.384-.438 1.34 3.684 1.887 6.684 1.992 7.308 2.3-1.555 3.936-4.02 4.395-6.87zm-6.115 7.808c-.153-.9-.75-4.032-2.19-7.77l-.066.02c-5.79 2.015-7.86 6.025-8.048 6.379 1.73 1.35 3.92 2.165 6.298 2.165 1.42 0 2.77-.29 4.006-.794zm-9.84-2.58c.25-.445 3.182-5.197 8.409-6.9a19.88 19.88 0 0 0-.518-1.09c-4.986 1.49-9.83 1.43-10.275 1.42a10.05 10.05 0 0 0 2.385 6.57zm-2.645-8.97c.453.006 4.562 0 9.284-1.22A58.63 58.63 0 0 0 10 5.5c-2.13 3.21-4.46 5.58-4.69 5.81a10.07 10.07 0 0 1-.79-1.01zM7.37 4.33a54.04 54.04 0 0 1 2.823 3.26C12.944 6.5 15.4 4.89 16.132 4.4c-1.29-1.02-2.9-1.65-4.66-1.65-1.46 0-2.84.39-4.1 1.08zm9.98 1.38c-.822.58-3.397 2.29-6.238 3.42.2.411.39.835.56 1.263.06.15.12.3.17.45 3.37-.424 6.72.27 7.065.336a9.993 9.993 0 0 0-1.557-5.469z" />
      </svg>
    ),
  },
]

export default function ContactPage() {
  return (
    <div className="min-h-screen pt-24 pb-16 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl mx-auto">

        <header className="mb-16">
          <p className="text-xs font-semibold text-[#6366f1] uppercase tracking-widest mb-4">
            Contact
          </p>
          <h1 className="text-4xl sm:text-5xl font-bold font-syne text-[#f5f5f5] mb-4 leading-tight">
            Let&apos;s build something
          </h1>
          <p className="text-lg text-[#a1a1aa] max-w-lg">
            Available for CDI positions or remote freelance projects. If you have an idea or a problem to solve, let&apos;s talk.
          </p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-5 gap-12">

          <div className="lg:col-span-3">
            <ContactForm />
          </div>

          <div className="lg:col-span-2 flex flex-col gap-8">

            <div>
              <h2 className="text-sm font-semibold text-[#f5f5f5] mb-5">
                Reach me directly
              </h2>
              <div className="flex flex-col gap-3">
                {contactLinks.map((link) => (
                  <a
                    key={link.label}
                    href={link.href}
                    target={link.href.startsWith('mailto') ? undefined : '_blank'}
                    rel={link.href.startsWith('mailto') ? undefined : 'noopener noreferrer'}
                    className="flex items-center gap-3 p-4 rounded-lg card-bg hover:border-[#6366f1]/40 transition-all duration-200 group"
                  >
                    <span className="text-[#6366f1] shrink-0">{link.icon}</span>
                    <div className="min-w-0">
                      <p className="text-xs font-medium text-[#71717a] mb-0.5">{link.label}</p>
                      <p className="text-sm font-medium text-[#d4d4d8] group-hover:text-[#6366f1] transition-colors duration-200 truncate">
                        {link.value}
                      </p>
                    </div>
                  </a>
                ))}
              </div>
            </div>

            <div className="p-5 rounded-xl card-bg">
              <div className="flex items-start gap-3">
                <span className="text-[#6366f1] shrink-0 mt-0.5">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                    <path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z" />
                    <circle cx="12" cy="10" r="3" />
                  </svg>
                </span>
                <div>
                  <p className="text-sm font-semibold text-[#f5f5f5] mb-1">
                    Douala, Cameroun{' '}
                    <span role="img" aria-label="Cameroon flag">🇨🇲</span>
                  </p>
                  <p className="text-xs text-[#71717a] leading-relaxed">
                    UTC+1 (WAT). Available for remote work worldwide. Open to relocating for CDI opportunities in Europe.
                  </p>
                </div>
              </div>
            </div>

            <div className="p-5 rounded-xl bg-[#6366f1]/5 border border-[#6366f1]/20">
              <div className="flex items-center gap-2 mb-2">
                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                <span className="text-xs font-semibold text-emerald-400">Available now</span>
              </div>
              <p className="text-sm text-[#a1a1aa]">
                Currently open to new opportunities. Typical response time: within 24 hours.
              </p>
            </div>

          </div>
        </div>

      </div>
    </div>
  )
}
