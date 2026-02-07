'use client'

import { useState, useCallback } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { format } from 'date-fns'
import { Users } from 'lucide-react'
import { Badge } from '@/components/ui/badge'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { DataTable, type Column } from '@/components/features/data-table'
import { StatusBadge } from '@/components/features/status-badge'
import { BANTScoreBar } from '@/components/features/bant-score-bar'
import { FilterBar } from '@/components/features/filter-bar'
import { SearchInput } from '@/components/features/search-input'
import { Pagination } from '@/components/features/pagination'
import { PageTransition } from '@/components/motion'
import { useLeads, useCampaigns } from '@/lib/hooks/queries'
import { useTranslation } from '@/lib/i18n'
import type { Lead } from '@/types'

const PAGE_SIZE = 20

export default function LeadsPage() {
  const { t } = useTranslation()
  const router = useRouter()
  const searchParams = useSearchParams()

  const [skip, setSkip] = useState(0)
  const [search, setSearch] = useState(searchParams.get('search') ?? '')
  const [campaignId, setCampaignId] = useState(searchParams.get('campaign_id') ?? 'all')
  const [status, setStatus] = useState(searchParams.get('status') ?? 'all')
  const [intent, setIntent] = useState(searchParams.get('intent') ?? 'all')

  const { data: campaigns } = useCampaigns()
  const campaignList = Array.isArray(campaigns) ? campaigns : []

  const { data: leadsData, isLoading } = useLeads({
    skip,
    limit: PAGE_SIZE,
    search: search || undefined,
    campaign_id: campaignId === 'all' ? undefined : campaignId,
    status: status === 'all' ? undefined : status,
    intent: intent === 'all' ? undefined : intent,
  })

  const hasFilters = search !== '' || campaignId !== 'all' || status !== 'all' || intent !== 'all'

  const clearFilters = useCallback(() => {
    setSearch('')
    setCampaignId('all')
    setStatus('all')
    setIntent('all')
    setSkip(0)
  }, [])

  const columns: Column<Lead>[] = [
    {
      key: 'name',
      header: t('leads.table.name'),
      render: (l) => (
        <div>
          <p className="font-medium text-[var(--text-primary)]">{l.first_name} {l.last_name}</p>
          <p className="text-xs text-[var(--text-muted)]">{l.email}</p>
        </div>
      ),
    },
    {
      key: 'company',
      header: t('leads.table.company'),
      render: (l) => (
        <div>
          <p className="text-sm text-[var(--text-secondary)]">{l.company?.name ?? '-'}</p>
          {l.job?.title && <p className="text-xs text-[var(--text-muted)]">{l.job.title}</p>}
        </div>
      ),
    },
    {
      key: 'bant',
      header: t('leads.table.bant'),
      className: 'w-[140px]',
      render: (l) => l.bant ? <BANTScoreBar score={l.bant.score} /> : <span className="text-[var(--text-muted)]">-</span>,
    },
    {
      key: 'status',
      header: t('leads.table.status'),
      render: (l) => <StatusBadge status={l.status} type="lead" />,
    },
    {
      key: 'intent',
      header: t('leads.table.intent'),
      render: (l) => (
        <Badge variant="outline" className="text-xs capitalize">
          {t(`leads.intent.${l.intent}`)}
        </Badge>
      ),
    },
    {
      key: 'date',
      header: t('leads.table.date'),
      render: (l) => (
        <span className="text-sm text-[var(--text-muted)]">
          {format(new Date(l.created_at), 'dd/MM/yyyy')}
        </span>
      ),
    },
  ]

  return (
    <PageTransition>
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <h1 className="text-h1 text-[var(--text-primary)]">{t('leads.title')}</h1>
          {leadsData?.pagination && (
            <Badge variant="secondary">{leadsData.pagination.total}</Badge>
          )}
        </div>
      </div>

      <FilterBar showClear={hasFilters} onClear={clearFilters}>
        <SearchInput
          value={search}
          onChange={(v) => { setSearch(v); setSkip(0) }}
          placeholder={t('common.search')}
        />
        <Select value={campaignId} onValueChange={(v) => { setCampaignId(v); setSkip(0) }}>
          <SelectTrigger className="w-[180px]">
            <SelectValue placeholder={t('leads.filters.campaign')} />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">{t('leads.filters.allCampaigns')}</SelectItem>
            {campaignList.map((c) => (
              <SelectItem key={c.id} value={c.id}>{c.name}</SelectItem>
            ))}
          </SelectContent>
        </Select>
        <Select value={status} onValueChange={(v) => { setStatus(v); setSkip(0) }}>
          <SelectTrigger className="w-[160px]">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">{t('leads.filters.allStatuses')}</SelectItem>
            <SelectItem value="new">{t('leads.status.new')}</SelectItem>
            <SelectItem value="enriched">{t('leads.status.enriched')}</SelectItem>
            <SelectItem value="qualified">{t('leads.status.qualified')}</SelectItem>
            <SelectItem value="nurture">{t('leads.status.nurture')}</SelectItem>
            <SelectItem value="rejected">{t('leads.status.rejected')}</SelectItem>
            <SelectItem value="contacted">{t('leads.status.contacted')}</SelectItem>
          </SelectContent>
        </Select>
        <Select value={intent} onValueChange={(v) => { setIntent(v); setSkip(0) }}>
          <SelectTrigger className="w-[140px]">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">{t('leads.filters.allIntents')}</SelectItem>
            <SelectItem value="high">{t('leads.intent.high')}</SelectItem>
            <SelectItem value="medium">{t('leads.intent.medium')}</SelectItem>
            <SelectItem value="low">{t('leads.intent.low')}</SelectItem>
            <SelectItem value="unknown">{t('leads.intent.unknown')}</SelectItem>
          </SelectContent>
        </Select>
      </FilterBar>

      <DataTable
        columns={columns}
        data={leadsData?.data ?? []}
        isLoading={isLoading}
        emptyMessage={t('leads.empty.title')}
        emptyDescription={t('leads.empty.description')}
        emptyIcon={Users}
        onRowClick={(l) => router.push(`/leads/${l.id}`)}
      />

      {leadsData?.pagination && (
        <Pagination pagination={leadsData.pagination} onPageChange={setSkip} />
      )}
    </div>
    </PageTransition>
  )
}
