# Prompt Registry LangGraph Demo

`prompt-registry-langgraph-demo` is a synthetic refund-planning graph whose
system prompt comes from a managed prompt bundle instead of a string in the
code. It shows that a LangGraph thread paused for human approval keeps the
prompts it started with, across a process restart, even after production
moved to a new prompt version.

## What it does

- loads `prompt-bundle.json`, the production prompts of the refund agent, and
  checks it against the digest pinned in `app/main.py`
- binds the graph with `bind_langgraph(..., offline=True)`, so every thread is
  pinned to one prompt manifest when it starts
- runs thread `refund-42` until the `approve` node interrupts for a human
  decision, with checkpoints in SQLite and thread pins in a local binding store
- simulates a promotion: production now points to version 2 of the planner
  prompt, shipped as a new bundle with a new pinned digest
- restarts in a new Python process, resumes `refund-42` on its original
  prompts, and starts thread `refund-43` on the new ones
- checks both outcomes and exits non-zero if either thread used the wrong
  prompts

## What it never does

- opens a network connection or reads an API key: the model is LangChain's
  `GenericFakeChatModel`
- falls back to an inline prompt string: a slot missing from the pinned
  manifest is an error
- re-resolves the production channel on resume: the paused thread is answered
  from the bundle it was pinned to

## Files

```text
prompt-registry-langgraph-demo/
├── README.md
├── prompt-bundle.json
└── app/
    ├── main.py
    └── requirements.txt
```

`prompt-bundle.json` is an `agenomic.prompt_bundle/v1` document: the
production release of the refund agent, which pins version 1 of
`prm_refund_planner` in the slot `planner.instructions`.

## Run it

Python 3.11 or later. From the repository root:

```bash
python3 -m venv .venv
.venv/bin/pip install -r prompt-registry-langgraph-demo/app/requirements.txt
.venv/bin/python prompt-registry-langgraph-demo/app/main.py
```

Managed prompts are newer than the `agenomic` 0.1.3 release on PyPI. Until a
release ships `agenomic.prompts`, install the SDK from a checkout of the
public `agenomic-python` repository, here cloned next to this one, in the
same command:

```bash
.venv/bin/pip install -e ../agenomic-python \
  -r prompt-registry-langgraph-demo/app/requirements.txt
```

`requirements.txt` pins the LangGraph point the Python SDK is tested on:
`langgraph` 1.2.11, `langgraph-checkpoint` 4.2.0, `langgraph-prebuilt` 1.1.0,
`langgraph-sdk` 0.4.4, `langchain-core` 1.6.3, and the SQLite checkpointer
`langgraph-checkpoint-sqlite` 3.1.1 with `aiosqlite` 0.22.1.

Expected output:

```text
process 1: refund-42 paused on ['approve the refund plan?']
process 1: plan: Plan the refund in three steps: confirm the order, check the return window, refund the card.
simulation of the governed path: production now points to version 2,
shipped as prompt-bundle-v2.json with a new pinned digest; in Agenomic
Cloud that move is an approved, signed-in action
process 2: refund-42 -> ['plan: Plan the refund in three steps: confirm the order, check the return window, refund the card.', 'approve: approved: Plan the refund in three steps: confirm the order, check the return window, refund the card.']
process 2: refund-43 -> ['plan: Plan the refund in two steps: confirm the order, then offer a store voucher.']
the resumed thread kept sha256:a8357e64d16f and the new thread uses sha256:a60f7ca8eaf4
```

## How the bundle is trusted

`prompt-bundle.json` is unsigned and authenticated by its
`prompt_bundle_digest`, which `app/main.py` pins in `PROMPT_BUNDLE_DIGEST`.
The digest covers the manifest, the child manifests and every prompt
version, so editing a prompt body makes the load fail with
`prompt_digest_mismatch`. Check the file with the SDK command line:

```bash
.venv/bin/agenomic-py prompts bundle-verify \
  prompt-registry-langgraph-demo/prompt-bundle.json \
  --workspace 3f6d2a10-5c7b-4e8a-9d21-6b4c8e0f1a37 \
  --agent 7a2c9e41-0b6d-4f3a-8e57-2d1c4b6a9f80 \
  --expect-bundle-digest sha256:c51239a25d333dc00ad73dd222c4656eaaec41b542ba228387c1c1ffb547da84
```

A bundle exported from Agenomic Cloud is signed with the organization key
and always carries `expires_at`, so a deployment loads it with
`trust=BundleTrust.from_pem_files(...)` instead of a digest and replaces it
before it expires. An unsigned file is used here so the demo never expires.

## What is simulated

- The promotion. A local prompt engine publishes version 2, moves production
  to it, and writes the new bundle to a temporary directory. In Agenomic
  Cloud that move is an approved, signed-in action.
- The restart. The script runs itself again with `--resume` in a new
  process; both processes share the SQLite checkpoints and the local binding
  store in that temporary directory.
