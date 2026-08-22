import { useMemo, useState } from 'react';
import { Document, Page } from 'react-pdf';
import { ChevronLeft, ChevronRight, LayoutGrid, Search } from 'lucide-react';
import 'react-pdf/dist/Page/AnnotationLayer.css';
import 'react-pdf/dist/Page/TextLayer.css';
import '../../lib/pdfjsSetup';

const MIN_SCALE = 0.6;
const MAX_SCALE = 2.2;
const FILMSTRIP_RADIUS = 2; // hiện current page ± 2, giống mockup (5 thumbnail)

// Dựng từ panel-center trong detail_screen_lesson.html. Toàn bộ nội dung
// "slide" (sơ đồ neural network, công thức highlight vàng, tooltip pin...)
// trong mockup là ví dụ minh hoạ cố định cho 1 slide cụ thể — được THAY THẾ
// HOÀN TOÀN bằng nội dung PDF thật (react-pdf), không phải mock lại chúng,
// vì đã có nội dung thật để hiển thị. Filmstrip cũng render trang thật (react-pdf
// scale nhỏ) thay vì icon giả, chỉ giới hạn quanh trang hiện tại để không phải
// render hết toàn bộ tài liệu.
export default function SlideViewer({ filename, fileUrl, pageNumber, setPageNumber, numPages, setNumPages }) {
  const [scale, setScale] = useState(1);

  const filmstripPages = useMemo(() => {
    if (!numPages) return [];
    const start = Math.max(1, pageNumber - FILMSTRIP_RADIUS);
    const end = Math.min(numPages, pageNumber + FILMSTRIP_RADIUS);
    return Array.from({ length: end - start + 1 }, (_, i) => start + i);
  }, [pageNumber, numPages]);

  function goToPage(n) {
    setPageNumber(Math.min(Math.max(1, n), numPages || 1));
  }

  return (
    <main className="panel-center">
      <div className="viewer-top-row">
        <span className="lecture-main-title">{filename}</span>

        <div className="viewer-tools-group">
          <span className="slide-count-text">Trang {pageNumber} / {numPages || '…'}</span>

          <div className="stepper-zoom-box">
            <button type="button" className="stepper-btn" title="Thu nhỏ" onClick={() => setScale((s) => Math.max(MIN_SCALE, s - 0.15))}>−</button>
            <span className="stepper-vertical-line" />
            <button type="button" className="stepper-btn" title="Phóng to" onClick={() => setScale((s) => Math.min(MAX_SCALE, s + 0.15))}>+</button>
          </div>

          {/* Chưa có API "layout trình chiếu" / "tìm trong tài liệu" ở backend
              — disabled thay vì giả vờ hoạt động, cùng pattern với nút Google/SSO
              ở SignInPage. */}
          <button type="button" className="icon-box-btn" title="Chưa hỗ trợ" disabled>
            <LayoutGrid size={14} />
          </button>
          <button type="button" className="icon-box-btn" title="Chưa hỗ trợ" disabled>
            <Search size={14} />
          </button>
        </div>
      </div>

      {/* 1 <Document> DUY NHẤT bọc cả slide chính lẫn filmstrip — Page đọc
          PDF đã tải qua React Context (useDocumentContext), không phải con
          trực tiếp của Document, nên chỉ cần tải/parse file 1 lần dù render
          nhiều <Page> ở nhiều chỗ khác nhau trong cây, thay vì mỗi thumbnail
          tự mở lại cả file PDF. */}
      <Document
        file={fileUrl}
        className="slide-document-wrapper"
        loading={<div className="viewer-loading">Đang tải tài liệu...</div>}
        error={<div className="viewer-loading">Không tải được tài liệu.</div>}
        onLoadSuccess={({ numPages: n }) => setNumPages(n)}
      >
        <div className="slide-canvas-card">
          <Page pageNumber={pageNumber} scale={scale} />
        </div>

        <div className="thumbnails-footer-row">
          <button type="button" className="carousel-arrow-btn" title="Trang trước" onClick={() => goToPage(pageNumber - 1)} disabled={pageNumber <= 1}>
            <ChevronLeft size={16} />
          </button>

          <div className="mini-thumbs-container">
            {filmstripPages.map((n) => (
              <button
                key={n}
                type="button"
                className={`thumb-item-box ${n === pageNumber ? 'active' : ''}`}
                onClick={() => goToPage(n)}
              >
                <div className="thumb-mock-graphics">
                  <Page pageNumber={n} width={64} renderTextLayer={false} renderAnnotationLayer={false} />
                </div>
                <span className="thumb-title-label">Trang {n}</span>
              </button>
            ))}
          </div>

          <button type="button" className="carousel-arrow-btn" title="Trang sau" onClick={() => goToPage(pageNumber + 1)} disabled={!numPages || pageNumber >= numPages}>
            <ChevronRight size={16} />
          </button>
        </div>
      </Document>
    </main>
  );
}
