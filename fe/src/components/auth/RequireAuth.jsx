import { Navigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

// Bọc quanh route cần đăng nhập. status='checking' thì chưa render gì cả
// (tránh nháy redirect oan trong lúc đang xác nhận token cũ — xem AuthContext).
export default function RequireAuth({ children }) {
  const { status } = useAuth();

  if (status === 'checking') return null;
  if (status === 'anonymous') return <Navigate to="/signin" replace />;
  return children;
}
