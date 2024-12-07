import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { logoutUser } from '@/services/authService';

/**
 * Navbar Component
 * 
 * Top navigation bar with user controls and notifications.
 * 
 * Features:
 * - User profile dropdown
 * - Notification indicator
 * - Responsive design
 * - Authentication controls
 */
const Navbar: React.FC = () => {
  const [isProfileOpen, setIsProfileOpen] = useState(false);
  const router = useRouter();

  /**
   * Handles user logout
   * Clears authentication and redirects to login
   */
  const handleLogout = () => {
    logoutUser();
    router.push('/login');
  };

  return (
    <nav className="bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Logo and Brand */}
          <div className="flex items-center">
            <Link href="/dashboard" className="text-xl font-bold text-gray-900">
              Notification System
            </Link>
          </div>

          {/* Navigation Links */}
          <div className="hidden sm:flex sm:items-center sm:space-x-8">
            <Link
              href="/dashboard"
              className="text-gray-500 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
            >
              Dashboard
            </Link>
            <Link
              href="/preferences"
              className="text-gray-500 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
            >
              Preferences
            </Link>
          </div>

          {/* User Profile Dropdown */}
          <div className="flex items-center">
            <div className="relative">
              <button
                onClick={() => setIsProfileOpen(!isProfileOpen)}
                className="flex items-center space-x-2 text-gray-500 hover:text-gray-900"
              >
                <span className="h-8 w-8 rounded-full bg-gray-200 flex items-center justify-center">
                  <svg
                    className="h-5 w-5 text-gray-500"
                    fill="none"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                </span>
              </button>

              {/* Dropdown Menu */}
              {isProfileOpen && (
                <div className="absolute right-0 mt-2 w-48 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5">
                  <div
                    className="py-1"
                    role="menu"
                    aria-orientation="vertical"
                    aria-labelledby="user-menu"
                  >
                    <Link
                      href="/profile"
                      className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                      role="menuitem"
                    >
                      Your Profile
                    </Link>
                    <Link
                      href="/preferences"
                      className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                      role="menuitem"
                    >
                      Preferences
                    </Link>
                    <button
                      onClick={handleLogout}
                      className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                      role="menuitem"
                    >
                      Sign out
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
