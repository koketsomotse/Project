interface NotificationBadgeProps {
  count: number
}

export default function NotificationBadge({ count }: NotificationBadgeProps) {
  if (count === 0) return null

  return (
    <span className="absolute -top-1 -right-1 inline-flex items-center justify-center px-2 py-1 text-xs font-bold leading-none text-white transform translate-x-1/2 -translate-y-1/2 bg-red-600 rounded-full">
      {count > 99 ? '99+' : count}
    </span>
  )
}
