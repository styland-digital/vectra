"use client"

import { Formik, Form, Field, type FieldProps } from "formik"
import { useState } from "react"
import Link from "next/link"
import { z } from "zod"
import { Loader2, CheckCircle2 } from "lucide-react"

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

const forgotPasswordSchema = z.object({
  email: z.string().email("Please enter a valid email address"),
})

type ForgotPasswordFormData = z.infer<typeof forgotPasswordSchema>

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
      setIsSuccess(true)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="flex flex-col space-y-2 text-center">
      <h1 className="text-2xl font-semibold tracking-tight">
        {t("auth.forgotPassword.title")}
      </h1>
      <p className="text-sm text-muted-foreground">
        {t("auth.forgotPassword.subtitle")}
      </p>

      <Card className="w-full">
        <CardHeader className="space-y-1">
          <CardTitle className="text-2xl text-left">
            {t("auth.forgotPassword.title")}
          </CardTitle>
          <CardDescription className="text-left">
            {t("auth.forgotPassword.subtitle")}
          </CardDescription>
        </CardHeader>

        {isSuccess ? (
          <CardContent className="space-y-4 text-left">
            <div className="flex items-center space-x-3 rounded-lg border border-[var(--color-success-500)] bg-[var(--color-success-500)]/10 p-4">
              <CheckCircle2 className="h-5 w-5 text-[var(--color-success-500)]" />
              <p className="text-sm">
                {t("auth.forgotPassword.successMessage")}
              </p>
            </div>
            <div className="text-center">
              <Link
                href="/login"
                className="text-sm text-muted-foreground hover:text-primary underline underline-offset-4"
              >
                {t("auth.forgotPassword.backToLogin")}
              </Link>
            </div>
          </CardContent>
        ) : (
          <Formik
            initialValues={{ email: "" }}
            validate={toFormikValidate(forgotPasswordSchema)}
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
                    <Label htmlFor="email">
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
                        {t("auth.forgotPassword.submitting")}
                      </>
                    ) : (
                      t("auth.forgotPassword.submit")
                    )}
                  </Button>

                  <div className="text-center text-sm">
                    <Link
                      href="/login"
                      className="text-muted-foreground hover:text-primary underline underline-offset-4"
                    >
                      {t("auth.forgotPassword.backToLogin")}
                    </Link>
                  </div>
                </CardFooter>
              </Form>
            )}
          </Formik>
        )}
      </Card>
    </div>
  )
}
