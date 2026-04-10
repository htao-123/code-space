# Repository Workflow Rules

This repository uses the AI engineering workflow defined under [`agents/`](./agents/README.md).

## Mandatory Entry

Start with [`ai-pipeline-orchestrator`](./agents/skills/ai-pipeline-orchestrator/SKILL.md) for any non-trivial development task.

## Hard Requirements

- Do not invent a parallel workflow.
- Do not merge multiple roles into one step.
- Do not skip required roles.
- Every new requirement must complete the full workflow through the terminal role unless the user explicitly abandons the workflow.
- Do not start implementation without a current task document or handoff.
- Do not scatter a new project across repository root.
- For existing projects, record the approved landing zone before implementation.
- Do not stop for unnecessary confirmations when the next step is already determined by the workflow and existing handoffs.
- Use Chinese when presenting workflow roles, role conclusions, and role-to-role progression to the user.
- For roles 2-8, research is mandatory before formal output.
- When a plan or implementation may be affected by current external technology, standards, APIs, platform rules, or library behavior, external research is mandatory and may require internet verification.
- If an existing project lacks usable documentation, create the minimum necessary task and context documentation before continuing development.

## Gate Check

Before implementation work begins, run:

```bash
python3 agents/scripts/check_workflow_gate.py --help
```

Use this gate to verify:

- the current task document exists
- the project path or landing zone is defined
- required handoff documents contain the mandatory sections
- required Chinese handoff sublabels exist
- required research records exist
- new-project work is not being placed at repository root unless explicitly allowed
- existing-project work declares whether documentation was already usable or had to be backfilled

If the gate fails, stop and repair the missing workflow artifact before coding.

## Gate Fallback

If the automatic gate cannot run because the local environment is missing a required runtime or command:

1. report the exact environment problem
2. try a lightweight preflight check first
3. switch to the manual checklist in [`agents/scripts/workflow-gate-checklist.md`](./agents/scripts/workflow-gate-checklist.md)

Implementation may proceed only after either:

- the automatic gate passes, or
- the manual checklist is explicitly completed and recorded

## Confirmation Policy

Advance automatically when:

- the next role is already determined by the workflow
- the current handoff provides enough information
- there is no material branch with non-obvious consequences

Stop and ask only when:

- a key product or technical choice is still ambiguous
- multiple non-equivalent paths remain open
- the choice affects scope, architecture, delivery, or user promises
- the current handoff is missing required information
- the current role cannot determine its output from existing facts and handoffs

## Research Policy

For roles 2-8:

1. perform internal research first
2. perform external research when time-sensitive or potentially outdated facts could affect the result
3. do not proceed from memory alone when there is meaningful risk of outdated information

Internal research includes:

- current task document
- prior handoffs
- repository structure
- existing implementation facts

External research includes:

- official docs
- current platform or browser behavior
- library or framework changes
- deployment, SEO, distribution, or compatibility rules

If external research is required, it is not optional.

## Existing Project Without Documentation

If an existing project has no usable documentation:

1. do not proceed directly into implementation
2. create the minimum viable documentation first
3. base that documentation on repository facts, not guesses
4. treat that backfill document as required workflow input before downstream roles continue

Minimum viable documentation should cover:

- current task scope
- approved landing zone
- relevant modules or files
- known facts
- unknowns and risks

Use these references when needed:

- [`agents/references/documentation-backfill-playbook.md`](./agents/references/documentation-backfill-playbook.md)
- [`agents/references/external-research-playbook.md`](./agents/references/external-research-playbook.md)
