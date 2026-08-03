import { useState } from 'react';
import { askChatbot } from '../services/api';

export const useChat = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'assistant',
      content: 'Chào bạn! Mình là AI Tutor. Mình có thể giúp gì cho bạn hôm nay?',
      action: null,
      followUps: []
    }
  ]);
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = async (text, lesson = null) => {
    if (!text.trim()) return;

    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: text,
    };
    
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const data = await askChatbot(text, lesson);
      
      const botMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: data.answer,
        action: data.action_taken,
        followUps: data.follow_up_questions || []
      };
      
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      setMessages(prev => [...prev, {
        id: Date.now() + 1,
        role: 'assistant',
        content: 'Xin lỗi, hệ thống đang gặp sự cố kết nối. Vui lòng thử lại sau!',
        isError: true
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return { messages, isLoading, sendMessage };
};
