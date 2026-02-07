'use client'

import { useState } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { format } from 'date-fns'
import { ArrowLeft, Play, Pause, RotateCcw, Trash2, Users, Mail, Target, BarChart3 } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { StatusBadge } from '@/components/features/status-badge'
import { ConfirmDialog } from '@/components/features/confirm-dialog'
import { DataTable, type Column } from '@/components/features/data-table'
import { BANTScoreBar } from '@/components/features/bant-score-bar'
import { Pagination } from '@/components/features/pagination'
import { LoadingSkeleton } from '@/components/loading-skeleton'
import { useCampaign, useCampaignStats, useLeads, useEmails } from '@/lib/hooks/queries'
import { useDeleteCampaign, useLaunchCampaign, usePauseCampaign, useResumeCampaign } from '@/lib/hooks/mutations'
import { useTranslation } from '@/lib/i18n'
import { CampaignStatus, type Lead, type Email } from '@/types'
import Link from 'next/link'

const PAGE_SIZE = 10

export default function CampaignDetailPage() {
  const { t } = useTranslation()
  const router = useRouter()
  const params = useParams()
  const id = params.id as string

  const [deleteOpen, setDeleteOpen] = useState(false)
  const [leadsSkip, setLeadsSkip] = useState(0)
  const [emailsSkip, setEmailsSkip] = useState(0)

  const { data: campaign, isLoading } = useCampaign(id)
  const { data: stats } = useCampaignStats(id)
  const { data: leadsData } = useLeads({ campaign_id: id, skip: leadsSkip, limit: PAGE_SIZE })
  const { data: emailsData } = useEmails({ campaign_id: id, skip: emailsSkip, limit: PAGE_SIZE })

  const deleteMutation = useDeleteCampaign()
  const launchMutation = useLaunchCampaign()
  const pauseMutation = usePauseCampaign()
  const resumeMutation = useResumeCampaign()

  if (isLoading || !campaign) {
    return (
      <div className="space-y-6">
        <LoadingSkeleton variant="stats" />
        <LoadingSkeleton variant="card" />
      </div>
    )
  }

  const statCards = [
    { label: t('campaigns.detail.totalLeads'), value: stats?.leads?.total ?? 0, icon: Users },
    { label: t('campaigns.detail.qualifiedLeads'), value: stats?.leads?.qualified ?? 0, icon: Target },
    { label: t('campaigns.detail.emailsSent'), value: stats?.emails?.sent ?? 0, icon: Mail },
    { label: t('campaigns.detail.bantAverage'), value: stats?.bant?.average ?? 0, icon: BarChart3 },
  ]

  const leadColumns: Column<Lead>[] = [
    {
      key: 'name',
      header: t('leads.table.name'),
      render: (l) => (
        <span className="font-medium text-[var(--text-primary)]">
          {l.first_name} {l.last_name}
        </span>
      ),
    },
    {
      key: 'company',
      header: t('leads.table.company'),
      render: (l) => <span className="text-sm text-[var(--text-secondary)]">{l.company?.name ?? '-'}</span>,
    },
    {
      key: 'bant',
      header: t('leads.table.bant'),
      render: (l) => l.bant ? <BANTScoreBar score={l.bant.score} /> : <span className="text-[var(--text-muted)]">-</span>,
    },
    {
      key: 'status',
      header: t('leads.table.status'),
      render: (l) => <StatusBadge status={l.status} type="lead" />,
    },
  ]

  const emailColumns: Column<Email>[] = [
    {
      key: 'to',
      header: t('emails.table.to'),
      render: (e) => <span className="text-sm text-[var(--text-primary)]">{e.lead?.name ?? e.lead?.email}</span>,
    },
    {
      key: 'subject',
      header: t('emails.table.subject'),
      render: (e) => <span className="text-sm text-[var(--text-secondary)] truncate max-w-[200px] block">{e.subject}</span>,
    },
    {
      key: 'status',
      header: t('emails.table.status'),
      render: (e) => <StatusBadge status={e.status} type="email" />,
    },
    {
      key: 'created',
      header: t('emails.table.created'),
      render: (e) => <span className="text-sm text-[var(--text-muted)]">{format(new Date(e.created_at), 'dd/MM/yyyy')}</span>,
    },
  ]

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Button variant="ghost" size="sm" asChild>
            <Link href="/campaigns">
              <ArrowLeft className="mr-2 h-4 w-4" />
              {t('common.back')}
            </Link>
          </Button>
          <div>
            <div className="flex items-center space-x-3">
              <h1 className="text-3xl font-bold text-[var(--text-primary)]">{campaign.name}</h1>
              <StatusBadge status={campaign.status} type="campaign" />
            </div>
            {campaign.description && (
              <p className="text-[var(--text-muted)] mt-1">{campaign.description}</p>
            )}
          </div>
        </div>
        <div className="flex items-center space-x-2">
          {campaign.status === CampaignStatus.DRAFT && (
            <Button onClick={() => launchMutation.mutate(id)} disabled={launchMutation.isPending}>
              <Play className="mr-2 h-4 w-4" />
              {t('campaigns.launch')}
            </Button>
          )}
          {campaign.status === CampaignStatus.ACTIVE && (
            <Button variant="outline" onClick={() => pauseMutation.mutate(id)} disabled={pauseMutation.isPending}>
              <Pause className="mr-2 h-4 w-4" />
              {t('campaigns.pause')}
            </Button>
          )}
          {campaign.status === CampaignStatus.PAUSED && (
            <Button onClick={() => resumeMutation.mutate(id)} disabled={resumeMutation.isPending}>
              <RotateCcw className="mr-2 h-4 w-4" />
              {t('campaigns.resume')}
            </Button>
          )}
          <Button variant="destructive" size="sm" onClick={() => setDeleteOpen(true)}>
            <Trash2 className="h-4 w-4" />
          </Button>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {statCards.map((s) => (
          <Card key={s.label}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">{s.label}</CardTitle>
              <s.icon className="h-4 w-4 text-[var(--text-muted)]" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{typeof s.value === 'number' ? s.value.toLocaleString() : s.value}</div>
            </CardContent>
          </Card>
        ))}
      </div>

      <Tabs defaultValue="details">
        <TabsList>
          <TabsTrigger value="details">{t('campaigns.detail.tabs.details')}</TabsTrigger>
          <TabsTrigger value="leads">{t('campaigns.detail.tabs.leads')}</TabsTrigger>
          <TabsTrigger value="emails">{t('campaigns.detail.tabs.emails')}</TabsTrigger>
        </TabsList>

        <TabsContent value="details" className="space-y-4 mt-4">
          <Card>
            <CardHeader>
              <CardTitle>{t('campaigns.form.targetCriteria')}</CardTitle>
            </CardHeader>
            <CardContent>
              <dl className="grid gap-3 sm:grid-cols-2">
                {Object.entries(campaign.target_criteria || {}).map(([key, value]) => (
                  <div key={key}>
                    <dt className="text-sm text-[var(--text-muted)] capitalize">{key.replace(/_/g, ' ')}</dt>
                    <dd className="text-sm text-[var(--text-primary)]">{String(value) || '-'}</dd>
                  </div>
                ))}
              </dl>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>{t('campaigns.form.settings')}</CardTitle>
            </CardHeader>
            <CardContent>
              <dl className="grid gap-3 sm:grid-cols-2">
                <div>
                  <dt className="text-sm text-[var(--text-muted)]">{t('campaigns.form.bantThreshold')}</dt>
                  <dd className="text-sm text-[var(--text-primary)]">{campaign.bant_threshold}</dd>
                </div>
                <div>
                  <dt className="text-sm text-[var(--text-muted)]">{t('campaigns.form.dailyLimit')}</dt>
                  <dd className="text-sm text-[var(--text-primary)]">{campaign.daily_limit}</dd>
                </div>
                <div>
                  <dt className="text-sm text-[var(--text-muted)]">{t('campaigns.table.created')}</dt>
                  <dd className="text-sm text-[var(--text-primary)]">{format(new Date(campaign.created_at), 'dd/MM/yyyy HH:mm')}</dd>
                </div>
                {campaign.started_at && (
                  <div>
                    <dt className="text-sm text-[var(--text-muted)]">Started</dt>
                    <dd className="text-sm text-[var(--text-primary)]">{format(new Date(campaign.started_at), 'dd/MM/yyyy HH:mm')}</dd>
                  </div>
                )}
              </dl>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="leads" className="mt-4">
          <DataTable
            columns={leadColumns}
            data={leadsData?.data ?? []}
            isLoading={!leadsData}
            emptyMessage={t('leads.empty.title')}
            emptyIcon={Users}
            onRowClick={(l) => router.push(`/leads/${l.id}`)}
          />
          {leadsData?.pagination && (
            <Pagination pagination={leadsData.pagination} onPageChange={setLeadsSkip} />
          )}
        </TabsContent>

        <TabsContent value="emails" className="mt-4">
          <DataTable
            columns={emailColumns}
            data={emailsData?.data ?? []}
            isLoading={!emailsData}
            emptyMessage={t('emails.empty.title')}
            emptyIcon={Mail}
          />
          {emailsData?.pagination && (
            <Pagination pagination={emailsData.pagination} onPageChange={setEmailsSkip} />
          )}
        </TabsContent>
      </Tabs>

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
