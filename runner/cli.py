"""Shared CLI for the new demos.

Each demo's ``app/main.py`` is a 5-line wrapper that points this helper
at the right bundle and trace file.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .agenomic_runtime import Bundle, load_traces, print_result, run


def main(bundle_dir: Path, traces_path: Path, demo_name: str) -> None:
    parser = argparse.ArgumentParser(description=f"{demo_name} runner")
    parser.add_argument("--list", action="store_true", help="List available scenarios.")
    parser.add_argument("--scenario", help="Run one scenario by trace_id.")
    parser.add_argument("--all", action="store_true", help="Run every scenario.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the prepared input without calling the model.",
    )
    args = parser.parse_args()

    traces = load_traces(traces_path)

    if args.list or (not args.scenario and not args.all):
        print(f"{demo_name} scenarios:")
        for t in traces:
            print(f"  {t['trace_id']:<28} {t['scenario']}")
        return

    bundle = Bundle.load(bundle_dir)

    selected = (
        traces if args.all else [t for t in traces if t["trace_id"] == args.scenario]
    )
    if not selected:
        sys.exit(f"Unknown scenario: {args.scenario}")

    for trace in selected:
        if args.dry_run:
            print(f"\n=== {trace['trace_id']} (dry-run) ===")
            print(json.dumps(trace["input"], indent=2, ensure_ascii=False))
            continue
        result = run(bundle, trace["input"])
        print_result(trace["trace_id"], result)
        if "expected_outcome" in trace:
            print("expected outcome:")
            print(json.dumps(trace["expected_outcome"], indent=2, ensure_ascii=False))
