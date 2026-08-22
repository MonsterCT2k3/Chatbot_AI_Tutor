import { useEffect, useState } from 'react';
import { Document, Page } from 'react-pdf';
import { FileText, Presentation, Loader2, CheckCircle2, XCircle } from 'lucide-react';
import { getDocumentFileUrl } from '../../services/documentService';
import '../../lib/pdfjsSetup';

// status thật từ be/app/models/document.py: pending/parsing/embedding/ready/failed.
// 3 trạng thái đầu đều là "đang xử lý" với người dùng — không cần phân biệt
// UI riêng cho từng bước pipeline nội bộ.
const STATUS_META = {
  pending: { label: 'Đang xử lý', className: 'processing', icon: Loader2, spin: true },
  parsing: { label: 'Đang xử lý', className: 'processing', icon: Loader2, spin: true },
  embedding: { label: 'Đang xử lý', className: 'processing', icon: Loader2, spin: true },
  ready: { label: 'Sẵn sàng', className: 'ready', icon: CheckCircle2, spin: false },
  failed: { label: 'Lỗi xử lý', className: 'failed', icon: XCircle, spin: false },
};

function formatFileSize(bytes) {
  if (!bytes) return '';
  const mb = bytes / (1024 * 1024);
  return mb >= 1 ? `${mb.toFixed(1)} MB` : `${(bytes / 1024).toFixed(0)} KB`;
}

export default function DocumentCard({ document, onOpen }) {
  const meta = STATUS_META[document.status] ?? STATUS_META.pending;
  const StatusIcon = meta.icon;
  const isReady = document.status === 'ready';
  const TypeIcon = document.file_type === 'pptx' ? Presentation : FileText;

  // Ảnh bìa = trang 1 của bản PDF thật (kể cả tài liệu gốc là .pptx, backend
  // luôn có bản PDF xem được — GET /documents/{id}/file, xem
  // get_viewable_pdf_key trong be/app/routers/documents.py). Chỉ fetch presigned
  // URL này SAU KHI status='ready', vì endpoint trả 409 nếu chưa ingest xong.
  const [fileUrl, setFileUrl] = useState(null);
  const [thumbFailed, setThumbFailed] = useState(false);

  useEffect(() => {
    if (!isReady) return undefined;
    let cancelled = false;
    getDocumentFileUrl(document.id)
      .then((url) => { if (!cancelled) setFileUrl(url); })
      .catch(() => { if (!cancelled) setThumbFailed(true); });
    return () => { cancelled = true; };
  }, [isReady, document.id]);

  const showThumbnail = isReady && fileUrl && !thumbFailed;

  return (
    <button
      type="button"
      className="doc-card"
      onClick={() => onOpen(document)}
      disabled={!isReady}
      title={isReady ? 'Mở tài liệu' : meta.label}
    >
      <div className="preview-box">
        {showThumbnail ? (
          <Document
            file={fileUrl}
            loading={<TypeIcon size={40} strokeWidth={1.3} />}
            error={<TypeIcon size={40} strokeWidth={1.3} />}
            onLoadError={() => setThumbFailed(true)}
          >
            <Page pageNumber={1} height={110} renderTextLayer={false} renderAnnotationLayer={false} />
          </Document>
        ) : (
          <TypeIcon size={40} strokeWidth={1.3} />
        )}
      </div>

      <div className="doc-title">{document.filename}</div>
      <div className="doc-meta">
        {document.file_type?.toUpperCase()}
        {document.page_count ? ` • ${document.page_count} trang` : ''}
        {document.file_size_bytes ? ` • ${formatFileSize(document.file_size_bytes)}` : ''}
      </div>

      <span className={`status-badge ${meta.className}`}>
        <StatusIcon size={12} className={meta.spin ? 'spin-icon' : ''} />
        {meta.label}
      </span>

      {document.status === 'failed' && document.error_message && (
        <div className="doc-meta" style={{ color: '#B91C1C', marginBottom: 8, marginTop: -6 }}>
          {document.error_message}
        </div>
      )}

      <div className="doc-card-footer">{isReady ? 'Mở tài liệu →' : 'Vui lòng đợi...'}</div>
    </button>
  );
}
