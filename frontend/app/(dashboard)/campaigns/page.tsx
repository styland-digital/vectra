'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { format } from 'date-fns'
import { Target, MoreHorizontal, Play, Pause, RotateCcw, Archive, Trash2, Eye, Pencil } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
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
import { PageTransition } from '@/components/motion'
import { useCampaigns } from '@/lib/hooks/queries'
import { useDeleteCampaign, useLaunchCampaign, usePauseCampaign, useResumeCampaign } from '@/lib/hooks/mutations'
import { useTranslation } from '@/lib/i18n'
import { CampaignStatus, type Campaign } from '@/types'
import Link from 'next/link'

const PAGE_SIZE = 10

export default function CampaignsPage() {
  const { t } = useTranslation()
  const router = useRouter()
  const [skip, setSkip] = useState(0)
  const [statusFilter, setStatusFilter] = useState<string>('all')
  const [deleteId, setDeleteId] = useState<string | null>(null)

  const { data: campaigns, isLoading } = useCampaigns({
    skip,
    limit: PAGE_SIZE,
    status: statusFilter === 'all' ? undefined : statusFilter,
  })

  const deleteMutation = useDeleteCampaign()
  const launchMutation = useLaunchCampaign()
  const pauseMutation = usePauseCampaign()
  const resumeMutation = useResumeCampaign()

  const columns: Column<Campaign>[] = [
    {
      key: 'name',
      header: t('campaigns.table.name'),
      render: (c) => (
        <div>
          <p className="font-medium text-[var(--text-primary)]">{c.name}</p>
          {c.description && (
            <p className="text-xs text-[var(--text-muted)] truncate max-w-[200px]">{c.description}</p>
          )}
        </div>
      ),
    },
    {
      key: 'status',
      header: t('campaigns.table.status'),
      render: (c) => <StatusBadge status={c.status} type="campaign" />,
    },
    {
      key: 'bant',
      header: t('campaigns.table.bant'),
      render: (c) => (
        <span className="text-sm text-[var(--text-secondary)]">{c.bant_threshold}</span>
      ),
    },
    {
      key: 'created',
      header: t('campaigns.table.created'),
      render: (c) => (
        <span className="text-sm text-[var(--text-muted)]">
          {format(new Date(c.created_at), 'dd/MM/yyyy')}
        </span>
      ),
    },
    {
      key: 'actions',
      header: '',
      className: 'w-[50px]',
      render: (c) => (
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" size="sm" className="h-8 w-8 p-0" onClick={(e) => e.stopPropagation()}>
              <MoreHorizontal className="h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
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
              <DropdownMenuItem onClick={() => launchMutation.mutate(c.id)}>
                <Play className="mr-2 h-4 w-4" />
                {t('campaigns.launch')}
              </DropdownMenuItem>
            )}
            {c.status === CampaignStatus.ACTIVE && (
              <DropdownMenuItem onClick={() => pauseMutation.mutate(c.id)}>
                <Pause className="mr-2 h-4 w-4" />
                {t('campaigns.pause')}
              </DropdownMenuItem>
            )}
            {c.status === CampaignStatus.PAUSED && (
              <DropdownMenuItem onClick={() => resumeMutation.mutate(c.id)}>
                <RotateCcw className="mr-2 h-4 w-4" />
                {t('campaigns.resume')}
              </DropdownMenuItem>
            )}
            <DropdownMenuSeparator />
            <DropdownMenuItem
              className="text-[var(--color-error-500)]"
              onClick={() => setDeleteId(c.id)}
            >
              <Trash2 className="mr-2 h-4 w-4" />
              {t('common.delete')}
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      ),
    },
  ]

  const campaignList = Array.isArray(campaigns) ? campaigns : []

  return (
    <PageTransition>
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-h1 text-[var(--text-primary)]">{t('campaigns.title')}</h1>
          <p className="text-[var(--text-muted)]">{t('campaigns.subtitle')}</p>
        </div>
        <Button asChild>
          <Link href="/campaigns/new">
            <Target className="mr-2 h-4 w-4" />
            {t('campaigns.new')}
          </Link>
        </Button>
      </div>

      <FilterBar
        showClear={statusFilter !== 'all'}
        onClear={() => setStatusFilter('all')}
      >
        <Select value={statusFilter} onValueChange={(v) => { setStatusFilter(v); setSkip(0) }}>
          <SelectTrigger className="w-[180px]">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">{t('common.all')}</SelectItem>
            <SelectItem value="draft">{t('campaigns.status.draft')}</SelectItem>
            <SelectItem value="active">{t('campaigns.status.active')}</SelectItem>
            <SelectItem value="paused">{t('campaigns.status.paused')}</SelectItem>
            <SelectItem value="completed">{t('campaigns.status.completed')}</SelectItem>
            <SelectItem value="archived">{t('campaigns.status.archived')}</SelectItem>
          </SelectContent>
        </Select>
      </FilterBar>

      <DataTable
        columns={columns}
        data={campaignList}
        isLoading={isLoading}
        emptyMessage={t('campaigns.empty.title')}
        emptyDescription={t('campaigns.empty.description')}
        emptyIcon={Target}
        emptyAction={
          <Button asChild>
            <Link href="/campaigns/new">{t('campaigns.new')}</Link>
          </Button>
        }
        onRowClick={(c) => router.push(`/campaigns/${c.id}`)}
      />

      {campaignList.length > 0 && (
        <Pagination
          pagination={{
            total: campaignList.length,
            skip,
            limit: PAGE_SIZE,
            has_more: campaignList.length === PAGE_SIZE,
          }}
          onPageChange={setSkip}
        />
      )}

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
            deleteMutation.mutate(deleteId, {
              onSuccess: () => setDeleteId(null),
            })
          }
        }}
      />
    </div>
    </PageTransition>
  )
}
