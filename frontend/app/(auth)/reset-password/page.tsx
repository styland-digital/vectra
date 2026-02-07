"use client"

import { Formik, Form, Field, type FieldProps } from "formik"
import { useState } from "react"
import { useRouter, useSearchParams } from "next/navigation"
import Link from "next/link"
import { z } from "zod"
import { Loader2, Eye, EyeOff, CheckCircle2 } from "lucide-react"
import { Suspense } from "react"

import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { api } from "@/lib/api"
import { toFormikValidate } from "@/lib/formik-zod"
import { useTranslation } from "@/lib/i18n"

const resetPasswordSchema = z
  .object({
    password: z
      .string()
      .min(8, "Password must be at least 8 characters")
      .regex(
        /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/,
        "Password must contain uppercase, lowercase, and number"
      ),
    confirmPassword: z.string(),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: "Passwords do not match",
    path: ["confirmPassword"],
  })

type ResetPasswordFormData = z.infer<typeof resetPasswordSchema>

function ResetPasswordForm() {
  const [showPassword, setShowPassword] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isSuccess, setIsSuccess] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const router = useRouter()
  const searchParams = useSearchParams()
  const token = searchParams.get("token")
  const { t } = useTranslation()

  if (!token) {
    return (
      <Card className="w-full">
        <CardContent className="py-8">
          <Alert variant="destructive">
            <AlertDescription>
              {t("auth.resetPassword.invalidToken")}
            </AlertDescription>
          </Alert>
          <div className="mt-4 text-center">
            <Link
              href="/login"
              className="text-sm text-muted-foreground hover:text-primary underline underline-offset-4"
            >
              {t("auth.resetPassword.backToLogin")}
            </Link>
          </div>
        </CardContent>
      </Card>
    )
  }

  const handleSubmit = async (values: ResetPasswordFormData) => {
    setIsSubmitting(true)
    setError(null)
    try {
      await api.auth.resetPassword(
        token,
        values.password,
        values.confirmPassword
      )
      setIsSuccess(true)
      setTimeout(() => router.push("/login"), 3000)
    } catch {
      setError(t("auth.errors.genericError"))
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <Card className="w-full">
      <CardHeader className="space-y-1">
        <CardTitle className="text-2xl text-left">
          {t("auth.resetPassword.title")}
        </CardTitle>
        <CardDescription className="text-left">
          {t("auth.resetPassword.subtitle")}
        </CardDescription>
      </CardHeader>

      {isSuccess ? (
        <CardContent className="space-y-4 text-left">
          <div className="flex items-center space-x-3 rounded-lg border border-[var(--color-success-500)] bg-[var(--color-success-500)]/10 p-4">
            <CheckCircle2 className="h-5 w-5 text-[var(--color-success-500)]" />
            <p className="text-sm">
              {t("auth.resetPassword.successMessage")}
            </p>
          </div>
        </CardContent>
      ) : (
        <Formik
          initialValues={{ password: "", confirmPassword: "" }}
          validate={toFormikValidate(resetPasswordSchema)}
          onSubmit={handleSubmit}
        >
          {({ errors, touched }) => (
            <Form>
              <CardContent className="space-y-4 text-left">
                {error && (
                  <Alert variant="destructive">
                    <AlertDescription>{error}</AlertDescription>
                  </Alert>
                )}

                <div className="space-y-2">
                  <Label htmlFor="password">
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
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-[var(--text-muted)] hover:text-[var(--text-primary)]"
                    >
                      {showPassword ? (
                        <EyeOff className="h-4 w-4" />
                      ) : (
                        <Eye className="h-4 w-4" />
                      )}
                    </button>
                  </div>
                  {touched.password && errors.password && (
                    <p className="text-xs text-[var(--color-error-500)]">
                      {errors.password}
                    </p>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="confirmPassword">
                    {t("auth.resetPassword.confirmPassword")}
                  </Label>
                  <Field name="confirmPassword">
                    {({ field }: FieldProps) => (
                      <Input
                        {...field}
                        id="confirmPassword"
                        type="password"
                        disabled={isSubmitting}
                      />
                    )}
                  </Field>
                  {touched.confirmPassword && errors.confirmPassword && (
                    <p className="text-xs text-[var(--color-error-500)]">
                      {errors.confirmPassword}
                    </p>
                  )}
                </div>
              </CardContent>

              <CardFooter className="flex flex-col space-y-4">
                <Button
                  type="submit"
                  className="w-full"
                  disabled={isSubmitting}
                >
                  {isSubmitting ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      {t("auth.resetPassword.submitting")}
                    </>
                  ) : (
                    t("auth.resetPassword.submit")
                  )}
                </Button>

                <div className="text-center text-sm">
                  <Link
                    href="/login"
                    className="text-muted-foreground hover:text-primary underline underline-offset-4"
                  >
                    {t("auth.resetPassword.backToLogin")}
                  </Link>
                </div>
              </CardFooter>
            </Form>
          )}
        </Formik>
      )}
    </Card>
  )
}

export default function ResetPasswordPage() {
  const { t } = useTranslation()

  return (
    <div className="flex flex-col space-y-2 text-center">
      <h1 className="text-2xl font-semibold tracking-tight">
        {t("auth.resetPassword.title")}
      </h1>
      <p className="text-sm text-muted-foreground">
        {t("auth.resetPassword.subtitle")}
      </p>

      <Suspense
        fallback={
          <Card className="w-full">
            <CardContent className="py-8 flex justify-center">
              <Loader2 className="h-6 w-6 animate-spin" />
            </CardContent>
          </Card>
        }
      >
        <ResetPasswordForm />
      </Suspense>
    </div>
  )
}
