# Sổ khai báo nội dung có AI hỗ trợ

Cập nhật: 16/11/2026. Sổ này ghi rõ phần có AI hỗ trợ và phần người học tự đọc, kiểm tra, xác nhận. Không đưa `.env` vào nội dung rà soát.

| Phần | AI hỗ trợ | Người học kiểm tra/xác nhận |
|---|---|---|
| `src/filters.py`, `src/agent.py`, `src/metrics.py`, `src/run_agent_eval.py`, `src/run_retrieval.py`, `src/frozen.py`, `starter/agentic.py`, `starter/agent_metrics.py`, `scripts/build_benchmark.py`, `scripts/validate_benchmark.py` | Hỗ trợ viết và sửa code | Validator và 15 unit test đạt; người học rà soát code |
| `scripts/check_review.py`, `starter/agent_metrics.py` | Hỗ trợ rà soát/chỉnh checker và phần tổng hợp; checker chỉ tính chỉ số từ nhãn đã nhập | Hai bộ review qua checker và có `summary_review.json` |
| `data/benchmark_test.json` (q21–q25, u-test-01/02) và u-dev-01/02 | Hỗ trợ tạo bản nháp câu hỏi/đáp án và các tuyên bố thiếu evidence; evidence lấy từ chunk, benchmark qua validator | Người học ghi nhận đã đọc PDF và xác nhận câu hỏi, đáp án, bốn tuyên bố thiếu evidence ngày 16/11/2026; xem `Phieu_cham_tay_Day7.md` |
| `results/agent/*.json` | Trace do `gpt-4o-mini` sinh khi chạy agent | Trace là dữ liệu máy sinh; người học chấm kết quả |
| `results/agent/review-test-baseline/`, `results/agent/review-test-selected/` | Bản nháp điểm, lý do và nhận xét chung có AI hỗ trợ | Người học đọc PDF/citation/trace và xác nhận toàn bộ điểm, lý do ngày 16/11/2026; hai bộ review qua checker |
| `results/freeze-config.json`, `results/retrieval_dev.json` | Số liệu do chương trình tính; phần diễn giải có AI hỗ trợ | Người học duyệt cách chọn cấu hình |
| Báo cáo cá nhân | Hỗ trợ tổng hợp retrieval, diễn giải agent và biên tập báo cáo | Người học rà soát và xác nhận ngày 16/11/2026; kết luận nhãn review dựa trên việc tự đọc bằng chứng |
