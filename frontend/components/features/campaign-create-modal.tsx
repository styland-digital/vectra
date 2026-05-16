'use client'

import { useState } from 'react'
import { z } from 'zod'
import { Target, ChevronRight, Check, AlertCircle } from 'lucide-react'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Alert, AlertDescription } from '@/components/ui/alert'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { cn } from '@/lib/utils'
import { useCreateCampaign } from '@/lib/hooks/mutations'
import { useTranslation } from '@/lib/i18n'

// ─── Per-step Zod schemas ────────────────────────────────────────────────────

const step1Schema = z.object({
  name: z.string().min(1, 'Campaign name is required').max(100, 'Max 100 characters'),
  description: z.string().max(500, 'Max 500 characters').optional(),
})

const step3Schema = z.object({
  bant_threshold: z
    .number({ invalid_type_error: 'Must be a number' })
    .min(0, 'Min 0')
    .max(100, 'Max 100'),
  daily_limit: z
    .number({ invalid_type_error: 'Must be a number' })
    .min(1, 'Min 1')
    .max(200, 'Max 200'),
})

// ─── Types ───────────────────────────────────────────────────────────────────

interface FormState {
  name: string
  description: string
  job_titles: string
  locations: string
  company_sizes: string
  industries: string
  subject: string
  tone: 'professional' | 'friendly' | 'direct'
  bant_threshold: number
  daily_limit: number
}

const initialForm: FormState = {
  name: '',
  description: '',
  job_titles: '',
  locations: '',
  company_sizes: '',
  industries: '',
  subject: '',
  tone: 'professional',
  bant_threshold: 60,
  daily_limit: 50,
}

interface StepErrors {
  name?: string
  bant_threshold?: string
  daily_limit?: string
}

const STEPS = [
  { label: 'Basics', hint: 'Name & goal' },
  { label: 'Targeting', hint: 'Audience criteria' },
  { label: 'Settings', hint: 'Template & limits' },
] as const

// ─── Step indicator ───────────────────────────────────────────────────────────

function StepIndicator({ current }: { current: number }) {
  return (
    <div className="flex items-center gap-0 w-full mb-6">
      {STEPS.map((step, i) => {
        const idx = i + 1
        const done = idx < current
        const active = idx === current

        return (
          <div key={step.label} className="flex items-center flex-1 last:flex-none">
            <div className="flex flex-col items-center gap-1">
              <div
                className={cn(
                  'h-8 w-8 rounded-full flex items-center justify-center text-caption font-semibold border-2 transition-colors duration-200 shrink-0',
                  done && 'bg-[var(--color-primary-500)] border-[var(--color-primary-500)] text-white',
                  active && 'border-[var(--color-primary-500)] bg-[var(--surface-primary)] text-[var(--color-primary-500)]',
                  !done && !active && 'border-[var(--border-primary)] bg-[var(--surface-secondary)] text-[var(--text-muted)]'
                )}
              >
                {done ? <Check className="h-4 w-4" /> : <span>{idx}</span>}
              </div>
              <span
                className={cn(
                  'text-caption whitespace-nowrap',
                  active ? 'text-[var(--text-primary)] font-medium' : 'text-[var(--text-muted)]'
                )}
              >
                {step.label}
              </span>
            </div>
            {i < STEPS.length - 1 && (
              <div
                className={cn(
                  'flex-1 h-[2px] mx-2 mb-5 rounded-full transition-colors duration-200',
                  done ? 'bg-[var(--color-primary-500)]' : 'bg-[var(--border-primary)]'
                )}
              />
            )}
          </div>
        )
      })}
    </div>
  )
}

// ─── Modal ────────────────────────────────────────────────────────────────────

interface CampaignCreateModalProps {
  open: boolean
  onOpenChange: (open: boolean) => void
}

