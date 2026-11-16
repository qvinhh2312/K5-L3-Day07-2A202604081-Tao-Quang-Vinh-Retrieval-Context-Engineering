# Ghi chú chấm tay – Day 7 (test) — cấu hình SELECTED

- Người chấm: Tào Quang Vinh   Ngày chấm: 16/11/2026
- Đã mở PDF/chunk để đọc từng citation: ☒ có
- Trước khi chấm, tôi đã xem gợi ý của công cụ AI. Bản nháp điểm và lý do có AI hỗ trợ; tôi đã tự đọc PDF, citation và trace rồi xác nhận từng nhãn trong `reviews.json` ngày 16/11/2026. Các câu có thể bị ảnh hưởng: q21–q25, u-test-01 và u-test-02.
- Nhận xét chung:

Lỗi chính của agent là ở khâu đóng gói context chứ không phải khâu sinh câu trả lời. Ở q22 (trang 12), chunk gold p012-c00 hạng 1 (795 ký tự cộng header 60 là 855, vượt budget 800) bị bỏ; context chỉ có p027-c01 nên agent trả lời sai (nêu ai đặt chính sách thay vì định nghĩa) và citation không hỗ trợ. Bộ lọc không giúp ở q22 vì không có filter nào được suy ra; q23 vẫn là retrieval miss ở trang 26. Ở q21, q24, q25 context có đúng đoạn gốc nên trả lời đúng; hai câu thiếu evidence được từ chối đúng. Điều tôi sẽ thử tiếp: sửa cách tính budget và thêm bước kiểm tra câu trả lời có thực sự định nghĩa đúng thuật ngữ được hỏi.
