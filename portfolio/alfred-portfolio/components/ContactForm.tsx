'use client'

import { useState } from 'react'

interface FormState {
  name: string
  email: string
  message: string
}

export default function ContactForm() {
  const [form, setForm] = useState<FormState>({ name: '', email: '', message: '' })

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }))
  }

  const mailtoHref = `mailto:alfredlandrytalom2004@gmail.com?subject=Portfolio Contact from ${encodeURIComponent(form.name)}&body=${encodeURIComponent(`Name: ${form.name}\nEmail: ${form.email}\n\nMessage:\n${form.message}`)}`

  return (
    <form className="flex flex-col gap-5">
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
        <div className="flex flex-col gap-2">
          <label htmlFor="name" className="text-sm font-medium text-[#a1a1aa]">
            Name
          </label>
          <input
            id="name"
            name="name"
            type="text"
            required
            placeholder="Your name"
            value={form.name}
            onChange={handleChange}
            className="px-4 py-3 bg-[#111111] border border-[#27272a] rounded-lg text-[#f5f5f5] placeholder-[#52525b] text-sm focus:outline-none focus:border-[#6366f1] transition-colors duration-200"
          />
        </div>
        <div className="flex flex-col gap-2">
          <label htmlFor="email" className="text-sm font-medium text-[#a1a1aa]">
            Email
          </label>
          <input
            id="email"
            name="email"
            type="email"
            required
            placeholder="your@email.com"
            value={form.email}
            onChange={handleChange}
            className="px-4 py-3 bg-[#111111] border border-[#27272a] rounded-lg text-[#f5f5f5] placeholder-[#52525b] text-sm focus:outline-none focus:border-[#6366f1] transition-colors duration-200"
          />
        </div>
      </div>

      <div className="flex flex-col gap-2">
        <label htmlFor="message" className="text-sm font-medium text-[#a1a1aa]">
          Message
        </label>
        <textarea
          id="message"
          name="message"
          required
          rows={6}
          placeholder="Tell me about your project, timeline, and budget..."
          value={form.message}
          onChange={handleChange}
          className="px-4 py-3 bg-[#111111] border border-[#27272a] rounded-lg text-[#f5f5f5] placeholder-[#52525b] text-sm focus:outline-none focus:border-[#6366f1] transition-colors duration-200 resize-none"
        />
      </div>

      <a
        href={mailtoHref}
        className="inline-flex items-center justify-center gap-2 px-6 py-3 bg-[#6366f1] text-white font-semibold rounded-lg hover:bg-[#5558e8] transition-colors duration-200 text-sm"
      >
        Send Message
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
          <path d="m22 2-7 20-4-9-9-4Z" />
          <path d="M22 2 11 13" />
        </svg>
      </a>

      <p className="text-xs text-[#52525b] text-center">
        This form opens your email client.{' '}
        <span className="text-[#71717a]">
          EmailJS or Resend integration can replace this for a fully in-page experience.
        </span>
      </p>
    </form>
  )
}
