'use client'

import { VectraLogo } from '@/components/vectra-logo'
import { ThemeSwitcher } from '@/components/theme-switcher'
import { LanguageSwitcher } from '@/components/language-switcher'

export default function AuthLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="relative min-h-screen bg-[var(--bg-primary)] font-sans antialiased">
      {/* Controls — top-right overlay */}
      <div className="absolute top-5 right-5 flex items-center gap-1 z-10">
        <ThemeSwitcher />
        <LanguageSwitcher />
      </div>

      {/* Centered form */}
      <div className="flex min-h-screen flex-col items-center justify-center px-4 py-16">
        <div className="mb-10">
          <VectraLogo size="md" />
        </div>
        <div className="w-full sm:w-[420px]">
          {children}
        </div>
      </div>
    </div>
  )
}
