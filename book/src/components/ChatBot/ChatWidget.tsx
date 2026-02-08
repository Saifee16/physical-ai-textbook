import React, { useState, useEffect, useRef } from 'react';
import styles from './ChatWidget.module.css';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  sources?: Array<{
    chapter: string;
    section: string;
    page: number;
  }>;
}

interface ChatWidgetProps {
  backendUrl?: string;
}

export default function ChatWidget({ backendUrl = 'http://localhost:8000' }: ChatWidgetProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string>('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Generate session ID on mount
    setSessionId(crypto.randomUUID());
    
    // Add welcome message
    setMessages([{
      role: 'assistant',
      content: 'Hello! I\'m your Physical AI & Robotics teaching assistant. Ask me anything about the course content!'
    }]);
  }, []);

  useEffect(() => {
    // Scroll to bottom when new messages arrive
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput('');
    
    // Add user message
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setIsLoading(true);

    try {
      // Get current chapter context from URL
      const currentPath = window.location.pathname;
      const chapterMatch = currentPath.match(/\/(week\d+-\d+|hardware|capstone)\/([^/]+)/);
      const chapterContext = chapterMatch ? `${chapterMatch[1]}/${chapterMatch[2]}` : undefined;

      // Check if user has selected text
      const selectedText = window.getSelection()?.toString() || undefined;

      const response = await fetch(`${backendUrl}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: userMessage,
          chapter_context: chapterContext,
          selected_text: selectedText,
          session_id: sessionId,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to get response');
      }

      const data = await response.json();
      
      // Add assistant message
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: data.answer,
        sources: data.sources
      }]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.'
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className={styles.chatWidget}>
      {/* Chat Button */}
      <button
        className={styles.chatButton}
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Toggle chat"
      >
        {isOpen ? '✕' : '💬'}
      </button>

      {/* Chat Window */}
      {isOpen && (
        <div className={styles.chatWindow}>
          {/* Header */}
          <div className={styles.chatHeader}>
            <h3>🤖 AI Teaching Assistant</h3>
            <button
              onClick={() => setMessages([messages[0]])}
              className={styles.clearButton}
              title="Clear chat"
            >
              🗑️
            </button>
          </div>

          {/* Messages */}
          <div className={styles.messagesContainer}>
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`${styles.message} ${styles[msg.role]}`}
              >
                <div className={styles.messageContent}>
                  {msg.content}
                </div>
                {msg.sources && msg.sources.length > 0 && (
                  <div className={styles.sources}>
                    <small>📚 Sources:</small>
                    {msg.sources.map((source, i) => (
                      <small key={i} className={styles.source}>
                        {source.chapter} - {source.section}
                      </small>
                    ))}
                  </div>
                )}
              </div>
            ))}
            {isLoading && (
              <div className={`${styles.message} ${styles.assistant}`}>
                <div className={styles.messageContent}>
                  <span className={styles.loadingDots}>
                    <span>.</span><span>.</span><span>.</span>
                  </span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className={styles.inputContainer}>
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask a question about the course..."
              className={styles.input}
              rows={2}
              disabled={isLoading}
            />
            <button
              onClick={handleSend}
              disabled={!input.trim() || isLoading}
              className={styles.sendButton}
            >
              ➤
            </button>
          </div>
        </div>
      )}
    </div>
  );
}