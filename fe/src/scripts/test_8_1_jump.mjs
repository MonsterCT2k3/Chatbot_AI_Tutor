// Test simulation of 8.1 & 8.2 auto-jump, highlight state and overlay chip rendering

function createWorkspaceState(initialPage = 1, numPages = 50) {
  let pageNumber = initialPage;
  let highlightedPage = null;

  function revealCitationPage(page) {
    const n = Number(page);
    if (!Number.isFinite(n) || n < 1) return;
    const clamped = numPages ? Math.min(numPages, Math.max(1, n)) : n;
    pageNumber = clamped;
    highlightedPage = clamped;
  }

  function clearCitationHighlight() {
    highlightedPage = null;
  }

  function getSlideViewerRenderState() {
    const isCitationActive = highlightedPage != null && highlightedPage === pageNumber;
    return {
      className: `slide-canvas-card ${isCitationActive ? 'citation-page-active' : ''}`.trim(),
      dataCitationHighlight: isCitationActive ? '1' : '0',
      showChip: isCitationActive,
      chipText: isCitationActive ? `Nguồn · Trang ${highlightedPage}` : null,
    };
  }

  return {
    get pageNumber() { return pageNumber; },
    get highlightedPage() { return highlightedPage; },
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
          ws.revealCitationPage(p);
        }
      }
    } else if (ev.type === 'replace') {
      const nextCitations = ev.citations || [];
      if (nextCitations.length === 0) {
        ws.clearCitationHighlight();
      } else {
        didAutoJumpRef.current = true;
        const firstPage = Number(nextCitations[0]?.page_number);
        if (Number.isFinite(firstPage) && firstPage >= 1) {
          ws.revealCitationPage(firstPage);
        }
      }
    } else if (ev.type === 'error') {
      ws.clearCitationHighlight();
    }
  }
}

function runTests() {
  console.log('Testing 8.1 & 8.2 auto-jump, highlight state and overlay chip:');

  // Case 1: Initial state
  const ws = createWorkspaceState(1, 50);
  console.log('1. Initial state:', ws.getSlideViewerRenderState());
  let ui = ws.getSlideViewerRenderState();
  if (ui.showChip || ui.dataCitationHighlight !== '0') throw new Error('Initial UI mismatch');

  // Case 2: SSE citation stream with citation page 22
  simulateChatTurn(ws, [
    { type: 'citation', citation: { page_number: 22 } },
  ]);
  ui = ws.getSlideViewerRenderState();
  console.log('2. After citation stream on page 22:', ui);
  if (!ui.showChip || ui.chipText !== 'Nguồn · Trang 22' || ui.dataCitationHighlight !== '1') {
    throw new Error('Active citation overlay mismatch');
  }

  // Case 3: User navigates away to page 23 via prev/next
  ws.setPageNumber(23);
  ui = ws.getSlideViewerRenderState();
  console.log('3. After navigating away to page 23:', ui);
  if (ui.showChip || ui.dataCitationHighlight !== '0') {
    throw new Error('Chip and active class should hide when viewing other pages');
  }

  // Case 4: User navigates back to cited page 22
  ws.setPageNumber(22);
  ui = ws.getSlideViewerRenderState();
  console.log('4. After navigating back to cited page 22:', ui);
  if (!ui.showChip || ui.chipText !== 'Nguồn · Trang 22' || ui.dataCitationHighlight !== '1') {
    throw new Error('Chip and active class should re-appear when returning to cited page');
  }

  // Case 5: Click badge on page 15
  ws.revealCitationPage(15);
  ui = ws.getSlideViewerRenderState();
  console.log('5. After click badge (15):', ui);
  if (!ui.showChip || ui.chipText !== 'Nguồn · Trang 15' || ws.pageNumber !== 15) {
    throw new Error('Click badge overlay mismatch');
  }

  // Case 6: New question starts
  simulateChatTurn(ws, []);
  ui = ws.getSlideViewerRenderState();
  console.log('6. When new question starts:', ui);
  if (ui.showChip || ws.highlightedPage !== null) {
    throw new Error('Highlight should clear on new question');
  }

  console.log('\n============================================================');
  console.log('ALL 8.1 & 8.2 STATE, OVERLAY & CHIP TESTS PASSED 100%!');
  console.log('============================================================');
}

runTests();
