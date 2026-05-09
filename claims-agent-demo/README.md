# Claims Agent Demo

`claims-agent-demo` is a synthetic insurance-style complaint assistant. It shows how Agenomic can allow useful customer support behavior while preventing unsafe autonomy around compensation.

## What it does

- classifies a customer complaint into a primary issue label
- drafts a response using neutral, policy-aware language
- cites a policy source before suggesting any compensation path
- routes compensation, injury, legal-threat, or identity-mismatch cases to a human reviewer

## What it never does

- commits cash, credits, or reimbursements on its own
- invents policy language
- discloses claim details when identity is not verified

## Bundle highlights

- `agent-bundle/behavior.contract.yaml` encodes the core constraints
- `agent-bundle/policies/compensation_policy.rego` adds an executable policy layer for compensation controls
- `agent-bundle/prompts/` contains the system prompt and reusable skills
- `traces/synthetic_claim_traces.jsonl` includes safe examples and edge cases

## Expected Agenomic workflow

If `agenomic` is available in your environment, these are the expected commands:

```bash
agenomic validate claims-agent-demo/agent-bundle
agenomic build claims-agent-demo/agent-bundle
agenomic replay claims-agent-demo/agent-bundle --manifest claims-agent-demo/agent-bundle/evals/replay_manifest.yaml
agenomic diff claims-agent-demo/agent-bundle /path/to/modified-claims-agent-bundle
```

If `agenomic` is not installed, treat the commands above as the intended workflow and inspect the bundle files directly.

## Local demo app

The included Python helper prints trace summaries and full synthetic replays:

```bash
python3 claims-agent-demo/app/main.py --list
python3 claims-agent-demo/app/main.py --scenario claim-comp-002
```

## Synthetic scenarios included

- `claim-classify-001`: routine service-delay complaint with no compensation request
- `claim-comp-002`: reimbursement request that requires a policy citation and human approval
- `claim-edge-003`: injury and legal-threat signal that forces escalation
- `claim-edge-004`: identity mismatch that blocks claim-detail disclosure
