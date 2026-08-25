import { apiClient } from './apiClient';

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
