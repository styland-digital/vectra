'use client'

import { motion } from 'framer-motion'
import Link from 'next/link'

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.12,
      delayChildren: 0.1,
    },
  },
}

const itemVariants = {
  hidden: { opacity: 0, y: 24 },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.6,
      ease: [0.25, 0.4, 0.25, 1],
    },
  },
}

const titleWords = ['Full', 'Stack', 'Developer', '&', 'Product', 'Designer']

export default function Hero() {
  return (
    <section className="min-h-screen flex items-center justify-center px-4 sm:px-6 lg:px-8 pt-16">
      <div className="max-w-4xl mx-auto text-center">
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="flex flex-col items-center gap-6"
        >
          <motion.div variants={itemVariants}>
            <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-[#27272a] bg-[#111111] text-sm text-[#a1a1aa]">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
              Available for new projects
            </span>
          </motion.div>

          <motion.p
            variants={itemVariants}
            className="text-lg sm:text-xl text-[#a1a1aa] font-medium"
          >
            Hi, I&apos;m Alfred{' '}
            <span role="img" aria-label="waving hand">👋</span>
          </motion.p>

          <motion.h1
            variants={itemVariants}
            className="text-4xl sm:text-6xl lg:text-7xl font-bold font-syne leading-tight tracking-tight"
          >
            <span className="flex flex-wrap justify-center gap-x-3 gap-y-1">
              {titleWords.map((word, i) => (
                <motion.span
                  key={i}
                  initial={{ opacity: 0, y: 30 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{
                    duration: 0.5,
                    delay: 0.3 + i * 0.08,
                    ease: [0.25, 0.4, 0.25, 1],
                  }}
                  className={
                    word === '&' || word === 'Product' || word === 'Designer'
                      ? 'text-gradient'
                      : 'text-[#f5f5f5]'
                  }
                >
                  {word}
                </motion.span>
              ))}
            </span>
          </motion.h1>

          <motion.p
            variants={itemVariants}
            className="max-w-xl text-base sm:text-lg text-[#a1a1aa] leading-relaxed"
          >
            Building SaaS products that work — from pixel to production.
            <br />
            Based in Douala, Cameroon{' '}
            <span role="img" aria-label="Cameroon flag">🇨🇲</span>
          </motion.p>

          <motion.div
            variants={itemVariants}
            className="flex flex-col sm:flex-row items-center gap-4 mt-2"
          >
            <Link
              href="/projects"
              className="inline-flex items-center gap-2 px-6 py-3 bg-[#6366f1] text-white font-semibold rounded-lg hover:bg-[#5558e8] transition-colors duration-200 text-sm"
            >
              View Projects
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                <path d="M5 12h14" />
                <path d="m12 5 7 7-7 7" />
              </svg>
            </Link>
            <Link
              href="/contact"
              className="inline-flex items-center gap-2 px-6 py-3 border border-[#27272a] text-[#f5f5f5] font-semibold rounded-lg hover:border-[#6366f1] hover:text-[#6366f1] transition-colors duration-200 text-sm"
            >
              Contact me
            </Link>
          </motion.div>

          <motion.div
            variants={itemVariants}
            className="flex items-center gap-6 mt-4 text-sm text-[#71717a]"
          >
            <span className="flex items-center gap-1.5">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                <path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z" />
                <circle cx="12" cy="10" r="3" />
              </svg>
              Douala, Cameroun
            </span>
            <span className="w-1 h-1 rounded-full bg-[#27272a]" />
            <span>2+ years experience</span>
            <span className="w-1 h-1 rounded-full bg-[#27272a]" />
            <span>4+ projects shipped</span>
          </motion.div>
        </motion.div>
      </div>
    </section>
  )
}
