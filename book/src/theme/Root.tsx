import React from 'react';
import ChatWidget from '@site/src/components/ChatBot/ChatWidget';

// Default theme Root component
export default function Root({children}) {
  return (
    <>
      {children}
      <ChatWidget backendUrl={process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000'} />
    </>
  );
}