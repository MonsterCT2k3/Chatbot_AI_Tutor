import { useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ChevronsLeft, ChevronsRight, FileText, Loader2, Plus, Presentation } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { uploadDocument } from '../../services/documentService';

// Dựng từ fe/src/mock_html_ui/detail_screen_lesson/detail_screen_lesson.html
// panel-left. "Study Discussions" (session/thread) cần Phase 6 (chưa build) —
// giữ nguyên UI mockup nhưng để MOCK tĩnh, không gắn API/onClick thật (khác
// với phần Course Library/Storage/User bên dưới, toàn bộ đều là dữ liệu thật).
const MOCK_DISCUSSIONS = [
  { title: '1. Trao đổi về nội dung Slide 14', active: true },
  { title: '2. Câu hỏi ôn tập chương này' },
];

function formatBytes(bytes) {
  const gb = bytes / (1024 * 1024 * 1024);
  return gb >= 0.1 ? `${gb.toFixed(1)} GB` : `${(bytes / (1024 * 1024)).toFixed(0)} MB`;
}

// Không có khái niệm quota dung lượng thật ở backend (MAX_FILE_SIZE_BYTES chỉ
// giới hạn 1 file/lần upload, không phải tổng dung lượng tài khoản) — hiển thị
// TỔNG DUNG LƯỢNG THẬT (cộng từ chính danh sách documents) so với 1 mốc quota
// MOCK cố định, chỉ để có thanh progress trực quan như mockup, không phải số
// giả hoàn toàn.
const MOCK_QUOTA_BYTES = 10 * 1024 * 1024 * 1024;

export default function WorkspaceSidebar({ documents, currentDocumentId, onDocumentUploaded, collapsed, onToggleCollapse }) {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const fileInputRef = useRef(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadError, setUploadError] = useState(null);

  const displayName = user?.name || user?.email?.split('@')[0] || '';
  const usedBytes = documents.reduce((sum, d) => sum + (d.file_size_bytes || 0), 0);
  const usedPct = Math.min(100, Math.round((usedBytes / MOCK_QUOTA_BYTES) * 100));

  async function handleFileChange(e) {
    const file = e.target.files?.[0];
    e.target.value = '';
    if (!file) return;
    setUploadError(null);
    setIsUploading(true);
    try {
      const doc = await uploadDocument(file);
      onDocumentUploaded(doc);
    } catch (err) {
      setUploadError(err.response?.data?.message || 'Tải tài liệu lên thất bại.');
    } finally {
      setIsUploading(false);
    }
  }

  return (
    <aside className={`panel-left ${collapsed ? 'collapsed' : ''}`}>
      <div className="sidebar-top-row">
        <a href="/" className="brand-header" title="AI Tutor K3">
          <FileText size={26} strokeWidth={1.8} />
          {!collapsed && <span className="brand-title-text">AI Tutor K3</span>}
        </a>
        <button
          type="button"
          className="sidebar-collapse-btn"
          onClick={onToggleCollapse}
          title={collapsed ? 'Mở rộng thanh bên' : 'Thu gọn thanh bên'}
        >
          {collapsed ? <ChevronsRight size={15} /> : <ChevronsLeft size={15} />}
        </button>
      </div>

      {!collapsed && (
        <div className="kb-pill-badge">
          <span className="kb-dot-green" />
          <span>Knowledge Base: Active (pgvector)</span>
        </div>
      )}

      <input
        ref={fileInputRef}
        type="file"
        accept=".pdf,.pptx"
        hidden
        onChange={handleFileChange}
      />
      <button
        type="button"
        className="upload-box-btn"
        onClick={() => fileInputRef.current?.click()}
        disabled={isUploading}
        title="Tải bài giảng lên (PDF / PPTX)"
      >
        {isUploading ? <Loader2 size={14} className="spin-icon" /> : <Plus size={14} />}
        {!collapsed && <span>{isUploading ? 'Đang tải lên...' : 'Tải bài giảng lên (PDF / PPTX)'}</span>}
      </button>
      {!collapsed && uploadError && <div className="sidebar-upload-error">{uploadError}</div>}

      <div className="sidebar-library">
        {!collapsed && <h3 className="sidebar-section-title">Thư viện tài liệu</h3>}
        <div className="sidebar-list">
          {documents.map((doc) => {
            const Icon = doc.file_type === 'pptx' ? Presentation : FileText;
            const isReady = doc.status === 'ready';
            return (
              <a
                key={doc.id}
                href={`/documents/${doc.id}`}
                className={`sidebar-doc-item ${doc.id === currentDocumentId ? 'active' : ''} ${!isReady ? 'disabled' : ''}`}
                title={isReady ? doc.filename : 'Đang xử lý...'}
                onClick={(e) => {
                  e.preventDefault();
                  if (isReady) navigate(`/documents/${doc.id}`);
                }}
              >
                <Icon size={16} className="doc-icon-svg" />
                {!collapsed && <span>{doc.filename}</span>}
              </a>
            );
          })}
        </div>
      </div>

      {!collapsed && (
        <div>
          <h3 className="sidebar-section-title">Thảo luận học tập</h3>
          <div className="sidebar-list">
            {MOCK_DISCUSSIONS.map((d) => (
              <div key={d.title} className="sidebar-discuss-item">
                <span>{d.title}</span>
                {d.active && <span className="active-green-pill">Đang mở</span>}
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="sidebar-footer">
        {!collapsed && (
          <div>
            <div className="storage-text-title">Dung lượng: {formatBytes(usedBytes)} / 10 GB</div>
            <div className="storage-track-bar">
              <div className="storage-fill-bar" style={{ width: `${usedPct}%` }} />
            </div>
          </div>
        )}

        <button type="button" className="user-footer-card" onClick={logout} title="Đăng xuất">
          <span className="avatar-round-img avatar-fallback">{displayName ? displayName[0].toUpperCase() : '?'}</span>
          {!collapsed && (
            <div className="user-text-col">
              <span className="user-primary-name">{displayName || 'Tài khoản'}</span>
              <span className="user-secondary-role">Đăng xuất</span>
            </div>
          )}
        </button>
      </div>
    </aside>
  );
}
