import { apiClient } from './apiClient';

// Khớp đúng be/app/schemas/auth.py: SignupRequest{email,password,name?},
// LoginRequest{email,password}, TokenResponse{access_token,refresh_token,token_type}.

function storeTokens({ access_token, refresh_token }) {
  localStorage.setItem('access_token', access_token);
  localStorage.setItem('refresh_token', refresh_token);
}

export async function signup({ email, password, name }) {
  const { data } = await apiClient.post('/auth/signup', { email, password, name });
  storeTokens(data);
  return data;
}

export async function login({ email, password }) {
  const { data } = await apiClient.post('/auth/login', { email, password });
  storeTokens(data);
  return data;
}

export async function logout() {
  try {
    await apiClient.post('/auth/logout', { refresh_token: localStorage.getItem('refresh_token') });
  } finally {
    // Xóa token cục bộ dù request logout có thành công hay không — người dùng
    // bấm "đăng xuất" phải luôn thấy mình đã đăng xuất trên MÁY NÀY ngay lập
    // tức, không phụ thuộc mạng.
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }
}

export async function getCurrentUser() {
  const { data } = await apiClient.get('/auth/me');
  return data;
}

export function isAuthenticated() {
  return Boolean(localStorage.getItem('access_token'));
}
