'use client'

import { useState } from 'react'
import { useParams } from 'next/navigation'
import { format } from 'date-fns'
import { ArrowLeft, Pencil, Mail, Calendar, User, Building2, Briefcase } from 'lucide-react'
import { Formik, Form, Field } from 'formik'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '@/components/ui/dialog'
import { StatusBadge } from '@/components/features/status-badge'
import { BANTScoreBar } from '@/components/features/bant-score-bar'
import { LoadingSkeleton } from '@/components/loading-skeleton'
import { useLead } from '@/lib/hooks/queries'
import { useUpdateLead } from '@/lib/hooks/mutations'
import { useTranslation } from '@/lib/i18n'
import { toFormikValidate } from '@/lib/formik-zod'
import { leadUpdateSchema } from '@/lib/schemas/leads'
import Link from 'next/link'

export default function LeadDetailPage() {
  const { t } = useTranslation()
  const params = useParams()
  const id = params.id as string
  const [editOpen, setEditOpen] = useState(false)

  const { data: lead, isLoading } = useLead(id)
  const updateMutation = useUpdateLead()

  if (isLoading || !lead) {
    return (
      <div className="space-y-6">
        <LoadingSkeleton variant="card" />
        <LoadingSkeleton variant="card" />
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Button variant="ghost" size="sm" asChild>
            <Link href="/leads">
              <ArrowLeft className="mr-2 h-4 w-4" />
              {t('common.back')}
            </Link>
          </Button>
          <div>
            <div className="flex items-center space-x-3">
              <h1 className="text-3xl font-bold text-[var(--text-primary)]">
                {lead.first_name} {lead.last_name}
              </h1>
              <StatusBadge status={lead.status} type="lead" />
            </div>
            <p className="text-[var(--text-muted)]">{lead.email}</p>
          </div>
        </div>
        <Button variant="outline" onClick={() => setEditOpen(true)}>
          <Pencil className="mr-2 h-4 w-4" />
          {t('common.edit')}
        </Button>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <User className="mr-2 h-4 w-4" />
                {t('leads.detail.contactInfo')}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <dl className="space-y-3">
                <div className="flex justify-between">
                  <dt className="text-sm text-[var(--text-muted)]">Email</dt>
                  <dd className="text-sm text-[var(--text-primary)]">{lead.email}</dd>
                </div>
                {lead.phone && (
                  <div className="flex justify-between">
                    <dt className="text-sm text-[var(--text-muted)]">Phone</dt>
                    <dd className="text-sm text-[var(--text-primary)]">{lead.phone}</dd>
                  </div>
                )}
                {lead.linkedin_url && (
                  <div className="flex justify-between">
                    <dt className="text-sm text-[var(--text-muted)]">LinkedIn</dt>
                    <dd className="text-sm">
                      <a href={lead.linkedin_url} target="_blank" rel="noopener noreferrer" className="text-[var(--color-primary-500)] hover:underline">
                        Profile
                      </a>
                    </dd>
                  </div>
                )}
              </dl>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Building2 className="mr-2 h-4 w-4" />
                {t('leads.detail.companyInfo')}
              </CardTitle>
            </CardHeader>
            <CardContent>
              {lead.company ? (
                <dl className="space-y-3">
                  <div className="flex justify-between">
                    <dt className="text-sm text-[var(--text-muted)]">Name</dt>
                    <dd className="text-sm text-[var(--text-primary)]">{lead.company.name}</dd>
                  </div>
                  {lead.company.industry && (
                    <div className="flex justify-between">
                      <dt className="text-sm text-[var(--text-muted)]">Industry</dt>
                      <dd className="text-sm text-[var(--text-primary)]">{lead.company.industry}</dd>
                    </div>
                  )}
                  {lead.company.size && (
                    <div className="flex justify-between">
                      <dt className="text-sm text-[var(--text-muted)]">Size</dt>
                      <dd className="text-sm text-[var(--text-primary)]">{lead.company.size}</dd>
                    </div>
                  )}
                  {lead.company.location && (
                    <div className="flex justify-between">
                      <dt className="text-sm text-[var(--text-muted)]">Location</dt>
                      <dd className="text-sm text-[var(--text-primary)]">{lead.company.location}</dd>
                    </div>
                  )}
                </dl>
              ) : (
                <p className="text-sm text-[var(--text-muted)]">-</p>
              )}
            </CardContent>
          </Card>

          {lead.job && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Briefcase className="mr-2 h-4 w-4" />
                  {t('leads.detail.jobInfo')}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <dl className="space-y-3">
                  <div className="flex justify-between">
                    <dt className="text-sm text-[var(--text-muted)]">Title</dt>
                    <dd className="text-sm text-[var(--text-primary)]">{lead.job.title}</dd>
                  </div>
                  {lead.job.department && (
                    <div className="flex justify-between">
                      <dt className="text-sm text-[var(--text-muted)]">Department</dt>
                      <dd className="text-sm text-[var(--text-primary)]">{lead.job.department}</dd>
                    </div>
                  )}
                  {lead.job.seniority && (
                    <div className="flex justify-between">
                      <dt className="text-sm text-[var(--text-muted)]">Seniority</dt>
                      <dd className="text-sm text-[var(--text-primary)]">{lead.job.seniority}</dd>
                    </div>
                  )}
                </dl>
              </CardContent>
            </Card>
          )}
        </div>

        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>{t('leads.detail.bantScore')}</CardTitle>
            </CardHeader>
            <CardContent>
              {lead.bant ? (
                <BANTScoreBar
                  score={lead.bant.score}
                  budget={lead.bant.budget}
                  authority={lead.bant.authority}
                  need={lead.bant.need}
                  timeline={lead.bant.timeline}
                  showDetails
                />
              ) : (
                <p className="text-sm text-[var(--text-muted)]">-</p>
              )}
            </CardContent>
          </Card>

          {lead.email_status && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Mail className="mr-2 h-4 w-4" />
                  {t('leads.detail.emailStatus')}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <StatusBadge status={lead.email_status} type="email" />
                {lead.email_sent_at && (
                  <p className="text-xs text-[var(--text-muted)] mt-2">
                    Sent: {format(new Date(lead.email_sent_at), 'dd/MM/yyyy HH:mm')}
                  </p>
                )}
              </CardContent>
            </Card>
          )}

          {lead.meetings && lead.meetings.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Calendar className="mr-2 h-4 w-4" />
                  {t('leads.detail.meetingInfo')}
                </CardTitle>
              </CardHeader>
              <CardContent>
                {lead.meetings.map((m) => (
                  <div key={m.id} className="flex items-center justify-between">
                    <StatusBadge status={m.status} type="meeting" />
                    <span className="text-sm text-[var(--text-muted)]">
                      {format(new Date(m.scheduled_at), 'dd/MM/yyyy HH:mm')}
                    </span>
                  </div>
                ))}
              </CardContent>
            </Card>
          )}
        </div>
      </div>

      <Tabs defaultValue="interactions">
        <TabsList>
          <TabsTrigger value="interactions">{t('leads.detail.interactions')}</TabsTrigger>
        </TabsList>
        <TabsContent value="interactions" className="mt-4">
          {lead.interactions && lead.interactions.length > 0 ? (
            <div className="space-y-3">
              {lead.interactions.map((interaction) => (
                <Card key={interaction.id}>
                  <CardContent className="py-3">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium text-[var(--text-primary)] capitalize">
                          {interaction.type}
                        </p>
                        <p className="text-xs text-[var(--text-muted)]">
                          {interaction.agent_type} - {format(new Date(interaction.created_at), 'dd/MM/yyyy HH:mm')}
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          ) : (
            <p className="text-sm text-[var(--text-muted)] py-8 text-center">{t('leads.detail.noInteractions')}</p>
          )}
        </TabsContent>
      </Tabs>

      <Dialog open={editOpen} onOpenChange={setEditOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{t('leads.edit')}</DialogTitle>
          </DialogHeader>
          <Formik
            initialValues={{
              first_name: lead.first_name,
              last_name: lead.last_name,
              phone: lead.phone ?? '',
              company_name: lead.company?.name ?? '',
              job_title: lead.job?.title ?? '',
              notes: '',
            }}
            validate={toFormikValidate(leadUpdateSchema)}
            onSubmit={async (values) => {
              await updateMutation.mutateAsync({
                id,
                data: {
                  first_name: values.first_name,
                  last_name: values.last_name,
                  phone: values.phone || null,
                },
              })
              setEditOpen(false)
            }}
          >
            {({ errors, touched, isSubmitting }) => (
              <Form className="space-y-4">
                <div className="grid gap-4 sm:grid-cols-2">
                  <div className="space-y-2">
                    <Label>First name</Label>
                    <Field as={Input} name="first_name" />
                    {errors.first_name && touched.first_name && (
                      <p className="text-sm text-red-400">{errors.first_name}</p>
                    )}
                  </div>
                  <div className="space-y-2">
                    <Label>Last name</Label>
                    <Field as={Input} name="last_name" />
                    {errors.last_name && touched.last_name && (
                      <p className="text-sm text-red-400">{errors.last_name}</p>
                    )}
                  </div>
                </div>
                <div className="space-y-2">
                  <Label>Phone</Label>
                  <Field as={Input} name="phone" />
                </div>
                <DialogFooter>
                  <Button type="button" variant="outline" onClick={() => setEditOpen(false)}>
                    {t('common.cancel')}
                  </Button>
                  <Button type="submit" disabled={isSubmitting}>
                    {isSubmitting ? t('common.saving') : t('common.save')}
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
