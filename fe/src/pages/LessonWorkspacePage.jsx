import { useCallback, useEffect, useState } from 'react';
import { useNavigate, useParams, useSearchParams } from 'react-router-dom';
import WorkspaceSidebar from '../components/workspace/WorkspaceSidebar';
import SlideViewer from '../components/workspace/SlideViewer';
import ChatPanel from '../components/workspace/ChatPanel';
import { getDocument, getDocumentFileUrl, listDocuments } from '../services/documentService';
import { deleteSession, listSessions, renameSession } from '../services/sessionService';
import './LessonWorkspacePage.css';

// Dựng từ fe/src/mock_html_ui/detail_screen_lesson/detail_screen_lesson.html.
// Container chịu trách nhiệm fetch dữ liệu thật (danh sách tài liệu, metadata,
// URL PDF) và giữ state dùng chung giữa 2 panel (pageNumber — để trích dẫn
// trong chat có thể nhảy tới đúng trang PDF đang xem).
export default function LessonWorkspacePage() {
  const { documentId } = useParams();
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();
  const sessionId = searchParams.get('session');

  const [documents, setDocuments] = useState([]);
  const [currentDoc, setCurrentDoc] = useState(null);
  const [fileUrl, setFileUrl] = useState(null);
  const [pageNumber, setPageNumber] = useState(1);
  const [numPages, setNumPages] = useState(null);
  const [highlightedPage, setHighlightedPage] = useState(null);
  const [highlightedBbox, setHighlightedBbox] = useState(null);
  const [error, setError] = useState(null);
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const [sessions, setSessions] = useState([]);

  function revealCitationPage(page, bbox = null) {
    const n = Number(page);
    if (!Number.isFinite(n) || n < 1) return;
    const clamped = numPages ? Math.min(numPages, Math.max(1, n)) : n;
    setPageNumber(clamped);
    setHighlightedPage(clamped);
    setHighlightedBbox(bbox && Array.isArray(bbox.rects) && bbox.rects.length > 0 ? bbox : null);
  }

  function clearCitationHighlight() {
    setHighlightedPage(null);
    setHighlightedBbox(null);
  }

  function setSessionParam(id) {
    const next = new URLSearchParams(searchParams);
    if (id) next.set('session', id);
    else next.delete('session');
    setSearchParams(next, { replace: true });
  }

  const refreshDocuments = useCallback(() => {
    listDocuments().then(setDocuments).catch(() => {});
  }, []);

  useEffect(() => {
    refreshDocuments();
  }, [refreshDocuments]);

  useEffect(() => {
    setCurrentDoc(null);
    setFileUrl(null);
    setPageNumber(1);
    setHighlightedPage(null);
    setHighlightedBbox(null);
    setError(null);

    getDocument(documentId)
      .then((doc) => {
        setCurrentDoc(doc);
        if (doc.status !== 'ready') return;
        return getDocumentFileUrl(documentId).then(setFileUrl);
      })
      .catch((err) => {
        setError(err.response?.status === 404 ? 'Tài liệu không tồn tại hoặc bạn không có quyền xem.' : 'Không tải được tài liệu.');
      });
  }, [documentId]);

  useEffect(() => {
    setHighlightedPage(null);
    setHighlightedBbox(null);
  }, [sessionId]);

  useEffect(() => {
    let cancelled = false;
    listSessions(documentId)
      .then((list) => {
        if (cancelled) return;
        setSessions(list);
        const q = searchParams.get('session');
        if (q && list.some((s) => s.id === q)) return;
        if (list[0]) setSessionParam(list[0].id);
        else setSessionParam(null);
      })
      .catch(() => {
        if (!cancelled) setSessions([]);
      });
    return () => {
      cancelled = true;
    };
    // Chỉ re-run khi đổi tài liệu — không phụ thuộc searchParams kẻo loop.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [documentId]);

  function handleDocumentUploaded(newDoc) {
    setDocuments((prev) => [newDoc, ...prev]);
  }

  if (error) {
    return (
      <div className="workspace-status-page">
        <p>{error}</p>
        <button type="button" onClick={() => navigate('/')}>← Về trang chủ</button>
      </div>
    );
  }

  if (!currentDoc) {
    return <div className="workspace-status-page">Đang tải...</div>;
  }

  if (currentDoc.status !== 'ready') {
    return (
      <div className="workspace-status-page">
        <p>Tài liệu "{currentDoc.filename}" đang được xử lý ({currentDoc.status}), chưa thể mở.</p>
        <button type="button" onClick={() => navigate('/')}>← Về trang chủ</button>
      </div>
    );
  }

  return (
    <div className={`workspace-grid ${isSidebarCollapsed ? 'sidebar-collapsed' : ''}`}>
      <WorkspaceSidebar
        documents={documents}
        currentDocumentId={documentId}
        onDocumentUploaded={handleDocumentUploaded}
        collapsed={isSidebarCollapsed}
        onToggleCollapse={() => setIsSidebarCollapsed((v) => !v)}
      />

      {fileUrl && (
        <SlideViewer
          filename={currentDoc.filename}
          fileUrl={fileUrl}
          pageNumber={pageNumber}
          setPageNumber={setPageNumber}
          numPages={numPages}
          setNumPages={setNumPages}
          highlightedPage={highlightedPage}
          highlightedBbox={highlightedBbox}
        />
      )}

      <ChatPanel
        documentId={documentId}
        sessionId={sessionId}
        sessions={sessions}
        setPageNumber={setPageNumber}
        revealCitationPage={revealCitationPage}
        clearCitationHighlight={clearCitationHighlight}
        onSelectSession={setSessionParam}
        onNewSession={() => setSessionParam(null)}
        onRenameSession={async (id, title) => {
          const updated = await renameSession(id, title);
          setSessions((prev) => prev.map((s) => (s.id === id ? { ...s, ...updated } : s)));
          return updated;
        }}
        onDeleteSession={async (id) => {
          try {
            await deleteSession(id);
            const list = (await listSessions(documentId)) || [];
            setSessions(list);
            if (id === sessionId) setSessionParam(list[0]?.id || null);
          } catch {
            /* xoá fail: giữ nguyên danh sách */
          }
        }}
        onSessionEnsured={(session) => {
          setSessionParam(session.id);
          listSessions(documentId).then(setSessions).catch(() => {});
        }}
      />
    </div>
  );
}
