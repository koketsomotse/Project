'use client'

import { useEffect, useState } from 'react'
import NotificationItem from './NotificationItem'
import { useWebSocket } from '@/hooks/useNotifications'

interface Notification {
  id: string
  title: string
  message: string
  type: 'task_update' | 'task_assignment' | 'task_completion'
  createdAt: string
  read: boolean
}

export default function NotificationFeed() {
  const [notifications, setNotifications] = useState<Notification[]>([])
  const { lastMessage } = useWebSocket()

  useEffect(() => {
    if (lastMessage) {
      try {
        const newNotification = JSON.parse(lastMessage.data)
        setNotifications((prev) => [newNotification, ...prev])
      } catch (error) {
        console.error('Failed to parse notification:', error)
      }
    }
  }, [lastMessage])

  const handleMarkAsRead = async (id: string) => {
    try {
      // Call your API to mark notification as read
      await fetch(`/api/notifications/${id}/read`, {
        method: 'POST',
      })
      
      setNotifications((prev) =>
        prev.map((notification) =>
          notification.id === id
            ? { ...notification, read: true }
            : notification
        )
      )
    } catch (error) {
      console.error('Failed to mark notification as read:', error)
    }
  }

  const handleDismiss = async (id: string) => {
    try {
      // Call your API to dismiss notification
      await fetch(`/api/notifications/${id}`, {
        method: 'DELETE',
      })
      
      setNotifications((prev) =>
        prev.filter((notification) => notification.id !== id)
      )
    } catch (error) {
      console.error('Failed to dismiss notification:', error)
    }
  }

  if (notifications.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">No notifications yet</p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {notifications.map((notification) => (
        <NotificationItem
          key={notification.id}
          {...notification}
          onMarkAsRead={handleMarkAsRead}
          onDismiss={handleDismiss}
        />
      ))}
    </div>
  )
}
