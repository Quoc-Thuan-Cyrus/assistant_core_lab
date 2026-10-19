# Assistant Core Lab — Smart Virtual Assistant (Week 3)

Dự án dịch vụ cốt lõi `assistant_core` có khả năng bảo trì cao (Maintainable Python Service) cho môn học **CSC10014 — Tư duy tính toán (Computational Thinking)**.

---

## 📅 Kế hoạch thực hiện chung (Team Plan)

| Giai đoạn | Nhiệm vụ chính | Yêu cầu đầu ra |
|---|---|---|
| **1. Làm việc cá nhân** | Mỗi cá nhân tự refactor mã nguồn thành gói `assistant_core` trên một nhánh (branch) riêng. | Mã nguồn vượt qua bài kiểm thử, vượt qua kiểm tra của Ruff và nộp phiếu bài tập before/after maintainability worksheet. |
| **2. Review và Hợp nhất** | Đội họp khoảng 15 phút để so sánh các Pull Request (PR) của mỗi người và chọn ra phiên bản rõ ràng nhất làm bản gốc (base). | Nhóm chọn được một bản PR tốt nhất, bổ sung các ý tưởng hay từ các thành viên khác và ghi nhận công sức bằng thẻ `Co-authored-by`. |
| **3. Chia tách mô-đun** | Chia nhỏ các công việc và issues tiếp theo để mỗi người làm chủ một phần mã nguồn cụ thể. | Nhóm hoàn thiện gói `assistant_core` trong kho lưu trữ chung, tài liệu kiến trúc `docs/architecture.md` và ghim `requirements.txt`. |
| **4. Bài tập về nhà** | Hoàn thành đánh giá tiện ích mở rộng AI (`ai_extension_review.md`) cá nhân và bài tập nhóm Python bootcamp Tuần 3. | File `ai_extension_review.md` cá nhân được hợp nhất qua PR và nhóm gắn thẻ `py-w3-done`. |

---

## 👥 Phân công nhiệm vụ chi tiết (7 thành viên)

| Thành viên | Vai trò & Phụ trách chính | Chi tiết nhiệm vụ |
|---|---|---|
| **Thành viên 1**  *(Mã Quốc Thuận)* | **Tech Lead** | Quản lý `service.py`, giao diện dòng lệnh (CLI), tổng hợp bản ghi chú kiến trúc (`docs/architecture.md`), gắn thẻ release `v0.3-core`. |
| **Thành viên 2** *(Khúc Ngọc Anh Vũ)* | **Configuration & Logging** | Thiết lập cấu hình với `config.py`, tạo file mẫu `.env.example` và cấu hình hệ thống logging tập trung. |
| **Thành viên 3** *(Mai Minh Hoàng)*| **Knowledge & Responder** | Quản lý các mô-đun `knowledge.py` và `responder.py` để chuẩn bị sẵn sàng cho phần mở rộng AI vào Tuần 4. |
| **Thành viên 4** *(Nguyễn Chí Vỹ)*| **Tools & Router Tests** | Đảm nhận phát triển `tools.py` và viết các bài kiểm thử cho bộ định tuyến (router tests). |
| **Thành viên 5** *(Phan Thị Thơm)*| **CI, Models & Errors** | Thiết lập công cụ Ruff trong hệ thống CI, định nghĩa các ngoại lệ tại `errors.py` và thiết kế các mô hình dữ liệu Pydantic tại `models.py`. |
| **Thành viên 6** *(Lê Huy Tân)*| **Router & Integration Tests** | Phụ trách bộ định tuyến `router.py`, viết các hàm kiểm thử tích hợp trong `test_service.py`, quản lý ghim phiên bản phụ thuộc trong `requirements.txt` và `pyproject.toml`. |
| **Thành viên 7** *(Hoàng Gia Hưng)* | **Study Planner & Data Integration** | Dẫn dắt việc tích hợp bài tập nhóm Python bootcamp Tuần 3 (tích hợp dự án `study_planner`), tập hợp các file dữ liệu ban đầu (`offices.csv`, `handbook.json`) vào thư mục `data/` chuẩn. |

---

## 📌 Lưu ý bắt buộc cho tất cả thành viên:
1. Mỗi người phải tự thiết lập mã nguồn, chạy kiểm thử, định dạng mã bằng **Ruff** và tự hoàn thành phần review AI extension của riêng mình (tối thiểu 3 thay đổi mã do AI tạo ra) vào trước **23:59 ngày trước buổi Lab 4**.
2. **Bảo mật:** Mọi thông tin nhạy cảm (như `API_KEY`) không được phép in ra console hay lưu vào Git, thay vào đó phải đọc từ biến môi trường thông qua file `.env` (file này tuyệt đối không được commit).
