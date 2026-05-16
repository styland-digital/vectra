'use client'

import { useState } from 'react'
import { format } from 'date-fns'
import { Mail, Check, X, MousePointerClick, Eye } from 'lucide-react'
import { Formik, Form, Field } from 'formik'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetDescription,
} from '@/components/ui/sheet'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '@/components/ui/dialog'
import { Card, CardContent } from '@/components/ui/card'
import { DataTable, type Column } from '@/components/features/data-table'
import { StatusBadge } from '@/components/features/status-badge'
import { Pagination } from '@/components/features/pagination'
import { LoadingSkeleton } from '@/components/loading-skeleton'
import { useEmails, useEmail } from '@/lib/hooks/queries'
import { useApproveEmail, useRejectEmail } from '@/lib/hooks/mutations'
import { useTranslation } from '@/lib/i18n'
import { toFormikValidate } from '@/lib/formik-zod'
import { emailRejectSchema } from '@/lib/schemas/emails'
import { EmailStatus, type Email as EmailType } from '@/types'
import { cn } from '@/lib/utils'

const PAGE_SIZE = 10

interface CampaignEmailsTabProps {
  campaignId: string
}

function EmailEngagement({ email }: { email: EmailType }) {
  if (email.clicked_at) {
    return (
      <span className="inline-flex items-center gap-1 text-caption font-medium text-[var(--color-primary-600)]">
        <MousePointerClick className="h-3 w-3" />
        Clicked
      </span>
    )
  }
  if (email.opened_at) {
    return (
      <span className="inline-flex items-center gap-1 text-caption font-medium text-[var(--color-success-600)]">
        <Eye className="h-3 w-3" />
        Opened
      </span>
    )
  }
  return <span className="text-caption text-[var(--text-muted)]">—</span>
}

