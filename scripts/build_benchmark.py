"""Build the Day 7 benchmark from the reviewed Day 6 set and new cases.

The old Day 6 test questions are deliberately reassigned to dev because their
answers and results have already been observed. New test items are authored
here and must not be used for tuning.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAY6_QUESTIONS = ROOT / "data" / "benchmark_day6_seed.json"
CHUNKS_FILE = ROOT / "data" / "chunks_B.json"


def exact_evidence(chunks, page, starts_with):
    for chunk in chunks:
        if chunk["page"] == page and starts_with in chunk["text"]:
            start = chunk["text"].index(starts_with)
            tail = chunk["text"][start:]
            sentence_end = tail.find(". ")
            return tail[:sentence_end + 1] if sentence_end >= 0 else tail
    raise ValueError(f"Không tìm thấy evidence trên trang {page}: {starts_with}")


def answerable_case(q, split):
    return {
        "id": q["id"], "split": split, "answerable": True,
        "question": q["question"], "question_vi": q.get("question_vi"),
        "expected_answer": q["expected_answer"],
        "gold": [{"source_id": q["gold_source_id"], "page": q["gold_page"],
                  "evidence": q["evidence_quote"]}],
        "filter": q.get("filter"), "type": q.get("type"),
    }


def new_case(chunks, qid, question, answer, page, prefix, split="test"):
    return {"id": qid, "split": split, "answerable": True, "question": question,
            "expected_answer": answer,
            "gold": [{"source_id": "nist-ai-100-1", "page": page,
                      "evidence": exact_evidence(chunks, page, prefix)}],
            "filter": None, "type": "paraphrase"}


def unanswerable(qid, split, question, reason):
    return {"id": qid, "split": split, "answerable": False, "question": question,
            "gold": [], "absence_reason": reason, "filter": None}


def main():
    if not DAY6_QUESTIONS.exists():
        raise FileNotFoundError(f"Không tìm thấy benchmark Day 6: {DAY6_QUESTIONS}")
    old = json.loads(DAY6_QUESTIONS.read_text(encoding="utf-8"))
    chunks = json.loads(CHUNKS_FILE.read_text(encoding="utf-8"))
    # All 20 known Day 6 questions are dev; the former five test cases have
    # already been seen and are not held out for Day 7.
    dev = [answerable_case(q, "dev") for q in old]
    dev.extend([
        unanswerable("u-dev-01", "dev",
                     "Which GDPR articles does the AI RMF map its privacy subcategories to?",
                     "Đã tìm GDPR trên toàn bộ 42 trang nội dung (0 lần); phần Privacy (PDF page 22) bàn về nguyên tắc và rủi ro quyền riêng tư, không nêu điều khoản GDPR."),
        unanswerable("u-dev-02", "dev",
                     "Which differential privacy algorithm does the AI RMF recommend for protecting training data?",
                     "Đã tìm cụm differential privacy trên toàn bộ 42 trang nội dung (0 lần); tài liệu nói về privacy-enhancing techniques nhưng không chỉ định thuật toán differential privacy."),
    ])
    test = [
        new_case(chunks, "q21", "Within Part 1, when measuring impacts across a population, what should analysts keep in mind about which groups may be affected and their relationship to the system?",
                 "Because harms can affect groups differently, and potentially harmed communities may not be direct system users.", 11,
                 "Approaches for measuring impacts on a population work best"),
        new_case(chunks, "q22", "How does the AI RMF define an organization's risk tolerance?",
                 "Its readiness to bear risk in order to achieve its objectives.", 12,
                 "Risk tolerance refers to the organization"),
        new_case(chunks, "q23", "Must an organization follow the four AI RMF functions in one fixed sequence?",
                 "No. They may be performed in any order that adds value, and the process should be iterative.", 26,
                 "functions may be performed in any order"),
        new_case(chunks, "q24", "Who can set the policies that direct an organization's mission, values, culture, and risk tolerance?",
                 "Governing authorities.", 27,
                 "Governing authorities can determine the overarching policies"),
        new_case(chunks, "q25", "For the MAP 1.2 team described in Part 2, what kinds of diversity and experience should be reflected in participants?",
                 "Demographic diversity and broad domain and user experience expertise.", 31,
                 "Interdisciplinary AI actors, competencies, skills, and capacities"),
        unanswerable("u-test-01", "test",
                     "How many hours of red-team testing does the framework require before an AI system is released?",
                     "Đã tìm red team/red-team trên toàn bộ 42 trang nội dung (0 lần); tài liệu không đặt số giờ thử nghiệm bắt buộc."),
        unanswerable("u-test-02", "test",
                     "Which federated learning protocol does the AI RMF recommend?",
                     "Đã tìm federated learning trên toàn bộ 42 trang nội dung (0 lần); AI RMF không nêu giao thức học liên kết cụ thể."),
    ]
    test[0]["filter"] = {"part": "part1"}
    test[4]["filter"] = {"part": "part2"}
    for name, rows in (("benchmark_dev.json", dev), ("benchmark_test.json", test)):
        (ROOT / "data" / name).write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{name}: {len(rows)} câu; answerable={sum(x['answerable'] for x in rows)}; unanswerable={sum(not x['answerable'] for x in rows)}")


if __name__ == "__main__":
    main()
