'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { VectraLogo } from '@/components/vectra-logo'
import { PageLoader } from '@/components/page-loader'
import { useAuthStore } from '@/lib/stores/auth'
import { CheckCircle2, ArrowRight, Zap, Target, Calendar } from 'lucide-react'

export default function HomePage() {
  const router = useRouter()
  const { token, isLoading } = useAuthStore()
  const isAuthenticated = !!token

  useEffect(() => {
    // Rehydrate auth store
    useAuthStore.persist.rehydrate()
  }, [])

  useEffect(() => {
    // Redirect to dashboard if authenticated
    if (!isLoading && isAuthenticated) {
      router.push('/dashboard')
    }
  }, [isAuthenticated, isLoading, router])

  // Show loading state while checking auth (même pattern que AuthGuard)
  if (isLoading) {
    return <PageLoader />
  }

  // If authenticated, the useEffect will redirect - show nothing
  if (isAuthenticated) {
    return null
  }

  // Landing page for unauthenticated users
  return (
    <div className="min-h-screen bg-[var(--bg-primary)]">
      {/* Header */}
      <header className="border-b border-[var(--border-primary)]">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <VectraLogo size="sm" />
          <div className="flex items-center gap-4">
            <Button variant="ghost" asChild>
              <Link href="/login">Se connecter</Link>
            </Button>
            <Button asChild>
              <Link href="/register">
                Commencer gratuitement
                <ArrowRight className="ml-2 h-4 w-4" />
              </Link>
            </Button>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-24 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-[var(--color-primary-50)] text-[var(--color-primary-600)] text-sm font-medium mb-8">
            <Zap className="h-4 w-4" />
            Propulse par l&apos;IA
          </div>

          <h1 className="text-display text-[var(--text-primary)] mb-6">
            Powering your pipeline,{' '}
            <span className="text-[var(--color-primary-500)]">simply.</span>
          </h1>

          <p className="text-xl text-[var(--text-secondary)] mb-10 max-w-2xl mx-auto leading-relaxed">
            Agents IA autonomes qui automatisent votre cycle de vente B2B complet.
            Prospection, qualification BANT, et prise de rendez-vous automatique.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" asChild className="text-base px-8">
              <Link href="/register">
                Commencer gratuitement
                <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
            </Button>
            <Button size="lg" variant="outline" asChild className="text-base px-8">
              <Link href="/login">
                Se connecter
              </Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-16 px-6 bg-[var(--bg-secondary)]">
        <div className="max-w-5xl mx-auto">
          <div className="grid md:grid-cols-3 gap-8">
            <div className="p-6 rounded-xl bg-[var(--surface-primary)] border border-[var(--border-primary)]">
              <div className="h-12 w-12 rounded-lg bg-[var(--color-primary-50)] flex items-center justify-center mb-4">
                <Zap className="h-6 w-6 text-[var(--color-primary-500)]" />
              </div>
              <h3 className="text-h4 text-[var(--text-primary)] mb-2">Prospection IA</h3>
              <p className="text-[var(--text-secondary)]">
                Trouvez et enrichissez automatiquement des prospects qualifies grace a notre agent IA.
              </p>
            </div>

            <div className="p-6 rounded-xl bg-[var(--surface-primary)] border border-[var(--border-primary)]">
              <div className="h-12 w-12 rounded-lg bg-[var(--color-success-50)] flex items-center justify-center mb-4">
                <Target className="h-6 w-6 text-[var(--color-success-500)]" />
              </div>
              <h3 className="text-h4 text-[var(--text-primary)] mb-2">Qualification BANT</h3>
              <p className="text-[var(--text-secondary)]">
                Score automatique BANT (Budget, Authority, Need, Timeline) pour chaque prospect.
              </p>
            </div>

            <div className="p-6 rounded-xl bg-[var(--surface-primary)] border border-[var(--border-primary)]">
              <div className="h-12 w-12 rounded-lg bg-[var(--color-info-50)] flex items-center justify-center mb-4">
                <Calendar className="h-6 w-6 text-[var(--color-info-500)]" />
              </div>
              <h3 className="text-h4 text-[var(--text-primary)] mb-2">Prise de RDV</h3>
              <p className="text-[var(--text-secondary)]">
                Emails personnalises et prise de rendez-vous automatique via Calendly.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Stats */}
      <section className="py-16 px-6">
        <div className="max-w-4xl mx-auto">
          <div className="grid grid-cols-3 gap-8 text-center">
            <div>
              <p className="text-h1 text-[var(--color-primary-500)] font-bold">35%</p>
              <p className="text-[var(--text-secondary)] mt-2">Reduction du CAC</p>
            </div>
            <div>
              <p className="text-h1 text-[var(--color-primary-500)] font-bold">120%</p>
              <p className="text-[var(--text-secondary)] mt-2">Plus de leads</p>
            </div>
            <div>
              <p className="text-h1 text-[var(--color-primary-500)] font-bold">6-9</p>
              <p className="text-[var(--text-secondary)] mt-2">Mois ROI</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-16 px-6 bg-gradient-to-r from-[var(--color-primary-500)] to-[var(--color-primary-600)]">
        <div className="max-w-3xl mx-auto text-center">
          <h2 className="text-h1 text-white mb-4">Pret a automatiser vos ventes ?</h2>
          <p className="text-lg text-white/80 mb-8">
            Rejoignez 500+ entreprises B2B qui utilisent Vectra pour accelerer leur croissance.
          </p>
          <Button size="lg" variant="secondary" asChild className="text-base px-8">
            <Link href="/register">
              Commencer gratuitement
              <ArrowRight className="ml-2 h-5 w-5" />
            </Link>
          </Button>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 px-6 border-t border-[var(--border-primary)]">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
          <VectraLogo size="sm" />
          <p className="text-sm text-[var(--text-muted)]">
            2026 Vectra. Tous droits reserves.
          </p>
        </div>
      </footer>
    </div>
  )
}
