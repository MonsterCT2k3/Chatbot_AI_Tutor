import { useCallback, useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import WorkspaceSidebar from '../components/workspace/WorkspaceSidebar';
import SlideViewer from '../components/workspace/SlideViewer';
import ChatPanel from '../components/workspace/ChatPanel';
import { getDocument, getDocumentFileUrl, listDocuments } from '../services/documentService';
import './LessonWorkspacePage.css';

// Dựng từ fe/src/mock_html_ui/detail_screen_lesson/detail_screen_lesson.html.
// Container chịu trách nhiệm fetch dữ liệu thật (danh sách tài liệu, metadata,
// URL PDF) và giữ state dùng chung giữa 2 panel (pageNumber — để trích dẫn
// trong chat có thể nhảy tới đúng trang PDF đang xem).
export default function LessonWorkspacePage() {
  const { documentId } = useParams();
  const navigate = useNavigate();

  const [documents, setDocuments] = useState([]);
  const [currentDoc, setCurrentDoc] = useState(null);
  const [fileUrl, setFileUrl] = useState(null);
  const [pageNumber, setPageNumber] = useState(1);
  const [numPages, setNumPages] = useState(null);
  const [error, setError] = useState(null);
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);

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
    setNumPages(null);
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
        />
      )}

      <ChatPanel documentId={documentId} pageNumber={pageNumber} setPageNumber={setPageNumber} />
    </div>
  );
}