export function CampaignCreateModal({ open, onOpenChange }: CampaignCreateModalProps) {
  const { t } = useTranslation()
  const [step, setStep] = useState(1)
  const [form, setForm] = useState<FormState>(initialForm)
  const [errors, setErrors] = useState<StepErrors>({})
  const [apiError, setApiError] = useState<string | null>(null)

  const createMutation = useCreateCampaign()

  function set<K extends keyof FormState>(key: K, value: FormState[K]) {
    setForm((prev) => ({ ...prev, [key]: value }))
    // Clear field error on change
    if (key in errors) setErrors((e) => ({ ...e, [key]: undefined }))
    if (apiError) setApiError(null)
  }

  function validateStep1(): boolean {
    const result = step1Schema.safeParse({ name: form.name, description: form.description })
    if (!result.success) {
      const flat = result.error.flatten().fieldErrors
      setErrors({ name: flat.name?.[0] })
      return false
    }
    setErrors({})
    return true
  }

  function validateStep3(): boolean {
    const result = step3Schema.safeParse({
      bant_threshold: form.bant_threshold,
      daily_limit: form.daily_limit,
    })
    if (!result.success) {
      const flat = result.error.flatten().fieldErrors
      setErrors({
        bant_threshold: flat.bant_threshold?.[0],
        daily_limit: flat.daily_limit?.[0],
      })
      return false
    }
    setErrors({})
    return true
  }

  function handleNext() {
    if (step === 1 && !validateStep1()) return
    setStep((s) => (s + 1) as 1 | 2 | 3)
  }

  async function handleSubmit() {
    if (!validateStep3()) return
    setApiError(null)

    try {
      await createMutation.mutateAsync({
        name: form.name,
        description: form.description || undefined,
        target_criteria: {
          job_titles: form.job_titles,
          locations: form.locations,
          company_sizes: form.company_sizes,
          industries: form.industries,
        },
        email_template: {
          subject: form.subject,
          tone: form.tone,
        },
        bant_threshold: form.bant_threshold,
        daily_limit: form.daily_limit,
      })
      handleClose()
    } catch (err) {
      const msg = err instanceof Error ? err.message : 'Failed to create campaign'
      setApiError(msg)
    }
  }

  function handleClose() {
    onOpenChange(false)
    setTimeout(() => {
      setStep(1)
      setForm(initialForm)
      setErrors({})
      setApiError(null)
    }, 200)
  }

  return (
    <Dialog open={open} onOpenChange={handleClose}>
      <DialogContent
        className="sm:max-w-[520px] bg-[var(--surface-primary)] border-[var(--border-primary)] gap-0 p-0 overflow-hidden"
        onChange={() => { if (apiError) setApiError(null) }}
      >
        {/* Header */}
        <DialogHeader className="px-6 pt-6 pb-4 border-b border-[var(--border-primary)]">
          <div className="flex items-center gap-2">
            <div className="h-8 w-8 rounded-lg bg-[var(--surface-secondary)] border border-[var(--border-primary)] flex items-center justify-center shrink-0">
              <Target className="h-4 w-4 text-[var(--color-primary-500)]" />
            </div>
            <DialogTitle className="text-h4 text-[var(--text-primary)]">
              {t('campaigns.new')}
            </DialogTitle>
          </div>
          <DialogDescription className="text-body-sm text-[var(--text-secondary)] mt-1">
            {t('campaigns.createDescription')}
          </DialogDescription>
        </DialogHeader>

        {/* Body */}
        <div className="px-6 py-5">
          <StepIndicator current={step} />

          {apiError && (
            <Alert variant="destructive" className="mb-4">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{apiError}</AlertDescription>
            </Alert>
          )}

          {/* Step 1: Basics */}
          {step === 1 && (
            <div className="space-y-4">
              <div>
                <p className="text-body-sm text-[var(--text-muted)] mb-4">
                  Give your campaign a name and optional description to identify it later.
                </p>
              </div>
              <div className="space-y-1.5">
                <Label htmlFor="modal-name" className="text-body-sm text-[var(--text-secondary)]">
                  Campaign name <span className="text-[var(--color-error-500)]">*</span>
                </Label>
                <Input
                  id="modal-name"
                  value={form.name}
                  onChange={(e) => set('name', e.target.value)}
                  placeholder="e.g. Q2 SaaS Outreach — EMEA"
                  className={cn(errors.name && 'border-[var(--color-error-500)]')}
                  autoFocus
                />
                {errors.name && (
                  <p className="text-caption text-[var(--color-error-500)]">{errors.name}</p>
                )}
              </div>
              <div className="space-y-1.5">
                <Label htmlFor="modal-desc" className="text-body-sm text-[var(--text-secondary)]">
                  Description <span className="text-[var(--text-muted)]">(optional)</span>
                </Label>
                <Input
                  id="modal-desc"
                  value={form.description}
                  onChange={(e) => set('description', e.target.value)}
                  placeholder="Brief goal of this campaign…"
                />
              </div>
            </div>
          )}

          {/* Step 2: Targeting */}
          {step === 2 && (
            <div className="space-y-4">
              <p className="text-body-sm text-[var(--text-muted)] mb-1">
                Define your target audience. Use commas to separate multiple values. All fields are optional.
              </p>
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-1.5">
                  <Label className="text-body-sm text-[var(--text-secondary)]">Job titles</Label>
                  <Input
                    value={form.job_titles}
                    onChange={(e) => set('job_titles', e.target.value)}
                    placeholder="CEO, VP Sales, CTO"
                  />
                </div>
                <div className="space-y-1.5">
                  <Label className="text-body-sm text-[var(--text-secondary)]">Locations</Label>
                  <Input
                    value={form.locations}
                    onChange={(e) => set('locations', e.target.value)}
                    placeholder="France, Germany, UK"
                  />
                </div>
                <div className="space-y-1.5">
                  <Label className="text-body-sm text-[var(--text-secondary)]">Company sizes</Label>
                  <Input
                    value={form.company_sizes}
                    onChange={(e) => set('company_sizes', e.target.value)}
                    placeholder="50-200, 200-1000"
                  />
                </div>
                <div className="space-y-1.5">
                  <Label className="text-body-sm text-[var(--text-secondary)]">Industries</Label>
                  <Input
                    value={form.industries}
                    onChange={(e) => set('industries', e.target.value)}
                    placeholder="SaaS, Fintech, Healthcare"
                  />
                </div>
              </div>
            </div>
          )}

          {/* Step 3: Settings */}
          {step === 3 && (
            <div className="space-y-4">
              <p className="text-body-sm text-[var(--text-muted)] mb-1">
                Configure the email template and AI agent thresholds.
              </p>
              <div className="space-y-1.5">
                <Label className="text-body-sm text-[var(--text-secondary)]">Email subject</Label>
                <Input
                  value={form.subject}
                  onChange={(e) => set('subject', e.target.value)}
                  placeholder="e.g. Quick question about {company}"
                />
              </div>
              <div className="space-y-1.5">
                <Label className="text-body-sm text-[var(--text-secondary)]">Email tone</Label>
                <Select value={form.tone} onValueChange={(v) => set('tone', v as FormState['tone'])}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="professional">Professional</SelectItem>
                    <SelectItem value="friendly">Friendly</SelectItem>
                    <SelectItem value="direct">Direct</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-1.5">
                  <Label className="text-body-sm text-[var(--text-secondary)]">
                    BANT threshold
                    <span className="text-caption text-[var(--text-muted)] ml-1">(0–100)</span>
                  </Label>
                  <Input
                    type="number"
                    min={0}
                    max={100}
                    value={form.bant_threshold}
                    onChange={(e) => set('bant_threshold', Number(e.target.value))}
                    className={cn(errors.bant_threshold && 'border-[var(--color-error-500)]')}
                  />
                  {errors.bant_threshold && (
                    <p className="text-caption text-[var(--color-error-500)]">{errors.bant_threshold}</p>
                  )}
                </div>
                <div className="space-y-1.5">
                  <Label className="text-body-sm text-[var(--text-secondary)]">
                    Daily limit
                    <span className="text-caption text-[var(--text-muted)] ml-1">(1–200)</span>
                  </Label>
                  <Input
                    type="number"
                    min={1}
                    max={200}
                    value={form.daily_limit}
                    onChange={(e) => set('daily_limit', Number(e.target.value))}
                    className={cn(errors.daily_limit && 'border-[var(--color-error-500)]')}
                  />
                  {errors.daily_limit && (
                    <p className="text-caption text-[var(--color-error-500)]">{errors.daily_limit}</p>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="px-6 py-4 border-t border-[var(--border-primary)] flex items-center justify-between gap-3">
          <Button
            variant="ghost"
            size="sm"
            onClick={handleClose}
            className="text-[var(--text-muted)]"
          >
            {t('common.cancel')}
          </Button>
          <div className="flex items-center gap-2">
            {step > 1 && (
              <Button
                variant="outline"
                size="sm"
                onClick={() => setStep((s) => (s - 1) as 1 | 2 | 3)}
              >
                {t('common.back')}
              </Button>
            )}
            {step < 3 ? (
              <Button size="sm" onClick={handleNext}>
                {t('common.next') || 'Next'}
                <ChevronRight className="ml-1.5 h-4 w-4" />
              </Button>
            ) : (
              <Button
                size="sm"
                onClick={handleSubmit}
                disabled={createMutation.isPending}
              >
                {createMutation.isPending ? (t('common.submitting') || 'Creating…') : t('campaigns.create')}
              </Button>
            )}
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}
