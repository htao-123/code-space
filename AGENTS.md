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
- Bug fixes must use the same workflow, but run in `bugfix` mode instead of free-form patching.
- If the default project container folder does not exist yet, create it as part of normal new-project setup instead of treating that as a blocker.
- When historical data and the new version's data structure diverge, do not add long-lived compatibility handling by default; prefer a migration script that upgrades historical data into the new structure.

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
- required quality evidence fields exist
- the validated handoff block or validated closing chain uses the expected role ids and handoff id metadata for the current stage
- new-project work is not being placed at repository root unless explicitly allowed
- existing-project work declares whether documentation was already usable or had to be backfilled
- existing-project work points to the actual documentation artifact used for that declaration
- existing-project documentation artifacts are stored inside the approved project path
- bugfix work records bug mode metadata before implementation
- bugfix work records reproduction, expected result, actual result, root cause summary, and regression scope in the required stages
- tester handoffs record runtime verification, external-dependency verification, and unverified reasons when applicable
- static checks must not replace real success-path validation for features that depend on external APIs, browser runtime behavior, or network requests
- historical-data/schema mismatch work records whether a migration script is required and must not silently fall back to permanent compatibility branches by default

If the gate fails, stop and repair the missing workflow artifact before coding.

Run the appropriate stage gate, not only `--stage implementer`.
Use later stages as the workflow advances, and use the completion gate before treating a requirement as finished.
The completion gate should validate the closing chain from implementer through knowledge-keeper, not only the final archive block.
The workflow gate should also run the handoff quality checker by default.
The quality checker may not be disabled in normal workflow execution.
If the gate is blocked only by handoff formatting shape, run `python3 agents/scripts/normalize_handoff_format.py --handoff-doc <doc> --write` before deciding the requirement itself is blocked.
Use stable identifiers for workflow and evidence relations:

- `当前角色标识`
- `下一角色标识`
- `当前交接标识`
- `FACT-*`
- `EVID-IN-*`
- `EVID-EX-*`

For bugfix work, also require these fields in the active handoff chain:

- `问题类型：bugfix`
- `复现步骤：`
- `预期结果：`
- `实际结果：`
- `根因摘要：`
- `回归检查范围：`

Bugfix work must not skip:

- symptom definition
- reproduction path
- root cause capture
- regression scope definition
- post-fix regression validation

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
