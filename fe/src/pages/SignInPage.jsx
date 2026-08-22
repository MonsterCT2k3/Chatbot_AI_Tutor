import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Eye, EyeOff, PenLine, ArrowRight, Pin } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import '../components/auth/AuthLayout.css';
import './SignInPage.css';

// Dựng lại từ fe/src/mock_html_ui/auth/signin.html.
//
// 2 nút "Google" / "SSO Đại học" và link "Quên mật khẩu?" giữ NGUYÊN GIAO DIỆN
// vì là 1 phần thiết kế, nhưng cố tình để disabled (opacity mờ, cursor
// not-allowed) — backend hiện chỉ có POST /api/auth/login (email+password),
// không có OAuth/SSO hay endpoint reset mật khẩu nào. Không giả vờ các nút
// này hoạt động.
export default function SignInPage() {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [remember, setRemember] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    setIsSubmitting(true);
    try {
      await login({ email, password });
      navigate('/', { replace: true });
    } catch (err) {
      // Khớp be/app/routers/auth.py: 401 INVALID_CREDENTIALS, 429 rate limit
      // (5 lần/phút, xem @limiter.limit("5/minute") trên /auth/login).
      if (err.response?.status === 429) {
        setError('Bạn đã thử đăng nhập quá nhiều lần. Vui lòng đợi 1 phút rồi thử lại.');
      } else if (err.response?.data?.detail?.message) {
        setError('Email hoặc mật khẩu không đúng.');
      } else {
        setError('Không thể kết nối tới máy chủ. Vui lòng thử lại.');
      }
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="auth-body">
      <div className="page-container">
        {/* ── Cột trái: Hero + teaser ── */}
        <div className="hero-section">
          <a href="/" className="brand-logo">
            <PenLine size={32} strokeWidth={1.8} color="var(--text-dark)" />
            <span className="brand-name">AI Tutor K3</span>
          </a>

          <h1 className="hero-title">
            Trợ lý thông minh cho Slide bài giảng &amp; Nghiên cứu học thuật.
          </h1>

          <div className="teaser-window">
            <div className="teaser-topbar">
              <div className="window-controls">
                <span className="win-dot" />
                <span className="win-dot" />
                <span className="win-dot" />
              </div>
            </div>
            <div className="teaser-body">
              <div className="slide-card-preview">
                <h3 className="slide-heading">Neural 7: Hidden Layer Gradients</h3>
                <p className="slide-desc">Đồ thị tính toán mạng nơ-ron và công thức lan truyền ngược:</p>
                <div className="formula-highlight-box">
                  ∂L/∂W<sup>[1]</sup> = ∂L/∂Z<sup>[1]</sup> · (A<sup>[0]</sup>)<sup>T</sup>
                </div>
              </div>
              <div className="pin-tooltip-badge">
                <Pin size={16} />
                <div>
                  <div className="pin-text-title">[Trang 14: Hidden Layer Gradients]</div>
                  <div className="pin-text-sub">Trích dẫn xác thực từ tài liệu ✓</div>
                </div>
              </div>
            </div>
          </div>

          <div className="testimonial-card">
            <img
              className="student-avatar"
              src="https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=100&h=100&fit=crop&crop=faces"
              alt="Sinh viên"
            />
            <p className="testimonial-quote">
              "Làm chủ các học phần phức tạp với đối thoại tương tác và trích dẫn slide tức thì."
            </p>
          </div>
        </div>

        {/* ── Cột phải: Form đăng nhập ── */}
        <div className="form-card">
          <div className="form-header">
            <h2 className="form-title">Chào mừng trở lại</h2>
            <p className="form-subtitle">Đăng nhập để tiếp tục buổi học cá nhân hóa của bạn</p>
          </div>

          {error && <div className="error-banner">{error}</div>}

          <div className="social-buttons-group">
            <button type="button" className="social-btn" disabled title="Chưa hỗ trợ">
              <span>Tiếp tục với Google</span>
            </button>
            <button type="button" className="social-btn" disabled title="Chưa hỗ trợ">
              <span>Đăng nhập bằng SSO Đại học</span>
            </button>
          </div>

          <div className="divider-row">
            <span className="divider-text">— hoặc đăng nhập bằng email —</span>
          </div>

          <form className="auth-form" onSubmit={handleSubmit}>
            <div className="form-group">
              <label className="form-label" htmlFor="email">Email học tập hoặc Email cá nhân</label>
              <div className="input-wrapper">
                <input
                  id="email"
                  type="email"
                  className="form-input"
                  placeholder="student@university.edu.vn"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
            </div>

            <div className="form-group">
              <div className="label-row">
                <label className="form-label" htmlFor="password">Mật khẩu</label>
                <span className="forgot-link" title="Chưa hỗ trợ">Quên mật khẩu?</span>
              </div>
              <div className="input-wrapper">
                <input
                  id="password"
                  type={showPassword ? 'text' : 'password'}
                  className="form-input"
                  placeholder="Nhập mật khẩu của bạn"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
                <button
                  type="button"
                  className="toggle-password-btn"
                  onClick={() => setShowPassword((v) => !v)}
                  title="Hiện/ẩn mật khẩu"
                >
                  {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                </button>
              </div>
            </div>

            <div className="checkbox-group">
              <input
                id="remember"
                type="checkbox"
                className="custom-checkbox"
                checked={remember}
                onChange={(e) => setRemember(e.target.checked)}
              />
              {/* Chưa nối logic thật: refresh token backend LUÔN sống 30 ngày
                  (REFRESH_TOKEN_EXPIRE_DAYS, không phân biệt theo checkbox
                  này) — bỏ tick hiện KHÔNG làm phiên ngắn lại. Cần đổi
                  tokenStorage sang sessionStorage khi bỏ tick để đúng nghĩa
                  "không ghi nhớ"; để nguyên state ở đây, chưa wire, tránh giả
                  vờ hoạt động. */}
              <label className="checkbox-label" htmlFor="remember">
                Ghi nhớ thiết bị này trong 30 ngày
              </label>
            </div>

            <button type="submit" className="submit-btn" disabled={isSubmitting}>
              <span>{isSubmitting ? 'Đang đăng nhập...' : 'Đăng nhập vào AI Tutor'}</span>
              {!isSubmitting && <ArrowRight size={18} strokeWidth={2.4} />}
            </button>
          </form>

          <p className="auth-switch-footer">
            Chưa có tài khoản?
            <Link to="/signup" className="auth-switch-link">Đăng ký miễn phí</Link>
          </p>
        </div>
      </div>
    </div>
  );
}
