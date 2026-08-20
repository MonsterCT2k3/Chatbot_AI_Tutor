import { apiClient } from './apiClient';

// Khớp be/app/schemas/rag.py + be/app/routers/documents.py.
// LƯU Ý: endpoint /ask hiện là "Temporary test endpoint for Phase 5" — không
// session-aware, mỗi câu hỏi độc lập, KHÔNG có lịch sử hội thoại lưu server-side
// (khác hẳn ChatGPT). Sẽ đổi sang /api/sessions/{id}/messages khi Phase 6 xong;
// giữ nguyên chữ ký hàm ở đây để lúc đó chỉ cần đổi bên trong, không đổi caller.
export async function askQuestion(documentId, question) {
  const { data } = await apiClient.post(`/documents/${documentId}/ask`, { question });
  return data; // { answer_id, answer, citations: [{page_number, chunk_id, snippet}] }
}

// is_positive: boolean, reason: string | null (tùy chọn — xem be 5.6.12)
export async function submitFeedback(documentId, answerId, isPositive, reason = null) {
  await apiClient.post(`/documents/${documentId}/ask/${answerId}/feedback`, {
    is_positive: isPositive,
    reason,
  });
}
