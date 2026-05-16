import Image from 'next/image'
import { cn } from '@/lib/utils'

interface VectraLogoProps {
  variant?: 'default' | 'white'
  size?: 'sm' | 'md' | 'lg'
  className?: string
  showText?: boolean
}

export function VectraLogo({
  variant = 'default',
  size = 'md',
  className,
  showText = true,
}: VectraLogoProps) {
  const sizes = {
    sm: { width: 100, height: 44 },
    md: { width: 120, height: 52 },
    lg: { width: 150, height: 65 },
  }

  const { width, height } = sizes[size]

  return (
    <div className={cn('flex items-center', className)}>
      <Image
        src="/logo.svg"
        alt="Vectra"
        width={width}
        height={height}
        priority
        style={{ height: 'auto', width: 'auto', maxWidth: `${width}px` }}
        className={cn(
          variant === 'white' && 'brightness-0 invert'
        )}
      />
    </div>
  )
}

// Icon-only version for compact spaces
export function VectraIcon({
  variant = 'default',
  size = 'md',
  className,
}: Omit<VectraLogoProps, 'showText'>) {
  const sizes = {
    sm: 'h-6 w-6',
    md: 'h-8 w-8',
    lg: 'h-10 w-10',
  }

  return (
    <div
      className={cn(
        'rounded-lg bg-gradient-to-br from-[var(--color-primary-500)] to-[var(--color-primary-600)] flex items-center justify-center',
        sizes[size],
        className
      )}
    >
      <svg
        viewBox="0 0 24 24"
        fill="none"
        className={cn(
          'text-white',
          size === 'sm' ? 'h-3.5 w-3.5' : size === 'md' ? 'h-4 w-4' : 'h-5 w-5'
        )}
      >
        <path
          d="M12 3L4 9l8 8 8-8-8-6z"
          fill="currentColor"
        />
        <path
          d="M4 15l8 6 8-6"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    </div>
  )
}
