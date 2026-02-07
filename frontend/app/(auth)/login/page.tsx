"use client"

import { Formik, Form, Field, type FieldProps } from "formik"
import { useRouter, useSearchParams } from "next/navigation"
import Link from "next/link"
import { Loader2 } from "lucide-react"
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
import { PageTransition, AnimatePresence, motion } from "@/components/motion"
import { useAuthStore } from "@/lib/stores/auth"
import { loginSchema, type LoginFormData } from "@/lib/schemas/auth"
import { toFormikValidate } from "@/lib/formik-zod"
import { useTranslation } from "@/lib/i18n"

function LoginForm() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const redirectTo = searchParams.get("redirect") || "/"
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
    >
    <Card className="w-full">
      <CardHeader className="space-y-1">
        <CardTitle className="text-h3 text-left">
          {t("auth.login.cardTitle")}
        </CardTitle>
        <CardDescription className="text-left">
          {t("auth.login.cardDescription")}
        </CardDescription>
      </CardHeader>

      <Formik
        initialValues={initialValues}
        validate={toFormikValidate(loginSchema)}
        onSubmit={handleSubmit}
      >
        {({ errors, touched }) => (
          <Form>
            <CardContent className="space-y-4 text-left">
              <AnimatePresence>
                {error && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: "auto" }}
                    exit={{ opacity: 0, height: 0 }}
                    transition={{ duration: 0.2 }}
                  >
                    <Alert variant="destructive">
                      <AlertDescription>{error}</AlertDescription>
                    </Alert>
                  </motion.div>
                )}
              </AnimatePresence>

              <div className="space-y-2">
                <Label htmlFor="email">{t("auth.login.email")}</Label>
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
                <Label htmlFor="password">{t("auth.login.password")}</Label>
                <Field name="password">
                  {({ field }: FieldProps) => (
                    <Input
                      {...field}
                      id="password"
                      type="password"
                      disabled={isLoading}
                    />
                  )}
                </Field>
                {touched.password && errors.password && (
                  <p className="text-xs text-[var(--color-error-500)]">
                    {errors.password}
                  </p>
                )}
              </div>
            </CardContent>

            <CardFooter className="flex flex-col space-y-4">
              <Button
                type="submit"
                className="w-full"
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

              <div className="text-center text-sm">
                <Link
                  href="/register"
                  className="text-muted-foreground hover:text-primary underline underline-offset-4 transition-colors duration-150"
                >
                  {t("auth.login.noAccount")}
                </Link>
              </div>

              <div className="text-center text-sm">
                <Link
                  href="/forgot-password"
                  className="text-muted-foreground hover:text-primary underline underline-offset-4 transition-colors duration-150"
                >
                  {t("auth.login.forgotPassword")}
                </Link>
              </div>
            </CardFooter>
          </Form>
        )}
      </Formik>
    </Card>
    </motion.div>
  )
}

export default function LoginPage() {
  const { t } = useTranslation()

  return (
    <PageTransition>
      <div className="flex flex-col space-y-4 text-center">
        <div className="flex flex-col space-y-2">
          <h1 className="text-h2 tracking-tight">
            {t("auth.login.title")}
          </h1>
          <p className="text-sm text-muted-foreground">
            {t("auth.login.subtitle")}
          </p>
        </div>

        <Suspense
          fallback={
            <Card className="w-full">
              <CardContent className="py-8 flex justify-center">
                <Loader2 className="h-6 w-6 animate-spin" />
              </CardContent>
            </Card>
          }
        >
          <LoginForm />
        </Suspense>
      </div>
    </PageTransition>
  )
}
