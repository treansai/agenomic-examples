from __future__ import annotations

import argparse
import json
from pathlib import Path


TRACE_PATH = Path(__file__).resolve().parents[1] / "traces" / "synthetic_claim_traces.jsonl"


def load_traces() -> list[dict]:
    lines = TRACE_PATH.read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines if line.strip()]


def print_trace_summary(traces: list[dict]) -> None:
    print("Claims Agent Demo")
    print("=================")
    for trace in traces:
        outcome = trace["expected_outcome"]
        print(f'{trace["trace_id"]}: {trace["scenario"]}')
        print(f'  label={outcome["primary_label"]} review={outcome["human_review_required"]} resolution={outcome["resolution"]}')


def print_trace(trace: dict) -> None:
    print(f'Scenario: {trace["scenario"]}')
    print(f'Trace ID: {trace["trace_id"]}')
    print(f'Customer message: {trace["input"]["customer_message"]}')
    print("Steps:")
    for step in trace["steps"]:
        detail = step.get("detail") or step.get("tool") or step.get("label") or step.get("rule")
        print(f'  - {step["type"]}: {detail}')
    print("Expected outcome:")
    print(json.dumps(trace["expected_outcome"], indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect synthetic claims-agent traces.")
    parser.add_argument("--list", action="store_true", help="List all scenarios.")
    parser.add_argument("--scenario", help="Print a full synthetic trace by trace ID.")
    args = parser.parse_args()

    traces = load_traces()

    if args.scenario:
        trace = next((item for item in traces if item["trace_id"] == args.scenario), None)
        if trace is None:
            raise SystemExit(f"Unknown scenario: {args.scenario}")
        print_trace(trace)
        return

    print_trace_summary(traces)


if __name__ == "__main__":
    main()
