import React, { useState } from 'react';
import styles from './Translate.module.css';

interface TranslateButtonProps {
  chapterId: string;
  content: string;
  onTranslated?: (content: string) => void;
}

export default function TranslateButton({ 
  chapterId, 
  content, 
  onTranslated 
}: TranslateButtonProps) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleTranslate = async () => {
    setLoading(true);
    setError('');

    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000'}/api/translate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content,
          chapter_id: chapterId,
          target_language: 'ur'
        }),
      });

      if (!response.ok) {
        throw new Error('Translation failed');
      }

      const data = await response.json();
      
      if (onTranslated) {
        onTranslated(data.translated_content);
      }

      // Apply RTL
      document.body.setAttribute('dir', 'rtl');
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.translateContainer}>
      <button
        onClick={handleTranslate}
        disabled={loading}
        className={styles.translateButton}
      >
        {loading ? '⏳ ترجمہ ہو رہا ہے...' : '🌐 ترجمہ اردو میں'}
      </button>
      {error && <div className={styles.error}>{error}</div>}
    </div>
  );
}