"use client"

import { Suspense } from "react"
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Loader2 } from "lucide-react"

function LoadingFallback() {
  return (
    <div className="container mx-auto py-16 px-4 max-w-2xl">
      <Card className="text-center">
        <CardHeader>
          <div className="mx-auto w-16 h-16 mb-4">
            <Loader2 className="w-16 h-16 animate-spin text-primary" />
          </div>
          <CardTitle className="text-2xl">Loading...</CardTitle>
          <CardDescription>
            Please wait while we load the page...
          </CardDescription>
        </CardHeader>
      </Card>
    </div>
  )
}

export default function BillingSuccessPage() {
  return (
    <Suspense fallback={<LoadingFallback />}>
      <div className="container mx-auto py-16 px-4 max-w-2xl">
        <Card className="text-center">
          <CardHeader>
            <CardTitle className="text-2xl">Payment Processing</CardTitle>
            <CardDescription>
              Your payment is being processed. Thank you for your patience.
            </CardDescription>
          </CardHeader>
        </Card>
      </div>
    </Suspense>
  )
}
