# Data Classification Agent Demo

Synthetic DLP-style classifier. Looks at a snippet, assigns one sensitivity
label, names the categories it detected, and recommends controls — without
ever moving the data or echoing full PII back to the caller.

## What it does

- detects email, phone, card PAN, IBAN, government ID, health record, credentials, precise location
- picks one label in {public, internal, confidential, restricted}
- recommends a baseline control set per label
- escalates restricted, credentials, government IDs, and health records to the DPO

## What it never does

- moves or copies the data
- applies a DLP action automatically
- echoes full PII values back — evidence is masked

## Running with a real model

```bash
pip install -r data-classification-agent-demo/app/requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
python3 data-classification-agent-demo/app/main.py --list
python3 data-classification-agent-demo/app/main.py --scenario class-restricted-creds-003
python3 data-classification-agent-demo/app/main.py --all
```

## Synthetic scenarios

- `class-public-001`: marketing blurb, public, no escalation
- `class-confidential-002`: support ticket with email + phone, confidential
- `class-restricted-creds-003`: chat snippet leaking an API token, restricted + DPO
- `class-restricted-health-004`: survey text revealing a diagnosis, restricted + DPO
- `class-pan-005`: CRM note with a full card PAN, restricted + DPO
