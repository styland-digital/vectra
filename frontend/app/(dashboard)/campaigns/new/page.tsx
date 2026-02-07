'use client'

import { useRouter } from 'next/navigation'
import { Formik, Form, Field } from 'formik'
import { ArrowLeft } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { useCreateCampaign } from '@/lib/hooks/mutations'
import { useTranslation } from '@/lib/i18n'
import { toFormikValidate } from '@/lib/formik-zod'
import { campaignCreateSchema, type CampaignCreateFormData } from '@/lib/schemas/campaigns'
import Link from 'next/link'

const initialValues: CampaignCreateFormData = {
  name: '',
  description: '',
  target_criteria: {
    job_titles: '',
    locations: '',
    company_sizes: '',
    industries: '',
  },
  email_template: {
    subject: '',
    tone: 'professional',
  },
  bant_threshold: 60,
  daily_limit: 50,
}

export default function NewCampaignPage() {
  const { t } = useTranslation()
  const router = useRouter()
  const createMutation = useCreateCampaign()

  return (
    <div className="space-y-6">
      <div className="flex items-center space-x-4">
        <Button variant="ghost" size="sm" asChild>
          <Link href="/campaigns">
            <ArrowLeft className="mr-2 h-4 w-4" />
            {t('common.back')}
          </Link>
        </Button>
        <div>
          <h1 className="text-3xl font-bold text-[var(--text-primary)]">{t('campaigns.create')}</h1>
        </div>
      </div>

      <Formik
        initialValues={initialValues}
        validate={toFormikValidate(campaignCreateSchema)}
        onSubmit={async (values) => {
          const payload = {
            name: values.name,
            description: values.description || undefined,
            target_criteria: values.target_criteria as Record<string, unknown>,
            email_template: values.email_template as Record<string, unknown>,
            bant_threshold: values.bant_threshold,
            daily_limit: values.daily_limit,
          }
          await createMutation.mutateAsync(payload)
          router.push('/campaigns')
        }}
      >
        {({ errors, touched, isSubmitting }) => (
          <Form className="space-y-6 max-w-2xl">
            <Card>
              <CardHeader>
                <CardTitle>{t('campaigns.form.name')}</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="name">{t('campaigns.form.name')}</Label>
                  <Field
                    as={Input}
                    id="name"
                    name="name"
                    placeholder={t('campaigns.form.namePlaceholder')}
                  />
                  {errors.name && touched.name && (
                    <p className="text-sm text-red-400">{errors.name}</p>
                  )}
                </div>
                <div className="space-y-2">
                  <Label htmlFor="description">{t('campaigns.form.description')}</Label>
                  <Field
                    as={Input}
                    id="description"
                    name="description"
                    placeholder={t('campaigns.form.descriptionPlaceholder')}
                  />
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>{t('campaigns.form.targetCriteria')}</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid gap-4 sm:grid-cols-2">
                  <div className="space-y-2">
                    <Label>{t('campaigns.form.jobTitles')}</Label>
                    <Field
                      as={Input}
                      name="target_criteria.job_titles"
                      placeholder={t('campaigns.form.jobTitlesPlaceholder')}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label>{t('campaigns.form.locations')}</Label>
                    <Field
                      as={Input}
                      name="target_criteria.locations"
                      placeholder={t('campaigns.form.locationsPlaceholder')}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label>{t('campaigns.form.companySizes')}</Label>
                    <Field
                      as={Input}
                      name="target_criteria.company_sizes"
                      placeholder={t('campaigns.form.companySizesPlaceholder')}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label>{t('campaigns.form.industries')}</Label>
                    <Field
                      as={Input}
                      name="target_criteria.industries"
                      placeholder={t('campaigns.form.industriesPlaceholder')}
                    />
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>{t('campaigns.form.emailTemplate')}</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label>{t('campaigns.form.subject')}</Label>
                  <Field
                    as={Input}
                    name="email_template.subject"
                    placeholder={t('campaigns.form.subjectPlaceholder')}
                  />
                </div>
                <div className="space-y-2">
                  <Label>{t('campaigns.form.tone')}</Label>
                  <Field
                    as={Input}
                    name="email_template.tone"
                    placeholder="professional"
                  />
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>{t('campaigns.form.settings')}</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid gap-4 sm:grid-cols-2">
                  <div className="space-y-2">
                    <Label>{t('campaigns.form.bantThreshold')}</Label>
                    <Field
                      as={Input}
                      type="number"
                      name="bant_threshold"
                      min={0}
                      max={100}
                    />
                    {errors.bant_threshold && touched.bant_threshold && (
                      <p className="text-sm text-red-400">{errors.bant_threshold}</p>
                    )}
                  </div>
                  <div className="space-y-2">
                    <Label>{t('campaigns.form.dailyLimit')}</Label>
                    <Field
                      as={Input}
                      type="number"
                      name="daily_limit"
                      min={1}
                      max={200}
                    />
                    {errors.daily_limit && touched.daily_limit && (
                      <p className="text-sm text-red-400">{errors.daily_limit}</p>
                    )}
                  </div>
                </div>
              </CardContent>
            </Card>

            <div className="flex justify-end space-x-3">
              <Button type="button" variant="outline" asChild>
                <Link href="/campaigns">{t('common.cancel')}</Link>
              </Button>
              <Button type="submit" disabled={isSubmitting}>
                {isSubmitting ? t('common.submitting') : t('campaigns.create')}
              </Button>
            </div>
          </Form>
        )}
      </Formik>
    </div>
  )
}
