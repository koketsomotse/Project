import React, { useEffect, useState } from 'react';
import axios from 'axios';
import NotificationPreferences from '../components/NotificationPreferences';

const UserProfile = () => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchUserProfile = async () => {
            try {
                const response = await axios.get('http://localhost:8000/api/profile/');
                setUser(response.data);
            } catch (err) {
                setError('Failed to fetch user profile');
            } finally {
                setLoading(false);
            }
        };

        fetchUserProfile();
    }, []);

    const handleUpdate = async () => {
        try {
            await axios.put('http://localhost:8000/api/profile/', user);
            alert('Profile updated successfully');
        } catch (err) {
            setError('Failed to update profile');
        }
    };

    if (loading) return <div>Loading...</div>;
    if (error) return <div>{error}</div>;

    return (
        <div>
            <h1>User Profile</h1>
            <input 
                type="text" 
                value={user?.username || ''} 
                onChange={(e) => setUser({ ...user, username: e.target.value })} 
            />
            <button onClick={handleUpdate}>Update Profile</button>
            <NotificationPreferences />
        </div>
    );
};

export default UserProfile;
