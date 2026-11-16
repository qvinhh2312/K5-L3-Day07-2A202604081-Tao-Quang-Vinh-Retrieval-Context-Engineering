# Day 7 implementation

Run commands from the repository root in PowerShell.

## Setup and ingestion

1. Create `.env` with the local `DATABASE_URL` from `.env.example`.
2. Start PostgreSQL/pgvector: `docker compose -p day7 up -d --wait`.
3. Ingest Day 6 strategies: `python -m day6_src.run ingest`.
4. Export B chunks: `python scripts/export_chunks.py --strategy B --out data/chunks_B.json`.
5. Validate benchmark and evidence: `python scripts/validate_benchmark.py`.

## Retrieval

`src.run_retrieval` compares TF-IDF, dense pgvector, BM25 and hybrid RRF on dev, plus top-k and context-budget experiments and metadata-filter ablations. It writes `results/retrieval_dev.json`. If the model is already cached and the network is unavailable, set `HF_HUB_OFFLINE=1` and `TRANSFORMERS_OFFLINE=1` for the process.

The held-out test command requires the frozen config marker and runs only BM25 baseline plus the selected BM25 configuration:

```powershell
python -m src.run_retrieval --split test --final
```

## Agent

`src.run_agent_eval` uses a real OpenAI-compatible chat completion endpoint and tool calls. Configure `AGENT_MODEL`, one API key, and optionally `OPENAI_BASE_URL` in the ignored `.env`. It writes per-question traces with token counts; provider errors are recorded and never replaced with mock answers. Keep provider credentials private.

```powershell
python -m src.run_agent_eval --split dev --config bm25_filter_selected
python -m src.run_agent_eval --split test --final --config bm25_filter_selected
python scripts/prepare_agent_review.py --split test --traces results/agent/test_bm25_filter_selected.json --outdir results/agent/review-test
```

Human reviewers must fill the generated `reviews.json` grades before running `starter/agent_metrics.py`.
