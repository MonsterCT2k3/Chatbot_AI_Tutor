import axios from 'axios';

// Base URL của backend thật (be/app/main.py — auth/documents đã có, sessions/
// messages mới chỉ là router rỗng, CHƯA có endpoint nào, không gọi tới).
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

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
