import hashlib
import json
from pathlib import Path


def verify_freeze(root: Path) -> dict:
    marker = root / "results" / "freeze-config.json"
    if not marker.exists():
        raise RuntimeError("Missing results/freeze-config.json; freeze the dev-selected config first")
    freeze = json.loads(marker.read_text(encoding="utf-8"))
    if freeze.get("status") != "frozen":
        raise RuntimeError("Config marker is not frozen")
    if not freeze.get("test_eligible", True):
        raise RuntimeError(freeze.get("test_block_reason", "Test split is not eligible; prepare a fresh held-out test"))
    for relpath, expected in freeze.get("benchmark_files_sha256", {}).items():
        path = root / relpath
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected.lower():
            raise RuntimeError(f"Benchmark changed after freeze: {relpath}")
    return freeze
