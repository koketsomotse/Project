import { useEffect, useState } from 'react';
import axios from 'axios';

const NotificationPreferences = () => {
    const [preferences, setPreferences] = useState({
        task_updated: true,
        task_assigned: true,
        task_completed: true,
    });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(false);

    useEffect(() =>module.exports = {
      content: [
        "./src/**/*.{js,jsx,ts,tsx}",
      ],
      theme: {
        extend: {},
      },
      plugins: [],
    } {
        const fetchPreferences = async () => {
            try {
                const response = await axios.get('http://localhost:8000/api/preferences/');
                setPreferences(response.data);
            } catch (err) {
                setError('Failed to fetch preferences');
            } finally {
                setLoading(false);
            }
        };

        fetchPreferences();
    }, []);

    const handleChange = (e) => {
        const { name, checked } = e.target;
        setPreferences((prev) => ({ ...prev, [name]: checked }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        setSuccess(false);

        try {
            await axios.post('http://localhost:8000/api/preferences/', preferences);
            setSuccess(true);
        } catch (err) {
            setError('Failed to update preferences');
        } finally {
            setLoading(false);
        }
    };

    if (loading) return <div className="text-gray-500">Loading...</div>;
    if (error) return <div className="text-red-500">{error}</div>;

    return (
        <form onSubmit={handleSubmit} className="flex flex-col p-4 space-y-4 bg-white rounded shadow-md">
            <h2 className="text-lg font-semibold">Notification Preferences</h2>
            <div className="flex items-center">
                <input
                    type="checkbox"
                    name="task_updated"
                    checked={preferences.task_updated}
                    onChange={handleChange}
                    className="mr-2"
                />
                <label className="text-gray-700">Task Updated</label>
            </div>
            <div className="flex items-center">
                <input
                    type="checkbox"
                    name="task_assigned"
                    checked={preferences.task_assigned}
                    onChange={handleChange}
                    className="mr-2"
                />
                <label className="text-gray-700">Task Assigned</label>
            </div>
            <div className="flex items-center">
                <input
                    type="checkbox"
                    name="task_completed"
                    checked={preferences.task_completed}
                    onChange={handleChange}
                    className="mr-2"
                />
                <label className="text-gray-700">Task Completed</label>
            </div>
            <button type="submit" disabled={loading} className="px-4 py-2 text-white bg-blue-500 rounded hover:bg-blue-600 disabled:opacity-50">Save Preferences</button>
            {success && <div className="text-green-500">Preferences updated successfully!</div>}
        </form>
    );
};

export default NotificationPreferences;
