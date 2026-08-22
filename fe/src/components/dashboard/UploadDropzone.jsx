import { useRef, useState } from 'react';
import { Loader2, UploadCloud } from 'lucide-react';

// Chỉ hỗ trợ click-to-browse (input file ẩn) — KHÔNG làm drag-and-drop thật dù
// mockup gốc gợi ý "kéo thả" bằng chữ, vì cần thêm xử lý dragOver/dragLeave/drop
// event + validate file type khi thả mà chưa có yêu cầu cụ thể nào cần nó ngay;
// click vẫn đủ dùng cho luồng chính. Giữ lại text "kéo thả" trong mockup nhưng
// nói rõ trong code đây là gợi ý UI, hành vi THẬT là click.
export default function UploadDropzone({ onUpload }) {
  const inputRef = useRef(null);
  const [isUploading, setIsUploading] = useState(false);

  async function handleFileChange(e) {
    const file = e.target.files?.[0];
    e.target.value = ''; // cho phép chọn lại đúng file đó lần sau
    if (!file) return;

    setIsUploading(true);
    try {
      await onUpload(file);
    } finally {
      setIsUploading(false);
    }
  }

  return (
    <>
      <input
        ref={inputRef}
        type="file"
        accept=".pdf,.pptx"
        style={{ display: 'none' }}
        onChange={handleFileChange}
      />
      <button
        type="button"
        className="dropzone-card"
        onClick={() => inputRef.current?.click()}
        disabled={isUploading}
      >
        {isUploading ? <Loader2 size={44} className="spin-icon" color="var(--amber-accent)" /> : <UploadCloud size={44} color="var(--amber-accent)" strokeWidth={1.6} />}
        <div className="dropzone-text">
          {isUploading ? 'Đang tải lên...' : 'Bấm để chọn tài liệu (PDF hoặc PPTX)'}
        </div>
      </button>
    </>
  );
}
