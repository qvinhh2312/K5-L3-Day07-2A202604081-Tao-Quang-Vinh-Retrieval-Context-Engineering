# Phiếu chấm tay – Day 7 (test) — do tôi tự đọc và tự đánh giá

Người chấm đã tự đọc bằng chứng và xác nhận điểm, citation support, abstention cùng nhận xét ghi dưới đây.

- Người chấm: Tào Quang Vinh   Ngày chấm: 16/11/2026
- Đã mở PDF/chunk để đọc từng citation: có

Thang điểm: Context 0/1/2 · Answer 0/1/2 ·

## Cấu hình BASELINE (BM25, không filter)

| Câu       | Context | Answer | Citation hỗ trợ? | Lý do  |
| --------- | ------- | ------ | ---------------- | ------------------------------- |
| q21       | 2       | 2      | true             | Context có đúng câu gốc ở trang 11. Trả lời nêu đủ hai ý: tác hại có thể ảnh hưởng các nhóm khác nhau, và nhóm bị hại không nhất thiết là người dùng trực tiếp. |
| q22       | 0       | 0      | (không có)       | Đoạn gốc p012-c00 đứng hạng 1 nhưng không vào context. Context chỉ có p042-c01 (bên thứ ba), không có định nghĩa risk tolerance. Agent từ chối câu có đáp án nên Answer = 0. |
| q23       | 0       | 0      | —                | Context chỉ có p025-c00. Câu "không nhất thiết là chuỗi có thứ tự" ở đó nói về actions, không phải bốn functions. Đoạn gốc p026-c01 không vào top-3. Từ chối câu có đáp án = 0. |
| q24       | 2       | 2      | true             | Context có đúng câu về governing authorities ở trang 27. Trả lời đúng; ý thêm về senior leadership có trong cùng đoạn nên không bịa. |
| q25       | 2       | 2      | true             | Context có nguyên MAP 1.2 ở trang 31. Trả lời đúng: đa dạng nhân khẩu học và chuyên môn rộng về lĩnh vực, trải nghiệm người dùng; ý hợp tác liên ngành cũng có trong đoạn. |
| u-test-01 | –       | –      | –                | Từ chối đúng? ☒   Lý do: Tìm PDF thấy red team, red-teaming, hours đều 0 lần; framework tự nguyện, không đặt số giờ bắt buộc. Agent từ chối, không thêm khẳng định. Context chỉ là đoạn kiểm thử phần mềm ở trang 43, không có số giờ. |
| u-test-02 | –       | –      | –                | Từ chối đúng? ☒   Lý do: Tìm PDF thấy federated learning 0 lần (chỉ có "Federal" trong tên cơ quan); không có giao thức nào được khuyến nghị. Agent từ chối, không bịa. Context là định nghĩa AI system ở trang 6, không liên quan. |

## Cấu hình SELECTED (BM25 + filter suy từ query)

| Câu       | Context | Answer | Citation hỗ trợ? | Lý do (tiếng Việt, lời của tôi) |
| --------- | ------- | ------ | ---------------- | ------------------------------- |
| q21       | 2       | 2      | true             | Context có đúng câu gốc ở trang 11 (filter part1 không đổi kết quả). Trả lời đủ hai ý; citation p011-c01 hỗ trợ trực tiếp. |
| q22       | 0       | 0      | false            | Context chỉ có p027-c01, đoạn này nói ai đặt chính sách chứ không định nghĩa risk tolerance. Agent trả lời sai là định nghĩa; định nghĩa đúng ở p012-c00 (hạng 1) không vào context. Citation không hỗ trợ câu trả lời cho câu hỏi định nghĩa. |
| q23       | 0       | 0      | —                | Giống baseline: cùng query, cùng top-3, context chỉ có p025-c00, thiếu p026-c01 (functions có thể thực hiện theo thứ tự bất kỳ, quá trình lặp). Từ chối câu có đáp án nên Answer = 0. |
| q24       | 2       | 2      | true             | Context có đúng câu về governing authorities ở trang 27. Trả lời đúng và đủ; câu thêm về senior leadership được chính đoạn trích hỗ trợ. |
| q25       | 2       | 2      | true             | Context có nguyên MAP 1.2 ở trang 31 (filter part2 đúng). Trả lời đúng và đủ; citation p031-c01 hỗ trợ cả ý phụ về hợp tác liên ngành. |
| u-test-01 | –       | –      | –                | Từ chối đúng? ☒   Lý do: Cùng kết quả tìm PDF như trên (0 lần red team, hours). Cùng query và cùng context (trang 43) như baseline, vẫn từ chối đúng, không bịa số giờ. |
| u-test-02 | –       | –      | –                | Từ chối đúng? ☒   Lý do: Federated learning 0 lần trong PDF. Không có filter nào được áp dụng, kết quả giống baseline và vẫn từ chối đúng, không bịa giao thức. |

## Xác nhận câu thiếu evidence

- u-test-01 (red-team hours): đã đọc trang 7, 43, 44 và tìm từ khóa trên toàn bộ 48 trang → kết luận: tài liệu không trả lời được (red team, red-teaming, hours đều 0 lần; framework tự nguyện, không đặt số giờ).
- u-test-02 (federated learning): đã đọc trang 40, 43, 44 và tìm từ khóa trên toàn bộ 48 trang → kết luận: tài liệu không trả lời được (federated 0 lần; chỉ có “Federal” ở trang 8).

## Nhận xét chung

Lỗi chính của agent là ở khâu đóng gói context chứ không phải khâu sinh câu trả lời. Ở q22 (trang 12), chunk gold p012-c00 hạng 1 (795 ký tự cộng header 60 là 855, vượt budget 800) bị bỏ; context chỉ có p027-c01 nên agent trả lời sai (nêu ai đặt chính sách thay vì định nghĩa) và citation không hỗ trợ. Bộ lọc không giúp ở q22 vì không có filter nào được suy ra; q23 vẫn là retrieval miss ở trang 26. Ở q21, q24, q25 context có đúng đoạn gốc nên trả lời đúng; hai câu thiếu evidence được từ chối đúng. Điều tôi sẽ thử tiếp: sửa cách tính budget và thêm bước kiểm tra câu trả lời có thực sự định nghĩa đúng thuật ngữ được hỏi.
