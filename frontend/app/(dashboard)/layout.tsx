'use client'

import { useState } from 'react'
import { Inter } from 'next/font/google'
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Input } from '@/components/ui/input'
import {
  Sheet,
  SheetContent,
  SheetTrigger,
} from '@/components/ui/sheet'
import { Toaster } from '@/components/ui/toaster'
import {
  LayoutDashboard,
  Target,
  Users,
  Mail,
  Calendar,
  BarChart3,
  Settings,
  Menu,
  Bell,
  LogOut,
  Globe,
  Search,
  HelpCircle,
  ChevronDown,
} from 'lucide-react'
import { VectraLogo } from '@/components/vectra-logo'
import { motion } from '@/components/motion'
import Link from 'next/link'
import { usePathname, useRouter } from 'next/navigation'
import { useAuthStore } from '@/lib/stores/auth'
import { useUIStore } from '@/lib/stores/ui'
import { useTranslation } from '@/lib/i18n'

const inter = Inter({ subsets: ['latin'] })

interface NavItemProps {
  href: string
  icon: React.ComponentType<{ className?: string }>
  label: string
  isActive: boolean
}

function NavItem({ href, icon: Icon, label, isActive }: NavItemProps) {
  return (
    <motion.div whileHover={{ x: 2 }} whileTap={{ scale: 0.98 }} transition={{ duration: 0.15 }}>
      <Link
        href={href}
        className={cn(
          'relative flex items-center gap-3 px-3 py-2 rounded-lg text-body-sm font-medium transition-all duration-200',
          isActive
            ? 'bg-[var(--color-primary-50)] text-[var(--color-primary-600)]'
            : 'text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[var(--surface-hover)]'
        )}
      >
        {isActive && (
          <span className="absolute left-0 top-1/2 -translate-y-1/2 w-[3px] h-5 bg-[var(--color-primary-500)] rounded-r-full" />
        )}
        <Icon className={cn(
          'h-5 w-5 transition-colors duration-200',
          isActive ? 'text-[var(--color-primary-500)]' : 'text-[var(--text-muted)]'
        )} />
        {label}
      </Link>
    </motion.div>
  )
}

