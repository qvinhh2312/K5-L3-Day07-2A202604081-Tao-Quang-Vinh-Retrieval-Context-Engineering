# Báo cáo cá nhân — Day 7: Agentic RAG

**Học viên:** Tào Quang Vinh · **MSSV:** 2A202604081 · **Lớp:** L3B

## 1. Dữ liệu và benchmark

- **Corpus:** NIST, *Artificial Intelligence Risk Management Framework (AI RMF 1.0)*, tháng 1/2023. SHA-256: `7576edb531d9848825814ee88e28b1795d3a84b435b4b797d3670eafdc4a89f1`. PDF có 48 trang vật lý, 42 trang nội dung; nguồn và quyền sử dụng ghi trong `data/manifest.json`.
- **Index:** Chunk B kiểu paragraph-aware từ Day 6, 175 chunks, tối đa 800 ký tự; PostgreSQL 16 và pgvector 0.8.7, exact cosine scan. Embedding `sentence-transformers/all-MiniLM-L6-v2`, 384 chiều, `max_seq_length=256`, chạy local.
- **Benchmark:** 22 câu dev (20 có đáp án, 2 thiếu evidence) và 7 câu test mới (5 có đáp án, 2 thiếu evidence). q16–q20 của Day 6 được chuyển sang dev vì test cũ đã được xem. Test mới dùng evidence ở trang 11, 12, 26, 27, 31 và không dùng để chọn cấu hình.
- **Thay đổi schema:** Chỉ đổi cách lưu bộ lọc từ `filter` sang `expected_filter`/`oracle_filter`; đối chiếu hai phiên bản dev và test không thấy khác biệt nội dung nào khác.
- **Freeze:** Hash benchmark trong `results/freeze-config.json`: dev `345b0f408781ba5eace469b07b81fa844ef1b50ada3c129178aeb8c0f3d26f10`; test `4920072c4fb9bca6e09c55d6209264e64e79b5b59127f7f98123dfd0dd035e00`. Đã xác minh hash byte thô trong Git index khớp hai giá trị này sau khi loại trừ chuyển đổi line ending cho benchmark trong `.gitattributes`.
- **Thời điểm đóng băng:** Nội dung benchmark và hash được ghi trước lần chạy test. Commit benchmark `576164c` được tạo sau lần chạy test vì lần thử commit đầu bị chặn quyền ghi `.git`; giữ nguyên ghi chú này. Test chỉ dùng so sánh baseline với cấu hình đã chọn, không dùng để chỉnh cấu hình.
- **Đối chiếu PDF:** Đã đối chiếu các trang gold 11, 12, 26, 27 và 31 với q21–q25; các đoạn evidence và đáp án mong đợi khớp nội dung nguồn, chưa phát hiện lỗi benchmark. Tìm toàn văn không thấy các cụm GDPR, differential privacy, federated learning, red-team/red team hoặc yêu cầu số giờ kiểm thử. Tác giả ghi nhận đã tự đọc và xác nhận benchmark ngày 16/11/2026; xem `Phieu_cham_tay_Day7.md` và `results/AI_CONTENT_REGISTER.md`.
- **Giới hạn benchmark:** Một tài liệu duy nhất nên dev và test cùng chủ đề; test có 5 câu có đáp án nên lệch một câu tương đương 20%; tác giả ghi nhận đã tự đọc PDF và xác nhận câu hỏi, đáp án cùng các tuyên bố thiếu evidence ngày 16/11/2026 (xem `Phieu_cham_tay_Day7.md`).

## 2. Retrieval và lựa chọn cấu hình

Hit@1, Evidence Hit@3 và Context Evidence dùng mẫu số là số câu có đáp án. Thời gian là median mỗi query của retrieval cục bộ, không gồm thời gian tải model. Chi phí retrieval/embedding cục bộ là $0.

