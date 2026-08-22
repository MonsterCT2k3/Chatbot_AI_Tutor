import { pdfjs } from 'react-pdf';

// react-pdf cần 1 worker script riêng để parse PDF ngoài main thread — không
// tự tìm ra được worker của chính nó khi build bằng Vite, phải trỏ tay vào
// file thật trong node_modules. Import 1 lần duy nhất, dùng chung cho mọi nơi
// cần <Document>/<Page> (DocumentCard thumbnail, LessonWorkspacePage viewer).
pdfjs.GlobalWorkerOptions.workerSrc = new URL(
  'pdfjs-dist/build/pdf.worker.min.mjs',
  import.meta.url,
).toString();
