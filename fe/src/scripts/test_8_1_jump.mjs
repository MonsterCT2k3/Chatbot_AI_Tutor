// Test simulation of 8.1, 8.2, 8.3b auto-jump, highlight state, overlay chip, and bbox rects

function createWorkspaceState(initialPage = 1, numPages = 50) {
  let pageNumber = initialPage;
  let highlightedPage = null;
  let highlightedBbox = null;

  function revealCitationPage(page, bbox = null) {
    const n = Number(page);
    if (!Number.isFinite(n) || n < 1) return;
    const clamped = numPages ? Math.min(numPages, Math.max(1, n)) : n;
    pageNumber = clamped;
    highlightedPage = clamped;
    highlightedBbox = bbox && Array.isArray(bbox.rects) && bbox.rects.length > 0 ? bbox : null;
  }

  function clearCitationHighlight() {
    highlightedPage = null;
    highlightedBbox = null;
  }

  function getSlideViewerRenderState(displayWidth = 600) {
    const isCitationActive = highlightedPage != null && highlightedPage === pageNumber;
    const hasBbox = isCitationActive && highlightedBbox && Array.isArray(highlightedBbox.rects) && highlightedBbox.rects.length > 0;

    let computedRects = [];
    if (hasBbox) {
      const scale = displayWidth / (highlightedBbox.page_width || 1);
      computedRects = highlightedBbox.rects.map((r) => ({
        left: Math.round(r.x * scale * 100) / 100,
        top: Math.round(((highlightedBbox.page_height || 0) - (r.y + r.h)) * scale * 100) / 100,
        width: Math.round(r.w * scale * 100) / 100,
        height: Math.round(r.h * scale * 100) / 100,
      }));
    }

    return {
      className: `slide-canvas-card ${isCitationActive ? 'citation-page-active' : ''}`.trim(),
      dataCitationHighlight: isCitationActive ? '1' : '0',
      showChip: isCitationActive,
      chipText: isCitationActive ? `Nguồn · Trang ${highlightedPage}` : null,
      showBboxRects: hasBbox,
      bboxRectsCount: computedRects.length,
      computedRects,
    };
  }

  return {
    get pageNumber() { return pageNumber; },
    get highlightedPage() { return highlightedPage; },
    get highlightedBbox() { return highlightedBbox; },
    setPageNumber: (p) => { pageNumber = p; },
    revealCitationPage,
    clearCitationHighlight,
    getSlideViewerRenderState,
  };
}

function simulateChatTurn(ws, events) {
  const didAutoJumpRef = { current: false };
  ws.clearCitationHighlight();

  for (const ev of events) {
    if (ev.type === 'citation') {
      if (!didAutoJumpRef.current) {
        const p = Number(ev.citation?.page_number);
        if (Number.isFinite(p) && p >= 1) {
          didAutoJumpRef.current = true;
          ws.revealCitationPage(p, ev.citation?.bbox ?? null);
        }
      }
    } else if (ev.type === 'replace') {
      const nextCitations = ev.citations || [];
      if (nextCitations.length === 0) {
        ws.clearCitationHighlight();
      } else {
        didAutoJumpRef.current = true;
        const first = nextCitations[0];
        const firstPage = Number(first?.page_number);
        if (Number.isFinite(firstPage) && firstPage >= 1) {
          ws.revealCitationPage(firstPage, first?.bbox ?? null);
        }
      }
    } else if (ev.type === 'error') {
      ws.clearCitationHighlight();
    }
  }
}

function runTests() {
  console.log('Testing 8.1, 8.2, 8.3b state, chip, and bbox rect overlay:');

  const sampleBbox = {
    version: 1,
    coord: 'pdf_user_space',
    page_width: 960.0,
    page_height: 540.0,
    rects: [
      { x: 104.07, y: 497.02, w: 137.92, h: 18.2 },
    ],
  };

  // Case 1: Initial state
  const ws = createWorkspaceState(1, 50);
  let ui = ws.getSlideViewerRenderState();
  console.log('1. Initial state:', ui);
  if (ui.showChip || ui.showBboxRects) throw new Error('Initial UI mismatch');

  // Case 2: SSE citation stream with bbox on page 22
  simulateChatTurn(ws, [
    { type: 'citation', citation: { page_number: 22, bbox: sampleBbox } },
  ]);
  ui = ws.getSlideViewerRenderState(600);
  console.log('2. After citation stream on page 22 with bbox:', ui);
  if (!ui.showChip || !ui.showBboxRects || ui.bboxRectsCount !== 1) {
    throw new Error('Bbox overlay rendering failed');
  }
  const r0 = ui.computedRects[0];
  if (r0.left !== 65.04 || r0.top !== 15.49 || r0.width !== 86.2 || r0.height !== 11.38) {
    throw new Error(`Bbox coordinate calculation mismatch: ${JSON.stringify(r0)}`);
  }

  // Case 3: Navigating away to page 23
  ws.setPageNumber(23);
  ui = ws.getSlideViewerRenderState(600);
  console.log('3. Navigating away to page 23:', ui);
  if (ui.showChip || ui.showBboxRects) throw new Error('Bbox rects and chip must hide when viewing another page');

  // Case 4: Navigating back to page 22
  ws.setPageNumber(22);
  ui = ws.getSlideViewerRenderState(600);
  console.log('4. Navigating back to page 22:', ui);
  if (!ui.showChip || !ui.showBboxRects) throw new Error('Bbox rects and chip must re-appear when returning');

  // Case 5: Fallback when bbox is null (e.g. unindexed/legacy document)
  ws.revealCitationPage(15, null);
  ui = ws.getSlideViewerRenderState(600);
  console.log('5. Citation on page 15 with null bbox:', ui);
  if (!ui.showChip || ui.showBboxRects || ui.chipText !== 'Nguồn · Trang 15') {
    throw new Error('Null bbox must fallback to page-level chip and viền without rects');
  }

  // Case 6: Clear on new question
  simulateChatTurn(ws, []);
  ui = ws.getSlideViewerRenderState(600);
  console.log('6. New question clear:', ui);
  if (ui.showChip || ui.showBboxRects || ws.highlightedBbox !== null) {
    throw new Error('Highlight and bbox must clear on new question');
  }

  console.log('\n============================================================');
  console.log('ALL 8.1, 8.2, 8.3b STATE & BBOX OVERLAY TESTS PASSED 100%!');
  console.log('============================================================');
}

runTests();
