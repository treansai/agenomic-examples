# Trading Risk Agent Demo

`trading-risk-agent-demo` is a synthetic trading-assistant risk checker. It demonstrates how Agenomic can support a pre-trade control function without letting the agent execute trades or act as an autonomous portfolio manager.

## What it does

- reviews a proposed strategy against synthetic leverage, concentration, and event-risk limits
- assigns a risk label such as `green`, `amber`, or `red`
- explains which rule was triggered and whether human review is required

## What it never does

- places, routes, or suggests executable trades
- creates order tickets
- bypasses hard risk limits

## Expected Agenomic workflow

If `agenomic` is available in your environment, these are the expected commands:

```bash
agenomic validate trading-risk-agent-demo/agent-bundle
agenomic build trading-risk-agent-demo/agent-bundle
agenomic replay trading-risk-agent-demo/agent-bundle --manifest trading-risk-agent-demo/agent-bundle/evals/replay_manifest.yaml
agenomic diff trading-risk-agent-demo/agent-bundle /path/to/modified-trading-risk-agent-bundle
```

If `agenomic` is not installed, inspect the bundle files directly and use the local app to browse the synthetic traces.

## Local demo app

```bash
python3 trading-risk-agent-demo/app/main.py --list
python3 trading-risk-agent-demo/app/main.py --scenario risk-check-002
```

## Synthetic scenarios included

- `risk-check-001`: strategy stays inside leverage and concentration limits
- `risk-check-002`: hard limit breach that must be labeled `red`
- `risk-check-003`: incomplete controls and event risk that require human review
