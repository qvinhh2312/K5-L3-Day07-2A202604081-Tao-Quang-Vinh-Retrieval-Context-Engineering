"""Kiểm tra phiếu review đã hoàn tất rồi tổng hợp chỉ số."""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AI_NAME = re.compile(r"\b(ai|codex|gpt|chatgpt|claude|llm|copilot|gemini)\b", re.I)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Kiểm tra phiếu review, sau đó tổng hợp kết quả."
    )
    parser.add_argument("--dir", type=Path, required=True)
    parser.add_argument("--split", choices=("dev", "test"), default="test")
    parser.add_argument("--min-reason-chars", type=int, default=25)
    args = parser.parse_args()
    folder = args.dir if args.dir.is_absolute() else ROOT / args.dir

    def load(name: str):
        return json.loads((folder / name).read_text(encoding="utf-8"))

    cases, traces, reviews = load("cases.json"), load("traces.json"), load("reviews.json")
    case_ids = {row.get("id") for row in cases}
    trace_by_id = {row.get("query_id"): row for row in traces}
    review_by_id = {row.get("query_id"): row for row in reviews}
    errors: list[str] = []
    warnings: list[str] = []
    seen_reasons: dict[str, list[str]] = {}

    if len(case_ids) != len(cases):
        errors.append("cases.json có ID bị trùng")
    if len(trace_by_id) != len(traces) or set(trace_by_id) != case_ids:
        errors.append("ID trong traces.json không khớp chính xác với cases.json")
    if len(review_by_id) != len(reviews) or set(review_by_id) != case_ids:
        errors.append("ID trong reviews.json không khớp chính xác với cases.json")

    for case in cases:
        query_id = case.get("id", "?")
        review, trace = review_by_id.get(query_id), trace_by_id.get(query_id)
        if review is None or trace is None:
            continue

        reviewer = review.get("reviewer")
        if not isinstance(reviewer, str) or len(reviewer.strip()) < 3:
            errors.append(f"{query_id}: thiếu reviewer (tên người chấm)")
        elif AI_NAME.search(reviewer):
            errors.append(f"{query_id}: reviewer phải là tên người, không phải tên công cụ AI")

        basis = review.get("review_basis")
        if not isinstance(basis, str) or len(basis.strip()) < 15:
            errors.append(f"{query_id}: review_basis cần ghi chunk/trang đã đọc và ngày chấm")
        reason = review.get("ly_do_vi")
        if not isinstance(reason, str) or len(reason.strip()) < args.min_reason_chars:
            errors.append(f"{query_id}: ly_do_vi cần có ít nhất {args.min_reason_chars} ký tự")
        else:
            seen_reasons.setdefault(reason.strip(), []).append(query_id)

        citations, support = trace.get("citations"), review.get("citation_support")
        if not isinstance(citations, list) or not isinstance(support, list):
            errors.append(f"{query_id}: citations và citation_support phải là danh sách")
        elif len(support) != len(citations) or any(type(value) is not bool for value in support):
            errors.append(f"{query_id}: cần một nhãn true/false trong citation_support cho mỗi trích dẫn")

        if case.get("answerable"):
            for key in ("answer_grade", "context_grade"):
                value = review.get(key)
                if type(value) is not int or value not in (0, 1, 2):
                    errors.append(f"{query_id}: {key} phải là 0, 1 hoặc 2")
            if trace.get("status") == "abstain" and review.get("answer_grade") != 0:
                errors.append(f"{query_id}: câu có đáp án nhưng bị từ chối phải nhận answer_grade 0")
        else:
            value = review.get("abstention_correct")
            if type(value) is not bool:
                errors.append(f"{query_id}: abstention_correct phải là true hoặc false")
            elif value and trace.get("status") != "abstain":
                errors.append(f"{query_id}: nhãn từ chối đúng không khớp trạng thái trong trace")

    for reason, query_ids in seen_reasons.items():
        if len(query_ids) > 1:
            warnings.append(f"lý do giống hệt nhau ở {query_ids}; hãy ghi lý do riêng cho từng câu")
    for warning in warnings:
        print("CẢNH BÁO:", warning)
    if errors:
        print("CHƯA ĐẠT, cần sửa:")
        for error in errors:
            print(" -", error)
        raise SystemExit(1)

    output = folder / "summary_review.json"
    command = [
        sys.executable,
        str(ROOT / "starter" / "agent_metrics.py"),
        "--cases", str(folder / "cases.json"),
        "--traces", str(folder / "traces.json"),
        "--reviews", str(folder / "reviews.json"),
        "--split", args.split,
        "--output", str(output),
    ]
    raise SystemExit(subprocess.run(command, cwd=ROOT).returncode)


if __name__ == "__main__":
    main()
