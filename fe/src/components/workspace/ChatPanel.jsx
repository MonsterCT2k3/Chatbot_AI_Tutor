import { useEffect, useRef, useState } from 'react';
import { BookOpen, Check, History, Mic, Paperclip, Plus, Send, ThumbsDown, ThumbsUp, X } from 'lucide-react';
import { submitFeedback } from '../../services/chatService';
import { createSession, listMessages, sendSessionMessage } from '../../services/sessionService';

const FOLLOWUP_SUGGESTIONS = [
  'Giải thích chi tiết hơn phần vừa rồi',
  'Cho tôi 1 ví dụ minh hoạ cụ thể',
  'Tóm tắt lại các ý chính',
];

function mapServerMessage(m) {
  return {
    role: m.role,
    content: m.content,
    answerId: m.answer_id ?? null,
    citations: m.citations || [],
    feedback: null,
  };
}

function errorMessage(err) {
  const body = err.response?.data;
  return body?.message || body?.error?.message || 'Không thể lấy câu trả lời lúc này. Thử lại sau.';
}

function formatSessionTime(iso) {
  if (!iso) return '';
  const then = new Date(iso);
  if (Number.isNaN(then.getTime())) return '';
  const diffMs = Date.now() - then.getTime();
  const diffMin = Math.max(0, Math.floor(diffMs / 60000));
  if (diffMin < 1) return 'Vừa xong';
  if (diffMin < 60) return `${diffMin} phút trước`;
  const diffHour = Math.floor(diffMin / 60);
  if (diffHour < 24) return `${diffHour} giờ trước`;
  return then.toLocaleString('vi-VN', { day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit' });
}

export default function ChatPanel({
  documentId,
  sessionId,
  sessions = [],
  onSessionEnsured,
  onSelectSession,
  onNewSession,
  onDeleteSession,
  setPageNumber,
}) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isAsking, setIsAsking] = useState(false);
  const [error, setError] = useState(null);
  const [historyOpen, setHistoryOpen] = useState(false);
  const scrollRef = useRef(null);
  const skipLoadRef = useRef(false);
  const historyRef = useRef(null);

  const currentSession = sessions.find((s) => s.id === sessionId);
  const sessionTitle = currentSession?.title || (sessionId ? 'Cuộc trò chuyện' : 'Cuộc trò chuyện mới');

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: 'smooth' });
  }, [messages, isAsking]);

  useEffect(() => {
    if (!historyOpen) return undefined;
    function onPointerDown(e) {
      if (historyRef.current && !historyRef.current.contains(e.target)) setHistoryOpen(false);
    }
    document.addEventListener('mousedown', onPointerDown);
    return () => document.removeEventListener('mousedown', onPointerDown);
  }, [historyOpen]);

  useEffect(() => {
    setHistoryOpen(false);
  }, [sessionId]);

  useEffect(() => {
    if (skipLoadRef.current) {
      skipLoadRef.current = false;
      return;
    }
    if (!sessionId) {
      setMessages([]);
      setError(null);
      return;
    }
    let cancelled = false;
    listMessages(sessionId)
      .then((data) => {
        if (!cancelled) setMessages((data.messages || []).map(mapServerMessage));
      })
      .catch(() => {
        if (!cancelled) setError('Không tải được lịch sử hội thoại.');
      });
    return () => {
      cancelled = true;
    };
  }, [sessionId]);

  async function sendQuestion(question) {
    if (!question.trim() || isAsking) return;
    setError(null);
    setMessages((prev) => [...prev, { role: 'user', content: question }]);
    setInput('');
    setIsAsking(true);
    try {
      let sid = sessionId;
      if (!sid) {
        const created = await createSession(documentId);
        sid = created.id;
        skipLoadRef.current = true;
        onSessionEnsured(created);
      }
      const result = await sendSessionMessage(sid, question);
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          answerId: result.answer_id ?? null,
          content: result.content,
          citations: result.citations || [],
          feedback: null,
        },
      ]);
      onSessionEnsured({ id: sid });
    } catch (err) {
      setError(errorMessage(err));
    } finally {
      setIsAsking(false);
    }
  }

  async function handleFeedback(answerId, isPositive) {
    if (!answerId) return;
    setMessages((prev) => prev.map((m) => (m.answerId === answerId ? { ...m, feedback: isPositive ? 'up' : 'down' } : m)));
    try {
      await submitFeedback(documentId, answerId, isPositive);
    } catch {
      // Feedback phụ — lỗi thì không làm phiền.
    }
  }

  function handleSubmit(e) {
    e.preventDefault();
    sendQuestion(input);
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendQuestion(input);
    }
  }

  const lastAssistant = [...messages].reverse().find((m) => m.role === 'assistant');
  const isVerified = lastAssistant?.citations?.length > 0;

  return (
    <aside className="panel-right">
      <div className="chat-session-bar" ref={historyRef}>
        <div className="chat-session-title" title={sessionTitle}>
          {sessionTitle}
        </div>
        <button
          type="button"
          className={`chat-history-btn ${historyOpen ? 'open' : ''}`}
          title="Lịch sử hội thoại"
          onClick={() => setHistoryOpen((v) => !v)}
        >
          <History size={16} />
        </button>
        {historyOpen && (
          <div className="chat-history-menu">
            <button
              type="button"
              className="chat-history-new"
              onClick={() => {
                onNewSession?.();
                setHistoryOpen(false);
              }}
            >
              <Plus size={14} />
              <span>Cuộc trò chuyện mới</span>
            </button>
            {sessions.length === 0 && (
              <div className="chat-history-empty">Chưa có cuộc trò chuyện nào.</div>
            )}
            <ul className="chat-history-list">
              {sessions.map((s) => {
                const active = s.id === sessionId;
                return (
                  <li key={s.id}>
                    <button
                      type="button"
                      className={`chat-history-item ${active ? 'active' : ''}`}
                      onClick={() => {
                        onSelectSession?.(s.id);
                        setHistoryOpen(false);
                      }}
                    >
                      <span className="chat-history-item-title">{s.title || 'New chat'}</span>
                      <span className="chat-history-item-time">{formatSessionTime(s.updated_at)}</span>
                    </button>
                    <button
                      type="button"
                      className="chat-history-item-delete"
                      title="Xoá"
                      onClick={() => onDeleteSession?.(s.id)}
                    >
                      <X size={12} />
                    </button>
                  </li>
                );
              })}
            </ul>
          </div>
        )}
      </div>
      <div className="chat-status-badges-row">
        <span className="socratic-chip">🎓 Trợ giảng AI</span>
        {isVerified && (
          <span className="verified-chip">
            <Check size={11} strokeWidth={3} />
            <span>Có trích dẫn từ tài liệu</span>
          </span>
        )}
      </div>

      <div className="chat-scroll-stream" ref={scrollRef}>
        {messages.length === 0 && (
          <div className="chat-empty-state">
            Đặt câu hỏi về nội dung tài liệu — AI sẽ trả lời kèm trích dẫn trang thật.
          </div>
        )}

        {messages.map((m, i) =>
          m.role === 'user' ? (
            <div className="user-bubble-container" key={m.id || `u-${i}`}>
              <div className="user-bubble-content">{m.content}</div>
            </div>
          ) : (
            <div className="ai-bubble-container" key={m.answerId || `a-${i}`}>
              <div className="ai-book-avatar">
                <BookOpen size={14} color="#92400E" />
              </div>
              <div className="ai-card-content">
                {m.citations?.[0] && (
                  <span className="source-tag-chip">
                    [Nguồn: Trang {m.citations[0].page_number} · Xác thực qua pgvector]
                  </span>
                )}

                <div className="ai-response-text">{m.content}</div>

                {m.citations?.length > 0 && (
                  <div className="citation-badges-row">
                    {m.citations.map((c, ci) => (
                      <button
                        key={c.chunk_id || `${c.page_number}-${ci}`}
                        type="button"
                        className="citation-link-badge"
                        onClick={() => setPageNumber(c.page_number)}
                        title={c.snippet || ''}
                      >
                        <span>📖</span>
                        <span>Trang {c.page_number}</span>
                      </button>
                    ))}
                  </div>
                )}

                {m.answerId && (
                  <div className="feedback-row">
                    <button
                      type="button"
                      className={`feedback-btn ${m.feedback === 'up' ? 'active' : ''}`}
                      disabled={m.feedback !== null}
                      onClick={() => handleFeedback(m.answerId, true)}
                      title="Câu trả lời hữu ích"
                    >
                      <ThumbsUp size={13} />
                    </button>
                    <button
                      type="button"
                      className={`feedback-btn ${m.feedback === 'down' ? 'active' : ''}`}
                      disabled={m.feedback !== null}
                      onClick={() => handleFeedback(m.answerId, false)}
                      title="Câu trả lời chưa tốt"
                    >
                      <ThumbsDown size={13} />
                    </button>
                  </div>
                )}
              </div>
            </div>
          ),
        )}

        {isAsking && (
          <div className="ai-bubble-container">
            <div className="ai-book-avatar">
              <BookOpen size={14} color="#92400E" />
            </div>
            <div className="ai-card-content ai-card-loading">Đang tìm trong tài liệu...</div>
          </div>
        )}

        {!isAsking && lastAssistant && (
          <div className="quiz-followup-box">
            <div className="quiz-header-title">
              <span>💡</span>
              <span>Hỏi tiếp:</span>
            </div>
            {FOLLOWUP_SUGGESTIONS.map((s) => (
              <button key={s} type="button" className="quiz-option-btn" onClick={() => sendQuestion(s)}>
                {s}
              </button>
            ))}
          </div>
        )}

        {error && <div className="error-banner">{error}</div>}
      </div>

      <form className="input-dock-box" onSubmit={handleSubmit}>
        <textarea
          className="dock-textarea"
          placeholder="Đặt câu hỏi về tài liệu này..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={isAsking}
        />
        <div className="dock-actions-row">
          <button type="button" className="tool-icon-btn" title="Chưa hỗ trợ" disabled>
            <Paperclip size={15} />
          </button>
          <div className="dock-right-group">
            <button type="button" className="tool-icon-btn" title="Chưa hỗ trợ" disabled>
              <Mic size={15} />
            </button>
            <button type="submit" className="send-action-btn" disabled={isAsking || !input.trim()}>
              <span>Gửi</span>
              <Send size={12} strokeWidth={2.5} />
            </button>
          </div>
        </div>
      </form>
    </aside>
  );
}
