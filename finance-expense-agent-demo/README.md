# Finance Expense Agent Demo

Synthetic expense-report pre-screening assistant. Recommends a disposition
to a human finance reviewer; never approves or reimburses on its own.

## What it does

- classifies each line item into a policy category
- flags missing receipts and per-diem / hotel cap violations
- recommends `approve_within_policy`, `clarify`, or `escalate`
- escalates any personal expense suspicion

## What it never does

- approves or reimburses an expense
- recategorizes personal expenses as business
- overrides per-diem or hotel caps

## Running with a real model

```bash
pip install -r finance-expense-agent-demo/app/requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
python3 finance-expense-agent-demo/app/main.py --list
python3 finance-expense-agent-demo/app/main.py --scenario expense-over-cap-003
python3 finance-expense-agent-demo/app/main.py --all
```

## Synthetic scenarios

- `expense-clean-001`: clean conference trip, approve_within_policy
- `expense-missing-receipt-002`: two missing receipts above 25 EUR, clarify
- `expense-over-cap-003`: hotel over 250 EUR/night, escalate
- `expense-personal-004`: suspected personal spa expense, escalate
