"use client"

import { Formik, Form, Field, type FieldProps } from "formik"
import { useState } from "react"
import Link from "next/link"
import { Loader2, CheckCircle2 } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { api } from "@/lib/api"
import { createForgotPasswordSchema } from "@/lib/schemas/auth"
import { toFormikValidate } from "@/lib/formik-zod"
import { useTranslation } from "@/lib/i18n"

type ForgotPasswordFormData = { email: string }

export default function ForgotPasswordPage() {
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isSuccess, setIsSuccess] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const { t } = useTranslation()

  const handleSubmit = async (values: ForgotPasswordFormData) => {
    setIsSubmitting(true)
    setError(null)
    try {
      await api.auth.forgotPassword(values.email)
      setIsSuccess(true)
    } catch {
      setError(t("auth.errors.genericError"))
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="flex flex-col space-y-6">
      <div>
        <h2 className="text-h3 text-[var(--text-primary)]">
          {t("auth.forgotPassword.title")}
        </h2>
        <p className="text-body-sm text-[var(--text-muted)] mt-1">
          {t("auth.forgotPassword.subtitle")}
        </p>
      </div>

      {isSuccess ? (
        <div className="space-y-4">
          <div className="flex items-center space-x-3 rounded-lg border border-[var(--color-success-500)] bg-[var(--color-success-50)] p-4">
            <CheckCircle2 className="h-5 w-5 text-[var(--color-success-600)] shrink-0" />
            <p className="text-body-sm text-[var(--color-success-700)]">
              {t("auth.forgotPassword.successMessage")}
            </p>
          </div>
          <Link
            href="/login"
            className="block text-center text-body-sm text-[var(--color-primary-500)] hover:text-[var(--color-primary-600)] hover:underline underline-offset-4 transition-colors duration-150"
          >
            {t("auth.forgotPassword.backToLogin")}
          </Link>
        </div>
      ) : (
        <Formik
          initialValues={{ email: "" }}
          validate={toFormikValidate(createForgotPasswordSchema(t))}
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
                <Label htmlFor="email" className="text-body-sm font-medium text-[var(--text-primary)]">
                  {t("auth.forgotPassword.email")}
                </Label>
                <Field name="email">
                  {({ field }: FieldProps) => (
                    <Input
                      {...field}
                      id="email"
                      type="email"
                      placeholder="m@example.com"
                      disabled={isSubmitting}
                    />
                  )}
                </Field>
                {touched.email && errors.email && (
                  <p className="text-xs text-[var(--color-error-500)]">
                    {errors.email}
                  </p>
                )}
              </div>

              <div className="space-y-4 pt-1">
                <Button type="submit" className="w-full h-11" disabled={isSubmitting}>
                  {isSubmitting ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      {t("auth.forgotPassword.submitting")}
                    </>
                  ) : (
                    t("auth.forgotPassword.submit")
                  )}
                </Button>

                <p className="text-center">
                  <Link
                    href="/login"
                    className="text-body-sm text-[var(--color-primary-500)] hover:text-[var(--color-primary-600)] hover:underline underline-offset-4 transition-colors duration-150"
                  >
                    {t("auth.forgotPassword.backToLogin")}
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
