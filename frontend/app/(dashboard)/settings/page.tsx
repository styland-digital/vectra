'use client'

import { useState } from 'react'
import { format } from 'date-fns'
import { Formik, Form, Field } from 'formik'
import { UserPlus, Trash2, CreditCard, Globe } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '@/components/ui/dialog'
import { DataTable, type Column } from '@/components/features/data-table'
import { ConfirmDialog } from '@/components/features/confirm-dialog'
import { LoadingSkeleton } from '@/components/loading-skeleton'
import { PageTransition } from '@/components/motion'
import { useOrganization, useOrgUsers } from '@/lib/hooks/queries'
import {
  useUpdateOrganization,
  useInviteUser,
  useUpdateUserRole,
  useRemoveUser,
} from '@/lib/hooks/mutations'
import { useAuthStore } from '@/lib/stores/auth'
import { useUIStore } from '@/lib/stores/ui'
import { useTranslation } from '@/lib/i18n'
import { toFormikValidate } from '@/lib/formik-zod'
import { organizationUpdateSchema } from '@/lib/schemas/settings'
import { inviteUserSchema } from '@/lib/schemas/settings'
import { api } from '@/lib/api'
import { UserRole, type OrganizationUser } from '@/types'

const ROLE_OPTIONS = [
  { value: 'admin', labelKey: 'settings.team.roles.admin' },
  { value: 'manager', labelKey: 'settings.team.roles.manager' },
  { value: 'operator', labelKey: 'settings.team.roles.operator' },
  { value: 'viewer', labelKey: 'settings.team.roles.viewer' },
]

