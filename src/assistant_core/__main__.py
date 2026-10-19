import logging
import sys

from assistant_core.config import load_settings
from assistant_core.knowledge import OfficeDirectory
from assistant_core.logging_setup import JsonFormatter
from assistant_core.models import Message
from assistant_core.responder import StubLLMResponder
from assistant_core.service import AssistantService


def main():
    # 1. Thiết lập logging in ra stderr
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(JsonFormatter())
    logger = logging.getLogger("assistant_core")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    # 2. Lấy câu hỏi từ dòng lệnh
    if len(sys.argv) < 2:
        print("Usage: python -m assistant_core <message>")
        sys.exit(1)
    user_text = " ".join(sys.argv[1:])

    # 3. Khởi tạo cấu hình và dữ liệu
    settings = load_settings()
    offices_path = settings.data_dir / "offices.csv"
    offices = OfficeDirectory.from_csv(offices_path)

    # Tạo class giả cho Handbook (vì ta chưa hoàn thiện phần này)
    class DummyHandbook:
        def search(self, text):
            return None

    # 4. Khởi tạo Service
    responder = StubLLMResponder()
    service = AssistantService(settings, offices, DummyHandbook(), responder)

    # 5. Xử lý tin nhắn và in kết quả ra stdout
    msg = Message(text=user_text)
    logger.info("handled")
    response = service.handle(msg)

    print(response.answer)


if __name__ == "__main__":
    main()
