"""Tests for the local agent runner validation flow."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from agent_runner import ConfigValidationError, main, run


def test_run_returns_resolved_pipeline_summary() -> None:
    """Validate the happy path summary content."""
    summary = run(Path.cwd())

    assert "Workflow validado: feature_pipeline" in summary
    assert "1. implement_feature -> agent=dev_agent | skill=python_senior_dev" in summary
    assert "2. validate_feature -> agent=qa_agent | skill=qa_engineer" in summary


def test_run_fails_when_skill_is_missing(tmp_path: Path) -> None:
    """Validate that missing skill files are rejected."""
    project_root = _build_project_fixture(tmp_path)
    skill_file = project_root / ".agents" / "skills" / "qa_engineer.md"
    skill_file.unlink()

    with pytest.raises(ConfigValidationError, match="Skill referenciada nao encontrada"):
        run(project_root)


def test_run_fails_when_context_file_is_missing(tmp_path: Path) -> None:
    """Validate that shared context references are enforced."""
    project_root = _build_project_fixture(tmp_path)
    context_file = project_root / ".agents" / "context" / "application_context.md"
    context_file.unlink()

    with pytest.raises(ConfigValidationError, match="Contexto referenciado nao encontrado"):
        run(project_root)


def test_run_fails_when_agent_field_is_missing(tmp_path: Path) -> None:
    """Validate required field enforcement for agents."""
    project_root = _build_project_fixture(tmp_path)
    agent_path = project_root / ".agents" / "agents" / "dev_agent.json"
    agent_payload = json.loads(agent_path.read_text(encoding="utf-8"))
    del agent_payload["outputs"]
    agent_path.write_text(json.dumps(agent_payload, indent=2), encoding="utf-8")

    with pytest.raises(ConfigValidationError, match="campos obrigatorios"):
        run(project_root)


def test_run_fails_when_workflow_references_unknown_agent(tmp_path: Path) -> None:
    """Validate workflow agent cross-reference checks."""
    project_root = _build_project_fixture(tmp_path)
    workflow_path = project_root / ".agents" / "workflows" / "feature_pipeline.json"
    workflow_payload = json.loads(workflow_path.read_text(encoding="utf-8"))
    workflow_payload["steps"][1]["agent"] = "ghost_agent"
    workflow_path.write_text(json.dumps(workflow_payload, indent=2), encoding="utf-8")

    with pytest.raises(ConfigValidationError, match="agente inexistente"):
        run(project_root)


def test_main_returns_non_zero_on_validation_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Validate CLI exit code on failure."""
    monkeypatch.setattr("agent_runner.run", lambda base_path=None: (_ for _ in ()).throw(ConfigValidationError("falha")))

    assert main() == 1


def _build_project_fixture(base_dir: Path) -> Path:
    """Create a minimal project fixture mirroring the real repo structure."""
    project_root = base_dir / "project"
    for relative_dir in (
        ".agents/context",
        ".agents/skills",
        ".agents/agents",
        ".agents/workflows",
        "src",
        "tests",
    ):
        (project_root / relative_dir).mkdir(parents=True, exist_ok=True)

    fixture_files = {
        ".agents/context/application_context.md": "# context\n",
        ".agents/skills/python_senior_dev.md": "# dev\n",
        ".agents/skills/qa_engineer.md": "# qa\n",
        ".agents/skills/git_ops.md": "# git\n",
        ".agents/agents/dev_agent.json": {
            "name": "dev_agent",
            "role": "dev",
            "skill": "python_senior_dev",
            "responsibilities": ["implementar"],
            "inputs": ["feature_request"],
            "outputs": ["implementation_artifact"],
            "context_files": [".agents/context/application_context.md"],
            "next_agents": ["qa_agent"],
        },
        ".agents/agents/qa_agent.json": {
            "name": "qa_agent",
            "role": "qa",
            "skill": "qa_engineer",
            "responsibilities": ["validar"],
            "inputs": ["implementation_artifact"],
            "outputs": ["qa_report"],
            "context_files": [".agents/context/application_context.md"],
            "next_agents": [],
        },
        ".agents/agents/orchestrator.json": {
            "name": "orchestrator",
            "role": "orchestrator",
            "skill": "git_ops",
            "responsibilities": ["coordenar"],
            "inputs": ["workflow_name"],
            "outputs": ["resolved_pipeline"],
            "context_files": [".agents/context/application_context.md"],
            "next_agents": ["dev_agent", "qa_agent"],
            "workflow": "feature_pipeline",
            "available_agents": ["dev_agent", "qa_agent"],
        },
        ".agents/workflows/feature_pipeline.json": {
            "name": "feature_pipeline",
            "orchestrator": "orchestrator",
            "steps": [
                {
                    "id": "implement_feature",
                    "agent": "dev_agent",
                    "depends_on": [],
                },
                {
                    "id": "validate_feature",
                    "agent": "qa_agent",
                    "depends_on": ["implement_feature"],
                },
            ],
        },
    }

    for relative_path, content in fixture_files.items():
        path = project_root / relative_path
        if isinstance(content, dict):
            path.write_text(json.dumps(content, indent=2), encoding="utf-8")
        else:
            path.write_text(content, encoding="utf-8")

    return project_root
