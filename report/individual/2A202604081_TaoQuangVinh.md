# Báo cáo cá nhân — Day 7: Agentic RAG

**Học viên:** Tào Quang Vinh · **MSSV:** 2A202604081 · **Lớp:** L3B

## Dữ liệu và benchmark

- **Corpus:** NIST, *Artificial Intelligence Risk Management Framework (AI RMF 1.0)*, January 2023. SHA-256: `7576edb531d9848825814ee88e28b1795d3a84b435b4b797d3670eafdc4a89f1`. Có 48 trang PDF vật lý, 42 trang nội dung; nguồn và quyền sử dụng được ghi trong `data/manifest.json`.
- **Index:** Dùng chunk B paragraph-aware của Day 6: 175 chunks, tối đa 800 ký tự; PostgreSQL 16 + pgvector 0.8.7, bảng `lab_chunks`, exact cosine scan. Embedding `sentence-transformers/all-MiniLM-L6-v2`, 384 chiều, `max_seq_length=256`, chạy local; chi phí embedding/search ghi nhận $0.
- **Benchmark:** 22 dev (20 answerable, 2 unanswerable) và 7 test mới (5 answerable, 2 unanswerable). q16–q20 của Day 6 được chuyển sang dev vì test cũ đã được xem. Bộ test mới dùng trang evidence 11, 12, 26, 27, 31 và không được dùng để chọn cấu hình. Hash bộ benchmark và cấu hình khóa nằm trong `results/freeze-config.json`.
- **Freeze chronology:** Nội dung benchmark và hash cấu hình đã được ghi trước lần chạy test. Git commit benchmark (`576164c`) được tạo sau lần chạy test vì quyền ghi `.git` bị chặn ở lần thử đầu; test chỉ dùng để so baseline với cấu hình đã chọn, không dùng để chỉnh cấu hình.
- **Evidence:** Validator yêu cầu source/page khớp và evidence nằm nguyên trong một chunk B. Câu unanswerable có `gold: []` cùng `absence_reason`; hai câu dev được kiểm tra trên toàn văn về GDPR và differential privacy, hai câu test về red-team hours và federated learning. Hit metrics chỉ tính 20/5 câu answerable.
- **Giới hạn benchmark:** Tài liệu đơn lẻ nên dev/test cùng chủ đề; mẫu test nhỏ (5 answerable + 2 unanswerable). Các câu q21–q25 và absence cases là bản nháp AI hỗ trợ, cần tác giả rà soát nội dung và lý do thiếu evidence trước khi nộp.

## Retrieval và thử nghiệm

Hit@1/Evidence Hit@3/Context Evidence Rate đều dùng mẫu số answerable. Thời gian là median mili-giây mỗi query cho embedding/truy vấn cục bộ, không gồm khởi động model. Chi phí retrieval local là $0; chi phí LLM chưa có vì chưa chạy agent.

| Cấu hình | Phương pháp, tham số | Giả thuyết / thay đổi | Split | Hit@1 | Evidence Hit@3 | Context Evidence Rate | Thời gian / chi phí |
|---|---|---|---|---:|---:|---:|---|
| Baseline | TF-IDF, top-3, budget 800, không filter | Lexical baseline starter | dev | 13/20 (65%) | 14/20 (70%) | 10/20 (50%) | 2.904 ms/query; $0 |
| Dense | pgvector Day 6 B, top-3, budget 800 | Dense semantic retrieval | dev | 8/20 (40%) | 11/20 (55%) | 8/20 (40%) | 119.013 ms/query; $0 |
| BM25 | BM25 k1=1.5, b=0.75, top-3, budget 800, không filter | Lexical ranking trên cùng chunks | dev | 14/20 (70%) | 16/20 (80%) | 11/20 (55%) | 2.243 ms/query; $0 |
| Hybrid | Dense + BM25, RRF k=60, pool=20; top-3, budget 800 | Hợp nhất thứ hạng hai nguồn | dev | 11/20 (55%) | 13/20 (65%) | 8/20 (40%) | 106.107 ms/query; $0 |
| Cải thiện 1 | Hybrid RRF, top-5, budget 800 | Tăng candidate/context ranking; Hit@3 giữ nguyên | dev | 11/20 (55%) | 13/20 (65%) | 8/20 (40%) | 614.1 context chars trung bình; $0 |
| Cải thiện 2 | Hybrid RRF, top-5, budget 1200 | Tăng budget để giữ evidence dài | dev | 11/20 (55%) | 13/20 (65%) | 12/20 (60%) | 968.2 context chars trung bình; $0 |
| Cấu hình đã chọn | BM25, top-3, budget 800; chỉ áp filter có trong query | Hòa Context Evidence với cải thiện 2 nhưng context ngắn hơn | dev | 15/20 (75%) | 17/20 (85%) | 12/20 (60%) | 1.649 ms/query; 637.4 context chars; $0 |
| Baseline | BM25, top-3, budget 800, không filter | So sánh trên test mới | test | 4/5 (80%) | 4/5 (80%) | 3/5 (60%) | 0.423 ms/query; $0 |
| Cấu hình đã chọn | BM25, top-3, budget 800; filter theo query | Không thay đổi sau khi xem test | test | 4/5 (80%) | 4/5 (80%) | 3/5 (60%) | 0.365 ms/query; filter 2/2; $0 |

