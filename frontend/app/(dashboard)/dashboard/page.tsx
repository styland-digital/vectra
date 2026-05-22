'use client'

import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { KPIGrid } from '@/components/features/kpi-grid'
import { useDashboardKPIs } from '@/lib/hooks/useKPIs'
import { SubscriptionUsage } from '@/components/features/subscription-usage'
import { VectraBarChart } from '@/components/charts/vectra-bar-chart'
import Link from 'next/link'
import {
  Target,
  Mail,
  Settings,
  Users,
  ArrowRight,
  Plus,
  TrendingUp,
  Bot,
  BarChart2,
  Rocket,
} from 'lucide-react'
import { api } from '@/lib/api'
import { PageTransition } from '@/components/motion'
import { useTranslation } from '@/lib/i18n'
import { useAuthStore } from '@/lib/stores/auth'
import { cn } from '@/lib/utils'
import type { AnalyticsDashboard } from '@/types'

type Period = 7 | 30 | 90

// Fallback data used as placeholder while queries load
const fallbackData: AnalyticsDashboard = {
  overview: { active_campaigns: 0, qualified_leads: 0, emails_sent: 0, ai_success_rate: 0 },
  growth: { leads_current: 0, leads_previous: 0, leads_change: 0, emails_current: 0, emails_previous: 0, emails_change: 0 },
  team: { total_users: 0, active_users: 0, user_activity_rate: 0, role_distribution: {}, period_days: 30 },
  ai_agents: { total_agent_runs: 0, successful_runs: 0, success_rate: 0, prospector_runs: 0, bant_runs: 0, scheduler_runs: 0, period_days: 30 },
  subscription: { plan: 'starter', status: 'active', leads_used: 0, leads_limit: 500 },
  generated_at: new Date().toISOString(),
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
      className="flex items-center gap-3 p-3 rounded-lg border border-[var(--border-primary)] bg-[var(--surface-primary)] hover:bg-[var(--surface-hover)] hover:border-[var(--border-hover)] transition-colors duration-200 group"
    >
      <div className="h-8 w-8 rounded-lg bg-[var(--surface-secondary)] flex items-center justify-center shrink-0">
        <Icon className="h-4 w-4 text-[var(--text-muted)]" />
      </div>
      <div className="flex-1 min-w-0">
        <p className="text-body-sm font-medium text-[var(--text-primary)]">{title}</p>
        <p className="text-caption text-[var(--text-muted)] truncate">{description}</p>
      </div>
      <ArrowRight className="h-4 w-4 text-[var(--text-muted)] group-hover:text-[var(--text-secondary)] group-hover:translate-x-0.5 transition-all duration-200 shrink-0" />
    </Link>
  )
}

function PeriodSelector({ value, onChange }: { value: Period; onChange: (v: Period) => void }) {
  return (
    <div className="flex items-stretch h-10 rounded-lg border border-[var(--border-primary)] bg-[var(--surface-secondary)] p-0.5 gap-0.5">
      {([7, 30, 90] as Period[]).map((d) => (
        <button
          key={d}
          onClick={() => onChange(d)}
          className={cn(
            "flex items-center px-3 text-body-sm rounded-md transition-colors duration-150",
            value === d
              ? "bg-[var(--surface-primary)] text-[var(--text-primary)] font-medium shadow-sm"
              : "text-[var(--text-muted)] hover:text-[var(--text-secondary)]"
          )}
        >
          {d}d
        </button>
      ))}
    </div>
  )
}

interface ChartEmptyStateProps {
  icon: React.ComponentType<{ className?: string }>
  title: string
  description: string
  actionLabel?: string
  actionHref?: string
}

function ChartEmptyState({ icon: Icon, title, description, actionLabel, actionHref }: ChartEmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center h-[220px] gap-3 text-center">
      <div className="h-10 w-10 rounded-full bg-[var(--surface-secondary)] flex items-center justify-center">
        <Icon className="h-5 w-5 text-[var(--text-muted)]" />
      </div>
      <div>
        <p className="text-body-sm font-medium text-[var(--text-secondary)]">{title}</p>
        <p className="text-caption text-[var(--text-muted)] mt-0.5">{description}</p>
      </div>
      {actionLabel && actionHref && (
        <Button asChild size="sm" variant="outline" className="mt-1">
          <Link href={actionHref}>
            <Plus className="mr-1.5 h-3.5 w-3.5" />
            {actionLabel}
          </Link>
        </Button>
      )}
    </div>
  )
}

