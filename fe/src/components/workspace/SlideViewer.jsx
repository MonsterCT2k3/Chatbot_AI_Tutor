import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Document, Page } from 'react-pdf';
import { ChevronLeft, ChevronRight, LayoutGrid, Search } from 'lucide-react';
import 'react-pdf/dist/Page/AnnotationLayer.css';
import 'react-pdf/dist/Page/TextLayer.css';
import '../../lib/pdfjsSetup';

const MIN_ZOOM = 0.5;
const MAX_ZOOM = 3;
const ZOOM_STEP = 0.25;
const FILMSTRIP_RADIUS = 2; // hiện current page ± 2, giống mockup (5 thumbnail)
// Chừa vài px để phép "vừa khung" không bị lố 1-2px do làm tròn rồi sinh
// thanh cuộn thừa ngay ở mức zoom = 1 (mức lẽ ra phải vừa khít).
const FIT_SAFETY_PX = 4;
// Render canvas ở độ phân giải GẤP ĐÔI mức "vừa khung" rồi phóng/thu bằng CSS
// (xem ghi chú "VỀ CHỚP NHÁY KHI ZOOM" bên dưới). Ở 100% ảnh bị thu 2:1 -> rất
// nét; ở 200% là đúng tỉ lệ 1:1; ở mức tối đa 300% chỉ phóng 1.5x -> hơi mềm
// nhưng vẫn đọc tốt. Có trần tuyệt đối để không ngốn RAM trên màn hình siêu
// rộng (react-pdf còn tự nhân thêm devicePixelRatio nữa).
const RENDER_QUALITY = 2;
const MAX_RENDER_WIDTH = 2000;