function Sidebar() {
  const pathname = usePathname()
  const router = useRouter()
  const { user, logout } = useAuthStore()
  const { t } = useTranslation()

  const menuItems = [
    { name: t('nav.dashboard'), href: '/', icon: LayoutDashboard },
    { name: t('nav.campaigns'), href: '/campaigns', icon: Target },
    { name: t('nav.leads'), href: '/leads', icon: Users },
    { name: t('nav.emails'), href: '/emails', icon: Mail },
    { name: t('nav.meetings'), href: '/meetings', icon: Calendar },
    { name: t('nav.analytics'), href: '/analytics', icon: BarChart3 },
  ]

  const accountItems = [
    { name: t('nav.settings'), href: '/settings', icon: Settings },
  ]

  const supportItems = [
    { name: 'Help', href: '#', icon: HelpCircle },
  ]

  const userInitials = user
    ? `${user.first_name.charAt(0)}${user.last_name.charAt(0)}`.toUpperCase()
    : 'U'

  const userName = user ? `${user.first_name} ${user.last_name}` : ''
  const userEmail = user?.email ?? ''

  const [profileOpen, setProfileOpen] = useState(false)

  const handleLogout = () => {
    logout()
    router.push('/login')
  }

  return (
    <div className="flex h-full w-60 flex-col bg-[var(--surface-primary)] border-r border-[var(--border-primary)]">
      {/* Logo */}
      <div className="flex h-16 items-center px-4 border-b border-[var(--border-secondary)]">
        <VectraLogo size="sm" />
      </div>

      {/* Navigation */}
      <div className="flex-1 overflow-y-auto py-4 px-3">
        {/* Menu Section */}
        <div className="mb-6">
          <p className="text-overline text-[var(--text-muted)] px-3 mb-2">
            MENU
          </p>
          <nav className="space-y-1">
            {menuItems.map((item) => (
              <NavItem
                key={item.href}
                href={item.href}
                icon={item.icon}
                label={item.name}
                isActive={pathname === item.href}
              />
            ))}
          </nav>
        </div>

        {/* Divider */}
        <div className="h-px bg-[var(--border-secondary)] mx-3 mb-6" />

        {/* Account Section */}
        <div className="mb-6">
          <p className="text-overline text-[var(--text-muted)] px-3 mb-2">
            ACCOUNT
          </p>
          <nav className="space-y-1">
            {accountItems.map((item) => (
              <NavItem
                key={item.href}
                href={item.href}
                icon={item.icon}
                label={item.name}
                isActive={pathname === item.href}
              />
            ))}
          </nav>
        </div>

        {/* Divider */}
        <div className="h-px bg-[var(--border-secondary)] mx-3 mb-6" />

        {/* Support Section */}
        <div>
          <p className="text-overline text-[var(--text-muted)] px-3 mb-2">
            SUPPORT
          </p>
          <nav className="space-y-1">
            {supportItems.map((item) => (
              <NavItem
                key={item.name}
                href={item.href}
                icon={item.icon}
                label={item.name}
                isActive={false}
              />
            ))}
          </nav>
        </div>
      </div>

      {/* User Profile */}
      <div className="border-t border-[var(--border-secondary)] p-4 relative">
        <button
          onClick={() => setProfileOpen(!profileOpen)}
          className="w-full flex items-center gap-3 hover:bg-[var(--surface-hover)] rounded-lg p-1 -m-1 transition-colors duration-150 cursor-pointer"
        >
          <Avatar className="h-9 w-9">
            <AvatarImage src="/avatars/01.png" />
            <AvatarFallback className="bg-[var(--color-primary-100)] text-[var(--color-primary-700)] text-sm font-medium">
              {userInitials}
            </AvatarFallback>
          </Avatar>
          <div className="flex-1 min-w-0 text-left">
            <p className="text-body-sm font-medium text-[var(--text-primary)] truncate">
              {userName}
            </p>
            <p className="text-caption text-[var(--text-muted)] truncate">
              {userEmail}
            </p>
          </div>
          <ChevronDown className={cn(
            "h-4 w-4 text-[var(--text-muted)] transition-transform duration-200",
            profileOpen && "rotate-180"
          )} />
        </button>

        {/* Profile Dropdown */}
        {profileOpen && (
          <div className="absolute bottom-full left-3 right-3 mb-2 bg-[var(--surface-primary)] border border-[var(--border-primary)] rounded-lg shadow-lg overflow-hidden animate-scale-in">
            <Link
              href="/settings"
              onClick={() => setProfileOpen(false)}
              className="flex items-center gap-3 px-3 py-2.5 text-body-sm text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[var(--surface-hover)] transition-colors duration-150"
            >
              <Settings className="h-4 w-4" />
              {t('nav.settings')}
            </Link>
            <div className="h-px bg-[var(--border-secondary)]" />
            <button
              onClick={handleLogout}
              className="w-full flex items-center gap-3 px-3 py-2.5 text-body-sm text-[var(--color-error-500)] hover:bg-[var(--color-error-50)] transition-colors duration-150"
            >
              <LogOut className="h-4 w-4" />
              {t('common.logout')}
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

function LanguageToggle() {
  const { locale, setLocale } = useUIStore()

  return (
    <Button
      variant="ghost"
      size="sm"
      onClick={() => setLocale(locale === 'fr' ? 'en' : 'fr')}
      className="h-9 w-9 p-0 hover:bg-[var(--surface-hover)] transition-colors duration-150"
    >
      <Globe className="h-4 w-4 text-[var(--text-muted)]" />
      <span className="sr-only">Toggle language</span>
    </Button>
  )
}

function Header() {
  const { user } = useAuthStore()
  const { t } = useTranslation()

  const userInitials = user
    ? `${user.first_name.charAt(0)}${user.last_name.charAt(0)}`.toUpperCase()
    : 'U'

  return (
    <header className="h-16 border-b border-[var(--border-primary)] backdrop-blur-sm bg-[var(--surface-primary)]/95">
      <div className="flex h-full items-center px-4 gap-4">
        {/* Mobile menu */}
        <Sheet>
          <SheetTrigger asChild>
            <Button variant="ghost" size="sm" className="md:hidden h-9 w-9 p-0">
              <Menu className="h-5 w-5" />
              <span className="sr-only">Open menu</span>
            </Button>
          </SheetTrigger>
          <SheetContent side="left" className="w-60 p-0">
            <Sidebar />
          </SheetContent>
        </Sheet>

        {/* Mobile logo */}
        <div className="md:hidden">
          <VectraLogo size="sm" />
        </div>

        {/* Search */}
        <div className="flex-1 max-w-md hidden sm:block">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-[var(--text-muted)]" />
            <Input
              type="search"
              placeholder={t('common.search')}
              className="pl-10 h-9 bg-[var(--surface-secondary)] border-[var(--border-secondary)] focus:border-[var(--color-primary-500)]"
            />
          </div>
        </div>

        {/* Right side actions */}
        <div className="flex items-center gap-2 ml-auto">
          <LanguageToggle />

          <Button variant="ghost" size="sm" className="h-9 w-9 p-0 relative hover:bg-[var(--surface-hover)] transition-colors duration-150">
            <Bell className="h-4 w-4 text-[var(--text-muted)]" />
            <span className="sr-only">Notifications</span>
            <span className="absolute top-2 right-2 h-2 w-2 bg-[var(--color-error-500)] rounded-full"></span>
          </Button>

          <Button variant="ghost" size="sm" className="h-9 w-9 p-0 hover:bg-[var(--surface-hover)] transition-colors duration-150">
            <HelpCircle className="h-4 w-4 text-[var(--text-muted)]" />
            <span className="sr-only">Help</span>
          </Button>

          <div className="h-6 w-px bg-[var(--border-primary)] mx-1 hidden sm:block" />

          <Button variant="ghost" className="h-9 px-2 gap-2 group">
            <Avatar className="h-7 w-7">
              <AvatarImage src="/avatars/01.png" />
              <AvatarFallback className="bg-[var(--color-primary-100)] text-[var(--color-primary-700)] text-xs font-medium">
                {userInitials}
              </AvatarFallback>
            </Avatar>
            <span className="hidden sm:block text-body-sm text-[var(--text-secondary)]">
              {user?.first_name ?? ''}
            </span>
            <ChevronDown className="h-4 w-4 text-[var(--text-muted)] hidden sm:block group-hover:rotate-180 transition-transform duration-200" />
          </Button>
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
    <div className={cn('min-h-screen bg-[var(--bg-secondary)] font-sans antialiased', inter.className)}>
      <div className="flex h-screen">
        {/* Desktop sidebar */}
        <div className="hidden md:flex">
          <Sidebar />
        </div>

        {/* Main content */}
        <div className="flex flex-1 flex-col overflow-hidden">
          <Header />
          <main className="flex-1 overflow-y-auto">
            <div className="max-w-7xl mx-auto px-6 py-6">
              {children}
            </div>
          </main>
        </div>
      </div>
      <Toaster />
    </div>
  )
}
