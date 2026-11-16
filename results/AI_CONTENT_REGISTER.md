# Sổ khai báo nội dung có AI hỗ trợ

Cập nhật: 16/11/2026. Mục đích: phân biệt phần do tôi làm/kiểm chứng và phần có công cụ AI hỗ trợ. (`.env` không được quét hay mở.)

| Phần | Mức độ AI hỗ trợ | Tình trạng kiểm chứng |
|---|---|---|
| `src/filters.py`, `src/agent.py`, `src/metrics.py`, `src/run_agent_eval.py`, `src/run_retrieval.py`, `src/frozen.py`, `starter/agentic.py`, `starter/agent_metrics.py`, `scripts/build_benchmark.py`, `scripts/validate_benchmark.py` | Viết/sửa với công cụ AI lập trình | Validator và 15 unit test pass; tôi chịu trách nhiệm rà soát code |
| `scripts/check_review.py`, `starter/agent_metrics.py` | Checker và phần tổng hợp được công cụ AI rà soát/chỉnh sửa; công cụ chỉ kiểm tra cấu trúc và tính chỉ số từ nhãn đã nhập | Hai phiếu hoàn chỉnh đã qua `scripts/check_review.py`; đã tạo `summary_review.json` cho từng cấu hình. |
| `data/benchmark_test.json` (q21–q25, u-test-01/02) và u-dev-01/02 | Bản nháp câu hỏi/đáp án có AI hỗ trợ; evidence lấy từ chunk và qua validator | ☐ Tôi đã đọc PDF và xác nhận câu hỏi, đáp án, và 4 tuyên bố “không có trong tài liệu” (ngày ____/____/________) |
| `results/agent/*.json` | Trace do mô hình `gpt-4o-mini` sinh ra khi chạy agent | Dữ liệu máy sinh; tính đúng sai do tôi chấm |
| `results/agent/review-test-baseline/`, `results/agent/review-test-selected/` | Nhãn, lý do và phần nhận xét chung có AI hỗ trợ soạn. Tôi đã tự đọc lại PDF/citation và trace, rồi xác nhận toàn bộ điểm và lý do ngày 16/11/2026; nhận xét chung được ghi nhận là phần có AI hỗ trợ. | ☒ Đã chạy `scripts/check_review.py`; cả hai phiếu đạt và có `summary_review.json`. |
| `results/freeze-config.json`, `results/retrieval_dev.json` | Số liệu retrieval do chương trình tính; phần diễn giải có AI hỗ trợ | Tôi đã duyệt cách chọn cấu hình |
| Báo cáo cá nhân | ☒ Phần tổng hợp retrieval, diễn giải agent và trình bày kết quả có AI hỗ trợ; kết luận về nhãn test do tôi đọc và xác nhận | Đã rà soát ngày 16/11/2026 |

Ghi chú: các tệp chấm tạm cũ đã được xóa. Nhãn hiện tại dựa trên bản nháp có AI hỗ trợ; người chấm đã tự đọc lại bằng chứng và chấp thuận toàn bộ điểm/lý do trước khi tổng hợp. Phần hỗ trợ của AI được khai báo chung, không ghi tên công cụ cụ thể.
