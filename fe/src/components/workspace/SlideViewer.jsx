import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Document, Page } from 'react-pdf';
import { ChevronLeft, ChevronRight, LayoutGrid, Search } from 'lucide-react';
import 'react-pdf/dist/Page/AnnotationLayer.css';
import 'react-pdf/dist/Page/TextLayer.css';
import '../../lib/pdfjsSetup';

// Các hằng số dưới đây lấy theo ĐÚNG viewer chính thức của pdf.js (Mozilla) —
// đọc trực tiếp trong node_modules/pdfjs-dist/web/pdf_viewer.mjs và
// mozilla/pdf.js web/app_options.js, không phải tự nghĩ ra:
//   DEFAULT_SCALE_DELTA = 1.1   -> bước zoom là NHÂN, không phải cộng
//   MIN_SCALE = 0.1, MAX_SCALE = 10
//   defaultZoomDelay = 400      -> trễ trước khi vẽ lại ở độ phân giải thật
//   maxCanvasPixels = 2**25     -> trần số pixel của canvas
// Ta dùng bước 1.25 (thay 1.1) cho đỡ phải bấm nhiều, và dải hẹp hơn 0.25–5
// cho hợp với màn học liệu.
const MIN_ZOOM = 0.25;
const MAX_ZOOM = 5;
const ZOOM_FACTOR = 1.25;
const ZOOM_REDRAW_DELAY_MS = 400;
const MAX_CANVAS_PIXELS = 2 ** 25;
const FILMSTRIP_RADIUS = 2; // hiện current page ± 2, giống mockup (5 thumbnail)
// Chừa vài px để phép "vừa khung" không bị lố 1-2px do làm tròn rồi sinh
// thanh cuộn thừa ngay ở mức zoom = 1 (mức lẽ ra phải vừa khít).
const FIT_SAFETY_PX = 4;

const clampZoom = (z) => Math.min(MAX_ZOOM, Math.max(MIN_ZOOM, Math.round(z * 100) / 100));

