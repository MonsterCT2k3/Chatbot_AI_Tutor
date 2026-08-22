import { useEffect, useRef, useState } from 'react';
import { BookOpen, Check, Mic, Paperclip, Send, ThumbsDown, ThumbsUp } from 'lucide-react';
import { askQuestion, submitFeedback } from '../../services/chatService';

// Gợi ý câu hỏi tiếp theo — mockup có "Explore Further & Self-Quiz" cá nhân
// hoá theo đúng nội dung slide (cần LLM sinh riêng, backend chưa có endpoint
// này). Giữ 3 gợi ý CỐ ĐỊNH (mock nội dung gợi ý) nhưng bấm vào vẫn gửi câu
// hỏi THẬT qua /ask — khác với mock "chết", đây chỉ mock phần gợi ý, hành vi
// khi bấm là thật.
const FOLLOWUP_SUGGESTIONS = [
  'Giải thích chi tiết hơn phần vừa rồi',
  'Cho tôi 1 ví dụ minh hoạ cụ thể',
  'Tóm tắt lại các ý chính',
];

export default function ChatPanel({ documentId, pageNumber, setPageNumber }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isAsking, setIsAsking] = useState(false);
  const [error, setError] = useState(null);
  const scrollRef = useRef(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: 'smooth' });
  }, [messages, isAsking]);

  async function sendQuestion(question) {
    if (!question.trim() || isAsking) return;
    setError(null);
    setMessages((prev) => [...prev, { role: 'user', content: question }]);
    setInput('');
    setIsAsking(true);
    try {
      const result = await askQuestion(documentId, question);
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          answerId: result.answer_id,
          content: result.answer,
          citations: result.citations,
          feedback: null,
        },
      ]);
    } catch (err) {
      setError(err.response?.data?.message || 'Không thể lấy câu trả lời lúc này. Thử lại sau.');
    } finally {
      setIsAsking(false);
    }
  }

  async function handleFeedback(answerId, isPositive) {
    setMessages((prev) => prev.map((m) => (m.answerId === answerId ? { ...m, feedback: isPositive ? 'up' : 'down' } : m)));
    try {
      await submitFeedback(documentId, answerId, isPositive);
    } catch {
      // Feedback là phụ (không ảnh hưởng câu trả lời đã có) — lỗi thì âm thầm
      // bỏ qua, không làm phiền người dùng bằng 1 lỗi cho hành động rất nhỏ.
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
      <div className="chat-status-badges-row">
        {/* Không có khái niệm "chế độ" (Socratic/thường...) ở backend — chip
            trang trí cố định, giữ nguyên phong cách mockup. */}
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
            <div className="user-bubble-container" key={i}>
              <div className="user-bubble-content">{m.content}</div>
            </div>
          ) : (
            <div className="ai-bubble-container" key={i}>
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
                    {m.citations.map((c) => (
                      <button
                        key={c.chunk_id}
                        type="button"
                        className="citation-link-badge"
                        onClick={() => setPageNumber(c.page_number)}
                        title={c.snippet}
                      >
                        <span>📖</span>
                        <span>Trang {c.page_number}</span>
                      </button>
                    ))}
                  </div>
                )}

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
              </div>
            </div>
          ),
        )}

        {isAsking && (
          <div className="ai-bubble-container">
            <div className="ai-book-avatar">
              <BookOpen size={14} color="#92400E" />
            </div>
            <div className="ai-card-content ai-card-loading">Đang suy nghĩ...</div>
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
