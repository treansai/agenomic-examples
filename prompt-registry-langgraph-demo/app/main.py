from __future__ import annotations

import itertools
import json
import operator
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Annotated, Any

from agenomic.integrations import LocalBindingStore, bind_langgraph, prompts_for
from agenomic.prompts import LocalPromptEngine, PromptBundle
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import START, StateGraph
from langgraph.types import Command, interrupt
from typing_extensions import TypedDict

WORKSPACE_ID = "3f6d2a10-5c7b-4e8a-9d21-6b4c8e0f1a37"
AGENT_ID = "7a2c9e41-0b6d-4f3a-8e57-2d1c4b6a9f80"
PROMPT_BUNDLE = Path(__file__).resolve().parents[1] / "prompt-bundle.json"
PROMPT_BUNDLE_DIGEST = (
    "sha256:c51239a25d333dc00ad73dd222c4656eaaec41b542ba228387c1c1ffb547da84"
)
PROMPT_ID = "prm_refund_planner"
SLOT = "planner.instructions"
PROMOTED_PLAN = (
    "Plan the refund in two steps: confirm the order, then offer a store voucher."
)
PAUSED_THREAD = "refund-42"
NEW_THREAD = "refund-43"


class State(TypedDict, total=False):
    log: Annotated[list[str], operator.add]


def build_graph(saver: Any) -> Any:
    model = GenericFakeChatModel(
        messages=itertools.cycle([AIMessage(content="plan drafted")])
    )

    def plan(state: State, config: RunnableConfig) -> State:
        prompts = prompts_for(config)
        system = prompts.render_text(SLOT)
        model.invoke(
            [SystemMessage(system), HumanMessage("refund order 42")],
            prompts.config_for(SLOT),
        )
        return {"log": [f"plan: {system}"]}

    def approve(state: State, config: RunnableConfig) -> State:
        answer = interrupt("approve the refund plan?")
        system = prompts_for(config).render_text(SLOT)
        return {"log": [f"approve: {answer}: {system}"]}

    builder = StateGraph(State)
    builder.add_node("plan", plan)
    builder.add_node("approve", approve)
    builder.add_edge(START, "plan")
    builder.add_edge("plan", "approve")
    return builder.compile(checkpointer=saver)


def thread(thread_id: str) -> RunnableConfig:
    return {"configurable": {"thread_id": thread_id}}


def bind(
    graph: Any,
    workdir: Path,
    bundle: Path,
    digest: str,
    retained: list[tuple[Path, str]],
) -> Any:
    return bind_langgraph(
        graph,
        agent_id=AGENT_ID,
        channel="production",
        offline=True,
        workspace_id=WORKSPACE_ID,
        bundle=bundle,
        expected_bundle_digest=digest,
        retained_bundles=retained,
        binding_store=LocalBindingStore(workdir / "pins"),
    )


def promote(workdir: Path) -> dict[str, str]:
    original = PromptBundle.load(
        PROMPT_BUNDLE,
        expected_workspace_id=WORKSPACE_ID,
        expected_agent_id=AGENT_ID,
        expected_bundle_digest=PROMPT_BUNDLE_DIGEST,
    )
    content = original.document["prompts"][f"{PROMPT_ID}:1"]["content"]
    engine = LocalPromptEngine(WORKSPACE_ID)
    engine.create_prompt(PROMPT_ID, kind="text", name="Refund planner")
    for number, body in enumerate((content["body"], PROMOTED_PLAN), start=1):
        engine.publish(
            PROMPT_ID,
            {**content, "body": body},
            parent_version=None if number == 1 else number - 1,
            change_message=f"Version {number}",
        )
        release = engine.create_release(AGENT_ID, {SLOT: f"{PROMPT_ID}:{number}"})
        engine.move_channel(
            AGENT_ID, "production", release, expected_generation=number - 1
        )
    document = engine.resolve(AGENT_ID, channel="production")
    (workdir / "prompt-bundle-v2.json").write_text(
        json.dumps(document), encoding="utf-8"
    )
    print("simulation of the governed path: production now points to version 2,")
    print("shipped as prompt-bundle-v2.json with a new pinned digest; in Agenomic")
    print("Cloud that move is an approved, signed-in action")
    return {
        "old_manifest": original.prompt_manifest_digest,
        "new_manifest": str(document["prompt_manifest_digest"]),
        "new_bundle": str(document["prompt_bundle_digest"]),
    }


def first_process(workdir: Path) -> dict[str, str]:
    with SqliteSaver.from_conn_string(str(workdir / "checkpoints.sqlite")) as saver:
        managed = bind(
            build_graph(saver), workdir, PROMPT_BUNDLE, PROMPT_BUNDLE_DIGEST, []
        )
        paused = managed.invoke({"log": []}, thread(PAUSED_THREAD))
        print(
            "process 1:",
            PAUSED_THREAD,
            "paused on",
            [item.value for item in paused["__interrupt__"]],
        )
        print("process 1:", paused["log"][-1])
    return promote(workdir)


def second_process(workdir: Path, new_bundle_digest: str) -> None:
    with SqliteSaver.from_conn_string(str(workdir / "checkpoints.sqlite")) as saver:
        graph = build_graph(saver)
        managed = bind(
            graph,
            workdir,
            workdir / "prompt-bundle-v2.json",
            new_bundle_digest,
            [(PROMPT_BUNDLE, PROMPT_BUNDLE_DIGEST)],
        )
        resumed = managed.invoke(Command(resume="approved"), thread(PAUSED_THREAD))
        fresh = managed.invoke({"log": []}, thread(NEW_THREAD))
        summary = {
            name: {
                "log": output["log"],
                "digest": graph.get_state(thread(name)).metadata[
                    "agenomic_prompt_manifest_digest"
                ],
            }
            for name, output in ((PAUSED_THREAD, resumed), (NEW_THREAD, fresh))
        }
    print(json.dumps(summary))


def main() -> None:
    original_plan = json.loads(PROMPT_BUNDLE.read_text(encoding="utf-8"))["prompts"][
        f"{PROMPT_ID}:1"
    ]["content"]["body"]
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as directory:
        workdir = Path(directory)
        digests = first_process(workdir)
        child = subprocess.run(
            [
                sys.executable,
                str(Path(__file__).resolve()),
                "--resume",
                str(workdir),
                digests["new_bundle"],
            ],
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
    sys.stderr.write(child.stderr)
    if child.returncode != 0:
        raise SystemExit(
            f"the restarted process failed with exit code {child.returncode}"
        )
    summary = json.loads(child.stdout.strip().splitlines()[-1])
    for name, entry in summary.items():
        print(f"process 2: {name} -> {entry['log']}")
    paused, fresh = summary[PAUSED_THREAD], summary[NEW_THREAD]
    assert paused["log"] == [
        f"plan: {original_plan}",
        f"approve: approved: {original_plan}",
    ]
    assert paused["digest"] == digests["old_manifest"]
    assert fresh["log"] == [f"plan: {PROMOTED_PLAN}"]
    assert fresh["digest"] == digests["new_manifest"]
    print(
        "the resumed thread kept",
        digests["old_manifest"][:19],
        "and the new thread uses",
        digests["new_manifest"][:19],
    )


if __name__ == "__main__":
    if sys.argv[1:2] == ["--resume"]:
        second_process(Path(sys.argv[2]), sys.argv[3])
    else:
        main()
