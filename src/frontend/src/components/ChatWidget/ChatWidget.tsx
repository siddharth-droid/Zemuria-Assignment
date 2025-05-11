import React, { useState, useEffect, useRef } from 'react';
import './ChatWidget.css';

const ChatWidget: React.FC = () => {
  const [messages, setMessages] = useState<Array<{ text: string; isUser: boolean }>>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    loadChatHistory();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const loadChatHistory = async () => {
    try {
      const response = await fetch('http://localhost:7860/api/v2/chat/history');
      if (!response.ok) {
        throw new Error('Failed to fetch chat history');
      }
      const history = await response.json();
      
      // Clear existing messages
      setMessages([]);
      
      // Add messages in chronological order
      const formattedMessages = history.reverse().flatMap(msg => [
        { text: msg.user_message, isUser: true },
        { text: msg.assistant_message, isUser: false }
      ]);
      
      setMessages(formattedMessages);
    } catch (error) {
      console.error('Error loading chat history:', error);
    }
  };

  const handleKeyPress = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter') {
      sendMessage();
    }
  };

  const sendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage = inputMessage.trim();
    setInputMessage('');
    setMessages(prev => [...prev, { text: userMessage, isUser: true }]);
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:7860/api/v2/openai/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: userMessage
        })
      });

      const data = await response.json();
      
      if (response.ok) {
        setMessages(prev => [...prev, { text: data.response, isUser: false }]);
        
        // Save message to database
        await fetch('http://localhost:7860/api/v2/chat/save', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            user_message: userMessage,
            assistant_message: data.response
          })
        });
      } else {
        setMessages(prev => [...prev, { text: 'Sorry, there was an error processing your request.', isUser: false }]);
      }
    } catch (error) {
      setMessages(prev => [...prev, { text: 'Sorry, there was an error connecting to the server.', isUser: false }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-widget">
      <div className="chat-header">
        OpenAI Chat
      </div>
      <div className="chat-body">
        <div className="chat-messages">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`message ${message.isUser ? 'user-message' : 'assistant-message'}`}
            >
              {message.text}
            </div>
          ))}
          {isLoading && (
            <div className="loading">Thinking...</div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>
      <div className="chat-input">
        <div className="input-container">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message..."
          />
          <button onClick={sendMessage}>Send</button>
        </div>
      </div>
    </div>
  );
};

export default ChatWidget; 