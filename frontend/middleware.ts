import { NextResponse } from "next/server"
import type { NextRequest } from "next/server"

// Paths that don't require authentication
const publicPaths = [
  "/login",
  "/register",
  "/forgot-password",
  "/reset-password",
  "/pricing",
  "/billing/success",
]

// Auth pages (login, register, etc.) - redirect to dashboard if already authenticated
// Note: /reset-password is intentionally excluded — password reset links must work for authenticated users too
const authPaths = ["/login", "/register", "/forgot-password"]

function isPublicPath(pathname: string): boolean {
  return publicPaths.some((path) => pathname.startsWith(path))
}

function isAuthPath(pathname: string): boolean {
  return authPaths.some((path) => pathname.startsWith(path))
}

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl
  const token = request.cookies.get("vectra_token")?.value

  // Skip middleware for API routes, static files, and Next.js internals
  if (
    pathname.startsWith("/api") ||
    pathname.startsWith("/_next") ||
    pathname.startsWith("/favicon") ||
    pathname.includes(".")
  ) {
    return NextResponse.next()
  }

  // If user has token and visits auth pages, redirect to dashboard
  if (token && isAuthPath(pathname)) {
    return NextResponse.redirect(new URL("/", request.url))
  }

  // If user doesn't have token and visits protected pages, redirect to login
  // Note: We let the client-side AuthGuard handle this for better UX,
  // but this provides a fast server-side redirect as well
  if (!token && !isPublicPath(pathname)) {
    const loginUrl = new URL("/login", request.url)
    loginUrl.searchParams.set("redirect", pathname)
    return NextResponse.redirect(loginUrl)
  }

  return NextResponse.next()
}

export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public folder
     */
    "/((?!_next/static|_next/image|favicon.ico|public).*)",
  ],
}