| Cấu hình | Phương pháp và tham số | Split | Hit@1 | Evidence Hit@3 | Context Evidence | Thời gian / ghi chú |
|---|---|---|---:|---:|---:|---|
| TF-IDF | top-3, budget 800 | dev | 13/20 (65%) | 14/20 (70%) | 10/20 (50%) | 1.147 ms/query |
| Dense | pgvector Day 6 B, top-3, budget 800 | dev | 8/20 (40%) | 11/20 (55%) | 8/20 (40%) | 46.857 ms/query |
| BM25 | k1=1.5, b=0.75, top-3, budget 800 | dev | 14/20 (70%) | 16/20 (80%) | 11/20 (55%) | 0.562 ms/query |
| Hybrid | Dense + BM25, RRF k=60, pool=20; top-3, budget 800 | dev | 11/20 (55%) | 13/20 (65%) | 8/20 (40%) | 45.418 ms/query |
| Hybrid top-5 | RRF, budget 800 | dev | 11/20 (55%) | 13/20 (65%) | 8/20 (40%) | Context trung bình 614.1 ký tự |
| Hybrid top-5, budget 1200 | RRF | dev | 11/20 (55%) | 13/20 (65%) | 12/20 (60%) | Context trung bình 968.2 ký tự |
| BM25 exploratory, budget 1200 | top-3 | dev | 14/20 (70%) | 16/20 (80%) | 14/20 (70%) | Thử nghiệm dev, không thay freeze |
| BM25 exploratory, budget 2500 | top-3 | dev | 14/20 (70%) | 16/20 (80%) | 16/20 (80%) | Thử nghiệm retrieval dev |
| Cấu hình freeze | BM25 top-3, budget 800; chỉ lọc khi câu hỏi ghi rõ phạm vi Part/Appendix | dev | 14/20 (70%) | 16/20 (80%) | 11/20 (55%) | 658.8 ký tự trung bình; 0.562 ms/query |
| Baseline | BM25 top-3, budget 800, không filter | test | 4/5 (80%) | 4/5 (80%) | 3/5 (60%) | 0.423 ms/query |
| Cấu hình được chọn | BM25 top-3, budget 800; filter suy từ phạm vi nêu rõ trong query | test | 4/5 (80%) | 4/5 (80%) | 3/5 (60%) | 0.365 ms/query; filter tuân thủ 2/2 câu có nêu phạm vi |

Hybrid (11/20 Hit@1) thấp hơn BM25 (14/20). Dense MiniLM riêng đạt 8/20 Hit@1 trên tập này; đây là dấu hiệu embedding yếu hơn BM25 cho một số truy vấn, và khi RRF gộp thứ hạng, các kết quả dense có thể kéo thứ hạng của một số kết quả BM25 xuống. Đây là cách giải thích phù hợp với số liệu quan sát, không phải kết luận nhân quả từ một ablation riêng.

Ablation filter trên dev: không câu nào trong 20 câu nêu Part/Appendix, nên filter query không kích hoạt; Context Evidence giữ nguyên: TF-IDF 10/20, Dense 8/20, BM25 11/20, Hybrid 8/20. Các filter q05/q08/q09/q17/q18 cũ là nhãn oracle và không được dùng khi chạy retrieval. Trên test, q21 và q25 ghi rõ phạm vi nên filter được áp dụng đúng.

Cấu hình giữ nguyên sau freeze là BM25 top-3, budget 800. Budget 1200/2500 chỉ là exploratory trên dev; không dùng kết quả test để đổi retrieval.

## 3. Ba dạng lỗi trên dev

