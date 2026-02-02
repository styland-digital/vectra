import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import Link from 'next/link'

// Mock data - will be replaced with real API calls
const stats = [
  {
    title: 'Prospects Générés',
    value: '1,284',
    change: '+12%',
    changeType: 'positive' as const,
    description: 'Ce mois-ci'
  },
  {
    title: 'Taux de Qualification',
    value: '68%',
    change: '+5%',
    changeType: 'positive' as const,
    description: 'BANT Score ≥60'
  },
  {
    title: 'Rendez-vous Planifiés',
    value: '23',
    change: '+8%',
    changeType: 'positive' as const,
    description: 'Cette semaine'
  },
  {
    title: 'ROI Campagnes',
    value: '340%',
    change: '+15%',
    changeType: 'positive' as const,
    description: 'Retour sur investissement'
  }
]

const recentCampaigns = [
  {
    id: 1,
    name: 'SaaS B2B Tech',
    status: 'active',
    prospects: 156,
    qualified: 48,
    meetings: 12
  },
  {
    id: 2,
    name: 'E-commerce Directors',
    status: 'paused',
    prospects: 89,
    qualified: 23,
    meetings: 5
  },
  {
    id: 3,
    name: 'Fintech Managers',
    status: 'completed',
    prospects: 234,
    qualified: 67,
    meetings: 18
  }
]

function StatCard({ title, value, change, changeType, description }: {
  title: string
  value: string
  change: string
  changeType: 'positive' | 'negative'
  description: string
}) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium text-muted-foreground">
          {title}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        <div className="flex items-center space-x-2 text-xs text-muted-foreground">
          <Badge
            variant={changeType === 'positive' ? 'default' : 'destructive'}
            className="text-xs"
          >
            {change}
          </Badge>
          <span>{description}</span>
        </div>
      </CardContent>
    </Card>
  )
}

function CampaignCard({ campaign }: { campaign: typeof recentCampaigns[0] }) {
  const statusColors = {
    active: 'bg-green-100 text-green-800',
    paused: 'bg-yellow-100 text-yellow-800',
    completed: 'bg-blue-100 text-blue-800'
  }

  const statusLabels = {
    active: 'Actif',
    paused: 'En pause',
    completed: 'Terminé'
  }

  return (
    <div className="flex items-center justify-between border-b border-gray-100 dark:border-gray-800 py-4 last:border-b-0">
      <div className="flex-1">
        <div className="flex items-center space-x-3">
          <h3 className="font-medium">{campaign.name}</h3>
          <Badge
            className={statusColors[campaign.status]}
            variant="outline"
          >
            {statusLabels[campaign.status]}
          </Badge>
        </div>
        <div className="mt-1 text-sm text-muted-foreground">
          {campaign.prospects} prospects • {campaign.qualified} qualifiés • {campaign.meetings} RDV
        </div>
      </div>
      <Button variant="outline" size="sm">
        Voir détails
      </Button>
    </div>
  )
}

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Dashboard</h1>
          <p className="text-muted-foreground">
            Vue d'ensemble de vos campagnes de prospection
          </p>
        </div>
        <div className="flex space-x-3">
          <Button variant="outline">
            📊 Voir rapport
          </Button>
          <Button asChild>
            <Link href="/campaigns/new">
              🎯 Nouvelle campagne
            </Link>
          </Button>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => (
          <StatCard key={stat.title} {...stat} />
        ))}
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        {/* Recent Campaigns */}
        <Card>
          <CardHeader>
            <CardTitle>Campagnes Récentes</CardTitle>
            <CardDescription>
              Vos dernières campagnes de prospection
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-0">
              {recentCampaigns.map((campaign) => (
                <CampaignCard key={campaign.id} campaign={campaign} />
              ))}
            </div>
            <div className="mt-4 pt-4 border-t border-gray-100 dark:border-gray-800">
              <Button variant="ghost" className="w-full" asChild>
                <Link href="/campaigns">
                  Voir toutes les campagnes
                </Link>
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Quick Actions */}
        <Card>
          <CardHeader>
            <CardTitle>Actions Rapides</CardTitle>
            <CardDescription>
              Démarrez rapidement vos tâches courantes
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            <Button className="w-full justify-start" asChild>
              <Link href="/campaigns/new">
                🎯 Créer une nouvelle campagne
              </Link>
            </Button>
            <Button variant="outline" className="w-full justify-start" asChild>
              <Link href="/leads">
                👥 Gérer mes prospects
              </Link>
            </Button>
            <Button variant="outline" className="w-full justify-start" asChild>
              <Link href="/emails">
                📧 Voir emails en attente
              </Link>
            </Button>
            <Button variant="outline" className="w-full justify-start" asChild>
              <Link href="/settings">
                ⚙️ Configurer intégrations
              </Link>
            </Button>
          </CardContent>
        </Card>
      </div>

      {/* Recent Activity */}
      <Card>
        <CardHeader>
          <CardTitle>Activité Récente</CardTitle>
          <CardDescription>
            Les dernières actions de vos agents IA
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3 text-sm">
            <div className="flex items-center space-x-3 text-muted-foreground">
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
              <span>Agent Prospector a trouvé 23 nouveaux prospects pour "SaaS B2B Tech"</span>
              <span className="text-xs">Il y a 2h</span>
            </div>
            <div className="flex items-center space-x-3 text-muted-foreground">
              <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
              <span>Agent BANT a qualifié 8 prospects avec un score ≥60</span>
              <span className="text-xs">Il y a 3h</span>
            </div>
            <div className="flex items-center space-x-3 text-muted-foreground">
              <div className="w-2 h-2 bg-orange-500 rounded-full"></div>
              <span>Agent Scheduler a envoyé 15 emails personnalisés</span>
              <span className="text-xs">Il y a 5h</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}