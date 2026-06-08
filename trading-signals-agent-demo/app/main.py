from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from runner.cli import main  # noqa: E402

BUNDLE_DIR = Path(__file__).resolve().parents[1] / "agent-bundle"
TRACES_PATH = (
    Path(__file__).resolve().parents[1] / "traces" / "synthetic_signals_traces.jsonl"
)

if __name__ == "__main__":
    main(BUNDLE_DIR, TRACES_PATH, demo_name="trading-signals-agent-demo")
