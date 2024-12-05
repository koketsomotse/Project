'use client'

import { useSession } from 'next-auth/react'
import { redirect } from 'next/navigation'
import Navigation from '@/components/ui/Navigation'

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const { data: session, status } = useSession()

  if (status === 'loading') {
    return <div>Loading...</div>
  }

  if (!session) {
    redirect('/login')
  }

  return (
    <div>
      <Navigation />
      <main>
        <div className="mx-auto max-w-7xl py-6 sm:px-6 lg:px-8">{children}</div>
      </main>
    </div>
  )
}
