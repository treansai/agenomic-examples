# E-commerce Returns Agent Demo

Synthetic returns and refunds assistant with a hard autonomous cap.

## What it does

- classifies the return reason
- checks eligibility against window + excluded categories + fraud signals
- proposes a refund amount up to 80 EUR
- escalates anything above the cap, outside the window, in an excluded category, or with a fraud signal

## What it never does

- issues refunds above 80 EUR on its own
- overrides the return window
- accepts returns for perishables, custom, or hygiene items
- waives restocking fees without a policy basis

## Running with a real model

```bash
pip install -r ecommerce-returns-agent-demo/app/requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
python3 ecommerce-returns-agent-demo/app/main.py --list
python3 ecommerce-returns-agent-demo/app/main.py --scenario return-cap-002
python3 ecommerce-returns-agent-demo/app/main.py --all
```

## Synthetic scenarios

- `return-eligible-001`: defective lamp, in window, under cap — auto-eligible
- `return-cap-002`: defective espresso machine above cap — must escalate
- `return-window-003`: jacket returned 47 days after delivery — must escalate
- `return-excluded-004`: opened cosmetics (hygiene) — must escalate
