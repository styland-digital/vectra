export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm">
        <h1 className="text-4xl font-bold mb-4">Vectra</h1>
        <p className="text-xl">AI Sales Agents Platform</p>
        <p className="text-sm text-muted-foreground mt-4">
          Backend API: {process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/v1"}
        </p>
      </div>
    </main>
  )
}
