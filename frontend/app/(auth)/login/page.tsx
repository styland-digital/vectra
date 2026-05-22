"use client"

import { Formik, Form, Field, type FieldProps } from "formik"
import { useState } from "react"
import { useRouter, useSearchParams } from "next/navigation"
import Link from "next/link"
import { Loader2, Eye, EyeOff } from "lucide-react"
import { Suspense } from "react"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { PageTransition, AnimatePresence, motion } from "@/components/motion"
import { useAuthStore } from "@/lib/stores/auth"
import { createLoginSchema, type LoginFormData } from "@/lib/schemas/auth"
import { toFormikValidate } from "@/lib/formik-zod"
import { useTranslation } from "@/lib/i18n"

function LoginForm() {
  const [showPassword, setShowPassword] = useState(false)
  const router = useRouter()
  const searchParams = useSearchParams()
  const redirectTo = searchParams.get("redirect") || "/dashboard"
  const { login, isLoading, error, clearError } = useAuthStore()
  const { t } = useTranslation()

  const initialValues: LoginFormData = {
    email: "",
    password: "",
  }

  const handleSubmit = async (values: LoginFormData) => {
    clearError()
    try {
      await login(values.email, values.password)
      router.push(redirectTo)
    } catch {
      // Error is handled by the store
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, ease: [0, 0, 0.2, 1], delay: 0.1 }}
      className="w-full space-y-6"
    >
      <div>
        <h2 className="text-h3 text-[var(--text-primary)]">
          {t("auth.login.cardTitle")}
        </h2>
        <p className="text-body-sm text-[var(--text-muted)] mt-1">
          {t("auth.login.cardDescription")}
        </p>
      </div>

      <Formik
        initialValues={initialValues}
        validate={toFormikValidate(createLoginSchema(t))}
        onSubmit={handleSubmit}
      >
        {({ errors, touched }) => (
          <Form onChange={() => { if (error) clearError() }} className="space-y-5">
            <AnimatePresence>
              {error && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: "auto" }}
                  exit={{ opacity: 0, height: 0 }}
                  transition={{ duration: 0.2 }}
                >
                  <Alert variant="destructive">
                    <AlertDescription>
                      {error?.startsWith("auth.") ? t(error) : error}
                    </AlertDescription>
                  </Alert>
                </motion.div>
              )}
            </AnimatePresence>

            <div className="space-y-2">
              <Label htmlFor="email" className="text-body-sm font-medium text-[var(--text-primary)]">
                {t("auth.login.email")}
              </Label>
              <Field name="email">
                {({ field }: FieldProps) => (
                  <Input
                    {...field}
                    id="email"
                    type="email"
                    placeholder={t("auth.login.emailPlaceholder")}
                    disabled={isLoading}
                  />
                )}
              </Field>
              {touched.email && errors.email && (
                <p className="text-xs text-[var(--color-error-500)]">
                  {errors.email}
                </p>
              )}
            </div>

            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <Label htmlFor="password" className="text-body-sm font-medium text-[var(--text-primary)]">
                  {t("auth.login.password")}
                </Label>
                <Link
                  href="/forgot-password"
                  className="text-caption text-[var(--color-primary-500)] hover:text-[var(--color-primary-600)] hover:underline underline-offset-4 transition-colors duration-150"
                >
                  {t("auth.login.forgotPassword")}
                </Link>
              </div>
              <div className="relative">
                <Field name="password">
                  {({ field }: FieldProps) => (
                    <Input
                      {...field}
                      id="password"
                      type={showPassword ? "text" : "password"}
                      disabled={isLoading}
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
              {touched.password && errors.password && (
                <p className="text-xs text-[var(--color-error-500)]">
                  {errors.password}
                </p>
              )}
            </div>

            <div className="space-y-4 pt-1">
              <Button
                type="submit"
                className="w-full h-11"
                disabled={isLoading}
              >
                {isLoading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    {t("auth.login.submitting")}
                  </>
                ) : (
                  t("auth.login.submit")
                )}
              </Button>

              <p className="text-center text-body-sm text-[var(--text-muted)]">
                <Link
                  href="/register"
                  className="text-[var(--color-primary-500)] hover:text-[var(--color-primary-600)] hover:underline underline-offset-4 transition-colors duration-150"
                >
                  {t("auth.login.noAccount")}
                </Link>
              </p>
            </div>
          </Form>
        )}
      </Formik>
    </motion.div>
  )
}

export default function LoginPage() {
  return (
    <PageTransition>
      <Suspense fallback={<div className="h-64" />}>
        <LoginForm />
      </Suspense>
    </PageTransition>
  )
}
