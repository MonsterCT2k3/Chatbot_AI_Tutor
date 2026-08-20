import { apiClient } from './apiClient';

// Khớp be/app/routers/documents.py. status: 'pending'|'parsing'|'embedding'|
// 'ready'|'failed' (be/app/models/document.py) — page_count/error_message
// còn null cho tới khi status='ready' (hoặc 'failed' cho error_message).

export async function uploadDocument(file, extractionMode = 'pypdf') {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('extraction_mode', extractionMode);
  const { data } = await apiClient.post('/documents', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return data;
}

export async function listDocuments() {
  const { data } = await apiClient.get('/documents');
  return data;
}

export async function getDocument(documentId) {
  const { data } = await apiClient.get(`/documents/${documentId}`);
  return data;
}

export async function getDocumentStatus(documentId) {
  const { data } = await apiClient.get(`/documents/${documentId}/status`);
  return data;
}

// URL PDF thật (presigned R2) — dùng trực tiếp làm `file` prop cho react-pdf.
export async function getDocumentFileUrl(documentId) {
  const { data } = await apiClient.get(`/documents/${documentId}/file`);
  return data.url;
}

export async function deleteDocument(documentId) {
  await apiClient.delete(`/documents/${documentId}`);
}
