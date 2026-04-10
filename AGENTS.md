# Repository Workflow Rules

This repository uses the AI engineering workflow defined under [`agents/`](./agents/README.md).

## Mandatory Entry

Start with [`ai-pipeline-orchestrator`](./agents/skills/ai-pipeline-orchestrator/SKILL.md) for any non-trivial development task.

## Hard Requirements

- Do not invent a parallel workflow.
- Do not merge multiple roles into one step.
- Do not skip required roles.
- Do not start implementation without a current task document or handoff.
- Do not scatter a new project across repository root.
- For existing projects, record the approved landing zone before implementation.

## Gate Check

Before implementation work begins, run:

```bash
python3 agents/scripts/check_workflow_gate.py --help
```

Use this gate to verify:

- the current task document exists
- the project path or landing zone is defined
- required handoff documents contain the mandatory sections
- new-project work is not being placed at repository root unless explicitly allowed

If the gate fails, stop and repair the missing workflow artifact before coding.

## Gate Fallback

If the automatic gate cannot run because the local environment is missing a required runtime or command:

1. report the exact environment problem
2. try a lightweight preflight check first
3. switch to the manual checklist in [`agents/scripts/workflow-gate-checklist.md`](./agents/scripts/workflow-gate-checklist.md)

Implementation may proceed only after either:

- the automatic gate passes, or
- the manual checklist is explicitly completed and recorded
