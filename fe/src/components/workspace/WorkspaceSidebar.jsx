import { useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ChevronsLeft, ChevronsRight, FileText, Loader2, Plus, Presentation } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { uploadDocument } from '../../services/documentService';

function formatBytes(bytes) {
  const gb = bytes / (1024 * 1024 * 1024);
  return gb >= 0.1 ? `${gb.toFixed(1)} GB` : `${(bytes / (1024 * 1024)).toFixed(0)} MB`;
}

// Tổng dung lượng tính từ danh sách tài liệu hiện có (sum file_size_bytes).
// Mốc 10 GB (UI_STORAGE_CAP_BYTES) chỉ là mốc tham chiếu trực quan cho thanh
// progress bar của UI, backend không giới hạn tổng quota tài khoản (chỉ giới
// hạn MAX_FILE_SIZE_BYTES cho từng file khi upload).
const UI_STORAGE_CAP_BYTES = 10 * 1024 * 1024 * 1024;

export default function WorkspaceSidebar({
  documents,
  currentDocumentId,
  onDocumentUploaded,
  collapsed,
  onToggleCollapse,
}) {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const fileInputRef = useRef(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadError, setUploadError] = useState(null);

  const displayName = user?.name || user?.email?.split('@')[0] || '';
  const usedBytes = documents.reduce((sum, d) => sum + (d.file_size_bytes || 0), 0);
  const usedPct = Math.min(100, Math.round((usedBytes / UI_STORAGE_CAP_BYTES) * 100));

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

      <div className="sidebar-footer">
        {!collapsed && (
          <div
            className="storage-meter"
            title={`Tổng dung lượng tài liệu: ${formatBytes(usedBytes)}. Mốc 10 GB là mốc tham chiếu giao diện, hệ thống chưa giới hạn tổng dung lượng tài khoản.`}
          >
            <div className="storage-text-title">Đã dùng: {formatBytes(usedBytes)}</div>
            <div className="storage-text-sub">Mốc tham chiếu 10 GB (chưa giới hạn tài khoản)</div>
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
