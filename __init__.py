"""Throwaway skeleton plugin: verifies tool, skill, blueprint, hook and slash command registration."""
from __future__ import annotations

import json
from pathlib import Path

_HERE = Path(__file__).resolve().parent

PROBE_SCHEMA = {
    "name": "twf_probe",
    "description": "Report which context the plugin tool handler receives. Test only.",
    "parameters": {"type": "object", "properties": {}, "required": []},
}


def _probe(args, **kwargs):
    return json.dumps({"received_kwargs": sorted(kwargs)})


def _on_session_end(**kwargs):
    return None


def _pre_llm_call(**kwargs):
    return None


def _slash(raw_args: str, *, session_id: str = "", session_key: str = "", platform: str = "", source=None) -> str:
    return f"twf-skeleton: session={session_id or '-'} key={session_key or '-'} platform={platform or '-'}"


def register(ctx):
    ctx.register_tool(name="twf_probe", toolset="twf", schema=PROBE_SCHEMA, handler=_probe)
    ctx.register_skill("twf-setup", _HERE / "skills" / "twf-setup" / "SKILL.md",
                       description="Use when setting up the task workflow skeleton. Test only.")
    ctx.register_automation_blueprint(
        "discovery",
        title="Task discovery stream (skeleton)",
        description="Test blueprint for a discovery stream.",
        schedule_template="0 9 * * *",
        prompt_template="Reply with the word SKELETON.",
        deliver_default="origin",
    )
    ctx.register_hook("on_session_end", _on_session_end)
    ctx.register_hook("pre_llm_call", _pre_llm_call)
    ctx.register_command("twf", handler=_slash, description="Skeleton status")
