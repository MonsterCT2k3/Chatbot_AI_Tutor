import React, { useState } from 'react';
import { Send, Loader2 } from 'lucide-react';
import './ChatInput.css';

const ChatInput = ({ onSend, isLoading }) => {
  const [text, setText] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (text.trim() && !isLoading) {
      onSend(text);
      setText('');
    }
  };

  return (
    <form className="chat-input-form glass-panel" onSubmit={handleSubmit}>
      <input
        type="text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Hỏi AI Tutor bất cứ điều gì..."
        disabled={isLoading}
        className="chat-input-field"
      />
      <button type="submit" disabled={!text.trim() || isLoading} className="chat-submit-btn">
        {isLoading ? <Loader2 className="spinner" size={20} /> : <Send size={20} />}
      </button>
    </form>
  );
};

export default ChatInput;
