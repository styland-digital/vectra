"use client"

import { Formik, Form, Field, type FieldProps } from "formik"
import { useState } from "react"
import { useRouter, useSearchParams } from "next/navigation"
import Link from "next/link"
import { Loader2, Eye, EyeOff, CheckCircle2 } from "lucide-react"
import { Suspense } from "react"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { PageTransition } from "@/components/motion"
import { api } from "@/lib/api"
import { createResetPasswordSchema } from "@/lib/schemas/auth"
import { toFormikValidate } from "@/lib/formik-zod"
import { useTranslation } from "@/lib/i18n"

type ResetPasswordFormData = { password: string; confirmPassword: string }

function ResetPasswordForm() {
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isSuccess, setIsSuccess] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const router = useRouter()
  const searchParams = useSearchParams()
  const token = searchParams.get("token")
  const { t } = useTranslation()

  if (!token) {
    return (
      <div className="space-y-4">
        <Alert variant="destructive">
          <AlertDescription>
            {t("auth.resetPassword.invalidToken")}
          </AlertDescription>
        </Alert>
        <Link
          href="/login"
          className="block text-center text-body-sm text-[var(--color-primary-500)] hover:text-[var(--color-primary-600)] hover:underline underline-offset-4 transition-colors duration-150"
        >
          {t("auth.resetPassword.backToLogin")}
        </Link>
      </div>
    )
  }

  const handleSubmit = async (values: ResetPasswordFormData) => {
    setIsSubmitting(true)
    setError(null)
    try {
      await api.auth.resetPassword(token, values.password, values.confirmPassword)
      setIsSuccess(true)
      setTimeout(() => router.push("/login"), 3000)
    } catch {
      setError(t("auth.errors.genericError"))
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="w-full space-y-6">
      <div>
        <h2 className="text-h3 text-[var(--text-primary)]">
          {t("auth.resetPassword.title")}
        </h2>
        <p className="text-body-sm text-[var(--text-muted)] mt-1">
          {t("auth.resetPassword.subtitle")}
        </p>
      </div>

      {isSuccess ? (
        <div className="flex items-center space-x-3 rounded-lg border border-[var(--color-success-500)] bg-[var(--color-success-50)] p-4">
          <CheckCircle2 className="h-5 w-5 text-[var(--color-success-600)] shrink-0" />
          <p className="text-body-sm text-[var(--color-success-700)]">
            {t("auth.resetPassword.successMessage")}
          </p>
        </div>
      ) : (
        <Formik
          initialValues={{ password: "", confirmPassword: "" }}
          validate={toFormikValidate(createResetPasswordSchema(t))}
          onSubmit={handleSubmit}
        >
          {({ errors, touched }) => (
            <Form onChange={() => { if (error) setError(null) }} className="space-y-5">
              {error && (
                <Alert variant="destructive">
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              )}

              <div className="space-y-2">
                <Label htmlFor="password" className="text-body-sm font-medium text-[var(--text-primary)]">
                  {t("auth.resetPassword.password")}
                </Label>
                <div className="relative">
                  <Field name="password">
                    {({ field }: FieldProps) => (
                      <Input
                        {...field}
                        id="password"
                        type={showPassword ? "text" : "password"}
                        disabled={isSubmitting}
                        className="pr-10"
                      />
                    )}
                  </Field>
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-[var(--text-muted)] hover:text-[var(--text-secondary)] transition-colors duration-150"
                  >
                    {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </button>
                </div>
                <p className="text-xs text-[var(--text-muted)]">
                  {t("auth.register.passwordRequirements")}
                </p>
                {touched.password && errors.password && (
                  <p className="text-xs text-[var(--color-error-500)]">
                    {errors.password}
                  </p>
                )}
              </div>

              <div className="space-y-2">
                <Label htmlFor="confirmPassword" className="text-body-sm font-medium text-[var(--text-primary)]">
                  {t("auth.resetPassword.confirmPassword")}
                </Label>
                <div className="relative">
                  <Field name="confirmPassword">
                    {({ field }: FieldProps) => (
                      <Input
                        {...field}
                        id="confirmPassword"
                        type={showConfirmPassword ? "text" : "password"}
                        disabled={isSubmitting}
                        className="pr-10"
                      />
                    )}
                  </Field>
                  <button
                    type="button"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-[var(--text-muted)] hover:text-[var(--text-secondary)] transition-colors duration-150"
                  >
                    {showConfirmPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </button>
                </div>
                {touched.confirmPassword && errors.confirmPassword && (
                  <p className="text-xs text-[var(--color-error-500)]">
                    {errors.confirmPassword}
                  </p>
                )}
              </div>

              <div className="space-y-4 pt-1">
                <Button type="submit" className="w-full h-11" disabled={isSubmitting}>
                  {isSubmitting ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      {t("auth.resetPassword.submitting")}
                    </>
                  ) : (
                    t("auth.resetPassword.submit")
                  )}
                </Button>

                <p className="text-center">
                  <Link
                    href="/login"
                    className="text-body-sm text-[var(--color-primary-500)] hover:text-[var(--color-primary-600)] hover:underline underline-offset-4 transition-colors duration-150"
                  >
                    {t("auth.resetPassword.backToLogin")}
                  </Link>
                </p>
              </div>
            </Form>
          )}
        </Formik>
      )}
    </div>
  )
}

export default function ResetPasswordPage() {
  return (
    <PageTransition>
      <Suspense fallback={<div className="h-64" />}>
        <ResetPasswordForm />
      </Suspense>
    </PageTransition>
  )
}
