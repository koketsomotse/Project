'use client'

import { useSession } from 'next-auth/react'

export default function DashboardPage() {
  const { data: session } = useSession()

  return (
    <div className="py-6">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <h1 className="text-2xl font-semibold text-gray-900">Dashboard</h1>
      </div>
      <div className="mx-auto max-w-7xl px-4 sm:px-6 md:px-8">
        {/* Welcome Message */}
        <div className="bg-white shadow sm:rounded-lg mt-6">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg font-medium leading-6 text-gray-900">
              Welcome back, {session?.user?.name}!
            </h3>
            <div className="mt-2 max-w-xl text-sm text-gray-500">
              <p>Your notification system is active and running.</p>
            </div>
          </div>
        </div>

        {/* Stats */}
        <div className="mt-8">
          <dl className="grid grid-cols-1 gap-5 sm:grid-cols-3">
            <div className="overflow-hidden rounded-lg bg-white px-4 py-5 shadow sm:p-6">
              <dt className="truncate text-sm font-medium text-gray-500">
                Total Notifications
              </dt>
              <dd className="mt-1 text-3xl font-semibold tracking-tight text-gray-900">
                0
              </dd>
            </div>
            <div className="overflow-hidden rounded-lg bg-white px-4 py-5 shadow sm:p-6">
              <dt className="truncate text-sm font-medium text-gray-500">
                Unread Notifications
              </dt>
              <dd className="mt-1 text-3xl font-semibold tracking-tight text-gray-900">
                0
              </dd>
            </div>
            <div className="overflow-hidden rounded-lg bg-white px-4 py-5 shadow sm:p-6">
              <dt className="truncate text-sm font-medium text-gray-500">
                Notification Types
              </dt>
              <dd className="mt-1 text-3xl font-semibold tracking-tight text-gray-900">
                3
              </dd>
            </div>
          </dl>
        </div>
      </div>
    </div>
  )
}
