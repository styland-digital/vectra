"use client"

import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

// Plan data matching the backend configuration
const plans = [
  {
    id: 'starter',
    name: 'Starter',
    price: 99,
    currency: 'EUR',
    interval: 'mois',
    description: 'Parfait pour les équipes qui commencent',
    features: {
      leads_per_month: 500,
      campaigns_active: 2,
      users: 2,
      emails_per_day: 50,
      support: 'Email'
    },
    popular: false
  },
  {
    id: 'growth',
    name: 'Growth',
    price: 299,
    currency: 'EUR',
    interval: 'mois',
    description: 'Pour les équipes en croissance',
    features: {
      leads_per_month: 2000,
      campaigns_active: 5,
      users: 5,
      emails_per_day: 200,
      support: 'Email + Chat'
    },
    popular: true
  },
  {
    id: 'scale',
    name: 'Scale',
    price: 799,
    currency: 'EUR',
    interval: 'mois',
    description: 'Pour les entreprises en croissance rapide',
    features: {
      leads_per_month: 10000,
      campaigns_active: 999,
      users: 15,
      emails_per_day: 1000,
      support: 'Support prioritaire'
    },
    popular: false
  }
]

function PlanCard({ plan }: { plan: typeof plans[0] }) {
  const [isLoading, setIsLoading] = useState(false)

  const handleSubscribe = async () => {
    setIsLoading(true)

    try {
      // Call frontend API route that proxies to backend
      const token = localStorage.getItem('token')
      const response = await fetch('/api/v1/user/billing/create-checkout-session', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          plan_type: plan.id,
          success_url: window.location.origin + '/billing/success',
          cancel_url: window.location.origin + '/pricing'
        })
      })

      if (response.ok) {
        const data = await response.json()
        // Redirect to Stripe checkout
        window.location.href = data.session_url
      } else {
        console.error('Failed to create checkout session')
        alert('Erreur lors de la création de la session de paiement')
      }
    } catch (error) {
      console.error('Error:', error)
      alert('Erreur lors de la connexion au serveur')
    }

    setIsLoading(false)
  }

  return (
    <Card className={`relative ${plan.popular ? 'border-primary shadow-lg' : ''}`}>
      {plan.popular && (
        <div className="absolute -top-3 left-1/2 -translate-x-1/2">
          <Badge className="bg-primary text-primary-foreground">
            Plus populaire
          </Badge>
        </div>
      )}

      <CardHeader className="text-center pb-6">
        <CardTitle className="text-2xl">{plan.name}</CardTitle>
        <CardDescription>{plan.description}</CardDescription>
        <div className="mt-4">
          <span className="text-4xl font-bold">{plan.price}€</span>
          <span className="text-muted-foreground">/{plan.interval}</span>
        </div>
      </CardHeader>

      <CardContent className="space-y-4">
        <div className="space-y-2">
          <div className="flex items-center justify-between text-sm">
            <span>Prospects par mois</span>
            <span className="font-medium">{plan.features.leads_per_month.toLocaleString()}</span>
          </div>
          <div className="flex items-center justify-between text-sm">
            <span>Campagnes actives</span>
            <span className="font-medium">
              {plan.features.campaigns_active === 999 ? 'Illimité' : plan.features.campaigns_active}
            </span>
          </div>
          <div className="flex items-center justify-between text-sm">
            <span>Utilisateurs</span>
            <span className="font-medium">{plan.features.users}</span>
          </div>
          <div className="flex items-center justify-between text-sm">
            <span>Emails par jour</span>
            <span className="font-medium">{plan.features.emails_per_day.toLocaleString()}</span>
          </div>
          <div className="flex items-center justify-between text-sm">
            <span>Support</span>
            <span className="font-medium">{plan.features.support}</span>
          </div>
        </div>

        <div className="pt-4 border-t">
          <h4 className="font-medium mb-2">Inclus dans tous les plans:</h4>
          <ul className="text-sm text-muted-foreground space-y-1">
            <li>✅ 3 Agents IA (Prospector, BANT, Scheduler)</li>
            <li>✅ Intégrations (RocketReach, Calendly, HubSpot)</li>
            <li>✅ Analytics et rapports détaillés</li>
            <li>✅ API et webhooks</li>
            <li>✅ Sécurité enterprise (SOC2)</li>
          </ul>
        </div>
      </CardContent>

      <CardFooter>
        <Button
          className="w-full"
          onClick={handleSubscribe}
          disabled={isLoading}
          variant={plan.popular ? 'default' : 'outline'}
        >
          {isLoading ? 'Redirection...' : 'Commencer l\'essai gratuit'}
        </Button>
      </CardFooter>
    </Card>
  )
}

export default function PricingPage() {
  return (
    <div className="container mx-auto py-16 px-4">
      {/* Header */}
      <div className="text-center mb-16">
        <h1 className="text-4xl font-bold mb-4">
          Choisissez votre plan
        </h1>
        <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
          Automatisez votre prospection B2B avec nos agents IA.
          Essai gratuit de 14 jours, sans engagement.
        </p>

        <div className="flex items-center justify-center space-x-4 text-sm text-muted-foreground">
          <div className="flex items-center">
            ✅ 14 jours d'essai gratuit
          </div>
          <div className="flex items-center">
            ✅ Annulation à tout moment
          </div>
          <div className="flex items-center">
            ✅ Support français
          </div>
        </div>
      </div>

      {/* Plans Grid */}
      <div className="grid lg:grid-cols-3 gap-8 max-w-6xl mx-auto mb-16">
        {plans.map((plan) => (
          <PlanCard key={plan.id} plan={plan} />
        ))}
      </div>

      {/* FAQ Section */}
      <div className="max-w-2xl mx-auto">
        <h2 className="text-2xl font-bold text-center mb-8">Questions fréquentes</h2>
        <div className="space-y-6">
          <div>
            <h3 className="font-medium mb-2">Puis-je changer de plan à tout moment ?</h3>
            <p className="text-muted-foreground text-sm">
              Oui, vous pouvez upgrader ou downgrader votre plan à tout moment.
              Les changements prennent effet immédiatement et nous calculons la facturation au prorata.
            </p>
          </div>
          <div>
            <h3 className="font-medium mb-2">Que se passe-t-il si je dépasse mes limites ?</h3>
            <p className="text-muted-foreground text-sm">
              Nous vous préviendrons lorsque vous approchez de vos limites.
              Vous pouvez upgrader votre plan ou attendre le prochain cycle de facturation.
            </p>
          </div>
          <div>
            <h3 className="font-medium mb-2">Proposez-vous des plans annuels ?</h3>
            <p className="text-muted-foreground text-sm">
              Oui, nous proposons des plans annuels avec 2 mois gratuits.
              Contactez notre équipe commerciale pour plus d'informations.
            </p>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="text-center mt-16 p-8 bg-muted rounded-lg">
        <h2 className="text-2xl font-bold mb-4">
          Besoin d'un plan sur mesure ?
        </h2>
        <p className="text-muted-foreground mb-6">
          Pour les grandes entreprises avec des besoins spécifiques
        </p>
        <Button variant="outline" size="lg">
          Contacter les ventes
        </Button>
      </div>
    </div>
  )
}