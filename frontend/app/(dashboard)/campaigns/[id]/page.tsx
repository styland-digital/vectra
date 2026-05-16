'use client'

import { useState } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { format, differenceInDays } from 'date-fns'
import {
  ArrowLeft, Play, Pause, RotateCcw, Trash2, Users, Mail,
  Calendar, Clock, Zap, Target,
  BarChart3, Info, FileText,
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Badge } from '@/components/ui/badge'
import { KPIGrid } from '@/components/features/kpi-grid'
import { useCampaignKPIs } from '@/lib/hooks/useKPIs'
import { StatusBadge } from '@/components/features/status-badge'
import { ConfirmDialog } from '@/components/features/confirm-dialog'
import { DataTable, type Column } from '@/components/features/data-table'
import { BANTScoreBar } from '@/components/features/bant-score-bar'
import { Pagination } from '@/components/features/pagination'
import { UserAvatar } from '@/components/features/user-avatar'
import { VectraBarChart } from '@/components/charts/vectra-bar-chart'
import { VectraDonutChart } from '@/components/charts/vectra-donut-chart'
import { useCampaign, useCampaignStats, useLeads } from '@/lib/hooks/queries'
import { CampaignEmailsTab } from '@/components/features/campaign-emails-tab'
import {
  useDeleteCampaign,
  useLaunchCampaign,
  usePauseCampaign,
  useResumeCampaign,
} from '@/lib/hooks/mutations'
import { useTranslation } from '@/lib/i18n'
import { CampaignStatus, LeadIntent, type Lead } from '@/types'
import { cn } from '@/lib/utils'
import Link from 'next/link'

const PAGE_SIZE = 10

// ─── Skeleton ─────────────────────────────────────────────────────────────────

function Skel({ className }: { className?: string }) {
  return (
    <div className={cn('rounded-md bg-[var(--surface-secondary)] animate-vectra-skeleton', className)} />
  )
}

function DetailSkeleton() {
  return (
    <div className="space-y-6">
      <div className="flex items-start justify-between gap-4">
        <div className="space-y-2.5">
          <Skel className="h-4 w-20" />
          <Skel className="h-8 w-72" />
          <Skel className="h-4 w-48" />
          <div className="flex gap-3 pt-0.5">
            <Skel className="h-4 w-28" />
            <Skel className="h-4 w-24" />
            <Skel className="h-4 w-20" />
          </div>
        </div>
        <div className="flex gap-2 shrink-0">
          <Skel className="h-9 w-28 rounded-lg" />
          <Skel className="h-9 w-9 rounded-lg" />
        </div>
      </div>
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="rounded-xl border border-[var(--border-primary)] p-5 space-y-3">
            <Skel className="h-3.5 w-24" />
            <Skel className="h-7 w-14" />
            <Skel className="h-3 w-20" />
          </div>
        ))}
      </div>
      <div className="grid gap-4 lg:grid-cols-3">
        <div className="lg:col-span-2 rounded-xl border border-[var(--border-primary)] p-5 space-y-3">
          <Skel className="h-4 w-40" />
          <Skel className="h-3 w-52" />
          <Skel className="h-[220px] w-full rounded-lg mt-2" />
        </div>
        <div className="rounded-xl border border-[var(--border-primary)] p-5 space-y-4">
          <Skel className="h-4 w-36" />
          <div className="flex justify-center">
            <Skel className="h-36 w-36 rounded-full" />
          </div>
          <div className="space-y-2.5">
            <Skel className="h-3.5 w-full" />
            <Skel className="h-3.5 w-full" />
            <Skel className="h-3.5 w-full" />
          </div>
        </div>
      </div>
    </div>
  )
}

// ─── Intent badge ──────────────────────────────────────────────────────────────

const intentStyles: Record<LeadIntent, string> = {
  [LeadIntent.HIGH]:
    'bg-[var(--color-success-500)]/10 text-[var(--color-success-600)]',
  [LeadIntent.MEDIUM]:
    'bg-[var(--color-warning-500)]/10 text-[var(--color-warning-600)]',
  [LeadIntent.LOW]:
    'bg-[var(--surface-secondary)] text-[var(--text-muted)]',
  [LeadIntent.UNKNOWN]:
    'bg-[var(--surface-secondary)] text-[var(--text-muted)]',
}

