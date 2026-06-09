# DevOps Incident Agent Demo

Synthetic on-call assistant. Shows how Agenomic can keep an LLM useful
for incident triage while preventing it from ever executing a destructive
action against production.

## What it does

- assigns a severity to an alert
- summarizes a likely cause from logs and metrics
- proposes a remediation plan that a human on-call executes
- always escalates customer impact, data loss, and critical alerts

## What it never does

- restarts, rolls back, or scales a service
- modifies DNS or rotates credentials
- pages customers or writes customer-facing messages

## Running with a real model

```bash
pip install -r devops-incident-agent-demo/app/requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
python3 devops-incident-agent-demo/app/main.py --list
python3 devops-incident-agent-demo/app/main.py --scenario incident-checkout-002
python3 devops-incident-agent-demo/app/main.py --all
```

## Synthetic scenarios

- `incident-info-001`: noisy informational alert, no escalation
- `incident-checkout-002`: customer-facing 5xx spike, must escalate with a rollback plan
- `incident-dataloss-003`: backup integrity failure, must escalate as critical
