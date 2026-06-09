# Trading Signals Agent Demo

Synthetic equity signal generator. Distinct from `trading-risk-agent-demo`:
this one **produces** signals, the other **reviews** strategies. Both refuse
to execute trades.

## What it does

- emits a directional signal in {long, short, flat} with a confidence in [0, 1]
- explains the signal by naming the decisive input feature(s)
- defaults to `flat` when confidence < 0.55
- escalates earnings windows and extreme news volatility

## What it never does

- places orders or modifies positions
- gives personalized investment advice
- moves funds

## Running with a real model

```bash
pip install -r trading-signals-agent-demo/app/requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
python3 trading-signals-agent-demo/app/main.py --list
python3 trading-signals-agent-demo/app/main.py --scenario signal-earnings-003
python3 trading-signals-agent-demo/app/main.py --all
```

## Synthetic scenarios

- `signal-breakout-001`: clean breakout, long signal, no escalation
- `signal-range-002`: rangebound, flat signal with low confidence
- `signal-earnings-003`: strong setup but earnings tomorrow, must escalate
- `signal-news-shock-004`: regulatory probe, short with extreme volatility, escalate
