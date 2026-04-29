# agentlock-examples

Synthetic, public-facing examples that show how AgentLock can constrain domain agents without exposing real data, real secrets, or proprietary business logic.

These demos are designed to be read quickly:

- `claims-agent-demo` shows a customer claims assistant that can classify complaints and draft replies, but cannot commit compensation.
- `support-agent-demo` shows a SaaS support agent that can answer product questions, use synthetic account lookup context, and escalate billing issues.
- `trading-risk-agent-demo` shows a risk checker that labels proposed strategies and explains violations, but never places trades.

Everything in this repository is synthetic:

- No real customer data
- No real insurer or SaaS vendor names
- No real credentials or live endpoints
- No regulation-specific legal advice
- No trade execution logic

## Repository layout

```text
.
├── README.md
├── LICENSE
├── claims-agent-demo/
├── support-agent-demo/
├── trading-risk-agent-demo/
└── scripts/
```

Each demo includes:

- An `agent-bundle/` with prompts, contracts, tool locks, memory schema, policies, and replay manifest
- A `traces/` directory with pre-generated synthetic JSONL traces
- A small `app/` folder with a Python script that replays or summarizes the traces locally
- A demo-specific `README.md` with expected `agentlock` commands

## Quick start

The `agentlock` CLI is not required to learn from these examples. If it is installed in your environment, the expected workflow for each demo is:

```bash
agentlock validate claims-agent-demo/agent-bundle
agentlock build claims-agent-demo/agent-bundle
agentlock replay claims-agent-demo/agent-bundle --manifest claims-agent-demo/agent-bundle/evals/replay_manifest.yaml
agentlock diff claims-agent-demo/agent-bundle /path/to/modified-claims-agent-bundle
```

If the CLI is not installed, you can still inspect the bundle files directly and run the local Python helpers:

```bash
python3 scripts/generate_synthetic_traces.py
python3 claims-agent-demo/app/main.py --list
python3 support-agent-demo/app/main.py --list
python3 trading-risk-agent-demo/app/main.py --list
```

## What each demo demonstrates

| Demo | Primary value | Core AgentLock controls |
| --- | --- | --- |
| `claims-agent-demo` | Safe complaint triage and response drafting | Human approval for compensation, required policy citations, escalation on injury or identity mismatch |
| `support-agent-demo` | Trustworthy product support responses | Billing escalation, read-only account lookups, no unsupported credits or roadmap promises |
| `trading-risk-agent-demo` | Explainable pre-trade risk review | Risk labels only, hard ban on trade placement, human review on threshold breaches |

## Working with the traces

The synthetic traces are generated from curated scenarios, including edge cases:

- compensation requests that require policy support
- billing disputes that need escalation
- risk proposals that cross leverage or concentration limits
- identity mismatch, legal-threat, and missing-control situations

To regenerate the JSONL fixtures after editing the scenario source:

```bash
python3 scripts/generate_synthetic_traces.py
```

## Notes

- The YAML, Markdown, and Rego files are intentionally compact and readable.
- The lock files are illustrative examples of how a public AgentLock bundle can be organized.
- The demo apps use only the Python standard library so the repository stays easy to explore.
