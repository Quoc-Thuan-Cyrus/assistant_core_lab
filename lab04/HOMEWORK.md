# Lab 4 — Bài tập về nhà (Homework)

## H1 — Thêm endpoint GET /v1/offices
- **Thực hiện:**
  - Bổ sung phương thức `all()` trong lớp `OfficeDirectory` (`src/assistant_core/knowledge.py`) trả về danh sách các văn phòng được sắp xếp theo tên (thứ tự chữ cái).
  - Thêm endpoint `@app.get("/v1/offices")` trong `src/assistant_api/main.py`.
  - Bổ sung 2 bài kiểm thử trong `tests/test_api.py`: kiểm tra status code 200, kiểm tra danh sách có chứa văn phòng `"Library"` và xác nhận thứ tự sắp xếp theo tên.

---

## H2 — Đoạn phản tư (Reflection - 5 dòng)

1. Ở Lab 3, việc gọi trực tiếp `service.handle()` là lời gọi hàm nội bộ (in-process function call) diễn ra hoàn toàn trong cùng một không gian bộ nhớ của chương trình Python.
2. Sang Lab 4, dịch vụ được đóng gói thành Web API và giao tiếp thông qua giao thức mạng HTTP chuẩn hóa với định dạng trao đổi dữ liệu JSON (`POST /v1/chat`).
3. Kiến trúc này giúp vượt qua ranh giới tiến trình, cho phép các client chạy ở những máy tính hoặc môi trường độc lập (trình duyệt web, ứng dụng di động, các service khác) có thể tái sử dụng dịch vụ dễ dàng.
4. Nhóm phát triển ưa chuộng HTTP API vì nó tách biệt hoàn toàn giữa client và server (Decoupling), giúp phân chia công việc độc lập và nâng cấp logic backend mà không ảnh hưởng phía frontend.
5. Tuy nhiên, việc chuyển đổi sang API cũng đòi hỏi phải xử lý các vấn đề mạng đặc thù như độ trễ, kiểm tra hợp lệ dữ liệu (validation), xác thực bảo mật và xử lý mã lỗi HTTP chuẩn mực.

---

## Bonus — Giới hạn tốc độ truy cập (Rate Limiting)
- Tích hợp lớp `RateLimiter` (`src/assistant_api/ratelimit.py`) vào endpoint `POST /v1/chat`.
- Nhận diện địa chỉ client từ request (`request.client.host`) và giới hạn tần suất yêu cầu trong cửa sổ thời gian 60 giây.
- Khi người dùng gửi vượt quá ngưỡng cấu hình, hệ thống trả về mã lỗi `HTTP 429 Too Many Requests`.
- Kiểm thử tự động `test_rate_limit` trong `tests/test_api.py` đã kích hoạt và vượt qua kiểm thử thành công.
