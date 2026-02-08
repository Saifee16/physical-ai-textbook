import React from 'react';
import styles from './Personalize.module.css';

interface PersonalizedContentProps {
  content: string;
  modifications: string[];
  onRevert?: () => void;
}

export default function PersonalizedContent({ 
  content, 
  modifications,
  onRevert 
}: PersonalizedContentProps) {
  return (
    <div className={styles.personalizedContent}>
      <div className={styles.banner}>
        <span>✨ Content personalized for you</span>
        {onRevert && (
          <button onClick={onRevert} className={styles.revertButton}>
            ← Revert to Original
          </button>
        )}
      </div>
      
      <div className={styles.modifications}>
        <strong>Adjustments made:</strong>
        <ul>
          {modifications.map((mod, idx) => (
            <li key={idx}>{mod}</li>
          ))}
        </ul>
      </div>

      <div dangerouslySetInnerHTML={{ __html: content }} />
    </div>
  );
}