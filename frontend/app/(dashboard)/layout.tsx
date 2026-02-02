'use client'

import { Inter } from 'next/font/google'
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Badge } from '@/components/ui/badge'
import {
  Sheet,
  SheetContent,
  SheetTrigger,
} from '@/components/ui/sheet'
import {
  BarChart3,
  Target,
  Users,
  Mail,
  Calendar,
  TrendingUp,
  Settings,
  Menu,
  Bell,
  LogOut,
  Sparkles
} from 'lucide-react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'

const inter = Inter({ subsets: ['latin'] })

// Navigation avec icônes Lucide React (ZERO emojis)
const navigation = [
  { name: 'Dashboard', href: '/', icon: BarChart3 },
  { name: 'Campaigns', href: '/campaigns', icon: Target },
  { name: 'Leads', href: '/leads', icon: Users },
  { name: 'Emails', href: '/emails', icon: Mail },
  { name: 'Meetings', href: '/meetings', icon: Calendar },
  { name: 'Analytics', href: '/analytics', icon: TrendingUp },
  { name: 'Settings', href: '/settings', icon: Settings },
]

function VectraLogo() {
  return (
    <div className="flex items-center text-lg font-semibold text-[var(--text-primary)]">
      <div className="mr-2 h-6 w-6 rounded-md bg-gradient-to-br from-[var(--color-primary-500)] to-[var(--color-primary-600)] flex items-center justify-center">
        <Sparkles className="h-3.5 w-3.5 text-white" />
      </div>
      <span className="font-semibold tracking-tight">Vectra</span>
    </div>
  )
}

function Sidebar() {
  const pathname = usePathname()

  return (
    <div className="flex h-full w-64 flex-col bg-[var(--surface-primary)] border-r border-[var(--border-primary)]">
      {/* Logo */}
      <div className="flex h-16 shrink-0 items-center px-6 border-b border-[var(--border-secondary)]">
        <VectraLogo />
      </div>

      {/* Navigation */}
      <nav className="flex-1 space-y-1 px-3 py-4">
        {navigation.map((item) => {
          const isActive = pathname === item.href
          const Icon = item.icon

          return (
            <Link
              key={item.name}
              href={item.href}
              className={cn(
                'flex items-center rounded-lg px-3 py-2.5 text-sm font-medium transition-all duration-200',
                isActive
                  ? 'bg-[var(--color-primary-500)] text-white shadow-md'
                  : 'text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[var(--surface-hover)]'
              )}
            >
              <Icon className={cn(
                'mr-3 h-4 w-4 transition-colors',
                isActive ? 'text-white' : 'text-[var(--text-muted)]'
              )} />
              {item.name}
            </Link>
          )
        })}
      </nav>

      {/* User section */}
      <div className="border-t border-[var(--border-secondary)] p-4">
        <div className="flex items-center space-x-3 mb-3">
          <Avatar className="h-8 w-8">
            <AvatarImage src="/avatars/01.png" />
            <AvatarFallback className="bg-[var(--color-primary-100)] text-[var(--color-primary-700)] text-xs font-medium">
              JD
            </AvatarFallback>
          </Avatar>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-[var(--text-primary)] truncate">
              John Doe
            </p>
            <p className="text-xs text-[var(--text-muted)] truncate">
              john@company.com
            </p>
          </div>
        </div>
        <div className="flex items-center justify-between">
          <Badge variant="secondary" className="text-xs px-2 py-0.5">
            Starter
          </Badge>
          <Button variant="ghost" size="sm" className="h-7 w-7 p-0">
            <LogOut className="h-3.5 w-3.5" />
            <span className="sr-only">Logout</span>
          </Button>
        </div>
      </div>
    </div>
  )
}

function Header() {
  return (
    <header className="border-b border-[var(--border-primary)] bg-[var(--surface-primary)]">
      <div className="flex h-16 items-center px-6">
        {/* Mobile menu button */}
        <Sheet>
          <SheetTrigger asChild>
            <Button variant="ghost" size="sm" className="md:hidden">
              <Menu className="h-4 w-4" />
              <span className="sr-only">Open menu</span>
            </Button>
          </SheetTrigger>
          <SheetContent side="left" className="w-64 p-0">
            <Sidebar />
          </SheetContent>
        </Sheet>

        <div className="flex flex-1 justify-between items-center">
          <div className="flex items-center">
            {/* Logo on mobile */}
            <div className="md:hidden mr-4">
              <VectraLogo />
            </div>

            {/* Page title or breadcrumb could go here */}
            <div className="hidden md:block">
              <h1 className="text-h4 text-[var(--text-primary)]">
                Dashboard
              </h1>
            </div>
          </div>

          <div className="flex items-center space-x-3">
            {/* Notifications bell */}
            <Button variant="ghost" size="sm" className="relative">
              <Bell className="h-4 w-4 text-[var(--text-muted)]" />
              <span className="sr-only">Notifications</span>
              {/* Notification indicator */}
              <span className="absolute top-1.5 right-1.5 h-2 w-2 bg-[var(--color-accent-500)] rounded-full"></span>
            </Button>

            {/* User menu */}
            <Button variant="ghost" className="flex items-center space-x-2 h-9 px-2">
              <Avatar className="h-7 w-7">
                <AvatarImage src="/avatars/01.png" />
                <AvatarFallback className="bg-[var(--color-primary-100)] text-[var(--color-primary-700)] text-xs">
                  JD
                </AvatarFallback>
              </Avatar>
              <span className="hidden sm:block text-sm text-[var(--text-secondary)]">John</span>
            </Button>
          </div>
        </div>
      </div>
    </header>
  )
}

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className={cn('min-h-screen bg-[var(--bg-primary)] font-sans antialiased', inter.className)}>
      <div className="flex h-screen">
        {/* Desktop sidebar */}
        <div className="hidden md:flex">
          <Sidebar />
        </div>

        {/* Main content */}
        <div className="flex flex-1 flex-col">
          <Header />
          <main className="flex-1 overflow-y-auto">
            <div className="max-w-7xl mx-auto px-6 py-8">
              {children}
            </div>
          </main>
        </div>
      </div>
    </div>
  )
}