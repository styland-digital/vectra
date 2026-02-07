'use client'

import { format } from 'date-fns'
import { Calendar, ExternalLink } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { StatusBadge } from '@/components/features/status-badge'
import { EmptyState } from '@/components/features/empty-state'
import { LoadingSkeleton } from '@/components/loading-skeleton'
import { PageTransition } from '@/components/motion'
import { useLeads } from '@/lib/hooks/queries'
import { useTranslation } from '@/lib/i18n'
import type { Lead, Meeting } from '@/types'

function MeetingCard({ lead, meeting }: { lead: Lead; meeting: Meeting }) {
  const { t } = useTranslation()

  return (
    <Card>
      <CardContent className="p-4">
        <div className="flex items-start justify-between">
          <div className="space-y-1">
            <p className="font-medium text-[var(--text-primary)]">
              {lead.first_name} {lead.last_name}
            </p>
            <p className="text-sm text-[var(--text-muted)]">{lead.company?.name ?? '-'}</p>
            <div className="flex items-center space-x-2 text-sm text-[var(--text-secondary)]">
              <Calendar className="h-3.5 w-3.5" />
              <span>{t('meetings.scheduledAt')}: {format(new Date(meeting.scheduled_at), 'dd/MM/yyyy HH:mm')}</span>
            </div>
          </div>
          <div className="flex flex-col items-end space-y-2">
            <StatusBadge status={meeting.status} type="meeting" />
            {meeting.calendly_url && (
              <Button variant="outline" size="sm" asChild>
                <a href={meeting.calendly_url} target="_blank" rel="noopener noreferrer">
                  <ExternalLink className="mr-1.5 h-3.5 w-3.5" />
                  {t('meetings.openCalendly')}
                </a>
              </Button>
            )}
          </div>
        </div>
        {meeting.notes && (
          <p className="mt-3 text-sm text-[var(--text-muted)] border-t border-[var(--border-primary)] pt-3">
            {meeting.notes}
          </p>
        )}
      </CardContent>
    </Card>
  )
}

export default function MeetingsPage() {
  const { t } = useTranslation()

  const { data: leadsData, isLoading } = useLeads({ limit: 100 })

  if (isLoading) {
    return (
      <div className="space-y-6">
        <h1 className="text-h1 text-[var(--text-primary)]">{t('meetings.title')}</h1>
        <LoadingSkeleton variant="card" />
        <LoadingSkeleton variant="card" />
      </div>
    )
  }

  const leads = leadsData?.data ?? []

  // Extract meetings from leads that have them
  const meetingsWithLeads: Array<{ lead: Lead; meeting: Meeting }> = []
  for (const lead of leads) {
    const leadDetail = lead as Lead & { meetings?: Meeting[] }
    if (leadDetail.meetings) {
      for (const meeting of leadDetail.meetings) {
        meetingsWithLeads.push({ lead, meeting })
      }
    }
  }

  const upcoming = meetingsWithLeads.filter((m) => m.meeting.status === 'scheduled')
  const completed = meetingsWithLeads.filter((m) => m.meeting.status === 'completed')
  const noShow = meetingsWithLeads.filter((m) => m.meeting.status === 'no_show')

  return (
    <PageTransition>
    <div className="space-y-6">
      <div>
        <h1 className="text-h1 text-[var(--text-primary)]">{t('meetings.title')}</h1>
        <p className="text-[var(--text-muted)]">{t('meetings.subtitle')}</p>
      </div>

      <Tabs defaultValue="upcoming">
        <TabsList>
          <TabsTrigger value="upcoming">
            {t('meetings.tabs.upcoming')} ({upcoming.length})
          </TabsTrigger>
          <TabsTrigger value="completed">
            {t('meetings.tabs.completed')} ({completed.length})
          </TabsTrigger>
          <TabsTrigger value="noShow">
            {t('meetings.tabs.noShow')} ({noShow.length})
          </TabsTrigger>
        </TabsList>

        <TabsContent value="upcoming" className="mt-4">
          {upcoming.length > 0 ? (
            <div className="grid gap-4 md:grid-cols-2">
              {upcoming.map((m) => (
                <MeetingCard key={m.meeting.id} lead={m.lead} meeting={m.meeting} />
              ))}
            </div>
          ) : (
            <EmptyState
              icon={Calendar}
              title={t('meetings.empty.title')}
              description={t('meetings.empty.description')}
            />
          )}
        </TabsContent>

        <TabsContent value="completed" className="mt-4">
          {completed.length > 0 ? (
            <div className="grid gap-4 md:grid-cols-2">
              {completed.map((m) => (
                <MeetingCard key={m.meeting.id} lead={m.lead} meeting={m.meeting} />
              ))}
            </div>
          ) : (
            <EmptyState icon={Calendar} title={t('meetings.noResults')} />
          )}
        </TabsContent>

        <TabsContent value="noShow" className="mt-4">
          {noShow.length > 0 ? (
            <div className="grid gap-4 md:grid-cols-2">
              {noShow.map((m) => (
                <MeetingCard key={m.meeting.id} lead={m.lead} meeting={m.meeting} />
              ))}
            </div>
          ) : (
            <EmptyState icon={Calendar} title={t('meetings.noResults')} />
          )}
        </TabsContent>
      </Tabs>
    </div>
    </PageTransition>
  )
}
