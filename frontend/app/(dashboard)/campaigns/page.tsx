'use client'

import { useState, useMemo } from 'react'
import { useRouter } from 'next/navigation'
import { useQuery } from '@tanstack/react-query'
import { format, subDays } from 'date-fns'
import {
  Target,
  MoreHorizontal,
  Play,
  Pause,
  RotateCcw,
  Trash2,
  Eye,
  Pencil,
  Plus,
  CalendarDays,
  Gauge,
  Search,
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { DataTable, type Column } from '@/components/features/data-table'
import { StatusBadge } from '@/components/features/status-badge'
import { FilterBar } from '@/components/features/filter-bar'
import { Pagination } from '@/components/features/pagination'
import { ConfirmDialog } from '@/components/features/confirm-dialog'
import { KPIGrid } from '@/components/features/kpi-grid'
import { CampaignCreateModal } from '@/components/features/campaign-create-modal'
import { CampaignOwners } from '@/components/features/user-avatar'
import { PageTransition } from '@/components/motion'
import { useCampaigns, useOrgUsers } from '@/lib/hooks/queries'
import { useDeleteCampaign, useLaunchCampaign, usePauseCampaign, useResumeCampaign } from '@/lib/hooks/mutations'
import { useCampaignsPageKPIs } from '@/lib/hooks/useKPIs'
import { useTranslation } from '@/lib/i18n'
import { api } from '@/lib/api'
import { cn } from '@/lib/utils'
import { CampaignStatus, type Campaign } from '@/types'
import type { AnalyticsDashboard, OrganizationUser } from '@/types'

const PAGE_SIZE = 10

// Stable fallback for analytics placeholder
const fallbackAnalytics: AnalyticsDashboard = {
  overview: { active_campaigns: 0, qualified_leads: 0, emails_sent: 0, ai_success_rate: 0 },
  growth: { leads_current: 0, leads_previous: 0, leads_change: 0, emails_current: 0, emails_previous: 0, emails_change: 0 },
  team: { total_users: 0, active_users: 0, user_activity_rate: 0, role_distribution: {}, period_days: 30 },
  ai_agents: { total_agent_runs: 0, successful_runs: 0, success_rate: 0, prospector_runs: 0, bant_runs: 0, scheduler_runs: 0, period_days: 30 },
  subscription: { plan: 'starter', status: 'active', leads_used: 0, leads_limit: 500 },
  generated_at: new Date().toISOString(),
}

type PeriodKey = 'all' | '7' | '30' | '90'

// ─── BANT threshold chip ──────────────────────────────────────────────────────

function BANTChip({ value }: { value: number }) {
  const color =
    value >= 70
      ? 'bg-[var(--color-success-500)]/10 text-[var(--color-success-600)]'
      : value >= 50
      ? 'bg-[var(--color-warning-500)]/10 text-[var(--color-warning-600)]'
      : 'bg-[var(--surface-secondary)] text-[var(--text-muted)]'

  return (
    <span className={cn('inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-caption font-medium', color)}>
      <Gauge className="h-3 w-3 shrink-0" />
      {value}
    </span>
  )
}

// ─── Page ─────────────────────────────────────────────────────────────────────

export default function CampaignsPage() {
  const { t } = useTranslation()
  const router = useRouter()

  // Filter state
  const [skip, setSkip] = useState(0)
  const [search, setSearch] = useState('')
  const [statusFilter, setStatusFilter] = useState('all')
  const [creatorFilter, setCreatorFilter] = useState('all')
  const [periodFilter, setPeriodFilter] = useState<PeriodKey>('all')

  // Dialog state
  const [deleteId, setDeleteId] = useState<string | null>(null)
  const [createOpen, setCreateOpen] = useState(false)

  // Compute created_after from period
  const createdAfter = useMemo(() => {
    if (periodFilter === 'all') return undefined
    return subDays(new Date(), Number(periodFilter)).toISOString()
  }, [periodFilter])

  // Campaigns list
  const { data: campaigns, isLoading } = useCampaigns({
    skip,
    limit: PAGE_SIZE,
    status: statusFilter === 'all' ? undefined : statusFilter,
    search: search.trim() || undefined,
    created_by: creatorFilter === 'all' ? undefined : creatorFilter,
    created_after: createdAfter,
  })

  // Org users for creator filter dropdown + avatar resolution
  const { data: orgUsers } = useOrgUsers({ limit: 100 })
  const userList: OrganizationUser[] = Array.isArray(orgUsers) ? orgUsers : []

  // Analytics KPIs (reuse cached query from dashboard)
  const { data: analytics } = useQuery({
    queryKey: ['analytics', 'overview'],
    queryFn: async () => {
      const res = await api.analytics.overview()
      return res.data
    },
    placeholderData: fallbackAnalytics,
    staleTime: 2 * 60 * 1000,
  })

  const kpis = useCampaignsPageKPIs(analytics ?? fallbackAnalytics)

  const deleteMutation = useDeleteCampaign()
  const launchMutation = useLaunchCampaign()
  const pauseMutation = usePauseCampaign()
  const resumeMutation = useResumeCampaign()

  const campaignList: Campaign[] = Array.isArray(campaigns) ? campaigns : []

  const hasFilters =
    statusFilter !== 'all' ||
    creatorFilter !== 'all' ||
    periodFilter !== 'all' ||
    search.trim() !== ''

  const columns: Column<Campaign>[] = [
    {
      key: 'name',
      header: t('campaigns.table.name'),
      render: (c) => (
        <div className="min-w-0">
          <p className="font-medium text-[var(--text-primary)] truncate">{c.name}</p>
          {c.description && (
            <p className="text-caption text-[var(--text-muted)] truncate max-w-[260px]">
              {c.description}
            </p>
          )}
        </div>
      ),
    },
    {
      key: 'owner',
      header: t('campaigns.table.owner'),
      hideBelow: 'md',
      render: (c) => (
        <CampaignOwners
          creator={c.created_by_user}
          launcher={c.launched_by_user}
        />
      ),
    },
    {
      key: 'status',
      header: t('campaigns.table.status'),
      width: 'w-[120px]',
      render: (c) => <StatusBadge status={c.status} type="campaign" />,
    },
    {
      key: 'bant',
      header: t('campaigns.table.bant'),
      width: 'w-[90px]',
      hideBelow: 'md',
      align: 'center',
      render: (c) => <BANTChip value={c.bant_threshold} />,
    },
    {
      key: 'daily_limit',
      header: t('campaigns.table.dailyLimit'),
      width: 'w-[110px]',
      hideBelow: 'lg',
      align: 'center',
      render: (c) => (
        <span className="text-body-sm text-[var(--text-secondary)] tabular-nums">
          {c.daily_limit} / {t('common.day') || 'day'}
        </span>
      ),
    },
    {
      key: 'started_at',
      header: t('campaigns.table.started'),
      width: 'w-[120px]',
      hideBelow: 'xl',
      render: (c) =>
        c.started_at ? (
          <span className="text-body-sm text-[var(--text-muted)] flex items-center gap-1">
            <CalendarDays className="h-3.5 w-3.5 shrink-0" />
            {format(new Date(c.started_at), 'dd MMM yyyy')}
          </span>
        ) : (
          <span className="text-caption text-[var(--text-muted)]">—</span>
        ),
    },
    {
      key: 'created_at',
      header: t('campaigns.table.created'),
      width: 'w-[110px]',
      hideBelow: 'lg',
      render: (c) => (
        <span className="text-body-sm text-[var(--text-muted)]">
          {format(new Date(c.created_at), 'dd MMM yyyy')}
        </span>
      ),
    },
    {
      key: 'actions',
      header: '',
      width: 'w-[48px]',
      align: 'right',
      render: (c) => (
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button
              variant="ghost"
              size="sm"
              className="h-8 w-8 p-0 text-[var(--text-muted)] hover:text-[var(--text-primary)]"
              onClick={(e) => e.stopPropagation()}
            >
              <MoreHorizontal className="h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end" className="w-[180px]">
            <DropdownMenuItem onClick={() => router.push(`/campaigns/${c.id}`)}>
              <Eye className="mr-2 h-4 w-4" />
              {t('common.view')}
            </DropdownMenuItem>
            {c.status === CampaignStatus.DRAFT && (
              <DropdownMenuItem onClick={() => router.push(`/campaigns/${c.id}`)}>
                <Pencil className="mr-2 h-4 w-4" />
                {t('common.edit')}
              </DropdownMenuItem>
            )}
            <DropdownMenuSeparator />
            {c.status === CampaignStatus.DRAFT && (
              <DropdownMenuItem
                onClick={(e) => { e.stopPropagation(); launchMutation.mutate(c.id) }}
                disabled={launchMutation.isPending}
              >
                <Play className="mr-2 h-4 w-4 text-[var(--color-success-500)]" />
                {t('campaigns.launch')}
              </DropdownMenuItem>
            )}
            {c.status === CampaignStatus.ACTIVE && (
              <DropdownMenuItem
                onClick={(e) => { e.stopPropagation(); pauseMutation.mutate(c.id) }}
                disabled={pauseMutation.isPending}
              >
                <Pause className="mr-2 h-4 w-4 text-[var(--color-warning-500)]" />
                {t('campaigns.pause')}
              </DropdownMenuItem>
            )}
            {c.status === CampaignStatus.PAUSED && (
              <DropdownMenuItem
                onClick={(e) => { e.stopPropagation(); resumeMutation.mutate(c.id) }}
                disabled={resumeMutation.isPending}
              >
                <RotateCcw className="mr-2 h-4 w-4 text-[var(--color-primary-500)]" />
                {t('campaigns.resume')}
              </DropdownMenuItem>
            )}
            <DropdownMenuSeparator />
            <DropdownMenuItem
              className="text-[var(--color-error-500)] focus:text-[var(--color-error-500)]"
              onClick={(e) => { e.stopPropagation(); setDeleteId(c.id) }}
            >
              <Trash2 className="mr-2 h-4 w-4" />
              {t('common.delete')}
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      ),
    },
  ]

  return (
    <PageTransition>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div>
            <h1 className="text-h1 text-[var(--text-primary)]">{t('campaigns.title')}</h1>
            <p className="text-body text-[var(--text-muted)] mt-0.5">{t('campaigns.subtitle')}</p>
          </div>
          <Button onClick={() => setCreateOpen(true)}>
            <Plus className="mr-2 h-4 w-4" />
            {t('campaigns.new')}
          </Button>
        </div>

        {/* KPIs */}
        <KPIGrid kpis={kpis} />

        {/* Filters */}
        <FilterBar
          title={t('common.filters')}
          showClear={hasFilters}
          onClear={() => {
            setSearch('')
            setStatusFilter('all')
            setCreatorFilter('all')
            setPeriodFilter('all')
            setSkip(0)
          }}
        >
          {/* Name search */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-[var(--text-muted)] pointer-events-none" />
            <Input
              value={search}
              onChange={(e) => { setSearch(e.target.value); setSkip(0) }}
              placeholder={t('campaigns.filters.searchPlaceholder')}
              className="pl-9 w-[200px]"
            />
          </div>

          {/* Status */}
          <Select value={statusFilter} onValueChange={(v) => { setStatusFilter(v); setSkip(0) }}>
            <SelectTrigger className="w-[150px]">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">{t('campaigns.filters.allStatuses')}</SelectItem>
              <SelectItem value="draft">{t('campaigns.status.draft')}</SelectItem>
              <SelectItem value="active">{t('campaigns.status.active')}</SelectItem>
              <SelectItem value="paused">{t('campaigns.status.paused')}</SelectItem>
              <SelectItem value="completed">{t('campaigns.status.completed')}</SelectItem>
              <SelectItem value="archived">{t('campaigns.status.archived')}</SelectItem>
            </SelectContent>
          </Select>

          {/* Creator */}
          {userList.length > 0 && (
            <Select value={creatorFilter} onValueChange={(v) => { setCreatorFilter(v); setSkip(0) }}>
              <SelectTrigger className="w-[170px]">
                <SelectValue placeholder={t('campaigns.filters.creator')} />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">{t('campaigns.filters.allCreators')}</SelectItem>
                {userList.map((u) => (
                  <SelectItem key={u.id} value={u.id}>
                    {u.first_name || u.last_name
                      ? `${u.first_name ?? ''} ${u.last_name ?? ''}`.trim()
                      : u.email}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          )}

          {/* Period */}
          <Select
            value={periodFilter}
            onValueChange={(v) => { setPeriodFilter(v as PeriodKey); setSkip(0) }}
          >
            <SelectTrigger className="w-[150px]">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">{t('campaigns.filters.allTime')}</SelectItem>
              <SelectItem value="7">{t('campaigns.filters.last7Days')}</SelectItem>
              <SelectItem value="30">{t('campaigns.filters.last30Days')}</SelectItem>
              <SelectItem value="90">{t('campaigns.filters.last90Days')}</SelectItem>
            </SelectContent>
          </Select>
        </FilterBar>

        {/* Table */}
        <DataTable
          columns={columns}
          data={campaignList}
          isLoading={isLoading}
          skip={skip}
          emptyMessage={t('campaigns.empty.title')}
          emptyDescription={t('campaigns.empty.description')}
          emptyIcon={Target}
          emptyAction={
            <Button onClick={() => setCreateOpen(true)}>
              <Plus className="mr-2 h-4 w-4" />
              {t('campaigns.new')}
            </Button>
          }
          onRowClick={(c) => router.push(`/campaigns/${c.id}`)}
        />

        {/* Pagination */}
        {campaignList.length > 0 && (
          <Pagination
            pagination={{
              total: campaignList.length + skip,
              skip,
              limit: PAGE_SIZE,
              has_more: campaignList.length === PAGE_SIZE,
            }}
            onPageChange={setSkip}
          />
        )}
      </div>

      {/* Create modal */}
      <CampaignCreateModal open={createOpen} onOpenChange={setCreateOpen} />

      {/* Delete confirm */}
      <ConfirmDialog
        open={!!deleteId}
        onOpenChange={(open) => !open && setDeleteId(null)}
        title={t('campaigns.confirmDelete.title')}
        description={t('campaigns.confirmDelete.description')}
        variant="destructive"
        confirmLabel={t('common.delete')}
        isLoading={deleteMutation.isPending}
        onConfirm={() => {
          if (deleteId) {
            deleteMutation.mutate(deleteId, { onSuccess: () => setDeleteId(null) })
          }
        }}
      />
    </PageTransition>
  )
}
