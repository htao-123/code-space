# Repository Workflow Rules

This repository uses the AI engineering workflow defined under [`agents/`](./agents/README.md).

## Mandatory Entry

Start with [`ai-pipeline-orchestrator`](./agents/skills/ai-pipeline-orchestrator/SKILL.md) for any non-trivial development task.

## Hard Requirements

- Do not invent a parallel workflow.
- Do not merge multiple roles into one step.
- Do not skip required roles.
- Every new requirement must complete the full workflow through the terminal role unless the user explicitly abandons the workflow.
- Do not start implementation without a current project document.
- Do not scatter a new project across repository root.
- For existing projects, record the approved landing zone before implementation.
- Do not stop for unnecessary confirmations when the next step is already determined by the workflow and existing handoffs.
- Use Chinese when presenting workflow roles, role conclusions, and role-to-role progression to the user.
- For every role, internal research and external research are mandatory before formal output.
- When a plan or implementation may be affected by current external technology, standards, APIs, platform rules, or library behavior, external research is mandatory and may require internet verification.
- External research must not stop at official facts only; when relevant, it must also cover current mainstream approaches and mature best-practice implementations.
- If an existing project lacks usable documentation, create the minimum necessary task and context documentation before continuing development.
- Bug fixes must use the same workflow, but run in `bugfix` mode instead of free-form patching.
- If the default project container folder does not exist yet, create it as part of normal new-project setup instead of treating that as a blocker.
- When historical data and the new version's data structure diverge, do not add long-lived compatibility handling by default; prefer a migration script that upgrades historical data into the new structure.
- Every completed requirement must include a requirement retrospective.
- Every completed requirement must include self-review and self-correction records in the terminal `knowledge-keeper` handoff.
- If project execution exposes a real workflow-rule or process problem, handle it as a separate rule-system change under `agents/`; do not record workflow governance fields inside the project document.
- Rule-side workflow governance must use the fixed `## Rule Governance` section in `agents/docs/context/workflow-system-context.md` as its current source of truth.
- Before advancing from `solution-designer` to `implementer`, present the proposed solution to the user and wait for explicit approval. Do not treat an internally completed solution handoff as approval to start implementation.
- The workflow gate uses project-document frontmatter as the primary source of workflow status.
- Frontmatter workflow fields are written by AI under rule-defined conditions; AI must not guess or advance a gate flag early.
- Project document body records project facts and role conclusions; gate-only state must not rely on brittle prose matching.
- When this rule system is used to build or modify a real project, that project must keep its own current project document inside the project path.
- When modifying the rule system itself under `agents/`, do not create or retain rule-side workflow history documents; update current rules directly.
- Before implementation, the gate must validate the full pre-implementation chain from `requirement-analyst` through `solution-designer`.
- Completion must validate one project document containing the full 8-role chain from `requirement-analyst` through `knowledge-keeper`.
- `agents/docs/` is reserved for current reusable context only, not for rule-side workflow history.

## Gate Check

Before implementation work begins, perform the workflow gate by following [`agents/scripts/workflow-gate-checklist.md`](./agents/scripts/workflow-gate-checklist.md).

This checklist is the single source of truth for workflow gate validation. AI must inspect it item by item, record explicit pass/fail results, and stop to repair workflow artifacts before coding when any required item fails.

Use this gate to verify:

- the current project document exists
- required frontmatter workflow fields exist
- required handoff sections and Chinese sublabels exist
- the validated handoff block or validated full chain uses the expected role ids and requirement identifiers for the current stage
- new-project work is not being placed at repository root unless explicitly allowed
- existing-project work has already completed the required minimum documentation backfill before downstream implementation
- bugfix work records bug mode metadata, reproduction, expected result, actual result, root cause summary, and regression scope in the required stages
- tester handoffs record runtime verification, external-dependency verification, and unverified reasons when applicable
- the terminal workflow archive records requirement retrospective, self-review, and self-correction

If the gate fails, stop and repair the missing workflow artifact before coding.
Do not repair a failed gate by silently changing workflow state fields or handoff conclusions.

Run the appropriate stage gate, not only `--stage implementer`.
Use later stages as the workflow advances, and use the completion gate before treating a requirement as finished.
The completion gate must validate one project document containing the full 8-role chain from requirement-analyst through knowledge-keeper; do not run completion with partial closing-chain inputs.
The workflow gate must execute the role-level handoff quality checks embedded in [`agents/scripts/workflow-gate-checklist.md`](./agents/scripts/workflow-gate-checklist.md) by default.
Those checklist-based quality checks may not be skipped or disabled in normal workflow execution.
Use stable identifiers for workflow and handoff relations:

- `requirement_id`
- `workflow_project_type`
- `workflow_work_type`
- `workflow_doc_backfilled`
- `workflow_current_stage`
- `workflow_solution_approved`
- `workflow_pre_chain_verified`
- `workflow_implementer_passed`
- `workflow_reviewer_passed`
- `workflow_tester_passed`
- `workflow_knowledge_keeper_passed`
- `workflow_completion_passed`

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

## Gate Execution

Workflow gate execution is standardized on [`agents/scripts/workflow-gate-checklist.md`](./agents/scripts/workflow-gate-checklist.md).

Requirements:

1. AI must execute the checklist in order
2. AI must explicitly record pass/fail status for each required section
3. AI must not skip failed checks by editing workflow state fields prematurely
4. Implementation may proceed only after the checklist has been completed and recorded as passing for the current stage

The gate may not be skipped simply because automation is unavailable or inconvenient.

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
- after the user approves, record the approval in the project document and set `workflow_solution_approved: 1`
- the implementer gate must fail unless the project document records `workflow_solution_approved: 1` and the solution handoff contains `- 用户方案批准：`

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

For every role:

1. perform internal research first
2. perform external research second
3. do not proceed from memory alone or skip either research phase before formal output

Internal research includes:

- current project document
- prior handoffs
- repository structure
- existing implementation facts

External research includes:

- official docs
- current platform or browser behavior
- library or framework changes
- deployment, SEO, distribution, or compatibility rules
- current mainstream approaches used in the ecosystem
- mature best-practice or reference implementations when they affect design or implementation quality

External research is not optional for any role. When no new outside difference is found, record that conclusion explicitly.

## Existing Project Without Documentation

If an existing project has no usable documentation:

1. do not proceed directly into implementation
2. create the minimum viable documentation first
3. base that documentation on repository facts, not guesses
4. treat that backfill document as required workflow input before downstream roles continue

If workflow needs to read and continue using an existing project's current project document, and that document still uses the legacy pre-frontmatter workflow shape, manually normalize it according to [`agents/references/documentation-backfill-playbook.md`](./agents/references/documentation-backfill-playbook.md) before continuing with the current rules.

Required normalization includes at least:

- add the current frontmatter workflow fields
- normalize handoff headings and metadata labels
- align the document with the current `<project>/docs/pipeline/` structure

Minimum viable documentation should cover:

- current task scope
- approved landing zone
- relevant modules or files
- known facts
- unknowns and risks

For work on a real project, store that project document inside the real project path.
Do not use any rule-side history-doc location as a catch-all task archive for unrelated projects or for rule-system self-edits.

Use these references when needed:

- [`agents/references/documentation-backfill-playbook.md`](./agents/references/documentation-backfill-playbook.md)
- [`agents/references/external-research-playbook.md`](./agents/references/external-research-playbook.md)
