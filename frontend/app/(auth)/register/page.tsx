"use client"

import { Formik, Form, Field, type FieldProps } from "formik"
import { useState } from "react"
import { useRouter } from "next/navigation"
import Link from "next/link"
import { Eye, EyeOff, Loader2 } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Checkbox } from "@/components/ui/checkbox"
import { PageTransition, AnimatePresence, motion } from "@/components/motion"
import { useAuthStore } from "@/lib/stores/auth"
import { createRegisterSchema, type RegisterFormData } from "@/lib/schemas/auth"
import { toFormikValidate } from "@/lib/formik-zod"
import { useTranslation } from "@/lib/i18n"

export default function RegisterPage() {
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const router = useRouter()
  const { register, isLoading, error, clearError } = useAuthStore()
  const { t } = useTranslation()

  const initialValues: RegisterFormData = {
    firstName: "",
    lastName: "",
    email: "",
    companyName: "",
    password: "",
    confirmPassword: "",
    terms: false,
  }

  const handleSubmit = async (values: RegisterFormData) => {
    clearError()
    try {
      await register({
        first_name: values.firstName,
        last_name: values.lastName,
        email: values.email,
        organization_name: values.companyName,
        password: values.password,
      })
      router.push("/dashboard")
    } catch {
      // Error is handled by the store
    }
  }

  return (
    <PageTransition>
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, ease: [0, 0, 0.2, 1], delay: 0.1 }}
        className="w-full space-y-6"
      >
          <div>
            <h2 className="text-h3 text-[var(--text-primary)]">
              {t("auth.register.cardTitle")}
            </h2>
            <p className="text-body-sm text-[var(--text-muted)] mt-1">
              {t("auth.register.cardDescription")}
            </p>
          </div>

          <Formik
            initialValues={initialValues}
            validate={toFormikValidate(createRegisterSchema(t))}
            onSubmit={handleSubmit}
          >
            {({ errors, touched, setFieldValue, values }) => (
              <Form onChange={() => { if (error) clearError() }} className="space-y-4">
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

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="firstName" className="text-body-sm font-medium text-[var(--text-primary)]">
                      {t("auth.register.firstName")}
                    </Label>
                    <Field name="firstName">
                      {({ field }: FieldProps) => (
                        <Input {...field} id="firstName" disabled={isLoading} />
                      )}
                    </Field>
                    {touched.firstName && errors.firstName && (
                      <p className="text-xs text-[var(--color-error-500)]">{errors.firstName}</p>
                    )}
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="lastName" className="text-body-sm font-medium text-[var(--text-primary)]">
                      {t("auth.register.lastName")}
                    </Label>
                    <Field name="lastName">
                      {({ field }: FieldProps) => (
                        <Input {...field} id="lastName" disabled={isLoading} />
                      )}
                    </Field>
                    {touched.lastName && errors.lastName && (
                      <p className="text-xs text-[var(--color-error-500)]">{errors.lastName}</p>
                    )}
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="email" className="text-body-sm font-medium text-[var(--text-primary)]">
                    {t("auth.register.email")}
                  </Label>
                  <Field name="email">
                    {({ field }: FieldProps) => (
                      <Input {...field} id="email" type="email" placeholder="m@example.com" disabled={isLoading} />
                    )}
                  </Field>
                  {touched.email && errors.email && (
                    <p className="text-xs text-[var(--color-error-500)]">{errors.email}</p>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="companyName" className="text-body-sm font-medium text-[var(--text-primary)]">
                    {t("auth.register.companyName")}
                  </Label>
                  <Field name="companyName">
                    {({ field }: FieldProps) => (
                      <Input {...field} id="companyName" disabled={isLoading} />
                    )}
                  </Field>
                  {touched.companyName && errors.companyName && (
                    <p className="text-xs text-[var(--color-error-500)]">{errors.companyName}</p>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="password" className="text-body-sm font-medium text-[var(--text-primary)]">
                    {t("auth.register.password")}
                  </Label>
                  <div className="relative">
                    <Field name="password">
                      {({ field }: FieldProps) => (
                        <Input {...field} id="password" type={showPassword ? "text" : "password"} disabled={isLoading} className="pr-10" />
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
                    <p className="text-xs text-[var(--color-error-500)]">{errors.password}</p>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="confirmPassword" className="text-body-sm font-medium text-[var(--text-primary)]">
                    {t("auth.register.confirmPassword")}
                  </Label>
                  <div className="relative">
                    <Field name="confirmPassword">
                      {({ field }: FieldProps) => (
                        <Input {...field} id="confirmPassword" type={showConfirmPassword ? "text" : "password"} disabled={isLoading} className="pr-10" />
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
                    <p className="text-xs text-[var(--color-error-500)]">{errors.confirmPassword}</p>
                  )}
                </div>

                <div className="flex items-center space-x-2">
                  <Checkbox
                    id="terms"
                    checked={values.terms}
                    onCheckedChange={(checked) => setFieldValue("terms", checked === true)}
                    disabled={isLoading}
                  />
                  <Label htmlFor="terms" className="text-body-sm font-normal text-[var(--text-secondary)]">
                    {t("auth.register.terms")}{" "}
                    <Link
                      href="/terms"
                      className="text-[var(--color-primary-500)] hover:text-[var(--color-primary-600)] underline underline-offset-4 transition-colors duration-150"
                    >
                      {t("auth.register.termsLink")}
                    </Link>
                  </Label>
                </div>
                {touched.terms && errors.terms && (
                  <p className="text-xs text-[var(--color-error-500)]">{errors.terms}</p>
                )}

                <div className="space-y-4 pt-1">
                  <Button type="submit" className="w-full h-11" disabled={isLoading}>
                    {isLoading ? (
                      <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        {t("auth.register.submitting")}
                      </>
                    ) : (
                      t("auth.register.submit")
                    )}
                  </Button>

                  <p className="text-center text-body-sm text-[var(--text-muted)]">
                    <Link
                      href="/login"
                      className="text-[var(--color-primary-500)] hover:text-[var(--color-primary-600)] hover:underline underline-offset-4 transition-colors duration-150"
                    >
                      {t("auth.register.hasAccount")}
                    </Link>
                  </p>
                </div>
              </Form>
            )}
          </Formik>
      </motion.div>
    </PageTransition>
  )
}
