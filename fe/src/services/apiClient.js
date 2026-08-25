import axios from 'axios';

// Base URL của backend thật. Auth/documents/sessions đều có endpoint.
const API_BASE_URL = (typeof import.meta !== 'undefined' && import.meta.env?.VITE_API_BASE_URL) || 'http://localhost:8000/api';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'Content-Type': 'application/json' },
});

// Gắn access token vào MỌI request — đọc lại từ localStorage mỗi lần thay vì
// đọc 1 lần lúc khởi tạo module, vì token có thể đổi (refresh) trong lúc app
// đang chạy mà không reload trang.
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Backend bọc MỌI response thành công (status < 400) trong envelope
// {success, message, data, error, requestId} — xem be/app/middleware.py
// ResponseEnvelopeMiddleware. Đã tự tay curl thật để xác nhận hình dạng này
// (không đoán qua Pydantic schema, vốn chỉ mô tả phần BÊN TRONG `data`) sau
// khi phát hiện bug đăng nhập thật: response.data.access_token luôn undefined
// vì token thật nằm ở response.data.data.access_token. Bóc vỏ Ở ĐÚNG 1 CHỖ
// này để mọi service (auth/document/chat) gọi apiClient như thể không có
// envelope nào cả — không phải tự bóc vỏ ở từng hàm.
//
// Response LỖI (status >= 400) KHÔNG bị đụng vào ở đây (được bọc bởi
// app/exceptions.py với hình dạng RIÊNG: {success:false, message, data:null,
// error:{code, details}, requestId}) — đọc lỗi ở service/component qua
// err.response.data.message / err.response.data.error.code.
apiClient.interceptors.response.use((response) => {
  if (response.data && typeof response.data === 'object' && 'success' in response.data) {
    response.data = response.data.data;
  }
  return response;
});

// Access token hết hạn (15 phút, xem be/app/config.py ACCESS_TOKEN_EXPIRE_MINUTES)
// -> tự động thử refresh 1 lần bằng refresh token, gắn lại token mới, gọi lại
// ĐÚNG request cũ. Refresh cũng fail (refresh token hết hạn/bị thu hồi) thì mới
// đăng xuất thật. `_retry` đánh dấu để không lặp vô hạn nếu refresh cũng 401.
let refreshPromise = null;

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config;
    if (error.response?.status !== 401 || original._retry || original.url?.includes('/auth/')) {
      return Promise.reject(error);
    }
    original._retry = true;

    try {
      // Nhiều request 401 cùng lúc chỉ nên trigger 1 lần refresh, không phải
      // mỗi request tự refresh riêng (tốn refresh token, dễ race condition).
      refreshPromise ??= apiClient
        .post('/auth/refresh', { refresh_token: localStorage.getItem('refresh_token') })
        .finally(() => { refreshPromise = null; });

      const { data } = await refreshPromise;
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('refresh_token', data.refresh_token);
      original.headers.Authorization = `Bearer ${data.access_token}`;
      return apiClient(original);
    } catch {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      window.location.href = '/signin';
      return Promise.reject(error);
    }
  },
);
