import React from 'react';
import { Bot, User, Globe, AlertTriangle, BookOpen } from 'lucide-react';
import './MessageBubble.css';

const MessageBubble = ({ message }) => {
  const isUser = message.role === 'user';
  
  // Format [Slide X] into beautiful spans
  const formatText = (text) => {
    if (!text) return null;
    const parts = text.split(/(\[Slide \d+\]|\[Nguồn: Internet\])/g);
    
    return parts.map((part, index) => {
      if (part.startsWith('[Slide')) {
        return <span key={index} className="citation slide-citation"><BookOpen size={14}/> {part.replace('[', '').replace(']', '')}</span>;
      }
      if (part === '[Nguồn: Internet]') {
        return <span key={index} className="citation web-citation"><Globe size={14}/> Internet</span>;
      }
      // Simple bold rendering
      const boldParts = part.split(/(\*\*.*?\*\*)/g);
      return boldParts.map((bp, i) => {
        if (bp.startsWith('**') && bp.endsWith('**')) {
          return <strong key={i}>{bp.replace(/\*\*/g, '')}</strong>;
        }
        return <React.Fragment key={i}>{bp}</React.Fragment>;
      });
    });
  };

  const getActionIcon = () => {
    if (message.action === '[WEB_SEARCH]') return <Globe size={14} className="action-icon web" />;
    if (message.action === '[IRRELEVANT]') return <AlertTriangle size={14} className="action-icon warning" />;
    return null;
  };

  return (
    <div className={`message-wrapper ${isUser ? 'user-wrapper' : 'bot-wrapper'}`}>
      {!isUser && (
        <div className="avatar bot-avatar">
          <Bot size={20} />
        </div>
      )}
      
      <div className={`message-content glass-panel ${isUser ? 'user-msg' : 'bot-msg'} ${message.isError ? 'error-msg' : ''}`}>
        {!isUser && message.action && (
          <div className="action-badge">
            {getActionIcon()}
            <span>{message.action.replace('[', '').replace(']', '')}</span>
          </div>
        )}
        
        <div className="text-body">
          {formatText(message.content)}
        </div>

        {message.followUps && message.followUps.length > 0 && (
          <div className="follow-ups">
            <p className="follow-ups-title">💡 Gợi ý tìm hiểu thêm:</p>
            <ul>
              {message.followUps.map((q, i) => (
                <li key={i} className="follow-up-item">{q}</li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {isUser && (
        <div className="avatar user-avatar">
          <User size={20} />
        </div>
      )}
    </div>
  );
};

export default MessageBubble;