function OrganizationTab() {
  const { t } = useTranslation()
  const { data: org, isLoading } = useOrganization()
  const updateMutation = useUpdateOrganization()

  if (isLoading || !org) return <LoadingSkeleton variant="card" />

  return (
    <div className="space-y-6 max-w-2xl">
      <Card>
        <CardHeader>
          <CardTitle>{t('settings.organization.title')}</CardTitle>
        </CardHeader>
        <CardContent>
          <Formik
            initialValues={{ name: org.name }}
            validate={toFormikValidate(organizationUpdateSchema)}
            onSubmit={async (values) => {
              await updateMutation.mutateAsync({ name: values.name })
            }}
            enableReinitialize
          >
            {({ errors, touched, isSubmitting, dirty }) => (
              <Form className="space-y-4">
                <div className="space-y-2">
                  <Label>{t('settings.organization.name')}</Label>
                  <Field as={Input} name="name" />
                  {errors.name && touched.name && (
                    <p className="text-sm text-[var(--color-error-500)]">{errors.name}</p>
                  )}
                </div>
                <Button type="submit" disabled={isSubmitting || !dirty}>
                  {isSubmitting ? t('common.saving') : t('common.save')}
                </Button>
              </Form>
            )}
          </Formik>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>{t('settings.organization.plan')}</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-between">
            <Badge variant="secondary" className="capitalize text-base px-3 py-1">
              {org.plan}
            </Badge>
            <Button
              variant="outline"
              onClick={async () => {
                const res = await api.billing.createPortal()
                window.open(res.data.session_url, '_blank')
              }}
            >
              <CreditCard className="mr-2 h-4 w-4" />
              {t('settings.organization.manageSubscription')}
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

function TeamTab() {
  const { t } = useTranslation()
  const { user } = useAuthStore()
  const { data: users, isLoading } = useOrgUsers()
  const updateRoleMutation = useUpdateUserRole()
  const removeMutation = useRemoveUser()
  const inviteMutation = useInviteUser()

  const [inviteOpen, setInviteOpen] = useState(false)
  const [removeUserId, setRemoveUserId] = useState<string | null>(null)

  const isAdmin = user?.role === UserRole.OWNER || user?.role === UserRole.ADMIN

  const columns: Column<OrganizationUser>[] = [
    {
      key: 'name',
      header: t('settings.team.table.name'),
      render: (u) => (
        <div>
          <p className="font-medium text-[var(--text-primary)]">{u.first_name} {u.last_name}</p>
          <p className="text-xs text-[var(--text-muted)]">{u.email}</p>
        </div>
      ),
    },
    {
      key: 'role',
      header: t('settings.team.table.role'),
      render: (u) => {
        if (!isAdmin || u.role === UserRole.OWNER || u.id === user?.id) {
          return (
            <Badge variant="outline" className="capitalize">
              {t(`settings.team.roles.${u.role}`)}
            </Badge>
          )
        }
        return (
          <Select
            value={u.role}
            onValueChange={(role) => updateRoleMutation.mutate({ userId: u.id, role })}
          >
            <SelectTrigger className="w-[130px] h-8">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {ROLE_OPTIONS.map((r) => (
                <SelectItem key={r.value} value={r.value}>{t(r.labelKey)}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        )
      },
    },
    {
      key: 'status',
      header: t('settings.team.table.status'),
      render: (u) => (
        <Badge variant={u.is_active ? 'default' : 'secondary'}>
          {u.is_active ? t('common.active') : t('common.inactive')}
        </Badge>
      ),
    },
    {
      key: 'lastLogin',
      header: t('settings.team.table.lastLogin'),
      render: (u) => (
        <span className="text-sm text-[var(--text-muted)]">
          {u.last_login_at ? format(new Date(u.last_login_at), 'dd/MM/yyyy') : '-'}
        </span>
      ),
    },
    {
      key: 'actions',
      header: '',
      className: 'w-[50px]',
      render: (u) => {
        if (!isAdmin || u.role === UserRole.OWNER || u.id === user?.id) return null
        return (
          <Button
            variant="ghost"
            size="sm"
            className="h-7 w-7 p-0 text-[var(--color-error-500)] hover:text-[var(--color-error-600)]"
            onClick={(e) => { e.stopPropagation(); setRemoveUserId(u.id) }}
          >
            <Trash2 className="h-4 w-4" />
          </Button>
        )
      },
    },
  ]

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-medium text-[var(--text-primary)]">{t('settings.team.title')}</h3>
          <p className="text-sm text-[var(--text-muted)]">{t('settings.team.subtitle')}</p>
        </div>
        {isAdmin && (
          <Button onClick={() => setInviteOpen(true)}>
            <UserPlus className="mr-2 h-4 w-4" />
            {t('settings.team.invite')}
          </Button>
        )}
      </div>

      <DataTable
        columns={columns}
        data={users ?? []}
        isLoading={isLoading}
        emptyMessage={t('common.noResults')}
      />

      {/* Invite Dialog */}
      <Dialog open={inviteOpen} onOpenChange={setInviteOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{t('settings.team.invite')}</DialogTitle>
          </DialogHeader>
          <Formik
            initialValues={{ email: '', first_name: '', last_name: '', role: 'viewer' }}
            validate={toFormikValidate(inviteUserSchema)}
            onSubmit={async (values) => {
              await inviteMutation.mutateAsync(values)
              setInviteOpen(false)
            }}
          >
            {({ errors, touched, isSubmitting }) => (
              <Form className="space-y-4">
                <div className="grid gap-4 sm:grid-cols-2">
                  <div className="space-y-2">
                    <Label>First name</Label>
                    <Field as={Input} name="first_name" />
                    {errors.first_name && touched.first_name && (
                      <p className="text-sm text-[var(--color-error-500)]">{errors.first_name}</p>
                    )}
                  </div>
                  <div className="space-y-2">
                    <Label>Last name</Label>
                    <Field as={Input} name="last_name" />
                    {errors.last_name && touched.last_name && (
                      <p className="text-sm text-[var(--color-error-500)]">{errors.last_name}</p>
                    )}
                  </div>
                </div>
                <div className="space-y-2">
                  <Label>Email</Label>
                  <Field as={Input} name="email" type="email" />
                  {errors.email && touched.email && (
                    <p className="text-sm text-[var(--color-error-500)]">{errors.email}</p>
                  )}
                </div>
                <div className="space-y-2">
                  <Label>Role</Label>
                  <Field name="role">
                    {({ field, form }: { field: { value: string }; form: { setFieldValue: (field: string, value: string) => void } }) => (
                      <Select value={field.value} onValueChange={(v) => form.setFieldValue('role', v)}>
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          {ROLE_OPTIONS.map((r) => (
                            <SelectItem key={r.value} value={r.value}>{t(r.labelKey)}</SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    )}
                  </Field>
                </div>
                <DialogFooter>
                  <Button type="button" variant="outline" onClick={() => setInviteOpen(false)}>
                    {t('common.cancel')}
                  </Button>
                  <Button type="submit" disabled={isSubmitting}>
                    {isSubmitting ? t('common.submitting') : t('settings.team.invite')}
                  </Button>
                </DialogFooter>
              </Form>
            )}
          </Formik>
        </DialogContent>
      </Dialog>

      <ConfirmDialog
        open={!!removeUserId}
        onOpenChange={(open) => !open && setRemoveUserId(null)}
        title={t('settings.team.confirmRemove.title')}
        description={t('settings.team.confirmRemove.description')}
        variant="destructive"
        confirmLabel={t('common.remove')}
        isLoading={removeMutation.isPending}
        onConfirm={() => {
          if (removeUserId) {
            removeMutation.mutate(removeUserId, {
              onSuccess: () => setRemoveUserId(null),
            })
          }
        }}
      />
    </div>
  )
}

function BillingTab() {
  const { t } = useTranslation()
  const { data: org, isLoading } = useOrganization()

  if (isLoading || !org) return <LoadingSkeleton variant="card" />

  return (
    <div className="space-y-6 max-w-2xl">
      <Card>
        <CardHeader>
          <CardTitle>{t('settings.billing.currentPlan')}</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-between">
            <Badge variant="secondary" className="capitalize text-base px-3 py-1">
              {org.plan}
            </Badge>
            <div className="flex space-x-2">
              <Button
                variant="outline"
                onClick={async () => {
                  const res = await api.billing.createPortal()
                  window.open(res.data.session_url, '_blank')
                }}
              >
                {t('settings.billing.manageSubscription')}
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

function AccountTab() {
  const { t } = useTranslation()
  const { user } = useAuthStore()
  const { locale, setLocale } = useUIStore()

  return (
    <div className="space-y-6 max-w-2xl">
      <Card>
        <CardHeader>
          <CardTitle>{t('settings.account.profile')}</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label>{t('settings.account.name')}</Label>
            <Input value={user ? `${user.first_name} ${user.last_name}` : ''} disabled />
          </div>
          <div className="space-y-2">
            <Label>{t('settings.account.email')}</Label>
            <Input value={user?.email ?? ''} disabled />
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>{t('settings.account.changePassword')}</CardTitle>
          <CardDescription>{t('settings.account.changePassword')}</CardDescription>
        </CardHeader>
        <CardContent>
          <Button
            variant="outline"
            onClick={async () => {
              await api.auth.changePasswordRequest()
            }}
          >
            {t('settings.account.changePassword')}
          </Button>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Globe className="mr-2 h-4 w-4" />
            {t('settings.account.language')}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <Select value={locale} onValueChange={(v) => setLocale(v as 'fr' | 'en')}>
            <SelectTrigger className="w-[200px]">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="fr">Francais</SelectItem>
              <SelectItem value="en">English</SelectItem>
            </SelectContent>
          </Select>
        </CardContent>
      </Card>
    </div>
  )
}

export default function SettingsPage() {
  const { t } = useTranslation()
  const { user } = useAuthStore()
  const isAdmin = user?.role === UserRole.OWNER || user?.role === UserRole.ADMIN

  return (
    <PageTransition>
    <div className="space-y-6">
      <div>
        <h1 className="text-h1 text-[var(--text-primary)]">{t('settings.title')}</h1>
        <p className="text-[var(--text-muted)]">{t('settings.subtitle')}</p>
      </div>

      <Tabs defaultValue="organization">
        <TabsList>
          <TabsTrigger value="organization">{t('settings.tabs.organization')}</TabsTrigger>
          {isAdmin && <TabsTrigger value="team">{t('settings.tabs.team')}</TabsTrigger>}
          <TabsTrigger value="billing">{t('settings.tabs.billing')}</TabsTrigger>
          <TabsTrigger value="account">{t('settings.tabs.account')}</TabsTrigger>
        </TabsList>

        <TabsContent value="organization" className="mt-6">
          <OrganizationTab />
        </TabsContent>

        {isAdmin && (
          <TabsContent value="team" className="mt-6">
            <TeamTab />
          </TabsContent>
        )}

        <TabsContent value="billing" className="mt-6">
          <BillingTab />
        </TabsContent>

        <TabsContent value="account" className="mt-6">
          <AccountTab />
        </TabsContent>
      </Tabs>
    </div>
    </PageTransition>
  )
}
