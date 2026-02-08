import React, { useEffect, useState } from 'react';
import { useAuth } from './AuthProvider';
import styles from './Auth.module.css';

interface UserProfile {
  email: string;
  software_level: string;
  hardware_level: string;
  robotics_knowledge: boolean;
  learning_goals?: string;
}

export default function ProfileDashboard() {
  const { token, logout } = useAuth();
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000'}/api/auth/profile`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setProfile(data);
      }
    } catch (err) {
      console.error('Failed to fetch profile:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className={styles.dashboard}>
      <h2>Your Profile</h2>
      
      {profile && (
        <div className={styles.profileInfo}>
          <p><strong>Email:</strong> {profile.email}</p>
          <p><strong>Software Level:</strong> {profile.software_level}</p>
          <p><strong>Hardware Level:</strong> {profile.hardware_level}</p>
          <p><strong>Robotics Background:</strong> {profile.robotics_knowledge ? 'Yes' : 'No'}</p>
          {profile.learning_goals && (
            <p><strong>Learning Goals:</strong> {profile.learning_goals}</p>
          )}
        </div>
      )}

      <button onClick={logout} className={styles.logoutButton}>
        Sign Out
      </button>
    </div>
  );
}