function IntentBadge({ intent, label }: { intent: LeadIntent; label: string }) {
  return (
    <span
      className={cn(
        'inline-flex items-center rounded-full px-2 py-0.5 text-caption font-medium',
        intentStyles[intent] ?? intentStyles[LeadIntent.UNKNOWN]
      )}
    >
      {label}
    </span>
  )
}

// ─── User info card (inside Team card) ────────────────────────────────────────

function TeamMemberRow({
  user,
  role,
}: {
  user: { id: string; first_name: string | null; last_name: string | null; email: string }
  role: string
}) {
  const fullName =
    user.first_name || user.last_name
      ? `${user.first_name ?? ''} ${user.last_name ?? ''}`.trim()
      : user.email
  return (
    <div className="flex items-center gap-3">
      <UserAvatar user={user} size="md" />
      <div className="min-w-0">
        <p className="text-body-sm font-medium text-[var(--text-primary)] truncate">{fullName}</p>
        <p className="text-caption text-[var(--text-muted)] truncate">{user.email}</p>
      </div>
      <Badge
        variant="secondary"
        className="ml-auto shrink-0 text-caption border-0 bg-[var(--surface-secondary)] text-[var(--text-muted)]"
      >
        {role}
      </Badge>
    </div>
  )
}

// ─── Main page ─────────────────────────────────────────────────────────────────

