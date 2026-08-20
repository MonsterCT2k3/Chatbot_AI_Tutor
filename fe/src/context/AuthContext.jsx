import { createContext, useContext, useEffect, useState } from 'react';
import * as authService from '../services/authService';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  // 3 trạng thái, không phải boolean: lúc mới load trang, ta CHƯA BIẾT còn
  // đăng nhập hay không (phải chờ gọi /auth/me để xác nhận token cũ còn hiệu
  // lực) — nếu chỉ dùng boolean isLoading, màn hình sẽ nháy qua "chưa đăng
  // nhập" trước khi kịp xác nhận, gây redirect oan về trang signin.
  const [status, setStatus] = useState('checking'); // 'checking' | 'authenticated' | 'anonymous'

  useEffect(() => {
    if (!authService.isAuthenticated()) {
      setStatus('anonymous');
      return;
    }
    authService
      .getCurrentUser()
      .then((u) => {
        setUser(u);
        setStatus('authenticated');
      })
      .catch(() => setStatus('anonymous'));
  }, []);

  async function login(credentials) {
    await authService.login(credentials);
    const u = await authService.getCurrentUser();
    setUser(u);
    setStatus('authenticated');
  }

  async function signup(payload) {
    await authService.signup(payload);
    const u = await authService.getCurrentUser();
    setUser(u);
    setStatus('authenticated');
  }

  async function logout() {
    await authService.logout();
    setUser(null);
    setStatus('anonymous');
  }

  return (
    <AuthContext.Provider value={{ user, status, login, signup, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth phải được gọi bên trong <AuthProvider>');
  return ctx;
}
