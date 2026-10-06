# AGENTS.md

Notes for maintainers and coding agents working in this repository.

## Managed prompts

- `prompt-registry-langgraph-demo/prompt-bundle.json` is an unsigned
  `agenomic.prompt_bundle/v1` document authenticated by the digest pinned in
  `app/main.py` (`PROMPT_BUNDLE_DIGEST`). A signed export always carries
  `expires_at` (at most 365 days), so a committed signed bundle would stop
  loading; an unsigned, digest-pinned bundle has no expiry, and the SDK skips
  its governance check because the pin is the operator's approval. The file
  is the output of `LocalPromptEngine.resolve(agent_id, channel="production")`
  after publishing `prm_refund_planner:1`, creating a release that pins it in
  `planner.instructions` and moving production to that release. The digest
  covers the manifest, the child manifests and the prompts, not `release`,
  `source` or `exported_at`: a regeneration with the same prompt keeps it,
  any prompt change needs `PROMPT_BUNDLE_DIGEST`, the README verify command
  and the README expected output updated in the same change.
- The demo builds the version 2 bundle at run time in a fresh
  `LocalPromptEngine` (same workspace and agent, version 1 copied from the
  committed bundle, production moved twice) and hands its digest to the
  restarted process on the command line. Resuming on one unchanged bundle
  would not show that a paused thread ignores a promotion, and a second
  committed bundle would only duplicate data.
- The restart is the same script run again in a child process,
  `sys.executable main.py --resume <dir> <digest>`. The parent forwards the
  child's stderr, compares the logs and the checkpoint
  `agenomic_prompt_manifest_digest` of both threads with the expected values
  and exits non-zero on a difference, so a regression fails the run instead
  of printing plausible output. The comparison is an explicit check, not
  `assert`, because `python -O` and `PYTHONOPTIMIZE` strip assertions and the
  run would then exit 0 on the wrong prompts. The code carries no comments
  or docstrings; the narrative is in its printed output and in the README.
- `app/requirements.txt` pins the primary LangGraph point the Python SDK is
  tested on and lists `agenomic[langgraph]` without a version, because no
  published release ships managed prompts yet; the README says to install
  the SDK from a checkout until then. The SQLite saver is imported at module
  level: the SDK example this demo mirrors exits 0 with a hint when the saver
  is missing, but the demo's requirements install it, so a missing saver
  must fail.
