import React from 'react';
import Navbar from './Navbar';
import Sidebar from './Sidebar';

interface MainLayoutProps {
  children: React.ReactNode;
}

/**
 * MainLayout Component
 * 
 * Provides the main application layout structure.
 * 
 * Features:
 * - Responsive layout with sidebar
 * - Navigation bar
 * - Content area
 * 
 * @param {MainLayoutProps} props - Component props
 */
const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Top Navigation */}
      <Navbar />
      
      <div className="flex">
        {/* Sidebar */}
        <Sidebar />
        
        {/* Main Content */}
        <main className="flex-1 p-6">
          <div className="max-w-7xl mx-auto">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
};

export default MainLayout;