export default function CampaignDetailPage() {
  const { t } = useTranslation()
  const router = useRouter()
  const params = useParams()
  const id = params.id as string

  const [deleteOpen, setDeleteOpen] = useState(false)
  const [leadsSkip, setLeadsSkip] = useState(0)

  const { data: campaign, isLoading } = useCampaign(id)
  const { data: stats } = useCampaignStats(id)
  const { data: leadsData, isLoading: leadsLoading } = useLeads({
    campaign_id: id,
    skip: leadsSkip,
    limit: PAGE_SIZE,
  })

  const deleteMutation = useDeleteCampaign()
  const launchMutation = useLaunchCampaign()
  const pauseMutation = usePauseCampaign()
  const resumeMutation = useResumeCampaign()

  const kpis = useCampaignKPIs(stats)

  if (isLoading || !campaign) {
    return <DetailSkeleton />
  }

  // ─── Pipeline chart data ───────────────────────────────────────────────────

  const pipelineData = stats
    ? [
        { stage: t('leads.status.new'), count: stats.leads.new ?? 0 },
        { stage: t('leads.status.enriched'), count: stats.leads.enriched ?? 0 },
        { stage: t('leads.status.qualified'), count: stats.leads.qualified ?? 0 },
        { stage: t('leads.status.contacted'), count: stats.leads.contacted ?? 0 },
        { stage: t('emails.status.sent'), count: stats.emails.sent ?? 0 },
        { stage: t('emails.status.opened'), count: stats.emails.opened ?? 0 },
        { stage: t('emails.status.clicked'), count: stats.emails.clicked ?? 0 },
      ]
    : []

  const hasActivity = pipelineData.some((d) => d.count > 0)

  const pipelineSeries = [
    { key: 'count', label: t('campaigns.detail.pipeline'), color: 'var(--color-primary-500)' },
  ]

  // ─── Qualification donut data ──────────────────────────────────────────────

  const totalLeads = stats?.leads?.total ?? 0
  const qualifiedLeads = stats?.leads?.qualified ?? 0
  const qualRate = totalLeads > 0 ? Math.round((qualifiedLeads / totalLeads) * 100) : 0
  const donutColor =
    qualRate >= 70
      ? 'var(--color-success-500)'
      : qualRate >= 40
        ? 'var(--color-warning-500)'
        : 'var(--color-primary-500)'

  // ─── Duration ─────────────────────────────────────────────────────────────

  const durationDays =
    campaign.started_at
      ? differenceInDays(
          campaign.completed_at ? new Date(campaign.completed_at) : new Date(),
          new Date(campaign.started_at)
        )
      : null

  // ─── Table columns ─────────────────────────────────────────────────────────

  const leadColumns: Column<Lead>[] = [
    {
      key: 'name',
      header: t('leads.table.name'),
      render: (l) => (
        <div>
          <p className="font-medium text-[var(--text-primary)]">
            {l.first_name} {l.last_name}
          </p>
          <p className="text-caption text-[var(--text-muted)] truncate max-w-[180px]">{l.email}</p>
        </div>
      ),
    },
    {
      key: 'company',
      header: t('leads.table.company'),
      hideBelow: 'md',
      render: (l) =>
        l.company ? (
          <div>
            <p className="text-body-sm text-[var(--text-secondary)]">{l.company.name}</p>
            <p className="text-caption text-[var(--text-muted)]">{l.job?.title ?? '—'}</p>
          </div>
        ) : (
          <span className="text-[var(--text-muted)]">—</span>
        ),
    },
    {
      key: 'bant',
      header: t('leads.table.bant'),
      hideBelow: 'lg',
      render: (l) =>
        l.bant ? (
          <BANTScoreBar score={l.bant.score} />
        ) : (
          <span className="text-[var(--text-muted)]">—</span>
        ),
    },
    {
      key: 'intent',
      header: t('leads.table.intent'),
      hideBelow: 'xl',
      render: (l) => (
        <IntentBadge
          intent={l.intent}
          label={t(`leads.intent.${l.intent}`) || l.intent}
        />
      ),
    },
    {
      key: 'status',
      header: t('leads.table.status'),
      render: (l) => <StatusBadge status={l.status} type="lead" />,
    },
  ]

  // ─── Target criteria helpers ───────────────────────────────────────────────

  const knownCriteriaKeys: Record<string, string> = {
    job_titles: t('campaigns.form.jobTitles'),
    locations: t('campaigns.form.locations'),
    company_sizes: t('campaigns.form.companySizes'),
    industries: t('campaigns.form.industries'),
  }

  return (
    <div className="space-y-6">
      {/* ─── Header ─────────────────────────────────────────────────────────── */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div className="space-y-2">
          <Button
            variant="ghost"
            size="sm"
            asChild
            className="-ml-2 text-[var(--text-muted)] hover:text-[var(--text-primary)]"
          >
            <Link href="/campaigns">
              <ArrowLeft className="mr-1.5 h-3.5 w-3.5" />
              {t('common.back')}
            </Link>
          </Button>

          <div className="flex items-center gap-3 flex-wrap">
            <h1 className="text-h1 text-[var(--text-primary)]">{campaign.name}</h1>
            <StatusBadge status={campaign.status} type="campaign" />
          </div>

          {campaign.description && (
            <p className="text-body-sm text-[var(--text-muted)] max-w-xl">{campaign.description}</p>
          )}

          {/* Meta row */}
          <div className="flex flex-wrap items-center gap-x-4 gap-y-1.5 text-caption text-[var(--text-muted)] pt-0.5">
            {campaign.created_by_user && (
              <span className="flex items-center gap-1.5">
                <UserAvatar user={campaign.created_by_user} size="xs" />
                <span>
                  {t('campaigns.detail.createdBy')}{' '}
                  {campaign.created_by_user.first_name} {campaign.created_by_user.last_name}
                </span>
              </span>
            )}
            {campaign.launched_by_user &&
              campaign.launched_by_user.id !== campaign.created_by_user?.id && (
                <span className="flex items-center gap-1">
                  <Zap className="h-3 w-3 text-[var(--color-vectra-yellow-500)]" />
                  <span>
                    {t('campaigns.detail.launchedBy')}{' '}
                    {campaign.launched_by_user.first_name} {campaign.launched_by_user.last_name}
                  </span>
                </span>
              )}
            {durationDays !== null && durationDays >= 0 && (
              <span className="flex items-center gap-1">
                <Clock className="h-3 w-3" />
                {durationDays} {t('campaigns.detail.daysRunning')}
              </span>
            )}
            {campaign.started_at && (
              <span className="flex items-center gap-1">
                <Calendar className="h-3 w-3" />
                {format(new Date(campaign.started_at), 'dd MMM yyyy')}
              </span>
            )}
          </div>
        </div>

        {/* Action buttons */}
        <div className="flex items-center gap-2 shrink-0">
          {campaign.status === CampaignStatus.DRAFT && (
            <Button
              onClick={() => launchMutation.mutate(id)}
              disabled={launchMutation.isPending}
            >
              <Play className="mr-2 h-4 w-4" />
              {t('campaigns.launch')}
            </Button>
          )}
          {campaign.status === CampaignStatus.ACTIVE && (
            <Button
              variant="outline"
              onClick={() => pauseMutation.mutate(id)}
              disabled={pauseMutation.isPending}
            >
              <Pause className="mr-2 h-4 w-4" />
              {t('campaigns.pause')}
            </Button>
          )}
          {campaign.status === CampaignStatus.PAUSED && (
            <Button
              onClick={() => resumeMutation.mutate(id)}
              disabled={resumeMutation.isPending}
            >
              <RotateCcw className="mr-2 h-4 w-4" />
              {t('campaigns.resume')}
            </Button>
          )}
          <Button
            variant="outline"
            size="icon"
            onClick={() => setDeleteOpen(true)}
            className="text-[var(--color-error-500)] border-[var(--border-primary)] hover:bg-[var(--color-error-500)]/5 hover:border-[var(--color-error-300)]"
          >
            <Trash2 className="h-4 w-4" />
          </Button>
        </div>
      </div>

      {/* ─── KPI row ─────────────────────────────────────────────────────────── */}
      <KPIGrid kpis={kpis} />

      {/* ─── Charts ──────────────────────────────────────────────────────────── */}
      <div className="grid gap-4 lg:grid-cols-3">
        {/* Pipeline bar chart — 2/3 */}
        <Card className="lg:col-span-2 border-[var(--border-primary)] bg-[var(--surface-primary)]">
          <CardHeader className="pb-3">
            <div className="flex items-center gap-2">
              <BarChart3 className="h-4 w-4 text-[var(--color-primary-500)]" />
              <CardTitle className="text-h4">{t('campaigns.detail.pipeline')}</CardTitle>
            </div>
            <CardDescription className="text-caption text-[var(--text-muted)]">
              {t('campaigns.detail.pipelineDescription')}
            </CardDescription>
          </CardHeader>
          <CardContent>
            {!hasActivity ? (
              <div className="flex flex-col items-center justify-center h-[200px] text-center gap-3">
                <div className="h-10 w-10 rounded-full bg-[var(--surface-secondary)] flex items-center justify-center">
                  <Target className="h-5 w-5 text-[var(--text-muted)]" />
                </div>
                <div className="space-y-1">
                  <p className="text-body-sm font-medium text-[var(--text-primary)]">
                    {t('campaigns.detail.noStats')}
                  </p>
                  <p className="text-caption text-[var(--text-muted)] max-w-xs">
                    {t('campaigns.detail.noStatsDescription')}
                  </p>
                </div>
              </div>
            ) : (
              <VectraBarChart
                data={pipelineData}
                series={pipelineSeries}
                xKey="stage"
                height={220}
                showLegend={false}
              />
            )}
          </CardContent>
        </Card>

        {/* Qualification donut — 1/3 */}
        <Card className="border-[var(--border-primary)] bg-[var(--surface-primary)]">
          <CardHeader className="pb-3">
            <CardTitle className="text-h4">{t('campaigns.detail.qualificationRate')}</CardTitle>
            <CardDescription className="text-caption text-[var(--text-muted)]">
              {qualifiedLeads}/{totalLeads} {t('campaigns.detail.qualifiedLeads').toLowerCase()}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex flex-col items-center gap-5">
              <VectraDonutChart
                value={qualifiedLeads}
                max={Math.max(totalLeads, 1)}
                label={t('campaigns.detail.qualifiedLeads')}
                color={donutColor}
                size={148}
              />
              <div className="w-full space-y-2.5 text-body-sm">
                <div className="flex items-center justify-between">
                  <span className="text-[var(--text-muted)]">{t('campaigns.detail.totalLeads')}</span>
                  <span className="font-medium text-[var(--text-primary)] tabular-nums">
                    {totalLeads.toLocaleString()}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-[var(--text-muted)]">{t('campaigns.detail.qualifiedLeads')}</span>
                  <span
                    className="font-medium tabular-nums"
                    style={{ color: donutColor }}
                  >
                    {qualifiedLeads.toLocaleString()}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-[var(--text-muted)]">{t('campaigns.detail.emailsSent')}</span>
                  <span className="font-medium text-[var(--text-primary)] tabular-nums">
                    {(stats?.emails?.sent ?? 0).toLocaleString()}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-[var(--text-muted)]">{t('emails.status.opened')}</span>
                  <span className="font-medium text-[var(--color-success-600)] tabular-nums">
                    {(stats?.emails?.opened ?? 0).toLocaleString()}
                  </span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* ─── Tabs ────────────────────────────────────────────────────────────── */}
      <Tabs defaultValue="details">
        <TabsList className="border-b border-[var(--border-primary)] bg-transparent rounded-none h-auto p-0 w-full justify-start gap-0 mb-0">
          {(['details', 'leads', 'emails'] as const).map((tab) => (
            <TabsTrigger
              key={tab}
              value={tab}
              className={cn(
                'rounded-none border-b-2 border-transparent px-4 py-2.5 text-body-sm text-[var(--text-muted)]',
                'data-[state=active]:border-[var(--color-primary-500)] data-[state=active]:text-[var(--text-primary)] data-[state=active]:bg-transparent',
                'hover:text-[var(--text-secondary)] transition-colors duration-150'
              )}
            >
              {tab === 'details'
                ? t('campaigns.detail.tabs.details')
                : tab === 'leads'
                  ? `${t('campaigns.detail.tabs.leads')}${totalLeads > 0 ? ` (${totalLeads})` : ''}`
                  : `${t('campaigns.detail.tabs.emails')}${(stats?.emails?.total ?? 0) > 0 ? ` (${stats?.emails?.total ?? 0})` : ''}`}
            </TabsTrigger>
          ))}
        </TabsList>

        {/* ── Details tab ──────────────────────────────────────────────────── */}
        <TabsContent value="details" className="space-y-4 mt-4">
          <div className="grid gap-4 lg:grid-cols-2">
            {/* Target criteria */}
            <Card className="border-[var(--border-primary)] bg-[var(--surface-primary)]">
              <CardHeader className="pb-3">
                <div className="flex items-center gap-2">
                  <Target className="h-4 w-4 text-[var(--text-muted)]" />
                  <CardTitle className="text-h5">{t('campaigns.detail.targetCriteria')}</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                {Object.keys(campaign.target_criteria || {}).length === 0 ? (
                  <p className="text-body-sm text-[var(--text-muted)]">—</p>
                ) : (
                  <dl className="space-y-3">
                    {Object.entries(campaign.target_criteria || {}).map(([key, value]) => (
                      <div key={key}>
                        <dt className="text-caption font-medium text-[var(--text-muted)] uppercase tracking-wider mb-1">
                          {knownCriteriaKeys[key] ?? key.replace(/_/g, ' ')}
                        </dt>
                        <dd className="text-body-sm text-[var(--text-primary)]">{String(value) || '—'}</dd>
                      </div>
                    ))}
                  </dl>
                )}
              </CardContent>
            </Card>

            {/* Campaign settings */}
            <Card className="border-[var(--border-primary)] bg-[var(--surface-primary)]">
              <CardHeader className="pb-3">
                <div className="flex items-center gap-2">
                  <Info className="h-4 w-4 text-[var(--text-muted)]" />
                  <CardTitle className="text-h5">{t('campaigns.detail.campaignInfo')}</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <dl className="space-y-3">
                  <div className="flex items-start justify-between gap-2">
                    <dt className="text-body-sm text-[var(--text-muted)]">{t('campaigns.form.bantThreshold')}</dt>
                    <dd className="flex items-center gap-2">
                      <div className="w-20 h-1.5 rounded-full bg-[var(--surface-secondary)] overflow-hidden">
                        <div
                          className="h-full bg-[var(--color-primary-500)] rounded-full"
                          style={{ width: `${campaign.bant_threshold}%` }}
                        />
                      </div>
                      <span className="text-body-sm font-medium text-[var(--text-primary)] tabular-nums">
                        {campaign.bant_threshold}
                      </span>
                    </dd>
                  </div>
                  <div className="flex items-center justify-between">
                    <dt className="text-body-sm text-[var(--text-muted)]">{t('campaigns.form.dailyLimit')}</dt>
                    <dd className="text-body-sm font-medium text-[var(--text-primary)] tabular-nums">
                      {campaign.daily_limit} / {t('common.day')}
                    </dd>
                  </div>
                  <div className="flex items-center justify-between">
                    <dt className="text-body-sm text-[var(--text-muted)]">{t('campaigns.table.created')}</dt>
                    <dd className="text-body-sm text-[var(--text-primary)] tabular-nums">
                      {format(new Date(campaign.created_at), 'dd MMM yyyy, HH:mm')}
                    </dd>
                  </div>
                  {campaign.started_at && (
                    <div className="flex items-center justify-between">
                      <dt className="text-body-sm text-[var(--text-muted)]">{t('campaigns.table.started')}</dt>
                      <dd className="text-body-sm text-[var(--text-primary)] tabular-nums">
                        {format(new Date(campaign.started_at), 'dd MMM yyyy, HH:mm')}
                      </dd>
                    </div>
                  )}
                  {campaign.completed_at && (
                    <div className="flex items-center justify-between">
                      <dt className="text-body-sm text-[var(--text-muted)]">Completed</dt>
                      <dd className="text-body-sm text-[var(--text-primary)] tabular-nums">
                        {format(new Date(campaign.completed_at), 'dd MMM yyyy, HH:mm')}
                      </dd>
                    </div>
                  )}
                  {durationDays !== null && durationDays >= 0 && (
                    <div className="flex items-center justify-between">
                      <dt className="text-body-sm text-[var(--text-muted)]">{t('campaigns.detail.daysRunning')}</dt>
                      <dd className="text-body-sm font-medium text-[var(--text-primary)] tabular-nums">
                        {durationDays}d
                      </dd>
                    </div>
                  )}
                </dl>
              </CardContent>
            </Card>
          </div>

          {/* Email template */}
          {campaign.email_template && Object.keys(campaign.email_template).length > 0 && (
            <Card className="border-[var(--border-primary)] bg-[var(--surface-primary)]">
              <CardHeader className="pb-3">
                <div className="flex items-center gap-2">
                  <FileText className="h-4 w-4 text-[var(--text-muted)]" />
                  <CardTitle className="text-h5">{t('campaigns.detail.emailTemplate')}</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <dl className="grid gap-3 sm:grid-cols-2">
                  {Object.entries(campaign.email_template).map(([key, value]) => (
                    <div key={key}>
                      <dt className="text-caption font-medium text-[var(--text-muted)] uppercase tracking-wider mb-1">
                        {key.replace(/_/g, ' ')}
                      </dt>
                      <dd className="text-body-sm text-[var(--text-primary)]">{String(value) || '—'}</dd>
                    </div>
                  ))}
                </dl>
              </CardContent>
            </Card>
          )}

          {/* Team */}
          {(campaign.created_by_user || campaign.launched_by_user) && (
            <Card className="border-[var(--border-primary)] bg-[var(--surface-primary)]">
              <CardHeader className="pb-3">
                <div className="flex items-center gap-2">
                  <Users className="h-4 w-4 text-[var(--text-muted)]" />
                  <CardTitle className="text-h5">{t('campaigns.detail.team')}</CardTitle>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {campaign.created_by_user && (
                    <TeamMemberRow
                      user={campaign.created_by_user}
                      role={t('campaigns.detail.createdBy')}
                    />
                  )}
                  {campaign.launched_by_user &&
                    campaign.launched_by_user.id !== campaign.created_by_user?.id && (
                      <TeamMemberRow
                        user={campaign.launched_by_user}
                        role={t('campaigns.detail.launchedBy')}
                      />
                    )}
                </div>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        {/* ── Leads tab ─────────────────────────────────────────────────────── */}
        <TabsContent value="leads" className="mt-4 space-y-3">
          <DataTable
            columns={leadColumns}
            data={leadsData?.data ?? []}
            isLoading={leadsLoading}
            emptyMessage={t('leads.empty.title')}
            emptyDescription={t('leads.empty.description')}
            emptyIcon={Users}
            skip={leadsSkip}
            onRowClick={(l) => router.push(`/leads/${l.id}`)}
          />
          {leadsData?.pagination && (
            <Pagination pagination={leadsData.pagination} onPageChange={setLeadsSkip} />
          )}
        </TabsContent>

        {/* ── Emails tab ────────────────────────────────────────────────────── */}
        <TabsContent value="emails" className="mt-4">
          <CampaignEmailsTab campaignId={id} />
        </TabsContent>
      </Tabs>

      {/* ─── Delete confirm ───────────────────────────────────────────────────── */}
      <ConfirmDialog
        open={deleteOpen}
        onOpenChange={setDeleteOpen}
        title={t('campaigns.confirmDelete.title')}
        description={t('campaigns.confirmDelete.description')}
        variant="destructive"
        confirmLabel={t('common.delete')}
        isLoading={deleteMutation.isPending}
        onConfirm={() => {
          deleteMutation.mutate(id, {
            onSuccess: () => router.push('/campaigns'),
          })
        }}
      />
    </div>
  )
}
