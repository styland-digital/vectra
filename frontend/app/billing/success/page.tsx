"use client"

import { useEffect, useState } from 'react'
import { useSearchParams, useRouter } from 'next/navigation'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { CheckCircle, AlertCircle, Loader2 } from 'lucide-react'

interface SessionStatus {
  status: 'loading' | 'success' | 'error'
  message?: string
  subscription?: {
    id: string
    plan_name: string
    status: string
  }
}

export default function BillingSuccessPage() {
  const searchParams = useSearchParams()
  const router = useRouter()
  const [sessionStatus, setSessionStatus] = useState<SessionStatus>({ status: 'loading' })

  const sessionId = searchParams.get('session_id')

  useEffect(() => {
    if (!sessionId) {
      setSessionStatus({
        status: 'error',
        message: 'Session ID manquant. Veuillez réessayer.'
      })
      return
    }

    // Verify the checkout session
    verifySession(sessionId)
  }, [sessionId])

  const verifySession = async (sessionId: string) => {
    try {
      const response = await fetch(`/api/v1/user/billing/session/${sessionId}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
      })

      if (response.ok) {
        const data = await response.json()
        setSessionStatus({
          status: 'success',
          subscription: {
            id: data.subscription,
            plan_name: data.display_items?.[0]?.description || 'Plan sélectionné',
            status: data.payment_status
          }
        })

        // Redirect to dashboard after 3 seconds
        setTimeout(() => {
          router.push('/dashboard')
        }, 3000)
      } else {
        setSessionStatus({
          status: 'error',
          message: 'Erreur lors de la vérification du paiement. Contactez le support.'
        })
      }
    } catch (error) {
      console.error('Session verification error:', error)
      setSessionStatus({
        status: 'error',
        message: 'Erreur de connexion. Vérifiez votre connexion internet.'
      })
    }
  }

  const handleReturnToDashboard = () => {
    router.push('/dashboard')
  }

  const handleReturnToPricing = () => {
    router.push('/pricing')
  }

  if (sessionStatus.status === 'loading') {
    return (
      <div className="container mx-auto py-16 px-4 max-w-2xl">
        <Card className="text-center">
          <CardHeader>
            <div className="mx-auto w-16 h-16 mb-4">
              <Loader2 className="w-16 h-16 animate-spin text-primary" />
            </div>
            <CardTitle className="text-2xl">Vérification du paiement</CardTitle>
            <CardDescription>
              Nous vérifions votre paiement, veuillez patienter...
            </CardDescription>
          </CardHeader>
        </Card>
      </div>
    )
  }

  if (sessionStatus.status === 'error') {
    return (
      <div className="container mx-auto py-16 px-4 max-w-2xl">
        <Card className="text-center border-destructive">
          <CardHeader>
            <div className="mx-auto w-16 h-16 mb-4">
              <AlertCircle className="w-16 h-16 text-destructive" />
            </div>
            <CardTitle className="text-2xl text-destructive">Erreur de paiement</CardTitle>
            <CardDescription className="text-destructive/80">
              {sessionStatus.message}
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="text-sm text-muted-foreground">
              Si le problème persiste, contactez notre équipe support à{' '}
              <a href="mailto:support@vectra.io" className="text-primary hover:underline">
                support@vectra.io
              </a>
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button variant="outline" onClick={handleReturnToPricing}>
                Retour aux tarifs
              </Button>
              <Button onClick={handleReturnToDashboard}>
                Aller au tableau de bord
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="container mx-auto py-16 px-4 max-w-2xl">
      <Card className="text-center border-green-200 bg-green-50/50">
        <CardHeader>
          <div className="mx-auto w-16 h-16 mb-4">
            <CheckCircle className="w-16 h-16 text-green-600" />
          </div>
          <CardTitle className="text-2xl text-green-900">Paiement réussi !</CardTitle>
          <CardDescription className="text-green-700">
            Votre abonnement a été activé avec succès
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          {sessionStatus.subscription && (
            <div className="bg-white rounded-lg p-4 border">
              <h3 className="font-medium text-green-900 mb-2">Détails de l'abonnement</h3>
              <div className="text-sm space-y-1">
                <p><span className="text-muted-foreground">Plan:</span> {sessionStatus.subscription.plan_name}</p>
                <p><span className="text-muted-foreground">Status:</span> Actif</p>
              </div>
            </div>
          )}

          <div className="space-y-4">
            <div className="text-sm text-green-700 bg-green-100 rounded-lg p-4">
              <h4 className="font-medium mb-2">Prochaines étapes :</h4>
              <ul className="text-left space-y-1">
                <li>✅ Accès à tous les agents IA</li>
                <li>✅ Configuration de votre première campagne</li>
                <li>✅ Intégration avec vos outils existants</li>
                <li>✅ Support dédié pendant l'onboarding</li>
              </ul>
            </div>

            <p className="text-sm text-muted-foreground">
              Vous serez automatiquement redirigé vers votre tableau de bord dans quelques secondes.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button variant="outline" onClick={handleReturnToPricing}>
                Voir les autres plans
              </Button>
              <Button onClick={handleReturnToDashboard} className="bg-green-600 hover:bg-green-700">
                Commencer maintenant
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}