import fs from 'fs';
import { createSession, listMessages, mapStreamStatus, sendSessionMessageStream } from '../services/sessionService.js';

// Mock localStorage for Node.js environment
const storage = {};
globalThis.localStorage = {
  getItem: (k) => storage[k] ?? null,
  setItem: (k, v) => { storage[k] = String(v); },
  removeItem: (k) => { delete storage[k]; },
};

async function main() {
  const tokenData = JSON.parse(fs.readFileSync('./src/scripts/test_tokens.json', 'utf8'));
  localStorage.setItem('access_token', tokenData.access_token);
  localStorage.setItem('refresh_token', tokenData.refresh_token);
  const documentId = tokenData.document_id;
  console.log(`1. Loaded tokens for EVAL_USER. Document ID: ${documentId}`);

  // 2. Create a chat session
  const session = await createSession(documentId);
  console.log(`2. Created session: ${session.id}`);

  // 3. Test sendSessionMessageStream
  console.log('\n3. Testing sendSessionMessageStream with callbacks:');
  const events = [];
  let answerContent = '';
  const citations = [];
  let donePayload = null;

  await sendSessionMessageStream(session.id, 'Transformer ra đời vào năm nào?', {
    onStatus(stage) {
      console.log(`-> onStatus: stage = "${stage}" (mapped: "${mapStreamStatus(stage)}")`);
      events.push({ type: 'status', stage });
    },
    onToken(delta) {
      console.log(`-> onToken: delta = "${delta}"`);
      answerContent += delta;
      events.push({ type: 'token', delta });
    },
    onCitation(citation) {
      console.log(`-> onCitation: page = ${citation.page_number}`);
      citations.push(citation);
      events.push({ type: 'citation', citation });
    },
    onReplace(payload) {
      console.log(`-> onReplace: content = "${payload.content}"`);
      answerContent = payload.content;
      events.push({ type: 'replace', payload });
    },
    onDone(payload) {
      console.log(`-> onDone: message_id = ${payload.message_id}, answer_id = ${payload.answer_id}`);
      donePayload = payload;
      events.push({ type: 'done', payload });
    },
    onError(payload) {
      console.log(`-> onError:`, payload);
      events.push({ type: 'error', payload });
    },
  });

  console.log('\n4. Verification assertions:');
  console.log(`Total events received: ${events.length}`);
  const eventTypes = events.map((e) => e.type);
  console.log(`Event types sequence:`, eventTypes);

  if (!eventTypes.includes('status')) throw new Error('Missing status event');
  if (!eventTypes.includes('token')) throw new Error('Missing token event');
  if (!eventTypes.includes('done')) throw new Error('Missing done event');
  if (!answerContent.includes('2017')) throw new Error('Answer content does not contain 2017');
  if (!donePayload?.answer_id) throw new Error('Done event missing answer_id');

  // 5. Test listMessages (F5 reload test)
  console.log('\n5. Testing listMessages (verifying persisted message in DB):');
  const history = await listMessages(session.id);
  const msgs = history.messages || [];
  console.log(`Persisted messages count: ${msgs.length}`);
  const lastAssistant = msgs.find((m) => m.role === 'assistant');
  console.log(`Persisted assistant content: "${lastAssistant?.content}"`);
  console.log(`Persisted assistant citations: ${lastAssistant?.citations?.length}`);
  console.log(`Persisted assistant answer_id: ${lastAssistant?.answer_id}`);

  if (!lastAssistant) throw new Error('Missing assistant message in history');
  if (lastAssistant.content !== answerContent) throw new Error('Persisted content mismatch');
  if (lastAssistant.answer_id !== donePayload.answer_id) throw new Error('Persisted answer_id mismatch');

  // 6. Test 401 token refresh on fetch
  console.log('\n6. Testing 401 token refresh on fetch:');
  // Invalidate access token deliberately to trigger 401 -> refresh -> retry
  localStorage.setItem('access_token', 'invalid_expired_token_12345');
  let refreshedDone = null;
  await sendSessionMessageStream(session.id, 'Transformer có ưu điểm gì?', {
    onDone(p) {
      refreshedDone = p;
    },
  });
  console.log(`Refreshed request succeeded! New token saved: ${localStorage.getItem('access_token')?.slice(0, 15)}...`);
  if (!refreshedDone?.answer_id) throw new Error('Refresh 401 retry failed to produce answer_id');

  console.log('\n============================================================');
  console.log('ALL FE SSE SERVICE, PERSISTENCE & 401 REFRESH TESTS PASSED 100%!');
  console.log('============================================================');
}

main().catch((err) => {
  console.error('Test failed:', err);
  process.exit(1);
});