export default function DashboardPage() {
  const { t } = useTranslation()
  const { user } = useAuthStore()
  const [period, setPeriod] = useState<Period>(30)

  // placeholderData renders immediately — no skeleton shown, data replaces placeholder when ready
  const { data: analytics, isFetching: overviewFetching } = useQuery({
    queryKey: ['analytics', 'overview'],
    queryFn: async () => {
      const res = await api.analytics.overview()
      return res.data
    },
    placeholderData: fallbackData,
    staleTime: 2 * 60 * 1000,
    retry: 1,
  })

  const { data: aiAgents } = useQuery({
    queryKey: ['analytics', 'ai-agents', period],
    queryFn: async () => {
      const res = await api.analytics.aiAgents(period)
      return res.data
    },
    placeholderData: fallbackData.ai_agents,
    staleTime: 5 * 60 * 1000,
    retry: 1,
  })

  const data = analytics ?? fallbackData
  const agents = aiAgents ?? data.ai_agents

  const kpis = useDashboardKPIs(data)

  // Detect whether the current data is the placeholder (all zeros = empty account)
  const hasGrowthData = data.growth.leads_current > 0 || data.growth.emails_current > 0 || data.growth.leads_previous > 0
  const hasAgentData = agents.total_agent_runs > 0

  // Growth chart data
  const growthData = [
    { name: 'Leads',  Previous: data.growth.leads_previous,  Current: data.growth.leads_current },
    { name: 'Emails', Previous: data.growth.emails_previous, Current: data.growth.emails_current },
  ]
  const growthSeries = [
    { key: 'Previous', label: 'Previous period', color: 'var(--border-hover)' },
    { key: 'Current',  label: 'Current period',  color: 'var(--color-primary-500)' },
  ]

  // AI agents chart data
  const agentsData = [
    { name: 'Prospector', 'Agent runs': agents.prospector_runs },
    { name: 'BANT',       'Agent runs': agents.bant_runs },
    { name: 'Scheduler',  'Agent runs': agents.scheduler_runs },
  ]
  const agentsSeries = [
    { key: 'Agent runs', label: 'Agent runs', color: 'var(--color-vectra-yellow-500)' },
  ]

  const firstName = user?.first_name ?? ''

  return (
    <PageTransition>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h1 className="text-h1 text-[var(--text-primary)]">
              {t('dashboard.welcomeBack')}{firstName ? `, ${firstName}` : ''}
            </h1>
            <p className="text-body text-[var(--text-secondary)] mt-1">
              {t('dashboard.subtitle')}
            </p>
          </div>
          <div className="flex items-center gap-3">
            <PeriodSelector value={period} onChange={setPeriod} />
            <Button asChild>
              <Link href="/campaigns/new">
                <Plus className="mr-2 h-4 w-4" />
                {t('dashboard.newCampaign')}
              </Link>
            </Button>
          </div>
        </div>

        {/* KPI Grid — always shows, zeros are meaningful */}
        <KPIGrid kpis={kpis} isLoading={overviewFetching && !analytics} />

        {/* Row 2: Growth chart + Subscription */}
        <div className="grid gap-6 lg:grid-cols-3">
          {/* Growth Analytics */}
          <Card className="lg:col-span-2 bg-[var(--surface-primary)] border-[var(--border-primary)] rounded-xl shadow-none">
            <CardHeader className="pb-2">
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="text-h4 text-[var(--text-primary)] flex items-center gap-2">
                    <TrendingUp className="h-4 w-4 text-[var(--color-primary-500)]" />
                    {t('dashboard.growthAnalytics')}
                  </CardTitle>
                  <CardDescription className="text-body-sm text-[var(--text-muted)] mt-0.5">
                    {t('dashboard.growthDescription').replace('{period}', String(period))}
                  </CardDescription>
                </div>
                {hasGrowthData && (
                  <div className="flex items-center gap-3 text-caption text-[var(--text-muted)]">
                    <span className={cn(
                      "inline-flex items-center gap-1 font-medium rounded-full px-2 py-0.5",
                      data.growth.leads_change >= 0
                        ? "bg-[var(--color-success-500)]/10 text-[var(--color-success-600)]"
                        : "bg-[var(--color-error-500)]/10 text-[var(--color-error-600)]"
                    )}>
                      {data.growth.leads_change >= 0 ? "+" : ""}{data.growth.leads_change}% leads
                    </span>
                    <span className={cn(
                      "inline-flex items-center gap-1 font-medium rounded-full px-2 py-0.5",
                      data.growth.emails_change >= 0
                        ? "bg-[var(--color-success-500)]/10 text-[var(--color-success-600)]"
                        : "bg-[var(--color-error-500)]/10 text-[var(--color-error-600)]"
                    )}>
                      {data.growth.emails_change >= 0 ? "+" : ""}{data.growth.emails_change}% emails
                    </span>
                  </div>
                )}
              </div>
            </CardHeader>
            <CardContent className="pt-2">
              {hasGrowthData ? (
                <VectraBarChart
                  data={growthData}
                  series={growthSeries}
                  xKey="name"
                  height={220}
                />
              ) : (
                <ChartEmptyState
                  icon={BarChart2}
                  title={t('dashboard.noGrowthTitle')}
                  description={t('dashboard.noGrowthDescription')}
                  actionLabel={t('dashboard.newCampaign')}
                  actionHref="/campaigns"
                />
              )}
            </CardContent>
          </Card>

          {/* Subscription Usage */}
          <Card className="bg-[var(--surface-primary)] border-[var(--border-primary)] rounded-xl shadow-none">
            <CardHeader className="pb-2">
              <CardTitle className="text-h4 text-[var(--text-primary)]">{t('dashboard.subscription')}</CardTitle>
              <CardDescription className="text-body-sm text-[var(--text-muted)]">
                {t('dashboard.subscriptionDescription')}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <SubscriptionUsage
                leadsUsed={data.subscription.leads_used}
                leadsLimit={data.subscription.leads_limit}
                plan={data.subscription.plan}
              />
            </CardContent>
          </Card>
        </div>

        {/* Row 3: AI Agents + Quick Actions */}
        <div className="grid gap-6 lg:grid-cols-3">
          {/* AI Agents Performance */}
          <Card className="lg:col-span-2 bg-[var(--surface-primary)] border-[var(--border-primary)] rounded-xl shadow-none">
            <CardHeader className="pb-2">
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="text-h4 text-[var(--text-primary)] flex items-center gap-2">
                    <Bot className="h-4 w-4 text-[var(--color-vectra-yellow-500)]" />
                    {t('dashboard.aiAgents')}
                  </CardTitle>
                  <CardDescription className="text-body-sm text-[var(--text-muted)] mt-0.5">
                    {hasAgentData
                      ? `${agents.total_agent_runs} ${t('dashboard.growthDescription').replace('{period}', String(period))}`
                      : t('dashboard.growthDescription').replace('{period}', String(period))}
                  </CardDescription>
                </div>
                {hasAgentData && (
                  <span className="inline-flex items-center gap-1 bg-[var(--color-success-500)]/10 text-[var(--color-success-600)] text-caption font-medium rounded-full px-2 py-0.5">
                    {Math.round(agents.success_rate)}% success
                  </span>
                )}
              </div>
            </CardHeader>
            <CardContent className="pt-2">
              {hasAgentData ? (
                <VectraBarChart
                  data={agentsData}
                  series={agentsSeries}
                  xKey="name"
                  height={220}
                  showLegend={false}
                />
              ) : (
                <ChartEmptyState
                  icon={Rocket}
                  title={t('dashboard.noAgentTitle')}
                  description={t('dashboard.noAgentDescription')}
                  actionLabel={t('dashboard.newCampaign')}
                  actionHref="/campaigns"
                />
              )}
            </CardContent>
          </Card>

          {/* Quick Actions */}
          <Card className="bg-[var(--surface-primary)] border-[var(--border-primary)] rounded-xl shadow-none">
            <CardHeader className="pb-3">
              <CardTitle className="text-h4 text-[var(--text-primary)]">{t('dashboard.quickActions')}</CardTitle>
              <CardDescription className="text-body-sm text-[var(--text-muted)]">
                {t('dashboard.quickActionsDescription')}
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-2">
              <QuickAction
                href="/campaigns/new"
                icon={Target}
                title={t('dashboard.newCampaign')}
                description="Start an AI-powered campaign"
              />
              <QuickAction
                href="/leads"
                icon={Users}
                title={t('dashboard.manageProspects')}
                description="Manage your qualified leads"
              />
              <QuickAction
                href="/emails"
                icon={Mail}
                title={t('dashboard.pendingEmails')}
                description="Review pending emails"
              />
              <QuickAction
                href="/settings"
                icon={Settings}
                title={t('dashboard.configureIntegrations')}
                description="Connect your tools and APIs"
              />
            </CardContent>
          </Card>
        </div>
      </div>
    </PageTransition>
  )
}