export function CampaignEmailsTab({ campaignId }: CampaignEmailsTabProps) {
  const { t } = useTranslation()
  const [skip, setSkip] = useState(0)
  const [statusFilter, setStatusFilter] = useState('all')
  const [selectedEmailId, setSelectedEmailId] = useState<string | null>(null)
  const [rejectEmailId, setRejectEmailId] = useState<string | null>(null)

  const { data: emailsData, isLoading } = useEmails({
    campaign_id: campaignId,
    skip,
    limit: PAGE_SIZE,
    status: statusFilter === 'all' ? undefined : statusFilter,
  })

  const { data: emailDetail, isLoading: detailLoading } = useEmail(selectedEmailId ?? '')

  const approveMutation = useApproveEmail()
  const rejectMutation = useRejectEmail()

  const pendingCount =
    emailsData?.data?.filter((e) => e.status === EmailStatus.PENDING).length ?? 0

  const columns: Column<EmailType>[] = [
    {
      key: 'to',
      header: t('emails.table.to'),
      render: (e) => (
        <div>
          <p className="font-medium text-[var(--text-primary)]">{e.lead?.name ?? '—'}</p>
          <p className="text-caption text-[var(--text-muted)] truncate max-w-[160px]">
            {e.lead?.email ?? ''}
          </p>
        </div>
      ),
    },
    {
      key: 'subject',
      header: t('emails.table.subject'),
      hideBelow: 'md',
      render: (e) => (
        <span className="text-body-sm text-[var(--text-secondary)] truncate max-w-[220px] block">
          {e.subject}
        </span>
      ),
    },
    {
      key: 'status',
      header: t('emails.table.status'),
      render: (e) => <StatusBadge status={e.status} type="email" />,
    },
    {
      key: 'engagement',
      header: t('emails.table.engagement'),
      hideBelow: 'lg',
      render: (e) => <EmailEngagement email={e} />,
    },
    {
      key: 'created',
      header: t('emails.table.created'),
      hideBelow: 'xl',
      render: (e) => (
        <span className="text-body-sm text-[var(--text-muted)] tabular-nums">
          {format(new Date(e.created_at), 'dd MMM yyyy')}
        </span>
      ),
    },
    {
      key: 'actions',
      header: '',
      className: 'w-[80px]',
      render: (e) => {
        if (e.status !== EmailStatus.PENDING) return null
        return (
          <div
            className="flex items-center gap-1"
            onClick={(ev) => ev.stopPropagation()}
          >
            <Button
              size="sm"
              variant="ghost"
              className="h-7 w-7 p-0 text-[var(--color-success-500)] hover:text-[var(--color-success-600)] hover:bg-[var(--color-success-500)]/10"
              onClick={() => approveMutation.mutate(e.id)}
              disabled={approveMutation.isPending}
              title={t('emails.approve')}
            >
              <Check className="h-4 w-4" />
            </Button>
            <Button
              size="sm"
              variant="ghost"
              className="h-7 w-7 p-0 text-[var(--color-error-500)] hover:text-[var(--color-error-600)] hover:bg-[var(--color-error-500)]/10"
              onClick={() => setRejectEmailId(e.id)}
              title={t('emails.reject')}
            >
              <X className="h-4 w-4" />
            </Button>
          </div>
        )
      },
    },
  ]

  return (
    <div className="space-y-4">
      {/* ─── Toolbar ─────────────────────────────────────────────────────────── */}
      <div className="flex items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          {pendingCount > 0 && (
            <Badge variant="default">
              {pendingCount} {t('emails.pending')}
            </Badge>
          )}
        </div>
        <Select
          value={statusFilter}
          onValueChange={(v) => {
            setStatusFilter(v)
            setSkip(0)
          }}
        >
          <SelectTrigger className="w-[160px]">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">{t('emails.filters.allStatuses')}</SelectItem>
            <SelectItem value="pending">{t('emails.status.pending')}</SelectItem>
            <SelectItem value="approved">{t('emails.status.approved')}</SelectItem>
            <SelectItem value="rejected">{t('emails.status.rejected')}</SelectItem>
            <SelectItem value="sent">{t('emails.status.sent')}</SelectItem>
            <SelectItem value="opened">{t('emails.status.opened')}</SelectItem>
            <SelectItem value="clicked">{t('emails.status.clicked')}</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* ─── Table ───────────────────────────────────────────────────────────── */}
      <DataTable
        columns={columns}
        data={emailsData?.data ?? []}
        isLoading={isLoading}
        emptyMessage={t('emails.empty.title')}
        emptyDescription={t('emails.empty.description')}
        emptyIcon={Mail}
        onRowClick={(e) => setSelectedEmailId(e.id)}
        rowClassName={(e) =>
          e.status === EmailStatus.PENDING
            ? 'ring-1 ring-inset ring-[var(--color-warning-500)]/25 bg-[var(--color-warning-500)]/5'
            : ''
        }
      />

      {emailsData?.pagination && (
        <Pagination pagination={emailsData.pagination} onPageChange={setSkip} />
      )}

      {/* ─── Email Detail Sheet ───────────────────────────────────────────────── */}
      <Sheet
        open={!!selectedEmailId}
        onOpenChange={(open) => !open && setSelectedEmailId(null)}
      >
        <SheetContent className="sm:max-w-lg overflow-y-auto">
          <SheetHeader>
            <SheetTitle>{t('emails.detail.preview')}</SheetTitle>
            <SheetDescription>{emailDetail?.subject ?? ''}</SheetDescription>
          </SheetHeader>

          {detailLoading ? (
            <div className="mt-6">
              <LoadingSkeleton variant="card" />
            </div>
          ) : emailDetail ? (
            <div className="mt-6 space-y-4">
              {/* Metadata */}
              <div className="space-y-2">
                <div className="flex justify-between text-body-sm">
                  <span className="text-[var(--text-muted)]">{t('emails.detail.from')}</span>
                  <span className="text-[var(--text-primary)]">
                    {emailDetail.from_name} &lt;{emailDetail.from_email}&gt;
                  </span>
                </div>
                <div className="flex justify-between text-body-sm">
                  <span className="text-[var(--text-muted)]">{t('emails.detail.to')}</span>
                  <span className="text-[var(--text-primary)]">{emailDetail.to_email}</span>
                </div>
                <div className="flex justify-between text-body-sm">
                  <span className="text-[var(--text-muted)]">{t('emails.detail.subject')}</span>
                  <span className="text-[var(--text-primary)] text-right max-w-[60%]">
                    {emailDetail.subject}
                  </span>
                </div>
                <div className="flex justify-between items-center text-body-sm">
                  <span className="text-[var(--text-muted)]">Status</span>
                  <StatusBadge status={emailDetail.status} type="email" />
                </div>
              </div>

              {/* Email body */}
              <Card>
                <CardContent className="p-4">
                  <div
                    className={cn(
                      'max-w-none text-body-sm text-[var(--text-secondary)]',
                      '[&_p]:mb-3 [&_p:last-child]:mb-0',
                      '[&_strong]:text-[var(--text-primary)] [&_strong]:font-medium',
                      '[&_a]:text-[var(--color-primary-500)] [&_a]:underline [&_a]:underline-offset-2'
                    )}
                    dangerouslySetInnerHTML={{
                      __html: emailDetail.body_html || emailDetail.body_text,
                    }}
                  />
                </CardContent>
              </Card>

              {/* Tracking */}
              {emailDetail.tracking && (
                <div className="space-y-2">
                  <h4 className="text-body-sm font-medium text-[var(--text-primary)]">
                    {t('emails.detail.tracking')}
                  </h4>
                  <div className="grid grid-cols-2 gap-3">
                    <div className="rounded-md border border-[var(--border-primary)] p-3 text-center">
                      <p className="text-2xl font-bold text-[var(--text-primary)]">
                        {emailDetail.tracking.opened_count}
                      </p>
                      <p className="text-caption text-[var(--text-muted)]">
                        {t('emails.detail.opens')}
                      </p>
                    </div>
                    <div className="rounded-md border border-[var(--border-primary)] p-3 text-center">
                      <p className="text-2xl font-bold text-[var(--text-primary)]">
                        {emailDetail.tracking.clicked_count}
                      </p>
                      <p className="text-caption text-[var(--text-muted)]">
                        {t('emails.detail.clicks')}
                      </p>
                    </div>
                  </div>
                </div>
              )}

              <p className="text-caption text-[var(--text-muted)]">
                {t('emails.detail.generatedBy')}: {emailDetail.generated_by} (
                {emailDetail.generation_model})
              </p>

              {/* Approve / Reject */}
              {emailDetail.status === EmailStatus.PENDING && (
                <div className="flex gap-2 pt-2">
                  <Button
                    className="flex-1"
                    onClick={() =>
                      approveMutation.mutate(emailDetail.id, {
                        onSuccess: () => setSelectedEmailId(null),
                      })
                    }
                    disabled={approveMutation.isPending}
                  >
                    <Check className="mr-2 h-4 w-4" />
                    {t('emails.approve')}
                  </Button>
                  <Button
                    variant="destructive"
                    className="flex-1"
                    onClick={() => {
                      setSelectedEmailId(null)
                      setRejectEmailId(emailDetail.id)
                    }}
                  >
                    <X className="mr-2 h-4 w-4" />
                    {t('emails.reject')}
                  </Button>
                </div>
              )}
            </div>
          ) : null}
        </SheetContent>
      </Sheet>

      {/* ─── Reject Dialog ────────────────────────────────────────────────────── */}
      <Dialog
        open={!!rejectEmailId}
        onOpenChange={(open) => !open && setRejectEmailId(null)}
      >
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{t('emails.reject')}</DialogTitle>
            <DialogDescription>{t('emails.rejectDescription')}</DialogDescription>
          </DialogHeader>
          <Formik
            initialValues={{ reason: '' }}
            validate={toFormikValidate(emailRejectSchema)}
            onSubmit={async (values) => {
              if (rejectEmailId) {
                await rejectMutation.mutateAsync({ id: rejectEmailId, reason: values.reason })
                setRejectEmailId(null)
              }
            }}
          >
            {({ errors, touched, isSubmitting }) => (
              <Form className="space-y-4">
                <div className="space-y-2">
                  <Label>{t('emails.detail.rejectReason')}</Label>
                  <Field
                    as={Input}
                    name="reason"
                    placeholder={t('emails.detail.rejectPlaceholder')}
                  />
                  {errors.reason && touched.reason && (
                    <p className="text-body-sm text-[var(--color-error-500)]">
                      {errors.reason}
                    </p>
                  )}
                </div>
                <DialogFooter>
                  <Button
                    type="button"
                    variant="outline"
                    onClick={() => setRejectEmailId(null)}
                  >
                    {t('common.cancel')}
                  </Button>
                  <Button type="submit" variant="destructive" disabled={isSubmitting}>
                    {isSubmitting ? t('common.submitting') : t('emails.reject')}
                  </Button>
                </DialogFooter>
              </Form>
            )}
          </Formik>
        </DialogContent>
      </Dialog>
    </div>
  )
}
