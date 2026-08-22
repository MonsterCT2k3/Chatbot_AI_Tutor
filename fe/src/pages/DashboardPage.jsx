import { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Bell, PenLine, Search } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { listDocuments, uploadDocument } from '../services/documentService';
import DocumentCard from '../components/dashboard/DocumentCard';
import UploadDropzone from '../components/dashboard/UploadDropzone';
import './DashboardPage.css';

// Dựng lại từ fe/src/mock_html_ui/mainscreen/mainscreen.html — xem đầu
// DashboardPage.css để biết chi tiết những gì đã BỎ/ĐỔI so với mockup gốc
// (mockup có nhiều số liệu/tính năng KHÔNG có dữ liệu thật đứng sau).
//
// Trạng thái tài liệu (pending/parsing/embedding) tự đổi thành 'ready' phía
// server SAU KHI ingest xong — không có cách nào server chủ động báo cho
// client (chưa có WebSocket/SSE, xem Phase 7 streaming). Poll lại danh sách
// mỗi 3s CHỈ KHI có tài liệu nào đó chưa xong, dừng poll khi tất cả đã
// ready/failed — tránh gọi API vô ích khi không có gì đang chờ.
const NON_TERMINAL_STATUSES = new Set(['pending', 'parsing', 'embedding']);
const POLL_INTERVAL_MS = 3000;

export default function DashboardPage() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const [documents, setDocuments] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');

  async function refreshDocuments() {
    try {
      const data = await listDocuments();
      setDocuments(data);
      setError(null);
    } catch {
      setError('Không tải được danh sách tài liệu. Vui lòng thử lại.');
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    refreshDocuments();
  }, []);

  useEffect(() => {
    const hasPending = documents.some((d) => NON_TERMINAL_STATUSES.has(d.status));
    if (!hasPending) return;
    const timer = setInterval(refreshDocuments, POLL_INTERVAL_MS);
    return () => clearInterval(timer);
  }, [documents]);

  async function handleUpload(file) {
    try {
      await uploadDocument(file);
      await refreshDocuments();
    } catch (err) {
      // err.response.data.message (envelope lỗi riêng của backend, xem
      // apiClient.js) — KHÔNG phải .detail.message.
      const message = err.response?.data?.message;
      setError(message || 'Tải tài liệu lên thất bại. Kiểm tra định dạng file (chỉ PDF/PPTX) và dung lượng (tối đa 50MB).');
    }
  }

  function handleOpenDocument(doc) {
    navigate(`/documents/${doc.id}`);
  }

  const filteredDocuments = useMemo(() => {
    const q = searchQuery.trim().toLowerCase();
    if (!q) return documents;
    return documents.filter((d) => d.filename.toLowerCase().includes(q));
  }, [documents, searchQuery]);

  const totalPages = useMemo(
    () => documents.reduce((sum, d) => sum + (d.status === 'ready' ? d.page_count || 0 : 0), 0),
    [documents],
  );

  const displayName = user?.name || user?.email?.split('@')[0] || '';

  return (
    <div className="dashboard-body">
      <div className="dashboard-page">
        <header className="navbar">
          <a href="/" className="logo-link">
            <PenLine size={26} strokeWidth={1.8} />
            <span>AI Tutor K3</span>
          </a>

          <div className="search-wrap">
            <Search size={15} />
            <input
              type="text"
              placeholder="Tìm tài liệu theo tên..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>

          <div className="nav-right">
            <button className="icon-btn" title="Thông báo (chưa có tính năng này)" disabled>
              <Bell size={20} />
            </button>
            <button className="user-block" onClick={logout} title="Đăng xuất">
              <span className="avatar-fallback">{displayName ? displayName[0].toUpperCase() : '?'}</span>
              <div>
                <div className="uname">{displayName || 'Tài khoản'}</div>
                <div className="urole">Đăng xuất</div>
              </div>
            </button>
          </div>
        </header>

        <hr className="nav-divider" />

        <section className="hero-row">
          <div className="hero-left">
            <h1>Chào mừng trở lại{displayName ? `, ${displayName}` : ''}.</h1>
            <p>Bạn có {documents.length} tài liệu, sẵn sàng để học cùng AI.</p>
            <div className="stats-row">
              <span className="stat-chip">{documents.length} tài liệu</span>
              {totalPages > 0 && <span className="stat-chip">{totalPages} trang đã index</span>}
            </div>
          </div>
        </section>

        {error && <div className="error-banner" style={{ maxWidth: 480 }}>{error}</div>}

        <main className="cards-grid">
          {isLoading ? (
            <div className="empty-state">Đang tải danh sách tài liệu...</div>
          ) : (
            <>
              {filteredDocuments.map((doc) => (
                <DocumentCard key={doc.id} document={doc} onOpen={handleOpenDocument} />
              ))}
              {documents.length === 0 && !isLoading && (
                <div className="empty-state">Chưa có tài liệu nào — tải lên tài liệu đầu tiên để bắt đầu.</div>
              )}
              <UploadDropzone onUpload={handleUpload} />
            </>
          )}
        </main>
      </div>
    </div>
  );
}
