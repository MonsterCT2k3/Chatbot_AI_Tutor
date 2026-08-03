import React, { useRef, useEffect } from 'react';
import ChatInput from './components/chat/ChatInput';
import MessageBubble from './components/chat/MessageBubble';
import { useChat } from './hooks/useChat';
import './App.css';

function App() {
  const { messages, isLoading, sendMessage } = useChat();
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div className="app-container">
      <header className="app-header glass-panel">
        <div className="header-content">
          <h1>AI Tutor <span>K3</span></h1>
          <p>Your intelligent learning companion</p>
        </div>
      </header>
      
      <main className="chat-container">
        <div className="messages-area">
          {messages.map(msg => (
            <MessageBubble key={msg.id} message={msg} />
          ))}
          <div ref={messagesEndRef} />
        </div>
        
        <div className="input-area">
          <ChatInput onSend={(text) => sendMessage(text, "b1")} isLoading={isLoading} />
        </div>
      </main>
    </div>
  );
}

export default App;
