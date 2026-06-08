# Hyperliquid-style Perp Pre-trade Agent Demo

Synthetic pre-trade reviewer for a Hyperliquid-style perpetuals venue. It
sizes, scopes, and labels a proposed order — and **never** signs, broadcasts,
or moves user funds.

## What it does

- computes effective leverage, liquidation distance, and notional-vs-equity
- picks one disposition: `accept_for_human_confirmation`, `reduce_size`, `reject`
- when reducing, suggests a safer size that brings the binding limit back inside policy
- always requires a human click in the trading UI before execution

## What it never does

- signs or broadcasts a transaction
- manages private keys
- bridges or withdraws funds
- promises directional alpha — that is the signal agent's job

## Hard limits

- max effective leverage: **10x**
- min liquidation distance: **8%**
- max single-order notional: **25% of equity**

## Running with a real model

```bash
pip install -r hyperliquid-agent-demo/app/requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
python3 hyperliquid-agent-demo/app/main.py --list
python3 hyperliquid-agent-demo/app/main.py --scenario perp-high-leverage-002
python3 hyperliquid-agent-demo/app/main.py --all
```

## Synthetic scenarios

- `perp-safe-001`: 3x long BTC, within every limit
- `perp-high-leverage-002`: 11.4x leverage, must reduce
- `perp-thin-liquidation-003`: liquidation distance below 8%, must reduce
- `perp-hostile-004`: 51x leverage, must reject

## Note

"Hyperliquid-style" refers to the generic shape of an on-chain perpetuals
venue (perp markets, mark price, maintenance margin, liquidation). No real
venue, account, or price is implied.
