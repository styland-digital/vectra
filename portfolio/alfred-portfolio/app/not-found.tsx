import Link from 'next/link'

export default function NotFound() {
  return (
    <div className="min-h-screen flex items-center justify-center px-4">
      <div className="text-center">
        <p className="text-8xl font-bold font-syne text-[#27272a] mb-4">404</p>
        <h1 className="text-2xl font-bold font-syne text-[#f5f5f5] mb-3">
          Page not found
        </h1>
        <p className="text-[#a1a1aa] mb-8 max-w-sm mx-auto">
          The page you&apos;re looking for doesn&apos;t exist or has been moved.
        </p>
        <Link
          href="/"
          className="inline-flex items-center gap-2 px-6 py-3 bg-[#6366f1] text-white font-semibold rounded-lg hover:bg-[#5558e8] transition-colors duration-200 text-sm"
        >
          Back to home
        </Link>
      </div>
    </div>
  )
}
