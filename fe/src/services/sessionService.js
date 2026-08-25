import { apiClient } from './apiClient.js';

const API_BASE_URL = (typeof import.meta !== 'undefined' && import.meta.env?.VITE_API_BASE_URL) || 'http://localhost:8000/api';

export async function listSessions(documentId) {
  const { data } = await apiClient.get('/sessions', { params: { document_id: documentId } });
  return data || [];
}

export async function createSession(documentId) {
  const { data } = await apiClient.post('/sessions', { document_id: documentId });
  return data;
}

export async function deleteSession(sessionId) {
  await apiClient.delete(`/sessions/${sessionId}`);
}

export async function listMessages(sessionId) {
  const { data } = await apiClient.get(`/sessions/${sessionId}/messages`);
  return data;
}

export async function sendSessionMessage(sessionId, question) {
  const { data } = await apiClient.post(`/sessions/${sessionId}/messages`, { question });
  return data;
}

export function mapStreamStatus(stage) {
  switch (stage) {
    case 'contextualize':
      return 'Đang nối ngữ cảnh...';
    case 'retrieving':
      return 'Đang tìm trong tài liệu...';
    case 'generating':
      return 'Đang soạn câu trả lời...';
    default:
      return 'Đang xử lý...';
  }
}

async function refreshAccessToken() {
  const refreshToken = localStorage.getItem('refresh_token');
  if (!refreshToken) {
    throw new Error('No refresh token available');
  }
  const res = await fetch(`${API_BASE_URL}/auth/refresh`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh_token: refreshToken }),
  });
  if (!res.ok) {
    throw new Error('Refresh token request failed');
  }
  const json = await res.json();
  const data = json.data || json;
  if (!data.access_token) {
    throw new Error('No access_token in refresh response');
  }
  localStorage.setItem('access_token', data.access_token);
  if (data.refresh_token) {
    localStorage.setItem('refresh_token', data.refresh_token);
  }
  return data.access_token;
}

function parseSseBlock(block, handlers, flags) {
  if (!block.trim()) return;
  let eventName = 'message';
  let dataStr = '';
  const lines = block.split('\n');
  for (const line of lines) {
    if (line.startsWith(':')) continue;
    if (line.startsWith('event:')) {
      eventName = line.slice(6).trim();
    } else if (line.startsWith('data:')) {
      const val = line.slice(5).trim();
      dataStr = dataStr ? `${dataStr}\n${val}` : val;
    }
  }
  if (!dataStr) return;

  let payload;
  try {
    payload = JSON.parse(dataStr);
  } catch (err) {
    console.error('Failed to parse SSE JSON payload:', dataStr, err);
    return;
  }

  switch (eventName) {
    case 'status':
      handlers.onStatus?.(payload.stage);
      break;
    case 'token':
      handlers.onToken?.(payload.delta);
      break;
    case 'citation':
      handlers.onCitation?.(payload);
      break;
    case 'replace':
      handlers.onReplace?.(payload);
      break;
    case 'done':
      flags.receivedDone = true;
      handlers.onDone?.(payload);
      break;
    case 'error':
      flags.receivedError = true;
      handlers.onError?.(payload);
      break;
    default:
      break;
  }
}

export async function sendSessionMessageStream(sessionId, question, handlers = {}, isRetry = false) {
  let token = localStorage.getItem('access_token');
  const url = `${API_BASE_URL}/sessions/${sessionId}/messages?stream=1`;

  let response;
  try {
    response = await fetch(url, {
      method: 'POST',
      headers: {
        'Accept': 'text/event-stream',
        'Content-Type': 'application/json',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
      },
      body: JSON.stringify({ question }),
    });
  } catch (err) {
    throw new Error(err.message || 'Không thể kết nối đến máy chủ.');
  }

  if (response.status === 401 && !isRetry) {
    try {
      token = await refreshAccessToken();
      return await sendSessionMessageStream(sessionId, question, handlers, true);
    } catch {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      window.location.href = '/signin';
      throw new Error('Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại.');
    }
  }

  if (!response.ok) {
    let errorDetail = 'Không thể gửi câu hỏi lúc này.';
    try {
      const errorJson = await response.json();
      errorDetail = errorJson.message || errorJson.error?.message || errorJson.detail?.message || errorDetail;
    } catch {
      // Body not JSON
    }
    throw new Error(errorDetail);
  }

  const contentType = response.headers.get('content-type') || '';
  if (!contentType.includes('text/event-stream')) {
    throw new Error('Máy chủ không trả về luồng sự kiện (event-stream).');
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder('utf-8');
  let buffer = '';
  const flags = { receivedDone: false, receivedError: false };

  try {
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const parts = buffer.split('\n\n');
      buffer = parts.pop(); // Giữ lại phần chưa kết thúc

      for (const block of parts) {
        parseSseBlock(block, handlers, flags);
      }
    }

    if (buffer.trim()) {
      parseSseBlock(buffer, handlers, flags);
    }

    if (!flags.receivedDone && !flags.receivedError) {
      throw new Error('Luồng kết nối bị đóng trước khi hoàn tất.');
    }
  } finally {
    reader.releaseLock();
  }
}