1. **q04 — retrieval miss.** BM25 top-3 trả trang 19, 10, 12, không có evidence ở trang gold 13. Trace ghi `invalid_or_missing_citations`; `candidate_answer` của model là câu từ chối. Lỗi chính xảy ra trước bước trả lời: evidence không được retrieval/context đưa tới agent.
2. **q07 — evidence rơi khỏi context, rồi query lặp bị chặn.** BM25 tìm chunk `nist-ai-100-1-para-p037-c01` trong top-3 nhưng chunk không lọt vào context vì độ dài cùng header vượt budget 800. Trace ghi `repeated_query_blocked` sau một search; wrapper từ chối ngay, không gọi model thêm để trả lời từ context hiện có.
3. **q19 — agent tự từ chối dù đã thấy evidence.** Chunk gốc `nist-ai-100-1-para-p042-c02` có trong top-3 và context. `candidate_answer` của model là “Không đủ bằng chứng để trả lời.”; sự kiện cuối là `invalid_or_missing_citations`. Evidence đã tới context nhưng model vẫn từ chối.

Ngoài ra, q01 và q03 cũng có `invalid_or_missing_citations` với `candidate_answer` là câu từ chối. q06 và q07 gặp `repeated_query_blocked`; cơ chế chặn query lặp hiện dừng ngay nên không cho model cơ hội trả lời từ context đã có. Đây là hướng cải thiện tiếp theo, không thay đổi trong lượt này vì test đã chạy.

## 4. Agent: thay đổi vòng lặp và kết quả máy đo

`starter/agentic.py` được sửa để chặn query trùng và từ chối ngay khi gặp lại query cũ, lưu `candidate_answer`, và ghi `new_context_ids` cho mỗi search. Controller `src/agent.py` đưa query trước đó vào prompt, buộc câu trả lời sau hai search hoặc khi không có context ID mới, thử lại tối đa ba lần cho lỗi mạng tạm thời, che chuỗi có dạng API key trong lỗi HTTP và giữ candidate sai để kiểm tra. Vòng lặp tối đa ba lượt search.

### Dev: trước và sau sửa vòng lặp

| Lần chạy | Đã trả lời | Từ chối | Lỗi | Tổng search | Chạm giới hạn search |
|---|---:|---:|---:|---:|---:|
| Trước sửa, baseline | 10/22 | 11/22 | 1 | 47 | 8 câu |
| Trước sửa, selected | 8/22 | 14/22 | 0 | 55 | 11 câu |
| Sau sửa, baseline | 14/22 | 8/22 | 0 | 28 | 0 câu |
| Sau sửa, selected | 14/22 | 8/22 | 0 | 28 | 0 câu |

Baseline trước sửa có một lỗi mạng WinError 10054. Theo trace, hai cấu hình sau sửa đều từ chối 2/2 câu dev được gắn nhãn thiếu evidence, đồng thời từ chối sáu câu có đáp án.

### Dev: thử lại budget 2500 với controller cuối

Lượt chạy `bm25_dev_selected_budget2500_final` dùng controller cuối và budget 2500: 17/22 câu answered, 5/22 abstain, 0 lỗi, 25 search, 0 lần chạm giới hạn; 21,892 prompt tokens và 2,386 completion tokens, tổng 24,278. Chi phí ước tính là khoảng $0.004715. Lượt exploratory budget 2500 trước đó dùng controller cũ, đạt 18/22 answered, 4/22 abstain, 26 search và 25,098 tokens; hai lượt không so sánh trực tiếp vì controller khác nhau. Lượt mới không thay cấu hình freeze.

### Kết quả agent trên test

| Cấu hình | Answered | Abstain | Lỗi API | Search | Prompt / completion / tổng token | Chi phí ước tính |
|---|---:|---:|---:|---:|---:|---:|
| Baseline, BM25 800 | 3/7 | 4/7 | 0 | 10 | 5,314 / 418 / 5,732 | $0.00105 |
| Selected, BM25 + filter query 800 | 4/7 | 3/7 | 0 | 9 | 4,944 / 457 / 5,401 | $0.00102 |

Trace cho thấy q22: chunk gold `p012-c00` (795 ký tự) đứng hạng 1 ở cả hai cấu hình nhưng bị `pack_context` bỏ qua vì phần citation header làm block vượt budget 800. Baseline đưa `p042-c01` vào context rồi từ chối; selected đưa `p027-c01` vào context rồi trả lời về governing authorities, trong khi gold định nghĩa risk tolerance là “readiness to bear the risk”. Cả hai cấu hình đều từ chối q23 dù benchmark có đáp án; context q23 chỉ có chunk trang 25, không có đoạn gold trang 26. Đây là phân tích kỹ thuật từ trace và cách đóng gói context, không thay thế nhãn chấm thủ công.