// Dựng từ panel-center trong detail_screen_lesson.html. Toàn bộ nội dung
// "slide" (sơ đồ neural network, công thức highlight vàng, tooltip pin...)
// trong mockup là ví dụ minh hoạ cố định cho 1 slide cụ thể — được THAY THẾ
// HOÀN TOÀN bằng nội dung PDF thật (react-pdf), không phải mock lại chúng.
//
// ─────────────────────────────────────────────────────────────────────────
// CƠ CHẾ ZOOM — làm theo đúng viewer của pdf.js (Mozilla), gồm 3 phần:
//
// (1) PHẢN HỒI TỨC THÌ BẰNG CSS TRANSFORM.
//     pdf.js: `this.cssTransform({...})` được gọi NGAY mỗi lần đổi scale, kể
//     cả trên nhánh sẽ vẽ lại. Canvas đang có được scale bằng CSS lập tức nên
//     người dùng thấy phản hồi ngay, không chờ vẽ, không nháy.
//
// (2) VẼ LẠI Ở ĐỘ PHÂN GIẢI THẬT, CÓ ĐỘ TRỄ.
//     pdf.js: `postponeDrawing = drawingDelay >= 0 && drawingDelay < 1000`,
//     mặc định `defaultZoomDelay = 400`ms. Trong lúc chờ thì HUỶ render đang
//     dở và chỉ CSS transform; hết 400ms yên tĩnh mới `refresh()` vẽ thật.
//     Nhờ vậy bấm zoom liên tục 10 lần chỉ tốn 1 lần vẽ, và ảnh cuối cùng
//     luôn nét đúng độ phân giải đang xem (không cần render dư thừa sẵn).
//
// (3) DOUBLE-BUFFER ĐỂ KHÔNG NHÁY LÚC TRÁO.
//     Đây là mấu chốt. pdf.js không vẽ đè lên canvas đang hiển thị:
//         let canvas = this.canvas = document.createElement("canvas");  // canvas MỚI
//         this.#showCanvas = isLastShow => {
//           if (!isLastShow) return;                 // chưa xong thì chưa tráo
//           prevCanvas.replaceWith(canvas);          // vẽ XONG mới tráo
//           prevCanvas.width = prevCanvas.height = 0;   // rồi mới giải phóng
//         }
//     Còn react-pdf thì TÁI DÙNG canvas cũ: gán canvas.width (xoá sạch pixel)
//     -> visibility='hidden' -> vẽ -> hiện lại, tức là nháy 1 cái mỗi lần vẽ.
//     Nên ở đây ta tự dựng double-buffer: giữ 2 "lớp" <Page> song song trong
//     CÙNG một mảng có key ổn định (để React không unmount/mount lại làm mất
//     canvas đã vẽ). Lớp mới vẽ ngầm ở visibility:hidden; chỉ khi
//     onRenderSuccess báo vẽ xong mới đổi lớp hiển thị rồi bỏ lớp cũ đi
//     (bỏ đi = giải phóng bộ nhớ canvas, giống bước prevCanvas.width = 0).
//
// Kết quả: không nháy, nét ở MỌI mức zoom, và ở trạng thái nghỉ chỉ tốn đúng
// 1 canvas đúng cỡ đang xem (bản trước đây phải render sẵn gấp đôi độ phân
// giải VĨNH VIỄN cho mọi người dùng chỉ để né cái nháy này).
// ─────────────────────────────────────────────────────────────────────────
//
// Ghi chú thêm về bố cục (giữ từ lần sửa trước, vẫn cần):
// - .slide-canvas-card (overflow:hidden) được ĐO, bọc ngoài .pdf-scroll-area
//   (overflow:auto) — tách phần tử đo khỏi phần tử cuộn để thanh cuộn không
//   tác động ngược vào số đo, đồng thời giữ 2 nút chuyển trang đứng yên khi
//   cuộn. pdf.js dùng cách khác (1 khung cuộn + trừ hằng số
//   SCROLLBAR_PADDING = 40) vì viewer của họ cuộn liên tục nhiều trang; ở đây
//   mỗi lần chỉ hiện 1 trang nên tách lớp gọn và chính xác hơn, không phải
//   hy sinh 40px.
// - Kích thước trang lấy từ pdf proxy (getViewport({scale:1})), không lấy từ
//   kết quả render, để không tạo phụ thuộc vòng.
export default function SlideViewer({
  filename,
  fileUrl,
  pageNumber,
  setPageNumber,
  numPages,
  setNumPages,
  highlightedPage = null,
}) {
  const [zoom, setZoom] = useState(1);          // mức người dùng thấy — đổi tức thì
  const [pdfProxy, setPdfProxy] = useState(null);
  const [pageSize, setPageSize] = useState(null); // kích thước THẬT của trang ở scale=1
  const [viewport, setViewport] = useState({ width: 0, height: 0 });
  const observerRef = useRef(null);

  // Đo khung NGOÀI (overflow:hidden) — kích thước của nó do grid/flex bên trên
  // quyết định, KHÔNG bao giờ bị nội dung PDF bên trong tác động ngược.
  //
  // Dùng CALLBACK REF chứ KHÔNG dùng useEffect(..., []) + useRef: khung này
  // nằm BÊN TRONG <Document>, mà <Document> lúc đầu chỉ render "Đang tải..."
  // và chỉ render children SAU KHI tải xong PDF. Vì vậy ở thời điểm effect
  // [] chạy (ngay khi SlideViewer mount), phần tử CHƯA TỒN TẠI -> ref là null
  // -> observer KHÔNG BAO GIỜ được gắn -> viewport mãi = 0 -> <Page> không
  // bao giờ render. Callback ref được React gọi ĐÚNG LÚC node xuất hiện.
  const measureRef = useCallback((node) => {
    observerRef.current?.disconnect();
    observerRef.current = null;
    if (!node) return;
    const observer = new ResizeObserver(([entry]) => {
      setViewport({ width: entry.contentRect.width, height: entry.contentRect.height });
    });
    observer.observe(node);
    observerRef.current = observer;
  }, []);

  useEffect(() => () => observerRef.current?.disconnect(), []);

  // Kích thước trang lấy thẳng từ pdf proxy — độc lập hoàn toàn với việc render.
  useEffect(() => {
    if (!pdfProxy) return undefined;
    let cancelled = false;
    pdfProxy.getPage(pageNumber).then((page) => {
      if (cancelled) return;
      const { width, height } = page.getViewport({ scale: 1 });
      setPageSize({ width, height });
    });
    return () => { cancelled = true; };
  }, [pdfProxy, pageNumber]);

  // Cỡ "vừa khung" (cả 2 chiều) ở zoom = 1.
  const fitWidth = useMemo(() => {
    if (!pageSize || !viewport.width || !viewport.height) return 0;
    const availW = viewport.width - FIT_SAFETY_PX;
    const availH = viewport.height - FIT_SAFETY_PX;
    return Math.min(availW, availH * (pageSize.width / pageSize.height));
  }, [pageSize, viewport]);

  // Cỡ NGƯỜI DÙNG THẤY — đổi tức thì theo zoom, quyết định layout & thanh cuộn.
  const displayWidth = fitWidth * zoom;
  const displayHeight = pageSize ? displayWidth * (pageSize.height / pageSize.width) : 0;

  // Cỡ MUỐN vẽ — đúng bằng cỡ đang hiển thị, chặn trần số pixel giống
  // maxCanvasPixels của pdf.js (react-pdf còn nhân thêm devicePixelRatio khi
  // tạo bitmap nên phải tính cả dpr vào trần).
  const desiredRenderWidth = useMemo(() => {
    if (!displayWidth || !pageSize) return 0;
    const aspect = pageSize.height / pageSize.width;
    const dpr = window.devicePixelRatio || 1;
    const maxWidth = Math.sqrt(MAX_CANVAS_PIXELS / (aspect * dpr * dpr));
    return Math.min(displayWidth, maxWidth);
  }, [displayWidth, pageSize]);

  // (2) Trễ trước khi vẽ lại. Debounce TOÀN BỘ mục tiêu render (chứ không chỉ
  // riêng `zoom`): đo thật cho thấy khi zoom to, thanh cuộn xuất hiện làm
  // fitWidth đổi vài px và kích hoạt thêm 1 lần vẽ ngoài ý muốn ngay giữa lúc
  // đang chờ. Gộp cả 2 nguồn thay đổi (zoom + đổi kích thước khung) vào cùng
  // một độ trễ vừa đúng hơn vừa bớt được 1 biến state.
  const [renderWidth, setRenderWidth] = useState(0);
  useEffect(() => {
    if (!desiredRenderWidth) return undefined;
    if (!renderWidth) { setRenderWidth(desiredRenderWidth); return undefined; } // lần đầu: vẽ ngay
    if (Math.abs(desiredRenderWidth - renderWidth) < 0.5) return undefined;
    const timer = setTimeout(() => setRenderWidth(desiredRenderWidth), ZOOM_REDRAW_DELAY_MS);
    return () => clearTimeout(timer);
  }, [desiredRenderWidth, renderWidth]);

  // (3) Double-buffer: mảng các lớp <Page>. Key ổn định trong CÙNG một mảng để
  // React giữ nguyên instance (không unmount/mount lại làm mất canvas đã vẽ).
  const layerSeq = useRef(0);
  const [layers, setLayers] = useState([]);   // [{ key, width }]
  const [activeKey, setActiveKey] = useState(null);

  // Sang trang khác thì bỏ hết lớp cũ (nội dung đổi hẳn, không double-buffer
  // qua trang để tránh hiện nhầm trang cũ ở khung của trang mới).
  useEffect(() => {
    setLayers([]);
    setActiveKey(null);
  }, [pageNumber]);

  useEffect(() => {
    if (!renderWidth) return;
    if (activeKey === null) {
      const key = (layerSeq.current += 1);
      setLayers([{ key, width: renderWidth }]);
      setActiveKey(key);
      return;
    }
    setLayers((prev) => {
      const active = prev.find((l) => l.key === activeKey);
      if (!active) return prev;
      const same = (w) => Math.abs(w - renderWidth) < 0.5;
      if (same(active.width)) return prev.length === 1 ? prev : [active];
      if (prev.some((l) => l.key !== activeKey && same(l.width))) return prev;
      return [active, { key: (layerSeq.current += 1), width: renderWidth }];
    });
  }, [renderWidth, activeKey]);

  // Lớp ngầm vẽ xong -> tráo sang hiển thị, rồi bỏ lớp cũ (giải phóng canvas).
  function handleLayerRendered(key) {
    if (key === activeKey) return;
    setActiveKey(key);
    setLayers((prev) => prev.filter((l) => l.key === key));
  }

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
            <button
              type="button"
              className="stepper-btn"
              title="Thu nhỏ"
              onClick={() => setZoom((z) => clampZoom(z / ZOOM_FACTOR))}
              disabled={zoom <= MIN_ZOOM}
            >
              −
            </button>
            <span className="stepper-vertical-line" />
            <button type="button" className="stepper-btn zoom-level-btn" title="Về mức vừa khung" onClick={() => setZoom(1)}>
              {Math.round(zoom * 100)}%
            </button>
            <span className="stepper-vertical-line" />
            <button
              type="button"
              className="stepper-btn"
              title="Phóng to"
              onClick={() => setZoom((z) => clampZoom(z * ZOOM_FACTOR))}
              disabled={zoom >= MAX_ZOOM}
            >
              +
            </button>
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
          nhiều <Page> ở nhiều chỗ khác nhau trong cây. */}
      <Document
        file={fileUrl}
        className="slide-document-wrapper"
        loading={<div className="viewer-loading">Đang tải tài liệu...</div>}
        error={<div className="viewer-loading">Không tải được tài liệu.</div>}
        onLoadSuccess={(pdf) => {
          setNumPages(pdf.numPages);
          setPdfProxy(pdf);
        }}
      >
        {/* Lớp NGOÀI: được đo, overflow:hidden nên không bao giờ có thanh cuộn
            -> kích thước không bị nội dung PDF tác động ngược. Cũng là nơi neo
            2 nút chuyển trang để chúng đứng yên khi cuộn. */}
        <div
          className={`slide-canvas-card ${highlightedPage != null && highlightedPage === pageNumber ? 'citation-page-active' : ''}`}
          ref={measureRef}
          data-citation-highlight={highlightedPage != null && highlightedPage === pageNumber ? '1' : '0'}
        >
          {highlightedPage != null && highlightedPage === pageNumber && (
            <div className="citation-source-chip" aria-live="polite">
              <span>📖</span>
              <span>Nguồn · Trang {highlightedPage}</span>
            </div>
          )}

          {/* Lớp TRONG: nơi thanh cuộn thật sự xuất hiện khi zoom > 1. */}
          <div className="pdf-scroll-area">
            {displayWidth > 0 && (
              // .pdf-zoom-box mang kích thước NGƯỜI DÙNG THẤY -> quyết định
              // layout/thanh cuộn/canh giữa. Các lớp <Page> bên trong nằm
              // absolute nên không ảnh hưởng layout, chỉ được CSS scale.
              <div className="pdf-zoom-box" style={{ width: displayWidth, height: displayHeight }}>
                {layers.map((layer) => (
                  <div
                    key={layer.key}
                    className={`pdf-layer ${layer.key === activeKey ? '' : 'pdf-layer-offscreen'}`}
                    style={layer.key === activeKey ? { transform: `scale(${displayWidth / layer.width})` } : undefined}
                    aria-hidden={layer.key === activeKey ? undefined : 'true'}
                  >
                    <Page
                      pageNumber={pageNumber}
                      width={layer.width}
                      onRenderSuccess={() => handleLayerRendered(layer.key)}
                    />
                  </div>
                ))}
              </div>
            )}
          </div>

          {pageNumber > 1 && (
            <button type="button" className="edge-nav-btn edge-nav-left" title="Trang trước" onClick={() => goToPage(pageNumber - 1)}>
              <ChevronLeft size={40} />
            </button>
          )}
          {numPages && pageNumber < numPages && (
            <button type="button" className="edge-nav-btn edge-nav-right" title="Trang sau" onClick={() => goToPage(pageNumber + 1)}>
              <ChevronRight size={40} />
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
