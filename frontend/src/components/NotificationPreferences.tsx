import React, { useEffect, useState } from 'react';
import {
  getNotificationPreferences,
  updateNotificationPreferences
} from '@/services/notificationService';

interface NotificationPreferences {
  task_updated: boolean;
  task_assigned: boolean;
  task_completed: boolean;
}

/**
 * NotificationPreferences Component
 * 
 * Allows users to manage their notification preferences.
 * 
 * Features:
 * - Toggle individual notification types
 * - Save preference changes
 * - Real-time validation
 * - Error handling
 */
const NotificationPreferences: React.FC = () => {
  const [preferences, setPreferences] = useState<NotificationPreferences>({
    task_updated: true,
    task_assigned: true,
    task_completed: true
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  /**
   * Fetches user's current notification preferences
   */
  const fetchPreferences = async () => {
    try {
      setLoading(true);
      const data = await getNotificationPreferences();
      setPreferences(data);
    } catch (err) {
      setError('Failed to load preferences');
    } finally {
      setLoading(false);
    }
  };

  /**
   * Handles preference toggle changes
   */
  const handleToggle = (key: keyof NotificationPreferences) => {
    setPreferences(prev => ({
      ...prev,
      [key]: !prev[key]
    }));
  };

  /**
   * Validates preferences before saving
   * Ensures at least one notification type is enabled
   */
  const validatePreferences = (): boolean => {
    const hasOneEnabled = Object.values(preferences).some(value => value);
    if (!hasOneEnabled) {
      setError('At least one notification type must be enabled');
      return false;
    }
    return true;
  };

  /**
   * Saves updated preferences
   */
  const handleSave = async () => {
    if (!validatePreferences()) return;

    try {
      setSaving(true);
      setError(null);
      
      await updateNotificationPreferences(preferences);
      
      setSuccessMessage('Preferences updated successfully');
      setTimeout(() => setSuccessMessage(null), 3000);
    } catch (err) {
      setError('Failed to update preferences');
    } finally {
      setSaving(false);
    }
  };

  // Fetch preferences on component mount
  useEffect(() => {
    fetchPreferences();
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-32">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900" />
      </div>
    );
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm">
      <h2 className="text-xl font-semibold mb-4">
        Notification Preferences
      </h2>

      {/* Error Message */}
      {error && (
        <div className="mb-4 p-2 bg-red-100 text-red-700 rounded">
          {error}
        </div>
      )}

      {/* Success Message */}
      {successMessage && (
        <div className="mb-4 p-2 bg-green-100 text-green-700 rounded">
          {successMessage}
        </div>
      )}

      {/* Preference Toggles */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <label className="flex items-center space-x-2">
            <input
              type="checkbox"
              checked={preferences.task_updated}
              onChange={() => handleToggle('task_updated')}
              className="form-checkbox h-4 w-4 text-indigo-600"
            />
            <span>Task Updates</span>
          </label>
          <span className="text-sm text-gray-500">
            Receive notifications when tasks are updated
          </span>
        </div>

        <div className="flex items-center justify-between">
          <label className="flex items-center space-x-2">
            <input
              type="checkbox"
              checked={preferences.task_assigned}
              onChange={() => handleToggle('task_assigned')}
              className="form-checkbox h-4 w-4 text-indigo-600"
            />
            <span>Task Assignments</span>
          </label>
          <span className="text-sm text-gray-500">
            Receive notifications when tasks are assigned to you
          </span>
        </div>

        <div className="flex items-center justify-between">
          <label className="flex items-center space-x-2">
            <input
              type="checkbox"
              checked={preferences.task_completed}
              onChange={() => handleToggle('task_completed')}
              className="form-checkbox h-4 w-4 text-indigo-600"
            />
            <span>Task Completions</span>
          </label>
          <span className="text-sm text-gray-500">
            Receive notifications when tasks are completed
          </span>
        </div>
      </div>

      {/* Save Button */}
      <div className="mt-6">
        <button
          onClick={handleSave}
          disabled={saving}
          className="w-full bg-black text-white py-2 px-4 rounded-md hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 disabled:opacity-50"
        >
          {saving ? 'Saving...' : 'Save Preferences'}
        </button>
      </div>
    </div>
  );
};

export default NotificationPreferences;
