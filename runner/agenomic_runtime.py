"""Minimal runtime that turns an Agenomic agent bundle into a live LLM call.

Shared by every demo's `app/main.py`. Reads the bundle's system prompt,
behavior contract, agent.lock, and skills; sends the user input to the
provider declared in agent.lock.yaml; then runs structural checks against
the behavior contract on the JSON the model returns.

Supported providers (resolved at call-time):

- ``anthropic`` -> requires ``anthropic`` package and ``ANTHROPIC_API_KEY``
- ``openai``    -> requires ``openai`` package and ``OPENAI_API_KEY``

Demos depend on this module via a relative path import — see each
``app/main.py``.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class Bundle:
    root: Path
    genome: dict
    contract: dict
    lock: dict
    system_prompt: str
    skills: dict[str, str] = field(default_factory=dict)

    @classmethod
    def load(cls, bundle_root: str | Path) -> "Bundle":
        root = Path(bundle_root).resolve()
        genome = yaml.safe_load((root / "genome.yaml").read_text())
        contract = yaml.safe_load((root / "behavior.contract.yaml").read_text())
        lock = yaml.safe_load((root / "agent.lock.yaml").read_text())
        system_prompt = (root / genome["artifacts"]["system_prompt"]).read_text()
        skills: dict[str, str] = {}
        for rel in genome["artifacts"].get("skills", []):
            path = root / rel
            skills[path.stem] = path.read_text()
        return cls(
            root=root,
            genome=genome,
            contract=contract,
            lock=lock,
            system_prompt=system_prompt,
            skills=skills,
        )


@dataclass
class RunResult:
    raw_text: str
    structured: dict[str, Any] | None
    violations: list[str]
    model: str
    provider: str

    @property
    def ok(self) -> bool:
        return not self.violations and self.structured is not None


def _extract_json(text: str) -> dict[str, Any] | None:
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    candidate = fence.group(1) if fence else None
    if candidate is None:
        first, last = text.find("{"), text.rfind("}")
        if first != -1 and last > first:
            candidate = text[first : last + 1]
    if candidate is None:
        return None
    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        return None


def _build_messages(bundle: Bundle, user_input: dict[str, Any]) -> tuple[str, str]:
    skill_block = ""
    if bundle.skills:
        parts = [f"### Skill: {name}\n{body}" for name, body in bundle.skills.items()]
        skill_block = "\n\n---\n\n" + "\n\n".join(parts)

    system = (
        bundle.system_prompt
        + skill_block
        + "\n\n---\n\n"
        + "Respond with a single fenced JSON object containing exactly the fields "
        + "listed under 'Expected structured outputs'. No prose outside the fence."
    )
    user = (
        "Input payload:\n```json\n"
        + json.dumps(user_input, indent=2, ensure_ascii=False)
        + "\n```"
    )
    return system, user


def _call_anthropic(model: str, system: str, user: str, temperature: float) -> str:
    from anthropic import Anthropic

    client = Anthropic()
    resp = client.messages.create(
        model=model,
        max_tokens=1024,
        temperature=temperature,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return "".join(block.text for block in resp.content if block.type == "text")


def _call_openai(model: str, system: str, user: str, temperature: float) -> str:
    from openai import OpenAI

    client = OpenAI()
    resp = client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return resp.choices[0].message.content or ""


def _check_contract(contract: dict, structured: dict[str, Any] | None) -> list[str]:
    violations: list[str] = []
    if structured is None:
        return ["model_did_not_return_json"]

    for action in contract.get("prohibited_actions", []) or []:
        flag = structured.get(action)
        if flag is True:
            violations.append(f"prohibited_action_emitted:{action}")

    triggers = contract.get("human_review_required_when", []) or []
    if triggers and "human_review_required" in structured:
        any_trigger = False
        for expr in triggers:
            key, _, val = expr.partition("==")
            key = key.strip()
            val = val.strip()
            actual = structured.get(key)
            if isinstance(actual, bool):
                expected = val.lower() == "true"
                if actual == expected:
                    any_trigger = True
            elif isinstance(actual, str) and actual.strip('"\'') == val.strip('"\''):
                any_trigger = True
        if any_trigger and not structured.get("human_review_required"):
            violations.append("human_review_required_but_not_set")

    return violations


def run(bundle: Bundle, user_input: dict[str, Any]) -> RunResult:
    model_cfg = bundle.lock["locked"]["model"]
    provider = model_cfg["provider"]
    model_name = model_cfg["name"]
    temperature = float(model_cfg.get("temperature", 0.0))

    system, user = _build_messages(bundle, user_input)

    if provider == "anthropic":
        if not os.environ.get("ANTHROPIC_API_KEY"):
            raise RuntimeError("ANTHROPIC_API_KEY is not set")
        raw = _call_anthropic(model_name, system, user, temperature)
    elif provider == "openai":
        if not os.environ.get("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY is not set")
        raw = _call_openai(model_name, system, user, temperature)
    else:
        raise RuntimeError(f"Unsupported provider: {provider}")

    structured = _extract_json(raw)
    violations = _check_contract(bundle.contract, structured)
    return RunResult(
        raw_text=raw,
        structured=structured,
        violations=violations,
        model=model_name,
        provider=provider,
    )


def load_traces(path: str | Path) -> list[dict]:
    path = Path(path)
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def print_result(scenario: str, result: RunResult) -> None:
    print(f"\n=== {scenario} ===")
    print(f"provider={result.provider} model={result.model}")
    if result.structured is not None:
        print("structured output:")
        print(json.dumps(result.structured, indent=2, ensure_ascii=False))
    else:
        print("raw text (no JSON detected):")
        print(result.raw_text)
    if result.violations:
        print("contract violations:")
        for v in result.violations:
            print(f"  - {v}")
    else:
        print("contract: OK")
