import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

/**
 * Sidebar Component
 * 
 * Navigation sidebar with links to different sections.
 * 
 * Features:
 * - Active route highlighting
 * - Collapsible on mobile
 * - Section organization
 */
const Sidebar: React.FC = () => {
  const pathname = usePathname();

  /**
   * Checks if a route is currently active
   * 
   * @param {string} path - Route path to check
   * @returns {boolean} True if route is active
   */
  const isActive = (path: string): boolean => {
    return pathname === path;
  };

  return (
    <aside className="hidden md:flex md:flex-col w-64 bg-white shadow-sm">
      <div className="flex-1 flex flex-col pt-5 pb-4 overflow-y-auto">
        <div className="flex-1 px-3 space-y-1">
          {/* Dashboard Section */}
          <Link
            href="/dashboard"
            className={`
              group flex items-center px-2 py-2 text-sm font-medium rounded-md
              ${isActive('/dashboard')
                ? 'bg-gray-100 text-gray-900'
                : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'}
            `}
          >
            <svg
              className={`
                mr-3 h-6 w-6
                ${isActive('/dashboard')
                  ? 'text-gray-500'
                  : 'text-gray-400 group-hover:text-gray-500'}
              `}
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"
              />
            </svg>
            Dashboard
          </Link>

          {/* Notifications Section */}
          <Link
            href="/notifications"
            className={`
              group flex items-center px-2 py-2 text-sm font-medium rounded-md
              ${isActive('/notifications')
                ? 'bg-gray-100 text-gray-900'
                : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'}
            `}
          >
            <svg
              className={`
                mr-3 h-6 w-6
                ${isActive('/notifications')
                  ? 'text-gray-500'
                  : 'text-gray-400 group-hover:text-gray-500'}
              `}
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
              />
            </svg>
            Notifications
          </Link>

          {/* Preferences Section */}
          <Link
            href="/preferences"
            className={`
              group flex items-center px-2 py-2 text-sm font-medium rounded-md
              ${isActive('/preferences')
                ? 'bg-gray-100 text-gray-900'
                : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'}
            `}
          >
            <svg
              className={`
                mr-3 h-6 w-6
                ${isActive('/preferences')
                  ? 'text-gray-500'
                  : 'text-gray-400 group-hover:text-gray-500'}
              `}
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"
              />
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
              />
            </svg>
            Preferences
          </Link>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