// Dựng từ panel-center trong detail_screen_lesson.html. Toàn bộ nội dung
// "slide" (sơ đồ neural network, công thức highlight vàng, tooltip pin...)
// trong mockup là ví dụ minh hoạ cố định cho 1 slide cụ thể — được THAY THẾ
// HOÀN TOÀN bằng nội dung PDF thật (react-pdf), không phải mock lại chúng,
// vì đã có nội dung thật để hiển thị.
//
// ─────────────────────────────────────────────────────────────────────────
// VỀ BUG "TRANG TRẮNG, LÚC ĐƯỢC LÚC KHÔNG" (đã đọc source react-pdf để xác
// nhận, không phải suy đoán):
//
// Trong node_modules/react-pdf/dist/Page/Canvas.js, MỖI lần render nó làm:
//     canvas.style.visibility = 'hidden';        // ẩn canvas TRƯỚC khi vẽ
//     page.render(...).promise
//        .then(()  => { canvas.style.visibility = ''; ... })   // chỉ hiện lại KHI VẼ XONG
//        .catch(onRenderError);                                // huỷ giữa chừng -> KHÔNG hiện lại
//     return () => cancelRunningTask(runningTask);             // cleanup effect = huỷ render
//
// => Nếu 1 lần render bị HUỶ giữa chừng (effect cleanup chạy vì `scale` đổi)
// mà không có lần render nào sau đó chạy xong, canvas sẽ nằm ở
// visibility:hidden VĨNH VIỄN — trang trắng, dù canvas có thể đã có nội dung.
//
// Trước đây tôi đặt ResizeObserver lên ĐÚNG phần tử đang cuộn (overflow:auto).
// Với tài liệu trang dọc: render ra cao hơn khung -> hiện thanh cuộn dọc ->
// contentRect.width tụt ~15px -> đổi width -> đổi scale -> HUỶ render đang
// chạy. Việc lần render kế tiếp có kịp xong trước lần huỷ tiếp theo hay không
// hoàn toàn là chạy đua thời gian => "lúc được lúc không", và tài liệu càng
// nặng càng dễ trắng.
//
// CÁCH SỬA (triệt tiêu tận gốc, không vá triệu chứng):
// 1. TÁCH phần tử ĐO khỏi phần tử CUỘN: .slide-canvas-card (overflow:hidden,
//    được đo) bọc ngoài .pdf-scroll-area (overflow:auto, chứa trang). Thanh
//    cuộn giờ chỉ xuất hiện ở lớp TRONG, không bao giờ làm đổi kích thước lớp
//    NGOÀI đang được ResizeObserver theo dõi -> vòng lặp bị cắt đứt hẳn.
// 2. Lấy kích thước trang từ CHÍNH pdf proxy (getViewport({scale:1})) chứ
//    không phải từ kết quả render — giá trị này cố định tuyệt đối, không phụ
//    thuộc ta đang render ở kích thước nào, nên không thể tạo phụ thuộc vòng.
// 3. CHỜ CÓ ĐỦ cả 2 số đo rồi mới render <Page> lần đầu -> render đúng 1 lần
//    ở đúng kích thước cuối, không có lần huỷ nào.
// ─────────────────────────────────────────────────────────────────────────
export default function SlideViewer({ filename, fileUrl, pageNumber, setPageNumber, numPages, setNumPages }) {
  const [zoom, setZoom] = useState(1);
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
  // bao giờ render (đã xác nhận bằng test trình duyệt thật: .pdf-scroll-area
  // rỗng hoàn toàn dù khung có kích thước 773x758). Callback ref được React
  // gọi ĐÚNG LÚC node xuất hiện/biến mất, nên luôn gắn đúng thời điểm.
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

  // ─────────────────────────────────────────────────────────────────────────
  // VỀ CHỚP NHÁY KHI PHÓNG TO/THU NHỎ:
  //
  // Trong react-pdf/dist/Page/Canvas.js, mỗi lần `scale` đổi là nó chạy lại:
  //     canvas.width = ...;                  // gán width XOÁ SẠCH pixel đang có
  //     canvas.style.visibility = 'hidden';  // rồi ẩn canvas đi
  //     page.render(...).then(() => { canvas.style.visibility = ''; })  // hiện lại KHI vẽ xong
  //
  // => mỗi lần bấm +/− là 1 chu kỳ "xoá -> ẩn -> vẽ lại -> hiện", tức là NHÁY
  // 1 cái; bấm liên tục thì chớp liên tục. Không thể vá bằng CSS
  // (visibility:visible !important chỉ làm lộ ra canvas ĐÃ BỊ XOÁ TRẮNG).
  //
  // CÁCH SỬA: KHÔNG cho `scale` của react-pdf đổi theo zoom nữa. Canvas được
  // render ĐÚNG 1 LẦN ở `renderWidth` (chỉ đổi khi cửa sổ đổi kích thước hoặc
  // sang trang khác), còn zoom xử lý HOÀN TOÀN bằng CSS transform — chạy trên
  // GPU, không đụng tới pdf.js, nên mượt tuyệt đối và không nháy.
  // ─────────────────────────────────────────────────────────────────────────
  const fitWidth = useMemo(() => {
    if (!pageSize || !viewport.width || !viewport.height) return 0;
    const availW = viewport.width - FIT_SAFETY_PX;
    const availH = viewport.height - FIT_SAFETY_PX;
    const fitScale = Math.min(availW / pageSize.width, availH / pageSize.height);
    return pageSize.width * fitScale;
  }, [pageSize, viewport]);

  // Kích thước THẬT truyền cho <Page> — cố tình KHÔNG phụ thuộc `zoom`, và
  // dùng HYSTERESIS: chỉ đổi khi khung đổi ĐÁNG KỂ (>15%).
  //
  // Vì sao cần: đo thật bằng trình duyệt cho thấy khi zoom lên 175%, fitWidth
  // tụt đúng 15px (bề rộng 1 thanh cuộn xuất hiện ở đâu đó trong layout) ->
  // renderWidth đổi 1538 -> 1508 -> pdf.js vẽ lại -> NHÁY, đúng thứ ta đang
  // muốn diệt. Hysteresis nuốt trọn các dao động vặt như vậy, đồng thời cắt
  // đứt mọi vòng phản hồi còn sót lại (giá trị đã chốt thì thay đổi nhỏ không
  // làm nó đổi nữa), nhưng vẫn render lại nét khi người dùng thật sự đổi kích
  // thước cửa sổ. Không có nhược điểm về hiển thị: renderWidth CHỈ quyết định
  // độ nét, còn kích thước nhìn thấy do displayWidth/visualScale lo, nên lệch
  // chút cũng không làm sai layout.
  const [renderWidth, setRenderWidth] = useState(0);
  useEffect(() => {
    const target = fitWidth ? Math.min(fitWidth * RENDER_QUALITY, MAX_RENDER_WIDTH) : 0;
    if (!target) return;
    setRenderWidth((prev) => (prev === 0 || Math.abs(target - prev) / prev > 0.15 ? target : prev));
  }, [fitWidth]);

  // Kích thước NGƯỜI DÙNG THẤY = vừa khung × zoom. Chênh lệch giữa 2 con số
  // này được bù bằng CSS transform, không render lại.
  const displayWidth = fitWidth * zoom;
  const displayHeight = pageSize ? displayWidth * (pageSize.height / pageSize.width) : 0;
  const visualScale = renderWidth ? displayWidth / renderWidth : 1;

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
              onClick={() => setZoom((z) => Math.max(MIN_ZOOM, +(z - ZOOM_STEP).toFixed(2)))}
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
              onClick={() => setZoom((z) => Math.min(MAX_ZOOM, +(z + ZOOM_STEP).toFixed(2)))}
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
          nhiều <Page> ở nhiều chỗ khác nhau trong cây, thay vì mỗi thumbnail
          tự mở lại cả file PDF. */}
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
            -> kích thước không bị nội dung PDF tác động ngược (xem ghi chú
            dài ở đầu file về bug canvas trắng). */}
        <div className="slide-canvas-card" ref={measureRef}>
          {/* Lớp TRONG: nơi thanh cuộn thật sự xuất hiện khi zoom > 1. */}
          <div className="pdf-scroll-area">
            {renderWidth > 0 && (
              // .pdf-zoom-box mang kích thước NGƯỜI DÙNG THẤY -> đây mới là thứ
              // quyết định layout/thanh cuộn. Còn <Page> bên trong luôn giữ
              // nguyên renderWidth và chỉ được CSS scale lại, nên pdf.js không
              // phải vẽ lại lần nào khi zoom.
              <div className="pdf-zoom-box" style={{ width: displayWidth, height: displayHeight }}>
                <div className="pdf-zoom-inner" style={{ transform: `scale(${visualScale})` }}>
                  <Page key={pageNumber} pageNumber={pageNumber} width={renderWidth} />
                </div>
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
