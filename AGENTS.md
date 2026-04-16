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
- Every completed requirement must include a requirement retrospective.
- Every completed requirement must include self-review and self-correction records in the terminal `knowledge-keeper` handoff.
- Every completed requirement must also include a workflow retrospective that checks whether the AI workflow exposed any rule or process issue.
- Workflow rule updates are mandatory only when that retrospective identifies a real rule or process problem; otherwise record that no rule update was needed.
- Before advancing from `solution-designer` to `implementer`, present the proposed solution to the user and wait for explicit approval. Do not treat an internally completed solution handoff as approval to start implementation.
- Do not silently edit completed role handoff blocks to make a failed gate pass.
- If a gate fails, record the failure and classify the repair as `format-only`, `evidence-correction`, `content-regeneration`, or `workflow-repair` before rerunning the gate.
- `format-only` repair may use the handoff normalizer; evidence/content/workflow repair must append an explicit correction or route back to the responsible role instead of overwriting history.
- Before implementation, the gate must validate the full pre-implementation chain from `requirement-analyst` through `solution-designer`, not only the latest solution block.
- Completion must validate one task document containing the full 8-role chain from `requirement-analyst` through `knowledge-keeper`.
- Repair records must use a task-level `## Repair Record` block with repair type, handling, responsible role, requirement-impact status, implementation-impact status, and follow-up validation.
- `normalize_handoff_format.py --write --repair-type format-only --ack-format-only` must append a task-level `format-only` repair record when it writes the file.

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
- the validated handoff block or validated full chain uses the expected role ids and handoff id metadata for the current stage
- new-project work is not being placed at repository root unless explicitly allowed
- existing-project work declares whether documentation was already usable or had to be backfilled
- existing-project work points to the actual documentation artifact used for that declaration
- existing-project documentation artifacts are stored inside the approved project path
- bugfix work records bug mode metadata before implementation
- bugfix work records reproduction, expected result, actual result, root cause summary, and regression scope in the required stages
- tester handoffs record runtime verification, external-dependency verification, and unverified reasons when applicable
- static checks must not replace real success-path validation for features that depend on external APIs, browser runtime behavior, or network requests
- historical-data/schema mismatch work records whether a migration script is required and must not silently fall back to permanent compatibility branches by default
- the terminal workflow archive records workflow learnings, workflow problems, and rule-update status
- the terminal workflow archive records requirement retrospective, self-review, self-correction, workflow retrospective, and rule-update status

If the gate fails, stop and repair the missing workflow artifact before coding.
Do not repair a failed gate by editing handoff content silently.
Record the failed command or failure summary, the repair type, the responsible role, and whether the repair changed meaning or only formatting.

Run the appropriate stage gate, not only `--stage implementer`.
Use later stages as the workflow advances, and use the completion gate before treating a requirement as finished.
The completion gate must validate one task document containing the full 8-role chain from requirement-analyst through knowledge-keeper; do not run completion with only implementer/reviewer/tester/knowledge-keeper handoff documents.
The workflow gate should also run the handoff quality checker by default.
The quality checker may not be disabled in normal workflow execution.
If the gate is blocked only by handoff formatting shape, run `python3 agents/scripts/normalize_handoff_format.py --handoff-doc <doc> --write --repair-type format-only --ack-format-only` before deciding the requirement itself is blocked; this writes a task-level `format-only` repair record.
The normalizer is allowed only for `format-only` repairs. It must not be used to add missing evidence, user approval, role conclusions, root cause, test results, or retrospective content.
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
- the workflow is not crossing from `solution-designer` into `implementer`

Always stop and ask for explicit user approval when:

- `solution-designer` has produced the implementation plan and the next role would be `implementer`
- a proposed solution changes user-facing behavior, architecture, dependencies, data handling, platform capabilities, or delivery scope
- the user has asked to review or confirm a plan before the next step

Stop and ask only when:

- a key product or technical choice is still ambiguous
- multiple non-equivalent paths remain open
- the choice affects scope, architecture, delivery, or user promises
- the current handoff is missing required information
- the current role cannot determine its output from existing facts and handoffs

When stopping for solution approval before implementation:

- present the proposed solution in Chinese, including scope, files/modules to change, verification plan, and main tradeoffs
- ask the user to approve, reject, or request changes before running the implementer gate or editing code
- record that stop explicitly in the handoff using:
  - `- 需要用户确认：是`
  - `- 推荐方案：`
  - `- 推荐原因：`
  - `- 主要权衡：`
- after the user approves, record the approval in the task document or next handoff before implementation begins
- the implementer gate must fail unless the `solution-designer` handoff contains `- 用户方案批准：` with explicit approval

When stopping for user confirmation because of real uncertainty:

- do not ask a bare question
- provide a clear recommendation
- provide the reason for that recommendation
- explain the main tradeoff or risk that makes confirmation necessary
- record that stop explicitly in the handoff using:
  - `- 需要用户确认：`
  - `- 推荐方案：`
  - `- 推荐原因：`
  - `- 主要权衡：`
- if no confirmation is needed, record `- 需要用户确认：否` and use `无` for the other three fields

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
