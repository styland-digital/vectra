"use client"

import { Formik, Form, Field, type FieldProps } from "formik"
import { useState } from "react"
import { useRouter } from "next/navigation"
import Link from "next/link"
import { Eye, EyeOff, Loader2 } from "lucide-react"

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
import { Checkbox } from "@/components/ui/checkbox"
import { PageTransition, AnimatePresence, motion } from "@/components/motion"
import { useAuthStore } from "@/lib/stores/auth"
import { registerSchema, type RegisterFormData } from "@/lib/schemas/auth"
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
      router.push("/")
    } catch {
      // Error is handled by the store
    }
  }

  return (
    <PageTransition>
      <div className="flex flex-col space-y-4 text-center">
        <div className="flex flex-col space-y-2">
          <h1 className="text-h2 tracking-tight text-foreground">
            {t("auth.register.title")}
          </h1>
          <p className="text-sm text-muted-foreground">
            {t("auth.register.subtitle")}
          </p>
        </div>

        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, ease: [0, 0, 0.2, 1], delay: 0.1 }}
        >
        <Card className="w-full">
          <CardHeader className="space-y-1">
            <CardTitle className="text-h3 text-left">
              {t("auth.register.cardTitle")}
            </CardTitle>
            <CardDescription className="text-left">
              {t("auth.register.cardDescription")}
            </CardDescription>
          </CardHeader>

          <Formik
            initialValues={initialValues}
            validate={toFormikValidate(registerSchema)}
            onSubmit={handleSubmit}
          >
            {({ errors, touched, setFieldValue, values }) => (
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

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="firstName">
                        {t("auth.register.firstName")}
                      </Label>
                      <Field name="firstName">
                        {({ field }: FieldProps) => (
                          <Input
                            {...field}
                            id="firstName"
                            disabled={isLoading}
                          />
                        )}
                      </Field>
                      {touched.firstName && errors.firstName && (
                        <p className="text-xs text-[var(--color-error-500)]">
                          {errors.firstName}
                        </p>
                      )}
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="lastName">
                        {t("auth.register.lastName")}
                      </Label>
                      <Field name="lastName">
                        {({ field }: FieldProps) => (
                          <Input
                            {...field}
                            id="lastName"
                            disabled={isLoading}
                          />
                        )}
                      </Field>
                      {touched.lastName && errors.lastName && (
                        <p className="text-xs text-[var(--color-error-500)]">
                          {errors.lastName}
                        </p>
                      )}
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="email">{t("auth.register.email")}</Label>
                    <Field name="email">
                      {({ field }: FieldProps) => (
                        <Input
                          {...field}
                          id="email"
                          type="email"
                          placeholder="m@example.com"
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
                    <Label htmlFor="companyName">
                      {t("auth.register.companyName")}
                    </Label>
                    <Field name="companyName">
                      {({ field }: FieldProps) => (
                        <Input
                          {...field}
                          id="companyName"
                          disabled={isLoading}
                        />
                      )}
                    </Field>
                    {touched.companyName && errors.companyName && (
                      <p className="text-xs text-[var(--color-error-500)]">
                        {errors.companyName}
                      </p>
                    )}
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="password">
                      {t("auth.register.password")}
                    </Label>
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
                        className="absolute right-3 top-1/2 -translate-y-1/2 text-[var(--text-muted)] hover:text-[var(--text-primary)] transition-colors duration-150"
                      >
                        {showPassword ? (
                          <EyeOff className="h-4 w-4" />
                        ) : (
                          <Eye className="h-4 w-4" />
                        )}
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
                    <Label htmlFor="confirmPassword">
                      {t("auth.register.confirmPassword")}
                    </Label>
                    <div className="relative">
                      <Field name="confirmPassword">
                        {({ field }: FieldProps) => (
                          <Input
                            {...field}
                            id="confirmPassword"
                            type={showConfirmPassword ? "text" : "password"}
                            disabled={isLoading}
                            className="pr-10"
                          />
                        )}
                      </Field>
                      <button
                        type="button"
                        onClick={() =>
                          setShowConfirmPassword(!showConfirmPassword)
                        }
                        className="absolute right-3 top-1/2 -translate-y-1/2 text-[var(--text-muted)] hover:text-[var(--text-primary)] transition-colors duration-150"
                      >
                        {showConfirmPassword ? (
                          <EyeOff className="h-4 w-4" />
                        ) : (
                          <Eye className="h-4 w-4" />
                        )}
                      </button>
                    </div>
                    {touched.confirmPassword && errors.confirmPassword && (
                      <p className="text-xs text-[var(--color-error-500)]">
                        {errors.confirmPassword}
                      </p>
                    )}
                  </div>

                  <div className="flex items-center space-x-2">
                    <Checkbox
                      id="terms"
                      checked={values.terms}
                      onCheckedChange={(checked) =>
                        setFieldValue("terms", checked === true)
                      }
                      disabled={isLoading}
                    />
                    <Label htmlFor="terms" className="text-sm font-normal">
                      {t("auth.register.terms")}{" "}
                      <Link
                        href="/terms"
                        className="text-primary underline underline-offset-4 hover:text-primary/80 transition-colors duration-150"
                      >
                        {t("auth.register.termsLink")}
                      </Link>
                    </Label>
                  </div>
                  {touched.terms && errors.terms && (
                    <p className="text-xs text-[var(--color-error-500)]">
                      {errors.terms}
                    </p>
                  )}
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
                        {t("auth.register.submitting")}
                      </>
                    ) : (
                      t("auth.register.submit")
                    )}
                  </Button>

                  <div className="text-center text-sm">
                    <Link
                      href="/login"
                      className="text-muted-foreground hover:text-primary underline underline-offset-4 transition-colors duration-150"
                    >
                      {t("auth.register.hasAccount")}
                    </Link>
                  </div>
                </CardFooter>
              </Form>
            )}
          </Formik>
        </Card>
        </motion.div>
      </div>
    </PageTransition>
  )
}
