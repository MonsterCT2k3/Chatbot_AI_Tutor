import { useEffect, useMemo, useRef, useState } from 'react';
import { Document, Page } from 'react-pdf';
import { ChevronLeft, ChevronRight, LayoutGrid, Search } from 'lucide-react';
import 'react-pdf/dist/Page/AnnotationLayer.css';
import 'react-pdf/dist/Page/TextLayer.css';
import '../../lib/pdfjsSetup';

// Khớp .slide-canvas-card { padding: 20px } trong LessonWorkspacePage.css —
// trừ ra để tính đúng phần diện tích THỰC hiển thị được, không tính cả padding.
const CANVAS_PADDING = 40;
const MIN_ZOOM = 0.5;
const MAX_ZOOM = 3;
const FILMSTRIP_RADIUS = 2; // hiện current page ± 2, giống mockup (5 thumbnail)

// Dựng từ panel-center trong detail_screen_lesson.html. Toàn bộ nội dung
// "slide" (sơ đồ neural network, công thức highlight vàng, tooltip pin...)
// trong mockup là ví dụ minh hoạ cố định cho 1 slide cụ thể — được THAY THẾ
// HOÀN TOÀN bằng nội dung PDF thật (react-pdf), không phải mock lại chúng,
// vì đã có nội dung thật để hiển thị. Filmstrip cũng render trang thật (react-pdf
// scale nhỏ) thay vì icon giả, chỉ giới hạn quanh trang hiện tại để không phải
// render hết toàn bộ tài liệu.
export default function SlideViewer({ filename, fileUrl, pageNumber, setPageNumber, numPages, setNumPages }) {
  // zoom = hệ số NHÂN THÊM lên trên mức "vừa khung" (fit) — zoom=1 nghĩa là
  // trang vừa khít khung, không cần cuộn; >1 mới thật sự tràn ra và cần cuộn.
  // Khác với cách cũ (dùng `scale` cố định theo kích thước gốc PDF, không
  // biết khung to nhỏ ra sao) nên hầu như luôn tràn ra 2 chiều, phải cuộn kể
  // cả khi không zoom gì cả.
  const [zoom, setZoom] = useState(1);
  const [containerSize, setContainerSize] = useState({ width: 0, height: 0 });
  const [pageAspect, setPageAspect] = useState(16 / 9); // fallback trước khi biết kích thước trang thật
  const canvasRef = useRef(null);

  useEffect(() => {
    const el = canvasRef.current;
    if (!el) return undefined;
    const observer = new ResizeObserver(([entry]) => {
      setContainerSize({ width: entry.contentRect.width, height: entry.contentRect.height });
    });
    observer.observe(el);
    return () => observer.disconnect();
  }, []);

  const fitWidth = useMemo(() => {
    const availW = Math.max(0, containerSize.width - CANVAS_PADDING);
    const availH = Math.max(0, containerSize.height - CANVAS_PADDING);
    if (!availW || !availH) return 0;
    // "contain": khớp theo chiều nào bị giới hạn trước (giống object-fit: contain).
    return Math.min(availW, availH * pageAspect);
  }, [containerSize, pageAspect]);

  const displayWidth = fitWidth * zoom;

  const filmstripPages = useMemo(() => {
    if (!numPages) return [];
    const start = Math.max(1, pageNumber - FILMSTRIP_RADIUS);
    const end = Math.min(numPages, pageNumber + FILMSTRIP_RADIUS);
    return Array.from({ length: end - start + 1 }, (_, i) => start + i);
  }, [pageNumber, numPages]);

  function goToPage(n) {
    setPageNumber(Math.min(Math.max(1, n), numPages || 1));
  }

  // Phím ← → chuyển trang — BỎ QUA khi đang gõ trong input/textarea (ô chat)
  // để không cướp mất phím mũi tên dùng để di chuyển con trỏ khi gõ.
  useEffect(() => {
    function handleKeyDown(e) {
      const tag = document.activeElement?.tagName;
      if (tag === 'INPUT' || tag === 'TEXTAREA' || document.activeElement?.isContentEditable) return;
      if (e.key === 'ArrowLeft') goToPage(pageNumber - 1);
      else if (e.key === 'ArrowRight') goToPage(pageNumber + 1);
    }
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [pageNumber, numPages]);

  return (
    <main className="panel-center">
      <div className="viewer-top-row">
        <span className="lecture-main-title">{filename}</span>

        <div className="viewer-tools-group">
          <span className="slide-count-text">Trang {pageNumber} / {numPages || '…'}</span>

          <div className="stepper-zoom-box">
            <button type="button" className="stepper-btn" title="Thu nhỏ" onClick={() => setZoom((z) => Math.max(MIN_ZOOM, +(z - 0.15).toFixed(2)))}>−</button>
            <span className="stepper-vertical-line" />
            <button type="button" className="stepper-btn" title="Phóng to" onClick={() => setZoom((z) => Math.min(MAX_ZOOM, +(z + 0.15).toFixed(2)))}>+</button>
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
        {/* zoom > 1: bỏ canh giữa flex khi tràn khung — flex center + overflow
            scroll có 1 lỗi CSS quen thuộc là phần bị đẩy ra ngoài ở góc
            trên-trái không cuộn tới được, chỉ đúng khi nội dung vừa/nhỏ hơn
            khung (trường hợp mặc định zoom=1 ở đây). */}
        <div className={`slide-canvas-card ${zoom > 1 ? 'zoomed' : ''}`} ref={canvasRef}>
          {displayWidth > 0 && (
            <Page
              pageNumber={pageNumber}
              width={displayWidth}
              onLoadSuccess={(page) => setPageAspect(page.width / page.height)}
            />
          )}

          {pageNumber > 1 && (
            <button type="button" className="edge-nav-btn edge-nav-left" title="Trang trước" onClick={() => goToPage(pageNumber - 1)}>
              <ChevronLeft size={22} />
            </button>
          )}
          {numPages && pageNumber < numPages && (
            <button type="button" className="edge-nav-btn edge-nav-right" title="Trang sau" onClick={() => goToPage(pageNumber + 1)}>
              <ChevronRight size={22} />
            </button>
          )}
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
