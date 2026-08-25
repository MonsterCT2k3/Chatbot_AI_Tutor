// Test simulation of 9.1 session rename flow and state transitions

function createSessionManager(initialSessions = []) {
  let sessions = [...initialSessions];
  let activeSessionId = sessions[0]?.id || null;
  let editingId = null;
  let editTitle = '';

  function startEditing(session) {
    editingId = session.id;
    editTitle = session.title || '';
  }

  function cancelEditing() {
    editingId = null;
    editTitle = '';
  }

  async function submitRename(sessionId, onRenameApi) {
    const t = editTitle.trim();
    if (!t) {
      cancelEditing();
      return;
    }
    const cleanTitle = t.slice(0, 200);
    const session = sessions.find((s) => s.id === sessionId);
    if (cleanTitle === (session?.title || '').trim()) {
      cancelEditing();
      return;
    }

    const updated = await onRenameApi(sessionId, cleanTitle);
    sessions = sessions.map((s) => (s.id === sessionId ? { ...s, ...updated } : s));
    cancelEditing();
  }

  return {
    get sessions() { return sessions; },
    get activeSessionId() { return activeSessionId; },
    get editingId() { return editingId; },
    get editTitle() { return editTitle; },
    setEditTitle: (t) => { editTitle = t; },
    setActiveSessionId: (id) => { activeSessionId = id; },
    startEditing,
    cancelEditing,
    submitRename,
  };
}

async function runTests() {
  console.log('Testing 9.1 session rename state & inline edit flow:');

  const mockApi = async (id, title) => {
    return { id, title, updated_at: new Date().toISOString() };
  };

  const mgr = createSessionManager([
    { id: 's1', title: 'Bài giảng Transformer 2017' },
    { id: 's2', title: 'New chat' },
  ]);

  // Case 1: Start editing s1 via pencil / double-click
  mgr.startEditing(mgr.sessions[0]);
  console.log('1. Start editing s1:', { editingId: mgr.editingId, title: mgr.editTitle });
  if (mgr.editingId !== 's1' || mgr.editTitle !== 'Bài giảng Transformer 2017') {
    throw new Error('Start editing failed');
  }

  // Case 2: Escape cancels editing without changes
  mgr.cancelEditing();
  console.log('2. Cancel editing (Escape):', { editingId: mgr.editingId });
  if (mgr.editingId !== null) throw new Error('Escape cancel failed');

  // Case 3: Edit and submit via Enter
  mgr.startEditing(mgr.sessions[0]);
  mgr.setEditTitle('  Tìm hiểu kiến trúc Attention và Transformer  ');
  await mgr.submitRename('s1', mockApi);
  console.log('3. After submit valid rename:', mgr.sessions[0]);
  if (mgr.sessions[0].title !== 'Tìm hiểu kiến trúc Attention và Transformer') {
    throw new Error('Rename submit failed');
  }

  // Case 4: Blur with whitespace only -> cancel without API call
  let apiCalled = false;
  const spyApi = async (id, t) => { apiCalled = true; return mockApi(id, t); };
  mgr.startEditing(mgr.sessions[1]);
  mgr.setEditTitle('     ');
  await mgr.submitRename('s2', spyApi);
  console.log('4. Blank title submission:', { apiCalled, s2Title: mgr.sessions[1].title });
  if (apiCalled || mgr.sessions[1].title !== 'New chat') {
    throw new Error('Blank title should cancel and not call API');
  }

  // Case 5: Length > 200 gets clamped
  mgr.startEditing(mgr.sessions[1]);
  mgr.setEditTitle('A'.repeat(250));
  await mgr.submitRename('s2', mockApi);
  console.log('5. Clamped title length:', mgr.sessions[1].title.length);
  if (mgr.sessions[1].title.length !== 200) {
    throw new Error('Title clamping failed');
  }

  console.log('\n============================================================');
  console.log('ALL 9.1 SESSION RENAME TESTS PASSED 100%!');
  console.log('============================================================');
}

runTests();
