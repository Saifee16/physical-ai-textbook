import React from 'react';
import styles from './Translate.module.css';

interface TranslatedContentProps {
  content: string;
  onRevert?: () => void;
}

export default function TranslatedContent({ content, onRevert }: TranslatedContentProps) {
  const handleRevert = () => {
    document.body.setAttribute('dir', 'ltr');
    if (onRevert) {
      onRevert();
    }
  };

  return (
    <div className={styles.translatedContent} dir="rtl">
      <div className={styles.banner}>
        <span>🌐 اردو میں ترجمہ</span>
        {onRevert && (
          <button onClick={handleRevert} className={styles.revertButton}>
            ← English میں واپس
          </button>
        )}
      </div>

      <div dangerouslySetInnerHTML={{ __html: content }} />
    </div>
  );
}