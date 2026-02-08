import React, { useState } from 'react';
import { useAuth } from '../Auth/AuthProvider';
import styles from './Personalize.module.css';

interface PersonalizeButtonProps {
  chapterId: string;
  content: string;
  onPersonalized?: (content: string) => void;
}

export default function PersonalizeButton({ 
  chapterId, 
  content, 
  onPersonalized 
}: PersonalizeButtonProps) {
  const { isAuthenticated, token } = useAuth();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handlePersonalize = async () => {
    if (!isAuthenticated) {
      alert('Please sign in to personalize content');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000'}/api/personalize`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          content,
          chapter_id: chapterId
        }),
      });

      if (!response.ok) {
        throw new Error('Personalization failed');
      }

      const data = await response.json();
      
      if (onPersonalized) {
        onPersonalized(data.personalized_content);
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className={styles.personalizeContainer}>
      <button
        onClick={handlePersonalize}
        disabled={loading}
        className={styles.personalizeButton}
      >
        {loading ? '⏳ Personalizing...' : '🎯 Personalize Content'}
      </button>
      {error && <div className={styles.error}>{error}</div>}
    </div>
  );
}