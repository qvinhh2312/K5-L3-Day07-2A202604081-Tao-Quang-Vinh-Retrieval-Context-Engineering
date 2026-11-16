# Ghi chú chấm tay – Day 7 (test) — cấu hình BASELINE

- Người chấm: Tào Quang Vinh   Ngày chấm: 16/11/2026
- Đã mở PDF/chunk để đọc từng citation: có
- Trước khi chấm; tôi đã tự đọc PDF, citation và trace rồi xác nhận từng nhãn trong `reviews.json` ngày 16/11/2026. Các câu có thể bị ảnh hưởng: q21–q25, u-test-01 và u-test-02.
- Nhận xét chung :

Lỗi chính của agent là ở khâu đóng gói context chứ không phải khâu sinh câu trả lời. Ở q22 (trang 12), chunk gold p012-c00 đứng hạng 1 nhưng dài 795 ký tự cộng header 60 ký tự là 855, vượt budget 800 nên bị bỏ; context chỉ có p042-c01 và agent từ chối. Ở q23 (trang 26) là retrieval miss: query “four AI RMF functions sequence” không đưa p026-c01 vào top-3. Ở q21, q24, q25 context có đúng đoạn gốc nên trả lời đúng và citation hỗ trợ; hai câu thiếu evidence được từ chối đúng. Điều tôi sẽ thử tiếp: không tính header vào budget hoặc cho chunk hạng 1 vượt budget, và viết lại query q23 với “any order”, “iterative”.
