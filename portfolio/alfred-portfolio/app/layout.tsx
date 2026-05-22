import type { Metadata } from 'next'
import { Inter, Syne } from 'next/font/google'
import './globals.css'
import Navbar from '@/components/Navbar'
import Footer from '@/components/Footer'

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
})

const syne = Syne({
  subsets: ['latin'],
  variable: '--font-syne',
  display: 'swap',
})

export const metadata: Metadata = {
  title: 'Alfred Landry Talom — Full Stack Developer & Product Designer',
  description:
    'Full Stack Developer & Product Designer based in Douala, Cameroon. Building SaaS products with Next.js, React, Node.js.',
  keywords: [
    'Full Stack Developer',
    'Product Designer',
    'Next.js',
    'React',
    'Node.js',
    'SaaS',
    'Douala',
    'Cameroon',
    'Alfred Landry Talom',
    'styland-digital',
  ],
  authors: [{ name: 'Alfred Landry Talom', url: 'https://styland.dev' }],
  creator: 'Alfred Landry Talom',
  openGraph: {
    type: 'website',
    locale: 'en_US',
    title: 'Alfred Landry Talom — Full Stack Developer & Product Designer',
    description:
      'Full Stack Developer & Product Designer based in Douala, Cameroon. Building SaaS products with Next.js, React, Node.js.',
    siteName: 'Alfred Landry Talom',
    images: [
      {
        url: '/og-image.png',
        width: 1200,
        height: 630,
        alt: 'Alfred Landry Talom — Full Stack Developer & Product Designer',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Alfred Landry Talom — Full Stack Developer & Product Designer',
    description:
      'Full Stack Developer & Product Designer based in Douala, Cameroon. Building SaaS products with Next.js, React, Node.js.',
    images: ['/og-image.png'],
  },
  robots: {
    index: true,
    follow: true,
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={`${inter.variable} ${syne.variable}`}>
      <body className="bg-[#0a0a0a] text-[#f5f5f5] min-h-screen flex flex-col">
        <Navbar />
        <main className="flex-1">{children}</main>
        <Footer />
      </body>
    </html>
  )
}