Người chấm đã tự đọc lại PDF/citation và xác nhận các điểm, lý do trong hai phiếu. Bảng dưới đây lấy trực tiếp từ `summary_review.json` của từng cấu hình.

| Chỉ số (test) | Baseline | Selected |
|---|---:|---:|
| Grounded answer 0 / 1 / 2; trung bình /2 | 2 / 0 / 3; 1.2 | 2 / 0 / 3; 1.2 |
| Citation hợp lệ và hỗ trợ | 3/3 | 3/4 |
| Câu trả lời có citation | 3/3 | 4/4 |
| Từ chối đúng câu thiếu evidence | 2/2 | 2/2 |
| Từ chối nhầm câu có đáp án | 2/5 | 1/5 |
| Context grade 0 / 1 / 2 | 2 / 0 / 3 | 2 / 0 / 3 |
| Tool use / lỗi API | 7/7 / 0 | 7/7 / 0 |

Nhãn từng câu, căn cứ và lý do tiếng Việt nằm trong `results/agent/review-test-baseline/reviews.json` và `results/agent/review-test-selected/reviews.json`; hai tệp summary lưu các phép tổng hợp tương ứng.

Mô hình chạy qua OpenRouter là `gpt-4o-mini`. Chi phí ước tính dùng mức $0.15/M prompt token và $0.60/M completion token, không phải hóa đơn: dev baseline khoảng $0.00343; dev selected khoảng $0.00341; exploratory budget 2500 với controller cũ khoảng $0.00492; test baseline khoảng $0.00105; test selected khoảng $0.00102; budget 2500 với controller cuối khoảng $0.00472. Tổng sáu lượt thành công được liệt kê khoảng $0.01853. Retrieval và embedding cục bộ có chi phí $0.

## 5. Tái lập và giới hạn

- `python scripts/validate_benchmark.py` kiểm tra schema, số lượng và evidence; `python -m unittest discover -s tests` chạy bộ 15 unit test.
- `python -m src.run_retrieval --split dev` chạy các phương pháp và ablation. PostgreSQL dùng exact scan, không có ANN.
- Embedding bị giới hạn 256 token trong khi chunk B dài tối đa 799 ký tự; một số đoạn có thể bị cắt khi embed. BM25, TF-IDF và dense dùng tokenization/thang điểm khác nhau; RRF chỉ hợp nhất thứ hạng.
- Thời gian một lượt và cỡ mẫu nhỏ không đại diện corpus khác. Không có OCR hoặc benchmark riêng cho bảng/ảnh; corpus chỉ có một tài liệu văn bản.
- Test retrieval đã được xem trước khi sửa agent; các sửa đổi controller chỉ dựa trên dev. Các câu q21–q25; tác giả đã ghi ngày tự xác nhận benchmark trong `Phieu_cham_tay_Day7.md`.
- Rà soát không phát hiện câu hỏi hoặc đáp án gold sai. q22: chunk gold `p012-c00` bị cắt sau cụm “varied risk tolerances due to their”; câu định nghĩa risk tolerance vẫn đầy đủ trong chunk. q23: đáp án mong đợi là paraphrase và không nêu thêm trình tự thường dùng sau GOVERN; điều này không làm sai đáp án cho câu hỏi về việc có bắt buộc một thứ tự cố định hay không. Không sửa benchmark sau lần chạy test.
- Khi `repeated_query_blocked` xảy ra, agent dừng ngay và không cho model cơ hội trả lời từ context đã có (q06 và q07 trên dev). Đây là hướng cải thiện tiếp theo; không đổi trong repo hiện tại vì test đã chạy.