Filter ablation trên dev: TF-IDF 10/20 context evidence (không filter) và 10/20 (filter); Dense 8/20 và 8/20; BM25 11/20 và 12/20; Hybrid top-3 8/20 và 8/20. Với các câu có filter, cấu hình filter tuân thủ 5/5 trên dev và 2/2 trên test. Filter được truyền từ phạm vi query, không suy ra từ gold.

Hai lỗi dev:

1. **q04 — retrieval miss.** BM25 top-3 trả trang 19, 10, 12, không có evidence ở trang gold 13; tăng top-k/budget ở hybrid cũng không tìm được evidence. Dense có chunk trang 13 nhưng không chứa trọn evidence nên không tính hit. Nguyên nhân chính là truy vấn diễn đạt khác với đoạn mô tả điều kiện dừng phát triển/triển khai. Đây vẫn là lỗi retrieval, không phải lỗi pack context.
2. **q07 — evidence rơi khỏi context.** BM25 tìm chunk đúng `nist-ai-100-1-para-p037-c01` ở rank 1 và Hit@3 đúng, nhưng chunk dài 749 ký tự cộng citation header vượt budget 800 nên bị bỏ. Thử top-5 riêng không sửa được; tăng budget lên 1200 đưa evidence vào context. Đây là bằng chứng cho cải thiện thứ hai.

Chọn BM25 + filter vì đạt Context Evidence `12/20`, bằng Hybrid top-5/budget-1200, nhưng context trung bình ngắn hơn (`637.4` so với `968.2` ký tự) và độ trễ cục bộ thấp hơn. Trên test, baseline và cấu hình chọn đều đạt `3/5` Context Evidence; filter không tăng retrieval hit trong 5 câu mới.

## Agent và đánh giá

Đã triển khai controller tool-calling OpenAI-compatible trong `src/agent.py`, dùng search tool thật, temperature 0, tối đa 4 lượt search, top-3 và context budget 800. `src/run_agent_eval.py` ghi trace/tokens và chạy tiếp khi một query gặp lỗi; lỗi không được thay bằng output giả. Chưa có trace agent, tổng token, chi phí LLM, grounded answer grades, citation audit hoặc abstention audit trong kết quả hiện tại. Các nội dung này phải được hoàn tất sau khi cấu hình provider/model trong `.env` và tác giả chấm thủ công; không điền số giả.

| Hạng mục | Trạng thái |
|---|---|
| Tool use, số lượt gọi, lỗi API | Chưa chạy agent thật |
| Grounded answer 0/1/2 | Chờ trace và audit thủ công |
| Citation validity/support | Chờ mở từng citation và chấm |
| Abstention và từ chối nhầm | Chờ chạy trên 2 dev + 2 test unanswerable |
| Trace/review files | Script `scripts/prepare_agent_review.py` tạo được khung sau khi có trace |

Lệnh chạy agent sau khi cấu hình provider trong `.env`:

```powershell
.\.venv\Scripts\python.exe -m src.run_agent_eval --split dev --config bm25_filter_selected
.\.venv\Scripts\python.exe -m src.run_agent_eval --split test --final --config bm25_baseline
.\.venv\Scripts\python.exe -m src.run_agent_eval --split test --final --config bm25_filter_selected
.\.venv\Scripts\python.exe .\scripts\prepare_agent_review.py --split test --traces .\results\agent\test_bm25_filter_selected.json --outdir .\results\agent\review-test
```

Sau khi điền các nhãn `null` bằng đánh giá thủ công, tổng hợp bằng `starter/agent_metrics.py` theo hướng dẫn trong `starter/README.md`.

## Tái lập và giới hạn

- `python scripts/validate_benchmark.py` kiểm tra schema, số lượng và evidence.
- `python -m src.run_retrieval --split dev` chạy các phương pháp và ablation; trên máy không có mạng nhưng model đã cache, đặt `HF_HUB_OFFLINE=1` và `TRANSFORMERS_OFFLINE=1`.
- `results/retrieval_dev.json`, `results/retrieval_test.json`, `results/freeze-config.json` lưu kết quả và cấu hình.
- PostgreSQL dùng exact scan; không có ANN. Chunk embeddings bị giới hạn 256 token trong khi chunk B tối đa 799 ký tự, nên một số đoạn có thể bị cắt khi embed. BM25, TF-IDF và dense dùng tokenization/thang điểm khác nhau; RRF chỉ hợp nhất thứ hạng. Thời gian một lượt và cỡ mẫu nhỏ không đại diện corpus khác.
- Không có OCR hoặc benchmark riêng cho bảng/ảnh; corpus chỉ là một tài liệu văn bản. Không khái quát kết quả sang nhiều tài liệu hoặc ngành khác.
