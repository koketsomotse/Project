import { formatDate } from '@/lib/utils'
import { CheckCircleIcon, XMarkIcon } from '@heroicons/react/24/outline'

interface NotificationItemProps {
  id: string
  title: string
  message: string
  type: 'task_update' | 'task_assignment' | 'task_completion'
  createdAt: string
  read: boolean
  onMarkAsRead: (id: string) => void
  onDismiss: (id: string) => void
}

export default function NotificationItem({
  id,
  title,
  message,
  type,
  createdAt,
  read,
  onMarkAsRead,
  onDismiss,
}: NotificationItemProps) {
  const getTypeStyles = () => {
    switch (type) {
      case 'task_completion':
        return 'bg-green-50 text-green-700'
      case 'task_assignment':
        return 'bg-blue-50 text-blue-700'
      case 'task_update':
        return 'bg-yellow-50 text-yellow-700'
      default:
        return 'bg-gray-50 text-gray-700'
    }
  }

  return (
    <div
      className={`relative rounded-lg p-4 ${
        read ? 'bg-white' : 'bg-primary-50'
      } shadow-sm transition-all hover:shadow-md`}
    >
      <div className="flex items-start space-x-4">
        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between">
            <p
              className={`text-sm font-medium ${
                read ? 'text-gray-900' : 'text-primary-900'
              }`}
            >
              {title}
            </p>
            <div className="flex items-center space-x-2">
              <span
                className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${getTypeStyles()}`}
              >
                {type.replace('_', ' ')}
              </span>
              <span className="text-xs text-gray-500">
                {formatDate(createdAt)}
              </span>
            </div>
          </div>
          <p
            className={`mt-1 text-sm ${
              read ? 'text-gray-500' : 'text-primary-700'
            }`}
          >
            {message}
          </p>
        </div>
      </div>
      {!read && (
        <div className="absolute bottom-4 right-4 flex space-x-2">
          <button
            onClick={() => onMarkAsRead(id)}
            className="inline-flex items-center rounded-full p-1.5 text-primary-600 hover:text-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            <CheckCircleIcon className="h-5 w-5" />
          </button>
          <button
            onClick={() => onDismiss(id)}
            className="inline-flex items-center rounded-full p-1.5 text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            <XMarkIcon className="h-5 w-5" />
          </button>
        </div>
      )}
    </div>
  )
}
