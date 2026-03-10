"""Validate and display local agent workflow configuration.

Example:
    python agent_runner.py
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


AGENTS_DIR = Path(".agents/agents")
SKILLS_DIR = Path(".agents/skills")
WORKFLOWS_DIR = Path(".agents/workflows")
CONTEXT_DIR = Path(".agents/context")
CONTEXT_DIR = Path(".agents/context")

AGENT_REQUIRED_FIELDS = {
    "name",
    "role",
    "skill",
    "responsibilities",
    "inputs",
    "outputs",
    "next_agents",
}
WORKFLOW_REQUIRED_FIELDS = {"name", "orchestrator", "steps"}
STEP_REQUIRED_FIELDS = {"id", "agent", "depends_on"}


class ConfigValidationError(Exception):
    """Raised when the agent configuration is invalid."""


@dataclass(frozen=True)
class ResolvedStep:
    """Represent one workflow step resolved against an agent and skill."""

    step_id: str
    agent_name: str
    skill_name: str
    depends_on: list[str]


def load_json_file(path: Path) -> dict[str, Any]:
    """Load a JSON file from disk.

    Args:
        path: JSON file path.

    Returns:
        Parsed JSON object.

    Raises:
        ConfigValidationError: If the file cannot be parsed as a JSON object.
    """
    try:
        raw_data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ConfigValidationError(f"Arquivo nao encontrado: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ConfigValidationError(f"JSON invalido em {path}: {exc.msg}") from exc

    if not isinstance(raw_data, dict):
        raise ConfigValidationError(f"O arquivo {path} deve conter um objeto JSON.")

    return raw_data


def load_agents(base_path: Path) -> dict[str, dict[str, Any]]:
    """Load and validate agent definitions.

    Args:
        base_path: Project root path.

    Returns:
        Agents indexed by name.
    """
    agents_dir = base_path / AGENTS_DIR
    agent_files = sorted(agents_dir.glob("*.json"))
    if not agent_files:
        raise ConfigValidationError("Nenhum agente foi encontrado em .agents/agents.")

    agents: dict[str, dict[str, Any]] = {}
    for agent_file in agent_files:
        agent = load_json_file(agent_file)
        missing = sorted(AGENT_REQUIRED_FIELDS - agent.keys())
        if missing:
            joined = ", ".join(missing)
            raise ConfigValidationError(
                f"Agente {agent_file.name} sem campos obrigatorios: {joined}"
            )

        name = agent["name"]
        if name in agents:
            raise ConfigValidationError(f"Nome de agente duplicado: {name}")
        agents[name] = agent

    return agents


def load_workflows(base_path: Path) -> dict[str, dict[str, Any]]:
    """Load and validate workflow definitions.

    Args:
        base_path: Project root path.

    Returns:
        Workflows indexed by name.
    """
    workflows_dir = base_path / WORKFLOWS_DIR
    workflow_files = sorted(workflows_dir.glob("*.json"))
    if not workflow_files:
        raise ConfigValidationError("Nenhum workflow foi encontrado em .agents/workflows.")

    workflows: dict[str, dict[str, Any]] = {}
    for workflow_file in workflow_files:
        workflow = load_json_file(workflow_file)
        missing = sorted(WORKFLOW_REQUIRED_FIELDS - workflow.keys())
        if missing:
            joined = ", ".join(missing)
            raise ConfigValidationError(
                f"Workflow {workflow_file.name} sem campos obrigatorios: {joined}"
            )

        steps = workflow["steps"]
        if not isinstance(steps, list) or not steps:
            raise ConfigValidationError(
                f"Workflow {workflow_file.name} deve conter uma lista de steps nao vazia."
            )

        for step in steps:
            if not isinstance(step, dict):
                raise ConfigValidationError(
                    f"Workflow {workflow_file.name} possui step invalido."
                )
            missing_step_fields = sorted(STEP_REQUIRED_FIELDS - step.keys())
            if missing_step_fields:
                joined = ", ".join(missing_step_fields)
                raise ConfigValidationError(
                    f"Workflow {workflow_file.name} possui step sem campos obrigatorios: {joined}"
                )

        name = workflow["name"]
        if name in workflows:
            raise ConfigValidationError(f"Nome de workflow duplicado: {name}")
        workflows[name] = workflow

    return workflows


def validate_skill_reference(base_path: Path, skill_name: str) -> None:
    """Ensure an agent skill markdown file exists.

    Args:
        base_path: Project root path.
        skill_name: Skill identifier without extension.
    """
    skill_path = base_path / SKILLS_DIR / f"{skill_name}.md"
    if not skill_path.exists():
        raise ConfigValidationError(f"Skill referenciada nao encontrada: {skill_name}")


def validate_context_references(base_path: Path, agent: dict[str, Any]) -> None:
    """Ensure optional shared context files exist.

    Args:
        base_path: Project root path.
        agent: Agent definition.
    """
    context_files = agent.get("context_files", [])
    if not context_files:
        return
    if not isinstance(context_files, list):
        raise ConfigValidationError(
            f"Agente {agent['name']} deve usar context_files como lista."
        )

    for context_file in context_files:
        context_path = base_path / context_file
        if not context_path.exists():
            raise ConfigValidationError(
                f"Contexto referenciado nao encontrado para {agent['name']}: {context_file}"
            )


def validate_context_references(base_path: Path, agent: dict[str, Any]) -> None:
    """Ensure optional shared context files exist.

    Args:
        base_path: Project root path.
        agent: Agent definition.
    """
    context_files = agent.get("context_files", [])
    if not context_files:
        return
    if not isinstance(context_files, list):
        raise ConfigValidationError(
            f"Agente {agent['name']} deve usar context_files como lista."
        )

    for context_file in context_files:
        context_path = base_path / context_file
        if not context_path.exists():
            raise ConfigValidationError(
                f"Contexto referenciado nao encontrado para {agent['name']}: {context_file}"
            )


def resolve_workflow(
    workflow: dict[str, Any],
    agents: dict[str, dict[str, Any]],
    base_path: Path,
) -> list[ResolvedStep]:
    """Resolve a workflow against the configured agents.

    Args:
        workflow: Workflow configuration.
        agents: Agent definitions indexed by name.
        base_path: Project root path.

    Returns:
        Ordered list of resolved steps.
    """
    orchestrator_name = workflow["orchestrator"]
    if orchestrator_name not in agents:
        raise ConfigValidationError(
            f"Workflow {workflow['name']} referencia orchestrator inexistente: {orchestrator_name}"
        )

    step_ids: set[str] = set()
    resolved_steps: list[ResolvedStep] = []

    for step in workflow["steps"]:
        step_id = step["id"]
        if step_id in step_ids:
            raise ConfigValidationError(
                f"Workflow {workflow['name']} possui step duplicado: {step_id}"
            )
        step_ids.add(step_id)

        agent_name = step["agent"]
        if agent_name not in agents:
            raise ConfigValidationError(
                f"Workflow {workflow['name']} referencia agente inexistente: {agent_name}"
            )

        depends_on = step["depends_on"]
        if not isinstance(depends_on, list):
            raise ConfigValidationError(
                f"Step {step_id} no workflow {workflow['name']} deve usar depends_on como lista."
            )

        unknown_dependencies = [dep for dep in depends_on if dep not in step_ids]
        if unknown_dependencies:
            joined = ", ".join(unknown_dependencies)
            raise ConfigValidationError(
                f"Step {step_id} no workflow {workflow['name']} possui dependencias desconhecidas: {joined}"
            )

        agent = agents[agent_name]
        validate_skill_reference(base_path, agent["skill"])
        resolved_steps.append(
            ResolvedStep(
                step_id=step_id,
                agent_name=agent_name,
                skill_name=agent["skill"],
                depends_on=depends_on,
            )
        )

    return resolved_steps


def validate_orchestrator(
    workflows: dict[str, dict[str, Any]],
    agents: dict[str, dict[str, Any]],
    orchestrator_name: str = "orchestrator",
) -> None:
    """Validate orchestrator cross-references.

    Args:
        workflows: Workflow definitions.
        agents: Agent definitions.
        orchestrator_name: Orchestrator agent name.
    """
    if orchestrator_name not in agents:
        raise ConfigValidationError("Agente orchestrator nao encontrado.")

    orchestrator = agents[orchestrator_name]
    workflow_name = orchestrator.get("workflow")
    if workflow_name not in workflows:
        raise ConfigValidationError(
            f"Orchestrator referencia workflow inexistente: {workflow_name}"
        )

    available_agents = orchestrator.get("available_agents")
    if not isinstance(available_agents, list) or not available_agents:
        raise ConfigValidationError(
            "Orchestrator deve definir available_agents como lista nao vazia."
        )

    unknown_agents = [agent_name for agent_name in available_agents if agent_name not in agents]
    if unknown_agents:
        joined = ", ".join(unknown_agents)
        raise ConfigValidationError(
            f"Orchestrator referencia agentes desconhecidos: {joined}"
        )


def render_summary(workflow_name: str, resolved_steps: list[ResolvedStep]) -> str:
    """Render a terminal summary of the resolved pipeline.

    Args:
        workflow_name: Workflow name.
        resolved_steps: Ordered resolved steps.

    Returns:
        Human-readable summary.
    """
    lines = [f"Workflow validado: {workflow_name}", "Etapas resolvidas:"]
    for index, step in enumerate(resolved_steps, start=1):
        dependency_suffix = ""
        if step.depends_on:
            dependency_suffix = f" | depende de: {', '.join(step.depends_on)}"
        lines.append(
            f"{index}. {step.step_id} -> agent={step.agent_name} | skill={step.skill_name}{dependency_suffix}"
        )
    return "\n".join(lines)


def run(base_path: Path | None = None) -> str:
    """Execute configuration loading, validation and summary generation.

    Args:
        base_path: Optional project root path. Defaults to current working directory.

    Returns:
        Summary string for the resolved workflow.
    """
    project_root = (base_path or Path.cwd()).resolve()
    agents = load_agents(project_root)
    workflows = load_workflows(project_root)

    for agent in agents.values():
        validate_skill_reference(project_root, agent["skill"])
        validate_context_references(project_root, agent)
        validate_context_references(project_root, agent)

    validate_orchestrator(workflows, agents)
    orchestrator = agents["orchestrator"]
    workflow = workflows[orchestrator["workflow"]]
    resolved_steps = resolve_workflow(workflow, agents, project_root)
    return render_summary(workflow["name"], resolved_steps)


def main() -> int:
    """Run the CLI entrypoint.

    Returns:
        Process exit code.
    """
    try:
        print(run())
    except ConfigValidationError as exc:
        print(f"Erro de validacao: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
