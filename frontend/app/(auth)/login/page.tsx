"use client"

import { useState } from 'react'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)

    // TODO: Connect to backend API
    console.log('Login attempt:', { email, password })

    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    setIsLoading(false)
  }

  return (
    <div className="flex flex-col space-y-2 text-center">
      <h1 className="text-2xl font-semibold tracking-tight">
        Connectez-vous à votre compte
      </h1>
      <p className="text-sm text-muted-foreground">
        Entrez votre email pour accéder à Vectra
      </p>

      <Card className="w-full">
        <CardHeader className="space-y-1">
          <CardTitle className="text-2xl text-left">Connexion</CardTitle>
          <CardDescription className="text-left">
            Accédez à votre dashboard et vos campagnes
          </CardDescription>
        </CardHeader>

        <form onSubmit={handleSubmit}>
          <CardContent className="space-y-4 text-left">
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="m@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                disabled={isLoading}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="password">Mot de passe</Label>
              <Input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                disabled={isLoading}
              />
            </div>
          </CardContent>

          <CardFooter className="flex flex-col space-y-4">
            <Button
              type="submit"
              className="w-full"
              disabled={isLoading}
            >
              {isLoading ? 'Connexion...' : 'Se connecter'}
            </Button>

            <div className="text-center text-sm">
              <Link
                href="/register"
                className="text-muted-foreground hover:text-primary underline underline-offset-4"
              >
                Pas encore de compte ? Créer un compte
              </Link>
            </div>

            <div className="text-center text-sm">
              <Link
                href="/forgot-password"
                className="text-muted-foreground hover:text-primary underline underline-offset-4"
              >
                Mot de passe oublié ?
              </Link>
            </div>
          </CardFooter>
        </form>
      </Card>
    </div>
  )
}