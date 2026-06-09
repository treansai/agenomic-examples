# Shared runtime

`agenomic_runtime.py` is a tiny helper used by every new demo's
`app/main.py`. It loads the agent bundle (system prompt + skills +
behavior contract + agent.lock), calls the LLM provider declared in the
lock, extracts the JSON response, and checks it against the contract.

It is intentionally minimal: it does not replace a real Agenomic runtime
(no Rego execution, no tool gating, no replay diffing). It is here so the
demos can be tested end-to-end against a live model.

## Providers

- `anthropic` — needs `anthropic>=0.40` and `ANTHROPIC_API_KEY`
- `openai` — needs `openai>=1.40` and `OPENAI_API_KEY`

The provider and model are read from each bundle's `agent.lock.yaml`.

## Usage

Each demo has its own `app/main.py`:

```bash
pip install anthropic pyyaml
export ANTHROPIC_API_KEY=sk-ant-...
python3 hr-agent-demo/app/main.py --scenario hr-leave-001
python3 hr-agent-demo/app/main.py --list
python3 hr-agent-demo/app/main.py --all
```
