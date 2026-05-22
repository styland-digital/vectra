'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { cn } from '@/lib/utils'

const navLinks = [
  { href: '/', label: 'Home' },
  { href: '/projects', label: 'Projects' },
  { href: '/about', label: 'About' },
  { href: '/contact', label: 'Contact' },
]

export default function Navbar() {
  const [isScrolled, setIsScrolled] = useState(false)
  const [isMobileOpen, setIsMobileOpen] = useState(false)
  const pathname = usePathname()

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20)
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  useEffect(() => {
    setIsMobileOpen(false)
  }, [pathname])

  useEffect(() => {
    if (isMobileOpen) {
      document.body.style.overflow = 'hidden'
    } else {
      document.body.style.overflow = ''
    }
    return () => {
      document.body.style.overflow = ''
    }
  }, [isMobileOpen])

  return (
    <header
      className={cn(
        'fixed top-0 left-0 right-0 z-50 transition-all duration-300',
        isScrolled
          ? 'bg-[#0a0a0a]/90 backdrop-blur-md border-b border-[#27272a]'
          : 'bg-transparent'
      )}
    >
      <nav className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link
            href="/"
            className="text-xl font-bold font-syne text-accent hover:opacity-80 transition-opacity"
            style={{ color: '#6366f1' }}
          >
            Alfred.
          </Link>

          <ul className="hidden md:flex items-center gap-8">
            {navLinks.map((link) => (
              <li key={link.href}>
                <Link
                  href={link.href}
                  className={cn(
                    'text-sm font-medium transition-colors duration-200 hover:text-[#6366f1]',
                    pathname === link.href
                      ? 'text-[#6366f1]'
                      : 'text-[#a1a1aa]'
                  )}
                >
                  {link.label}
                </Link>
              </li>
            ))}
          </ul>

          <button
            onClick={() => setIsMobileOpen(!isMobileOpen)}
            className="md:hidden flex flex-col gap-1.5 p-2 rounded-md hover:bg-[#1a1a1a] transition-colors"
            aria-label="Toggle mobile menu"
            aria-expanded={isMobileOpen}
          >
            <span
              className={cn(
                'block w-5 h-0.5 bg-[#f5f5f5] transition-all duration-300',
                isMobileOpen && 'translate-y-2 rotate-45'
              )}
            />
            <span
              className={cn(
                'block w-5 h-0.5 bg-[#f5f5f5] transition-all duration-300',
                isMobileOpen && 'opacity-0'
              )}
            />
            <span
              className={cn(
                'block w-5 h-0.5 bg-[#f5f5f5] transition-all duration-300',
                isMobileOpen && '-translate-y-2 -rotate-45'
              )}
            />
          </button>
        </div>
      </nav>

      {isMobileOpen && (
        <div className="md:hidden fixed inset-0 top-16 bg-[#0a0a0a] z-40">
          <ul className="flex flex-col items-center justify-center gap-8 h-full">
            {navLinks.map((link) => (
              <li key={link.href}>
                <Link
                  href={link.href}
                  className={cn(
                    'text-2xl font-semibold font-syne transition-colors duration-200 hover:text-[#6366f1]',
                    pathname === link.href
                      ? 'text-[#6366f1]'
                      : 'text-[#f5f5f5]'
                  )}
                >
                  {link.label}
                </Link>
              </li>
            ))}
          </ul>
        </div>
      )}
    </header>
  )
}
