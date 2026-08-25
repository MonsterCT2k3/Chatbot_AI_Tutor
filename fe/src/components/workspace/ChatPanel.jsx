import { useEffect, useRef, useState } from 'react';
import { BookOpen, Check, History, Mic, Paperclip, Pencil, Plus, Send, ThumbsDown, ThumbsUp, X } from 'lucide-react';
import { submitFeedback } from '../../services/chatService';
import { createSession, listMessages, mapStreamStatus, sendSessionMessageStream } from '../../services/sessionService';

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
  return body?.message || body?.error?.message || err.message || 'Không thể lấy câu trả lời lúc này. Thử lại sau.';
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
  onRenameSession,
  onDeleteSession,
  setPageNumber,
  revealCitationPage,
  clearCitationHighlight,
}) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isAsking, setIsAsking] = useState(false);
  const [streamStatus, setStreamStatus] = useState(null);
  const [error, setError] = useState(null);
  const [historyOpen, setHistoryOpen] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [editTitle, setEditTitle] = useState('');
  const [renameBusy, setRenameBusy] = useState(false);
  const editInputRef = useRef(null);
  const scrollRef = useRef(null);
  const skipLoadRef = useRef(false);
  const historyRef = useRef(null);
  const didAutoJumpRef = useRef(false);

  const currentSession = sessions.find((s) => s.id === sessionId);
  const sessionTitle = currentSession?.title || (sessionId ? 'Cuộc trò chuyện' : 'Cuộc trò chuyện mới');

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: 'smooth' });
  }, [messages, isAsking, streamStatus]);

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
    setEditingId(null);
  }, [sessionId]);

  useEffect(() => {
    if (!historyOpen) {
      setEditingId(null);
    }
  }, [historyOpen]);

  useEffect(() => {
    if (editingId) {
      editInputRef.current?.focus();
      editInputRef.current?.select();
    }
  }, [editingId]);

  function startEditing(s, e) {
    e?.stopPropagation?.();
    setEditingId(s.id);
    setEditTitle(s.title || '');
  }

  async function submitRename(s) {
    if (renameBusy) return;
    const t = editTitle.trim();
    if (!t) {
      setEditingId(null);
      return;
    }
    const cleanTitle = t.slice(0, 200);
    if (cleanTitle === (s.title || '').trim()) {
      setEditingId(null);
      return;
    }
    setRenameBusy(true);
    try {
      await onRenameSession?.(s.id, cleanTitle);
      setEditingId(null);
    } catch (err) {
      setError(err.response?.data?.message || 'Không đổi được tên cuộc trò chuyện.');
    } finally {
      setRenameBusy(false);
    }
  }

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
    clearCitationHighlight?.();
    didAutoJumpRef.current = false;
    setError(null);
    setMessages((prev) => [...prev, { role: 'user', content: question }]);
    setInput('');
    setIsAsking(true);
    setStreamStatus('Đang tìm trong tài liệu...');
    try {
      let sid = sessionId;
      if (!sid) {
        const created = await createSession(documentId);
        sid = created.id;
        skipLoadRef.current = true;
        onSessionEnsured(created);
      }

      await sendSessionMessageStream(sid, question, {
        onStatus(stage) {
          setStreamStatus(mapStreamStatus(stage));
        },
        onToken(delta) {
          setMessages((prev) => {
            const last = prev[prev.length - 1];
            if (last && last.role === 'assistant' && last._streaming) {
              return [
                ...prev.slice(0, -1),
                { ...last, content: last.content + delta },
              ];
            }
            return [
              ...prev,
              {
                role: 'assistant',
                content: delta,
                citations: [],
                answerId: null,
                feedback: null,
                _streaming: true,
              },
            ];
          });
          setStreamStatus(null);
        },
        onCitation(citation) {
          setMessages((prev) => {
            const last = prev[prev.length - 1];
            if (last && last.role === 'assistant' && last._streaming) {
              return [
                ...prev.slice(0, -1),
                { ...last, citations: [...(last.citations || []), citation] },
              ];
            }
            return prev;
          });

          if (!didAutoJumpRef.current) {
            const p = Number(citation?.page_number);
            if (Number.isFinite(p) && p >= 1) {
              didAutoJumpRef.current = true;
              if (revealCitationPage) revealCitationPage(p, citation?.bbox ?? null);
              else setPageNumber?.(p);
            }
          }
        },
        onReplace({ content, citations }) {
          const nextCitations = citations || [];
          setMessages((prev) => {
            const last = prev[prev.length - 1];
            if (last && last.role === 'assistant' && last._streaming) {
              return [
                ...prev.slice(0, -1),
                { ...last, content, citations: nextCitations },
              ];
            }
            return prev;
          });

          if (nextCitations.length === 0) {
            clearCitationHighlight?.();
          } else {
            didAutoJumpRef.current = true;
            const firstCitation = nextCitations[0];
            const firstPage = Number(firstCitation?.page_number);
            if (Number.isFinite(firstPage) && firstPage >= 1) {
              if (revealCitationPage) revealCitationPage(firstPage, firstCitation?.bbox ?? null);
              else setPageNumber?.(firstPage);
            }
          }
        },
        onDone(payload) {
          setMessages((prev) => {
            const last = prev[prev.length - 1];
            if (last && last.role === 'assistant' && last._streaming) {
              return [
                ...prev.slice(0, -1),
                {
                  ...last,
                  answerId: payload.answer_id ?? null,
                  citations: payload.citations || last.citations || [],
                  _streaming: false,
                },
              ];
            }
            return prev;
          });
          onSessionEnsured({ id: sid });
        },
        onError(payload) {
          clearCitationHighlight?.();
          setError(payload.message || 'Đã có lỗi xảy ra.');
          setMessages((prev) => {
            const last = prev[prev.length - 1];
            if (last && last.role === 'assistant' && last._streaming) {
              return prev.slice(0, -1);
            }
            return prev;
          });
        },
      });
    } catch (err) {
      clearCitationHighlight?.();
      setError(err.message || errorMessage(err));
      setMessages((prev) => {
        const last = prev[prev.length - 1];
        if (last && last.role === 'assistant' && last._streaming) {
          return prev.slice(0, -1);
        }
        return prev;
      });
    } finally {
      setIsAsking(false);
      setStreamStatus(null);
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
                const isEditing = editingId === s.id;
                if (isEditing) {
                  return (
                    <li key={s.id} className="chat-history-item-editing-row">
                      <input
                        ref={editInputRef}
                        type="text"
                        className="chat-history-edit-input"
                        value={editTitle}
                        maxLength={200}
                        disabled={renameBusy}
                        onChange={(e) => setEditTitle(e.target.value)}
                        onKeyDown={(e) => {
                          if (e.key === 'Enter') {
                            e.preventDefault();
                            submitRename(s);
                          } else if (e.key === 'Escape') {
                            e.preventDefault();
                            setEditingId(null);
                          }
                        }}
                        onBlur={() => submitRename(s)}
                        onClick={(e) => e.stopPropagation()}
                      />
                    </li>
                  );
                }
                return (
                  <li key={s.id}>
                    <button
                      type="button"
                      className={`chat-history-item ${active ? 'active' : ''}`}
                      onClick={() => {
                        onSelectSession?.(s.id);
                        setHistoryOpen(false);
                      }}
                      onDoubleClick={(e) => {
                        e.preventDefault();
                        startEditing(s, e);
                      }}
                    >
                      <span className="chat-history-item-title">{s.title || 'New chat'}</span>
                      <span className="chat-history-item-time">{formatSessionTime(s.updated_at)}</span>
                    </button>
                    <button
                      type="button"
                      className="chat-history-item-action chat-history-item-rename"
                      title="Đổi tên"
                      onClick={(e) => startEditing(s, e)}
                    >
                      <Pencil size={12} />
                    </button>
                    <button
                      type="button"
                      className="chat-history-item-action chat-history-item-delete"
                      title="Xoá"
                      onClick={(e) => {
                        e.stopPropagation();
                        onDeleteSession?.(s.id);
                      }}
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
            <div className="ai-bubble-container" key={m.answerId || (m._streaming ? 'streaming-msg' : `a-${i}`)}>
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
                        onClick={() => (revealCitationPage ? revealCitationPage(c.page_number, c.bbox ?? null) : setPageNumber?.(c.page_number))}
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

        {isAsking && streamStatus && (
          <div className="ai-bubble-container">
            <div className="ai-book-avatar">
              <BookOpen size={14} color="#92400E" />
            </div>
            <div className="ai-card-content ai-card-loading">{streamStatus}</div>
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
