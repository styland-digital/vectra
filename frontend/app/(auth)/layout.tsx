'use client'

import { Inter } from 'next/font/google'
import { cn } from '@/lib/utils'
import { CheckCircle2 } from 'lucide-react'
import { VectraLogo } from '@/components/vectra-logo'
import { StaggerContainer, StaggerItem } from '@/components/motion'

const inter = Inter({ subsets: ['latin'] })

export default function AuthLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className={cn('min-h-screen bg-[var(--bg-secondary)] font-sans antialiased', inter.className)}>
      <div className="container relative min-h-screen flex-col items-center justify-center grid lg:max-w-none lg:grid-cols-2 lg:px-0">
        {/* Left side - Branding/Info */}
        <div className="relative hidden h-full flex-col bg-[var(--color-primary-500)] p-10 text-white lg:flex">
          <div className="absolute inset-0 bg-gradient-to-br from-[var(--color-primary-500)] to-[var(--color-primary-700)]" />

          {/* Vectra Logo */}
          <div className="relative z-20">
            <VectraLogo variant="white" size="md" />
          </div>

          {/* Tagline */}
          <div className="relative z-20 mt-auto">
            <blockquote className="space-y-4">
              <p className="text-h1 leading-tight text-white">
                Powering your pipeline, simply.
              </p>
              <p className="text-body-lg text-white/80 leading-relaxed">
                Agents IA autonomes qui automatisent votre cycle de vente B2B complet.
                Prospection, qualification BANT, et prise de rendez-vous.
              </p>
            </blockquote>

            {/* Features */}
            <StaggerContainer className="mt-10 space-y-4" staggerDelay={0.1}>
              <StaggerItem>
                <div className="flex items-center gap-3">
                  <CheckCircle2 className="h-5 w-5 text-white/90" />
                  <span className="text-white/90">Reduction du CAC de 35%</span>
                </div>
              </StaggerItem>
              <StaggerItem>
                <div className="flex items-center gap-3">
                  <CheckCircle2 className="h-5 w-5 text-white/90" />
                  <span className="text-white/90">+120% de leads qualifies</span>
                </div>
              </StaggerItem>
              <StaggerItem>
                <div className="flex items-center gap-3">
                  <CheckCircle2 className="h-5 w-5 text-white/90" />
                  <span className="text-white/90">ROI en 6-9 mois</span>
                </div>
              </StaggerItem>
            </StaggerContainer>

            {/* Stats */}
            <StaggerContainer className="mt-10 grid grid-cols-3 gap-6 pt-10 border-t border-white/20" staggerDelay={0.1}>
              <StaggerItem>
                <div>
                  <p className="text-h1 font-bold text-white">35%</p>
                  <p className="text-body-sm text-white/70 mt-1">Reduction CAC</p>
                </div>
              </StaggerItem>
              <StaggerItem>
                <div>
                  <p className="text-h1 font-bold text-white">120%</p>
                  <p className="text-body-sm text-white/70 mt-1">Plus de leads</p>
                </div>
              </StaggerItem>
              <StaggerItem>
                <div>
                  <p className="text-h1 font-bold text-white">6-9</p>
                  <p className="text-body-sm text-white/70 mt-1">Mois ROI</p>
                </div>
              </StaggerItem>
            </StaggerContainer>
          </div>

          {/* Footer */}
          <div className="relative z-20 mt-10 text-body-sm text-white/60">
            Trusted by 500+ B2B companies worldwide
          </div>
        </div>

        {/* Right side - Auth forms */}
        <div className="flex items-center justify-center p-8 bg-[var(--bg-primary)]">
          <div className="mx-auto flex w-full flex-col justify-center space-y-6 sm:w-[400px]">
            {children}
          </div>
        </div>
      </div>
    </div>
  )
}
