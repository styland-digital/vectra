'use client'

import { useQuery } from '@tanstack/react-query'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import Link from 'next/link'
import {
  Target,
  Mail,
  Settings,
  Users,
  Calendar,
  TrendingUp,
  TrendingDown,
  ArrowRight,
  Sparkles,
  Plus,
} from 'lucide-react'
import { api } from '@/lib/api'
import { LoadingSkeleton } from '@/components/loading-skeleton'
import { PageTransition, StaggerContainer, StaggerItem } from '@/components/motion'
import { useTranslation } from '@/lib/i18n'
import type { AnalyticsDashboard } from '@/types'

interface StatCardProps {
  title: string
  value: string
  change: number
  description: string
  icon: React.ComponentType<{ className?: string }>
  iconColor?: string
}

function StatCard({ title, value, change, description, icon: Icon, iconColor = 'var(--color-primary-500)' }: StatCardProps) {
  const isPositive = change >= 0

  return (
    <Card className="bg-[var(--surface-primary)] border-[var(--border-primary)] interactive-card group">
      <CardContent className="p-6">
        <div className="flex items-start justify-between">
          <div className="space-y-3">
            <p className="text-body-sm text-[var(--text-secondary)]">{title}</p>
            <p className="text-h2 text-[var(--text-primary)] font-semibold">{value}</p>
            <div className="flex items-center gap-2">
              {isPositive ? (
                <TrendingUp className="h-4 w-4 text-[var(--color-success-500)]" />
              ) : (
                <TrendingDown className="h-4 w-4 text-[var(--color-error-500)]" />
              )}
              <span className={`text-caption font-medium ${isPositive ? 'text-[var(--color-success-600)]' : 'text-[var(--color-error-600)]'}`}>
                {isPositive ? '+' : ''}{change}%
              </span>
              <span className="text-caption text-[var(--text-muted)]">{description}</span>
            </div>
          </div>
          <div className="h-12 w-12 rounded-xl flex items-center justify-center bg-[var(--surface-secondary)] group-hover:scale-110 transition-transform duration-200">
            <Icon className="h-6 w-6 text-[var(--color-primary-500)]" />
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

interface QuickActionProps {
  href: string
  icon: React.ComponentType<{ className?: string }>
  title: string
  description: string
}

function QuickAction({ href, icon: Icon, title, description }: QuickActionProps) {
  return (
    <Link
      href={href}
      className="flex items-center gap-4 p-4 rounded-xl bg-[var(--surface-secondary)] hover:bg-[var(--surface-hover)] transition-colors duration-200 group"
    >
      <div className="h-10 w-10 rounded-lg bg-[var(--color-primary-50)] flex items-center justify-center group-hover:bg-[var(--color-primary-100)] transition-colors duration-200">
        <Icon className="h-5 w-5 text-[var(--color-primary-500)]" />
      </div>
      <div className="flex-1">
        <p className="text-body-sm font-medium text-[var(--text-primary)]">{title}</p>
        <p className="text-caption text-[var(--text-muted)]">{description}</p>
      </div>
      <ArrowRight className="h-4 w-4 text-[var(--text-muted)] group-hover:text-[var(--text-secondary)] group-hover:translate-x-1 transition-all duration-200" />
    </Link>
  )
}

const fallbackData: AnalyticsDashboard = {
  overview: { active_campaigns: 0, qualified_leads: 0, emails_sent: 0, ai_success_rate: 0 },
  growth: { leads_current: 0, leads_previous: 0, leads_change: 0, emails_current: 0, emails_previous: 0, emails_change: 0 },
  team: { total_users: 0, active_users: 0, user_activity_rate: 0, role_distribution: {} },
  ai_agents: { total_agent_runs: 0, successful_runs: 0, success_rate: 0, prospector_runs: 0, bant_runs: 0, scheduler_runs: 0, period_days: 30 },
  subscription: { plan: 'starter', status: 'active', leads_used: 0, leads_limit: 500 },
  generated_at: new Date().toISOString(),
}

export default function DashboardPage() {
  const { t } = useTranslation()

  const { data: analytics, isLoading } = useQuery({
    queryKey: ['analytics', 'overview'],
    queryFn: async () => {
      const res = await api.analytics.overview()
      return res.data
    },
  })

  const data = analytics ?? fallbackData

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div>
          <h1 className="text-h1 text-[var(--text-primary)]">{t('dashboard.title')}</h1>
          <p className="text-body text-[var(--text-secondary)] mt-1">{t('dashboard.subtitle')}</p>
        </div>
        <LoadingSkeleton variant="stats" />
        <div className="grid gap-6 lg:grid-cols-2">
          <LoadingSkeleton variant="card" />
          <LoadingSkeleton variant="card" />
        </div>
      </div>
    )
  }

  const stats = [
    {
      title: t('dashboard.stats.prospects'),
      value: data.overview.qualified_leads.toLocaleString(),
      change: data.growth.leads_change,
      description: t('dashboard.stats.thisMonth'),
      icon: Users,
      iconColor: 'var(--color-primary-500)',
    },
    {
      title: t('dashboard.stats.qualificationRate'),
      value: `${Math.round(data.ai_agents.success_rate)}%`,
      change: 5,
      description: t('dashboard.stats.bantScore'),
      icon: Target,
      iconColor: 'var(--color-success-500)',
    },
    {
      title: t('dashboard.stats.meetings'),
      value: data.overview.emails_sent.toLocaleString(),
      change: data.growth.emails_change,
      description: t('dashboard.stats.thisWeek'),
      icon: Calendar,
      iconColor: 'var(--color-info-500)',
    },
    {
      title: t('dashboard.stats.roi'),
      value: `${data.overview.active_campaigns}`,
      change: 15,
      description: t('dashboard.stats.returnOnInvestment'),
      icon: TrendingUp,
      iconColor: 'var(--color-accent-500)',
    }
  ]

  const usagePercentage = Math.min((data.subscription.leads_used / data.subscription.leads_limit) * 100, 100)

  return (
    <PageTransition>
      <div className="space-y-8">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h1 className="text-h1 text-[var(--text-primary)]">{t('dashboard.title')}</h1>
            <p className="text-body text-[var(--text-secondary)] mt-1">
              {t('dashboard.subtitle')}
            </p>
          </div>
          <Button asChild className="bg-[var(--color-primary-500)] hover:bg-[var(--color-primary-600)] text-white shadow-sm">
            <Link href="/campaigns/new">
              <Plus className="mr-2 h-4 w-4" />
              {t('dashboard.newCampaign')}
            </Link>
          </Button>
        </div>

        {/* Stats Grid */}
        <StaggerContainer className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {stats.map((stat) => (
            <StaggerItem key={stat.title}>
              <StatCard {...stat} />
            </StaggerItem>
          ))}
        </StaggerContainer>

        <div className="grid gap-6 lg:grid-cols-3">
          {/* Quick Actions */}
          <Card className="lg:col-span-2 bg-[var(--surface-primary)] border-[var(--border-primary)]">
            <CardHeader className="pb-4">
              <CardTitle className="text-h4 text-[var(--text-primary)]">{t('dashboard.quickActions')}</CardTitle>
              <CardDescription className="text-body-sm text-[var(--text-secondary)]">
                {t('dashboard.quickActionsDescription')}
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              <QuickAction
                href="/campaigns/new"
                icon={Target}
                title={t('dashboard.newCampaign')}
                description="Start a new AI-powered campaign"
              />
              <QuickAction
                href="/leads"
                icon={Users}
                title={t('dashboard.manageProspects')}
                description="View and manage your qualified leads"
              />
              <QuickAction
                href="/emails"
                icon={Mail}
                title={t('dashboard.pendingEmails')}
                description="Review and approve pending emails"
              />
              <QuickAction
                href="/settings"
                icon={Settings}
                title={t('dashboard.configureIntegrations')}
                description="Connect your tools and APIs"
              />
            </CardContent>
          </Card>

          {/* Subscription & AI Info */}
          <Card className="bg-[var(--surface-primary)] border-[var(--border-primary)]">
            <CardHeader className="pb-4">
              <div className="flex items-center justify-between">
                <CardTitle className="text-h4 text-[var(--text-primary)]">{t('dashboard.recentActivity')}</CardTitle>
                <Badge variant="secondary" className="bg-[var(--color-primary-50)] text-[var(--color-primary-600)] hover:bg-[var(--color-primary-100)] capitalize">
                  {data.subscription.plan}
                </Badge>
              </div>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Usage Progress */}
              <div className="space-y-2">
                <div className="flex items-center justify-between text-body-sm">
                  <span className="text-[var(--text-secondary)]">Leads Used</span>
                  <span className="font-medium text-[var(--text-primary)]">
                    {data.subscription.leads_used} / {data.subscription.leads_limit}
                  </span>
                </div>
                <div className="h-2 w-full bg-[var(--surface-secondary)] rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-[var(--color-primary-500)] to-[var(--color-primary-400)] rounded-full transition-all duration-500"
                    style={{ width: `${usagePercentage}%` }}
                  />
                </div>
                <p className="text-caption text-[var(--text-muted)]">
                  {Math.round(100 - usagePercentage)}% remaining this month
                </p>
              </div>

              {/* AI Stats */}
              <div className="space-y-4 pt-4 border-t border-[var(--border-secondary)]">
                <div className="flex items-center gap-3">
                  <div className="h-8 w-8 rounded-lg bg-[var(--color-success-50)] flex items-center justify-center">
                    <Sparkles className="h-4 w-4 text-[var(--color-success-500)]" />
                  </div>
                  <div className="flex-1">
                    <p className="text-body-sm font-medium text-[var(--text-primary)]">AI Success Rate</p>
                    <p className="text-caption text-[var(--text-muted)]">Last 30 days</p>
                  </div>
                  <span className="text-h4 font-semibold text-[var(--color-success-600)]">
                    {Math.round(data.ai_agents.success_rate)}%
                  </span>
                </div>

                <div className="flex items-center gap-3">
                  <div className="h-8 w-8 rounded-lg bg-[var(--color-primary-50)] flex items-center justify-center">
                    <Target className="h-4 w-4 text-[var(--color-primary-500)]" />
                  </div>
                  <div className="flex-1">
                    <p className="text-body-sm font-medium text-[var(--text-primary)]">Active Campaigns</p>
                    <p className="text-caption text-[var(--text-muted)]">Currently running</p>
                  </div>
                  <span className="text-h4 font-semibold text-[var(--text-primary)]">
                    {data.overview.active_campaigns}
                  </span>
                </div>

                <div className="flex items-center gap-3">
                  <div className="h-8 w-8 rounded-lg bg-[var(--color-info-50)] flex items-center justify-center">
                    <Mail className="h-4 w-4 text-[var(--color-info-500)]" />
                  </div>
                  <div className="flex-1">
                    <p className="text-body-sm font-medium text-[var(--text-primary)]">Emails Sent</p>
                    <p className="text-caption text-[var(--text-muted)]">This month</p>
                  </div>
                  <span className="text-h4 font-semibold text-[var(--text-primary)]">
                    {data.overview.emails_sent}
                  </span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </PageTransition>
  )
}
