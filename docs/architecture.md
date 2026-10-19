# Kiến trúc Assistant Core

## 1. Bảng Trách nhiệm Mô-đun
| Module | Trách nhiệm |
|---|---|
| `config.py` | Đọc cấu hình từ môi trường; xác thực. |
| `errors.py` | Định nghĩa các ngoại lệ (exceptions) có tên cụ thể. |
| `models.py` | Hợp đồng công khai: Message, Response, Intent, Source. |
| `router.py` | Chọn một Intent bằng các quy tắc đơn giản. |
| `knowledge.py` | Danh bạ văn phòng (CSV) và sổ tay (JSON) kèm chức năng tìm kiếm. |
| `tools.py` | Tính toán học phí mang tính tất định (deterministic). |
| `responder.py` | Sinh phản hồi đằng sau một giao diện duy nhất (stub LLM, template). |
| `service.py` | `AssistantService.handle(Message) -> Response` (điểm vào duy nhất). |
| `logging_setup.py` | Ghi log JSON có cấu trúc. |
| `__main__.py` | Giao diện dòng lệnh (CLI). |

## 2. Giao diện Dịch vụ (Service Interface)
- `AssistantService.handle(msg: Message) -> Response`
- **Message**: text (1-2000 ký tự), session_id
- **Response**: answer, intent, sources [], degraded (True nếu dùng fallback)
- **Errors**: 
  - Đầu vào không hợp lệ -> `ValidationError`
  - Khởi động -> `ConfigError` / `DataError`
  - Lỗi nhà cung cấp (provider) không bao giờ tới được caller (dùng fallback thay thế).

## 3. Các Quyết định Thiết kế & Lý do
1. **Tính phí được xử lý trong `tools.py`, không bao giờ dùng LLM:** Đảm bảo kết quả chính xác tuyệt đối và dễ dàng viết unit test thay vì phụ thuộc vào tính ngẫu nhiên của AI.
2. **LLM được đặt sau một interface `Responder`:** Giúp bài test và hệ thống CI có thể chạy ngoại tuyến bằng một "stub" mà không cần API key thực, đồng thời dễ dàng thay đổi nhà cung cấp AI sau này.
3. **Cấu hình đọc từ biến môi trường:** Tuân thủ nguyên tắc Twelve-Factor App, mã nguồn không chứa dữ liệu nhạy cảm. File `.env.example` lập tài liệu rõ ràng cho từng biến cần thiết.