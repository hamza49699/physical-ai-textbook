import React, { useState, useRef, useEffect } from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './Chatbot.module.css';

interface Message {
  type: 'user' | 'assistant';
  content: string;
  sources?: string[];
  confidence?: number;
}

export default function Chatbot() {
  const { siteConfig } = useDocusaurusContext();
  const backendUrl = (siteConfig.customFields?.backendUrl as string) || 'https://hamzakhan123-physical-ai-textbook.hf.space';
  
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    {
      type: 'assistant',
      content: 'Hello! I\'m the Physical AI Textbook Assistant. Ask me anything about ROS 2, Digital Twins, Isaac Sim, or Vision Language Models!'
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    // Add user message
    const userMessage: Message = { type: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch(`${backendUrl}/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: input, chapter: null })
      });

      const data = await response.json();
      const assistantMessage: Message = {
        type: 'assistant',
        content: data.response,
        sources: data.sources,
        confidence: data.confidence
      };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage: Message = {
        type: 'assistant',
        content: 'Sorry, I couldn\'t reach the chatbot service. Make sure the backend is running on http://localhost:8000'
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.chatbotContainer}>
      {/* Chat Button */}
      <button 
        className={styles.chatButton}
        onClick={() => setIsOpen(!isOpen)}
        title="Open chatbot"
      >
        💬
      </button>

      {/* Chat Window */}
      {isOpen && (
        <div className={styles.chatWindow}>
          <div className={styles.chatHeader}>
            <h3>Physical AI Assistant</h3>
            <button 
              className={styles.closeButton}
              onClick={() => setIsOpen(false)}
            >
              ✕
            </button>
          </div>

          <div className={styles.messagesContainer}>
            {messages.map((msg, idx) => (
              <div key={idx} className={`${styles.message} ${styles[msg.type]}`}>
                <div className={styles.messageContent}>{msg.content}</div>
                {msg.sources && msg.sources.length > 0 && (
                  <div className={styles.sources}>
                    <strong>Sources:</strong>
                    <ul>
                      {msg.sources.map((src, i) => (
                        <li key={i}>{src}</li>
                      ))}
                    </ul>
                  </div>
                )}
                {msg.confidence !== undefined && (
                  <div className={styles.confidence}>
                    Confidence: {(msg.confidence * 100).toFixed(0)}%
                  </div>
                )}
              </div>
            ))}
            {loading && (
              <div className={`${styles.message} ${styles.assistant}`}>
                <div className={styles.typing}>Thinking...</div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className={styles.inputArea}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSend()}
              placeholder="Ask about the textbook..."
              disabled={loading}
            />
            <button 
              onClick={handleSend}
              disabled={loading || !input.trim()}
            >
              Send
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
