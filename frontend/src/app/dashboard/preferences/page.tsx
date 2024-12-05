'use client'

import { useState } from 'react'
import { Switch } from '@headlessui/react'
import { cn } from '@/lib/utils'

interface NotificationPreference {
  id: string
  type: string
  description: string
  enabled: boolean
}

export default function PreferencesPage() {
  const [preferences, setPreferences] = useState<NotificationPreference[]>([
    {
      id: '1',
      type: 'task_update',
      description: 'Receive notifications when tasks are updated',
      enabled: true,
    },
    {
      id: '2',
      type: 'task_assignment',
      description: 'Receive notifications when tasks are assigned to you',
      enabled: true,
    },
    {
      id: '3',
      type: 'task_completion',
      description: 'Receive notifications when tasks are completed',
      enabled: true,
    },
  ])

  const handleToggle = async (id: string) => {
    try {
      const preference = preferences.find((p) => p.id === id)
      if (!preference) return

      // Call your API to update preference
      await fetch(`/api/preferences/${id}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          enabled: !preference.enabled,
        }),
      })

      setPreferences((prev) =>
        prev.map((p) =>
          p.id === id ? { ...p, enabled: !p.enabled } : p
        )
      )
    } catch (error) {
      console.error('Failed to update preference:', error)
    }
  }

  return (
    <div className="py-6">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <h1 className="text-2xl font-semibold text-gray-900">
          Notification Preferences
        </h1>
      </div>
      <div className="mx-auto max-w-7xl px-4 sm:px-6 md:px-8">
        <div className="py-4">
          <div className="bg-white shadow sm:rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <div className="space-y-6">
                {preferences.map((preference) => (
                  <Switch.Group key={preference.id} as="div" className="flex items-center justify-between">
                    <div className="flex flex-col">
                      <Switch.Label as="span" className="text-sm font-medium text-gray-900" passive>
                        {preference.type.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                      </Switch.Label>
                      <Switch.Description as="span" className="text-sm text-gray-500">
                        {preference.description}
                      </Switch.Description>
                    </div>
                    <Switch
                      checked={preference.enabled}
                      onChange={() => handleToggle(preference.id)}
                      className={cn(
                        preference.enabled ? 'bg-primary-600' : 'bg-gray-200',
                        'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-primary-600 focus:ring-offset-2'
                      )}
                    >
                      <span
                        aria-hidden="true"
                        className={cn(
                          preference.enabled ? 'translate-x-5' : 'translate-x-0',
                          'pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out'
                        )}
                      />
                    </Switch>
                  </Switch.Group>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
