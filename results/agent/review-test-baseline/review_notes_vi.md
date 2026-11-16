# Ghi chú chấm tay – Day 7 (test) — cấu hình BASELINE

- Người chấm: Tào Quang Vinh   Ngày chấm: 16/11/2026
- Đã mở PDF/chunk để đọc từng citation: ☒ có
- Trước khi chấm, tôi ☐ chưa / ☒ đã xem gợi ý của công cụ AI. Bản nháp nhãn và lý do có AI hỗ trợ soạn sau khi đối chiếu PDF NIST.AI.100-1 và trace; tôi đã tự đọc lại bằng chứng/citation và xác nhận toàn bộ điểm, lý do trong reviews.json. Các câu có thể bị ảnh hưởng: q21, q22, q23, q24, q25, u-test-01, u-test-02.
- Nhận xét chung (3-5 câu):

Lỗi chính của agent là ở khâu chọn context chứ không phải khâu sinh câu trả lời: ở q22 chunk gốc đứng hạng 1 nhưng context cuối chỉ có đoạn hạng 2, nên agent từ chối câu có đáp án; q23 cũng từ chối vì không tìm được trang 26.

Bằng chứng: q22 (trang 12, chunk p012-c00 hạng 1 nhưng không vào context) và q23 (trang 26, chunk p026-c01 không vào top-3). Ở q21, q24, q25, context có đúng đoạn gốc thì câu trả lời đúng và citation hỗ trợ. Hai câu thiếu evidence đều được từ chối đúng; tôi đã tìm PDF và thấy red team, federated learning đều 0 lần. Điều tôi sẽ thử tiếp: chọn context theo thứ hạng và để model thấy chunk hạng 1, thêm query viết lại cho câu hỏi về thứ tự các function.
