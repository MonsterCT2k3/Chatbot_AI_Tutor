import { apiClient } from './apiClient';

// 👍/👎 vẫn gắn ai_usage_log.id (6.6). Endpoint cũ giữ nguyên — id không đổi.
export async function submitFeedback(documentId, answerId, isPositive, reason = null) {
  await apiClient.post(`/documents/${documentId}/ask/${answerId}/feedback`, {
    is_positive: isPositive,
    reason,
  });
}
