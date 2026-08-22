import { useMemo, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Eye, EyeOff, PenLine, ArrowRight, Check } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import '../components/auth/AuthLayout.css';
import './SignUpPage.css';

// Dựng lại từ fe/src/mock_html_ui/auth/signup.html.
//
// "Tối thiểu 8 ký tự" và thanh đo độ mạnh mật khẩu CHỈ LÀ GỢI Ý PHÍA CLIENT —
// đã kiểm tra be/app/services/auth_service.py + schemas/auth.py: backend
// KHÔNG có bất kỳ ràng buộc độ dài/độ mạnh mật khẩu nào (SignupRequest.password
// chỉ là `str` trần). Không chặn submit chỉ vì thanh đo thấp, chỉ hiển thị gợi ý.

// 0-4, càng cao càng mạnh — tính lại từ 0 mỗi lần gõ, không cộng dồn state cũ
// (khác bản JS gốc trong mockup vốn cộng class chồng lên nhau khá rối).
function getPasswordStrength(password) {
  if (password.length >= 10 && /[0-9]/.test(password) && /[^A-Za-z0-9]/.test(password)) return 4;
  if (password.length >= 8 && /[A-Z]/.test(password)) return 3;
  if (password.length >= 6) return 2;
  if (password.length >= 1) return 1;
  return 0;
}

export default function SignUpPage() {
  const navigate = useNavigate();
  const { signup } = useAuth();

  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [agreedToTerms, setAgreedToTerms] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);

  const strength = useMemo(() => getPasswordStrength(password), [password]);
  const passwordsMismatch = confirmPassword.length > 0 && confirmPassword !== password;

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);

    if (passwordsMismatch) {
      setError('Mật khẩu xác nhận không khớp.');
      return;
    }

    setIsSubmitting(true);
    try {
      await signup({ email, password, name: fullName || null });
      navigate('/', { replace: true });
    } catch (err) {
      // Khớp be/app/routers/auth.py: 409 EMAIL_ALREADY_REGISTERED là lỗi cụ
      // thể duy nhất /auth/signup trả về ngoài lỗi mạng chung.
      if (err.response?.status === 409) {
        setError('Email này đã được đăng ký. Hãy đăng nhập hoặc dùng email khác.');
      } else {
        setError('Không thể tạo tài khoản. Vui lòng thử lại.');
      }
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="auth-body">
      <div className="page-container">
        {/* ── Cột trái: Hero + giá trị sản phẩm ── */}
        <div className="hero-section">
          <a href="/" className="brand-logo">
            <PenLine size={32} strokeWidth={1.8} color="var(--text-dark)" />
            <span className="brand-name">AI Tutor K3</span>
          </a>

          <h1 className="hero-title">
            Học tập thông minh hơn cùng AI dựa trên Slide bài giảng.
          </h1>

          <div className="features-list">
            <div className="feature-card">
              <div className="check-icon-wrapper"><Check size={18} strokeWidth={2.8} /></div>
              <p className="feature-text">
                <strong>⚡ Tìm kiếm RAG tức thì:</strong> Tra cứu và hỏi đáp chính xác trên toàn bộ tài liệu PDF & slide PPTX của bạn.
              </p>
            </div>
            <div className="feature-card">
              <div className="check-icon-wrapper"><Check size={18} strokeWidth={2.8} /></div>
              <p className="feature-text">
                <strong>📍 Trích dẫn chính xác:</strong> Highlight trực tiếp từng trang slide tương ứng, loại bỏ hoàn toàn việc AI bịa đặt.
              </p>
            </div>
            <div className="feature-card">
              <div className="check-icon-wrapper"><Check size={18} strokeWidth={2.8} /></div>
              <p className="feature-text">
                <strong>🧠 Học tập có định hướng:</strong> Hướng dẫn tư duy từng bước bám sát nội dung slide và giáo trình của bạn.
              </p>
            </div>
          </div>

          <div className="social-proof-pill">
            <div className="avatar-group">
              <img className="avatar-circle" src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=80&h=80&fit=crop&crop=faces" alt="" />
              <img className="avatar-circle" src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=80&h=80&fit=crop&crop=faces" alt="" />
              <img className="avatar-circle" src="https://images.unsplash.com/photo-1517841905240-472988babdf9?w=80&h=80&fit=crop&crop=faces" alt="" />
            </div>
            <span className="social-proof-text">Hơn 1.500+ sinh viên đang làm chủ môn AI & Khoa học máy tính</span>
          </div>
        </div>

        {/* ── Cột phải: Form đăng ký ── */}
        <div className="form-card">
          <div className="form-header">
            <h2 className="form-title">Tạo tài khoản của bạn</h2>
            <p className="form-subtitle">Đăng ký bằng email để bắt đầu các buổi học cá nhân hóa cùng AI Tutor</p>
          </div>

          {error && <div className="error-banner">{error}</div>}

          <form className="auth-form" onSubmit={handleSubmit}>
            <div className="form-group">
              <label className="form-label" htmlFor="fullName">Họ và tên</label>
              <div className="input-wrapper">
                <input
                  id="fullName"
                  type="text"
                  className="form-input"
                  placeholder="Nguyễn Văn A"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                />
              </div>
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="email">Địa chỉ Email</label>
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
              <label className="form-label" htmlFor="password">Mật khẩu</label>
              <div className="input-wrapper">
                <input
                  id="password"
                  type={showPassword ? 'text' : 'password'}
                  className="form-input"
                  placeholder="Nhập mật khẩu (khuyến nghị tối thiểu 8 ký tự)"
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
              <div className="strength-meter">
                {[1, 2, 3, 4].map((seg) => (
                  <div key={seg} className={`strength-segment ${seg <= strength ? `active-${strength}` : ''}`} />
                ))}
              </div>
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="confirmPassword">Xác nhận mật khẩu</label>
              <div className="input-wrapper">
                <input
                  id="confirmPassword"
                  type={showPassword ? 'text' : 'password'}
                  className="form-input"
                  placeholder="Nhập lại mật khẩu"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  required
                />
              </div>
              {passwordsMismatch && <span className="field-hint error">Mật khẩu chưa khớp</span>}
            </div>

            <div className="checkbox-group">
              <input
                id="termsCheck"
                type="checkbox"
                className="custom-checkbox"
                checked={agreedToTerms}
                onChange={(e) => setAgreedToTerms(e.target.checked)}
                required
              />
              <label className="checkbox-label" htmlFor="termsCheck">
                Tôi đồng ý với <a href="#">Điều khoản dịch vụ</a> &amp; <a href="#">Chính sách bảo mật</a>
              </label>
            </div>

            <button type="submit" className="submit-btn" disabled={isSubmitting || !agreedToTerms}>
              <span>{isSubmitting ? 'Đang tạo tài khoản...' : 'Tạo tài khoản & Bắt đầu học'}</span>
              {!isSubmitting && <ArrowRight size={18} strokeWidth={2.4} />}
            </button>
          </form>

          <p className="auth-switch-footer">
            Đã có tài khoản?
            <Link to="/signin" className="auth-switch-link">Đăng nhập</Link>
          </p>
        </div>
      </div>
    </div>
  );
}
