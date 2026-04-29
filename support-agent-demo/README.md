# Support Agent Demo

`support-agent-demo` is a synthetic SaaS support assistant. It shows how AgentLock can keep a support agent helpful on product questions while forcing safe escalation on billing-sensitive workflows.

## What it does

- answers product and configuration questions
- uses synthetic account lookup context to tailor replies
- escalates billing disputes, refund asks, and credit requests
- avoids unsupported promises about timelines, roadmap items, or account actions

## What it never does

- grants credits or refunds directly
- promises a feature release date
- claims an incident is resolved without a supporting status signal

## Expected AgentLock workflow

If `agentlock` is available in your environment, these are the expected commands:

```bash
agentlock validate support-agent-demo/agent-bundle
agentlock build support-agent-demo/agent-bundle
agentlock replay support-agent-demo/agent-bundle --manifest support-agent-demo/agent-bundle/evals/replay_manifest.yaml
agentlock diff support-agent-demo/agent-bundle /path/to/modified-support-agent-bundle
```

If `agentlock` is not installed, inspect the bundle files directly and use the local app to read the synthetic scenarios.

## Local demo app

```bash
python3 support-agent-demo/app/main.py --list
python3 support-agent-demo/app/main.py --scenario support-billing-002
```

## Synthetic scenarios included

- `support-product-001`: account-aware answer about SSO and audit logs
- `support-billing-002`: billing dispute that must escalate instead of promising a credit
- `support-edge-003`: active incident plus SLA-credit request without unsupported guarantees
