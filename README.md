# agenomic-examples

Synthetic, public-facing examples that show how Agenomic can constrain domain agents without exposing real data, real secrets, or proprietary business logic.

These demos are designed to be read quickly:

Read-only trace demos (no API key needed):

- `claims-agent-demo` — customer claims assistant that classifies complaints and drafts replies, but cannot commit compensation.
- `support-agent-demo` — SaaS support agent that answers product questions and escalates billing issues.
- `trading-risk-agent-demo` — risk checker that labels proposed strategies but never places trades.

Live-LLM demos (call a real provider; see each demo's README):

- `hr-agent-demo` — answers employee onboarding/leave questions, never approves leave or modifies payroll.
- `devops-incident-agent-demo` — triages alerts and proposes remediation plans for a human on-call to execute.
- `ecommerce-returns-agent-demo` — handles returns under an 80 EUR autonomous refund cap, escalates above.
- `finance-expense-agent-demo` — pre-screens expense reports against per-diem and receipt rules.
- `trading-signals-agent-demo` — emits directional equity signals with explicit confidence, never executes.
- `hyperliquid-agent-demo` — pre-trade reviewer for a Hyperliquid-style perp venue, never signs or broadcasts.
- `data-classification-agent-demo` — labels record snippets, recommends controls, never echoes PII back.

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
├── hr-agent-demo/
├── devops-incident-agent-demo/
├── ecommerce-returns-agent-demo/
├── finance-expense-agent-demo/
├── trading-signals-agent-demo/
├── hyperliquid-agent-demo/
├── data-classification-agent-demo/
├── runner/
└── scripts/
```

Each demo includes:

- An `agent-bundle/` with prompts, contracts, tool locks, memory schema, policies, and replay manifest
- A `traces/` directory with pre-generated synthetic JSONL traces
- A small `app/` folder with a Python script that replays or summarizes the traces locally
- A demo-specific `README.md` with expected `agenomic` commands

## Quick start

The `agenomic` CLI is not required to learn from these examples. If it is installed in your environment, the expected workflow for each demo is:

```bash
agenomic validate claims-agent-demo/agent-bundle
agenomic build claims-agent-demo/agent-bundle
agenomic replay claims-agent-demo/agent-bundle --manifest claims-agent-demo/agent-bundle/evals/replay_manifest.yaml
agenomic diff claims-agent-demo/agent-bundle /path/to/modified-claims-agent-bundle
```

If the CLI is not installed, you can still inspect the bundle files directly and run the local Python helpers:

```bash
python3 scripts/generate_synthetic_traces.py
python3 claims-agent-demo/app/main.py --list
python3 support-agent-demo/app/main.py --list
python3 trading-risk-agent-demo/app/main.py --list
```

## Live-LLM demos

The seven demos under `hr-agent-demo`, `devops-incident-agent-demo`,
`ecommerce-returns-agent-demo`, `finance-expense-agent-demo`,
`trading-signals-agent-demo`, `hyperliquid-agent-demo`, and
`data-classification-agent-demo` each ship a small `app/main.py` that
loads the agent bundle, calls the provider declared in
`agent-bundle/agent.lock.yaml`, and checks the model's JSON output
against the behavior contract.

```bash
pip install anthropic pyyaml
export ANTHROPIC_API_KEY=sk-ant-...
python3 hr-agent-demo/app/main.py --list
python3 hr-agent-demo/app/main.py --scenario hr-leave-002
python3 hr-agent-demo/app/main.py --all
# add --dry-run to inspect the input payload without calling the model
```

Switch a demo to OpenAI by editing its `agent.lock.yaml`
(`provider: openai`, `name: gpt-4.1-mini`) and exporting `OPENAI_API_KEY`
instead.

The shared runtime lives in `runner/agenomic_runtime.py` and is intentionally
minimal — it is here so the demos can be exercised end-to-end against a
real model, not as a replacement for the full Agenomic runtime.

## What each demo demonstrates

| Demo | Primary value | Core Agenomic controls |
| --- | --- | --- |
| `claims-agent-demo` | Safe complaint triage and response drafting | Human approval for compensation, required policy citations, escalation on injury or identity mismatch |
| `support-agent-demo` | Trustworthy product support responses | Billing escalation, read-only account lookups, no unsupported credits or roadmap promises |
| `trading-risk-agent-demo` | Explainable pre-trade risk review | Risk labels only, hard ban on trade placement, human review on threshold breaches |
| `hr-agent-demo` | Employee policy questions | No leave approval, no payroll change, escalation on exceptions and cross-employee requests |
| `devops-incident-agent-demo` | Production alert triage | Plans only — no restart, rollback, scale, DNS, or credential change |
| `ecommerce-returns-agent-demo` | Returns & refunds under an 80 EUR cap | Hard refund cap, 30-day window, excluded categories, fraud-signal escalation |
| `finance-expense-agent-demo` | Expense-report pre-screening | Per-diem and hotel caps, receipt rule, personal-expense detection, recommend not approve |
| `trading-signals-agent-demo` | Explainable directional signals | Flat below confidence 0.55, earnings-window escalation, never executes |
| `hyperliquid-agent-demo` | Perpetuals pre-trade review | 10x leverage cap, 8% liquidation distance, never signs or broadcasts |
| `data-classification-agent-demo` | Snippet sensitivity labeling | Masked evidence only, credentials/government IDs/health records always restricted, DPO review |

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
- The lock files are illustrative examples of how a public Agenomic bundle can be organized.
- The demo apps use only the Python standard library so the repository stays easy to explore.

## License

Copyright (C) 2026 Agenomic Contributors. GNU Affero General Public License
v3.0 (`AGPL-3.0-only`). See [LICENSE](LICENSE).

This repository is part of the Agenomic Community edition. Agenomic Cloud and
Enterprise components live in separate, private repositories and are not
covered by this license.
