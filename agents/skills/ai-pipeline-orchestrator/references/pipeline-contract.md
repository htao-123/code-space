# Pipeline Contract

This document defines the shared contract across the 8 role skills.

## Role Order

1. `requirement-analyst`
2. `architect`
3. `code-investigator`
4. `solution-designer`
5. `implementer`
6. `reviewer`
7. `tester`
8. `knowledge-keeper`

No role may skip forward.
No role may merge with another role.
No agent may replace this workflow with a self-invented process.
No agent may decide that the workflow is optional just because the task feels simple.
No new project or substantial subproject may be scattered across repository root when it should live in a dedicated folder.
No implementation may begin until the current project is documented in a project document.
No agent should pause for redundant confirmation when the next workflow step is already determined by the current handoff state.
Every requirement must run through the full workflow until `knowledge-keeper`, unless the user explicitly abandons the workflow.
User-facing workflow communication should use Chinese role names and Chinese progression language.
For every role, internal research and external research are mandatory before formal output.
If an existing project lacks usable documentation, minimum documentation backfill is mandatory before normal development continues.
Bug fixes must use the same workflow under explicit `bugfix` mode; they may not bypass roles as “small patches”.
When historical data and the new version's data structure diverge, the default response is a migration script, not long-lived compatibility handling in runtime code.
Every completed requirement must include a requirement retrospective.
Every completed requirement must include self-review and self-correction records in the terminal `knowledge-keeper` handoff.
If a real workflow-rule or process problem is exposed during project execution, handle it as a separate rule-system change under `agents/` instead of recording workflow governance fields in the project document.
That rule-side governance record must use the fixed `## Rule Governance` section in `agents/docs/context/workflow-system-context.md`.
Workflow status is declared in project-document frontmatter, not by brittle prose excerpts.
AI may write a workflow status field to `1` only after the rule-defined condition has already been satisfied.
When this workflow is used on a real project, that project's documents must live inside the real project path.
For real projects, all project documents use unified pipeline documents under `<project>/docs/pipeline/`.
Each project document maps to exactly one `requirement_id` and serves as both the current working document and historical record.
When a new independent requirement starts, create a new pipeline document `<project>/docs/pipeline/YYYY-MM-DD-<project>-<topic>-<work-type>.md` with unique `requirement_id`.
When a requirement continues, keep updating the same pipeline document and append evolution history as needed.
During research, the current requirement's pipeline document is the primary workflow input.
Historical pipeline documents are secondary research inputs used only for prior decisions, stage evolution, earlier handoffs, or evidence indexes.
Use these naming rules for real-project workflow artifacts:
- project document: `<project>/docs/pipeline/YYYY-MM-DD-<project>-<topic>-<work-type>.md`
- requirement id: `<WORKTYPE>-<PROJECT>-<TOPIC>-NNN`
- internal evidence: `<project>/references/internal/<topic>-<artifact>-YYYY-MM-DD.md`
- external research: `<project>/references/external/<topic>-research-YYYY-MM-DD.md`
The project document should store current state, current conclusions, and evidence indexes; long-form raw evidence should default to `references/internal` or `references/external`.
When modifying the rule system itself under `agents/`, do not create or retain rule-side workflow history documents; update current rules directly.
Implementation may begin only after the project document declares:
- `workflow_current_stage: solution-designer`
- `workflow_solution_approved: 1`
- `workflow_pre_chain_verified: 1`
Completion may pass only after the project document declares:
- `workflow_current_stage: knowledge-keeper`
- `workflow_knowledge_keeper_passed: 1`
and the full chain can be replayed from requirement-analyst through knowledge-keeper.

For real projects, project documents are located at `<project>/docs/pipeline/YYYY-MM-DD-<project>-<topic>-<work-type>.md`.
The current active requirement is the pipeline document with the most recent date that has `workflow_completion_passed: 0`.
Completed requirements have `workflow_completion_passed: 1` and serve as historical records.
`agents/docs/` is reserved for current reusable context, not for rule-side workflow history.

## Mandatory Handoff Shape

Every role output must contain:

```md
【角色结论】
【已核实输入】
【调研发现】
【交付物】
【约束】
【校验标准】
【禁止事项】
【交接给下一个角色】
```

If any heading is missing, the handoff is incomplete and the pipeline must stop.

Inside `【交接给下一个角色】`, use Chinese labels:

```md
- 下一角色：角色中文名【该角色职责说明】
- 可用输入：
- 非目标：
- 完成条件：
```

Inside each handoff block, also require these metadata labels:

```md
- 当前角色标识：
- 当前交接标识：
- 需求标识：
- 下一角色标识：
```

For bugfix work, the handoff chain must also carry these bug-mode labels:

```md
- 问题类型：bugfix
- 复现步骤：
- 预期结果：
- 实际结果：
```

Bugfix downstream stages must also carry:

```md
- 根因摘要：
- 回归检查范围：
```

Inside each handoff block, keep only the project-facing quality labels that remain useful to humans:

```md
- 是否需要外部调研：
- 外部调研来源：
- 外部调研结论：
- 未验证项：
- 需要用户确认：
- 推荐方案：
- 推荐原因：
- 主要权衡：
```

Frontmatter workflow expectations:

- `requirement_id` is required and must match every handoff block `需求标识`.
- `workflow_project_type` must be `new-project` or `existing-project`.
- `workflow_work_type` must be `feature`, `bugfix`, or `task`.
- `workflow_doc_backfilled` must be `0` or `1`.
- `workflow_current_stage` must be one of:
  `requirement-analyst`, `architect`, `code-investigator`, `solution-designer`, `implementer`, `reviewer`, `tester`, `knowledge-keeper`, `complete`.
- `workflow_solution_approved`, `workflow_pre_chain_verified`, `workflow_implementer_passed`, `workflow_reviewer_passed`, `workflow_tester_passed`, `workflow_knowledge_keeper_passed`, and `workflow_completion_passed` must be `0` or `1`.
- AI must not write any of those fields to `1` before the corresponding rule condition is actually satisfied.

## Allowed Transition Table

| Current role | Next role |
| --- | --- |
| `requirement-analyst` | `architect` |
| `architect` | `code-investigator` |
| `code-investigator` | `solution-designer` |
| `solution-designer` | `implementer` |
| `implementer` | `reviewer` |
| `reviewer` | `implementer` when blocking findings require review-fix |
| `reviewer` | `tester` |
| `tester` | `knowledge-keeper` |
| `knowledge-keeper` | terminal |

`reviewer -> tester` is allowed only when the review-fix-review loop has no blocking findings.
`reviewer -> implementer` is allowed only for fixing reviewed blocking findings.

## Input Discipline

The next role may use only:

- the original user request
- the latest valid handoff
- repository facts explicitly allowed by that role

The next role may not:

- import assumptions from older incomplete drafts
- bypass prior constraints
- invent missing evidence
- invent a shortcut workflow outside this contract
- combine two role responsibilities "for convenience"
- begin implementing a new project before its folder placement is defined
- rely on unstated memory when the current project document has not been created or updated
- skip required internal research
- skip required external verification when current facts may have changed
- continue coding in an existing undocumented project before minimum documentation has been backfilled
- validate multiple unrelated handoffs in a single non-complete stage gate run
- respond to historical-data/schema mismatch by silently adding permanent compatibility branches before migration has been evaluated and documented

## Minimum Checks By Role

### requirement-analyst

- clarifies scope
- splits work into implementable sub-functions
- marks non-goals and ambiguities
- in bugfix mode, defines symptom, repro, expected result, actual result, and impact

### architect

- verifies current project structure before deciding the landing zone
- identifies affected modules
- maps input to output flow
- defines structural invariants
- when historical data and the new version's data structure diverge, decides whether a migration script is required and records why runtime compatibility handling is not the default
- in bugfix mode, narrows the repair landing zone and excludes unrelated modules

### code-investigator

- researches internal code facts before drawing conclusions
- traces real call chains
- cites relevant files
- distinguishes fact from unknown
- when historical-data/schema mismatch exists, identifies the old structure, the new structure, and the real data gap that migration must close
- in bugfix mode, records reproduction evidence and root-cause-facing evidence

### solution-designer

- verifies whether the proposed solution depends on current external facts
- states root cause layer
- proposes minimum viable change
- defines impact range and fallback handling
- for historical-data/schema mismatch, prefers an explicit migration path over long-lived compatibility logic and records the migration strategy
- in bugfix mode, records `根因摘要` explicitly

### implementer

- verifies current implementation references and APIs before coding
- stays inside approved file scope
- follows the design handoff
- avoids unrelated refactors
- when review returns blocking findings, fixes only those reviewed findings and records the fix scope before returning to reviewer
- for historical-data/schema mismatch, implements the approved migration script or migration entrypoint instead of introducing default permanent compatibility branches
- in bugfix mode, fixes the validated root cause and records regression scope

### reviewer

- verifies review assumptions against current code and relevant current external standards when needed
- checks business correctness against the actual requirement, not only code plausibility
- checks whether the change stayed within the minimum necessary scope
- checks logic clarity and readability
- checks whether architecture boundaries or module responsibilities were damaged
- checks state flow, async safety, and data consistency risks
- checks failure handling, fallback behavior, and user-facing error handling
- checks obvious performance and resource risks
- checks testability, regression risk, and rollback readiness
- checks AI-generated-code risks such as imagined interfaces, copied-but-misaligned logic, silent requirement drift, and missed project constraints
- flags bugs and regressions
- checks scope drift
- records residual risk
- returns to `implementer` when P0/P1 findings exist
- treats P2 findings as fix-by-default; if any P2 is deferred, records the reason, risk, and explicit user approval
- sets `workflow_reviewer_passed: 1` only when there are no blocking findings and all required fixes have been re-reviewed
- in bugfix mode, checks whether the fix addresses root cause instead of only masking the symptom

## Review-Fix-Review Loop

After implementation, review is not a one-time checkpoint. It is a loop:

1. `implementer` produces an implementation handoff.
2. `reviewer` reviews the implementation and records findings.
3. If any P0/P1 finding exists, the pipeline must return to `implementer`.
4. P2 findings are fix-by-default. A deferred P2 requires explicit reason, risk, and user approval in the reviewer handoff.
5. The implementer may fix only the reviewed findings and must record the fix scope.
6. The reviewer must re-review the fix scope.
7. The pipeline may enter `tester` only after the reviewer records that there are no blocking findings.
8. AI must not set `workflow_reviewer_passed: 1` before the no-blocking-finding condition is met.

### tester

- verifies test approach against the approved scope and any relevant current platform behavior
- covers normal path
- covers failure path
- covers edge or boundary path
- records `运行时验证`
- records `外部依赖验证`
- records `未验证原因`
- when the feature depends on external APIs, browser runtime behavior, or network requests, validates the real success path or explicitly records why that validation could not be completed
- if the external success path is marked verified, binds that claim to a concrete passing test case
- in bugfix mode, covers original repro, fix verification, and nearby regression scope

### knowledge-keeper

- records symptom, root cause, fix
- records validated lessons
- marks remaining uncertainty
- records requirement retrospective, self-review, and self-correction
- in bugfix mode, archives recurrence-prevention notes and regression learnings

## Stop Conditions

The pipeline must stop when:

- the next required handoff does not exist
- the previous handoff is incomplete
- the user asks to skip a mandatory gate
- current work conflicts with prior constraints
- implementation or review evidence is missing for later stages
- review has unresolved P0/P1 findings
- review has unresolved P2 findings without an explicit deferral reason, risk record, and user approval
- any agent attempts to improvise an alternative process outside this contract
- a new project is being created but no dedicated folder has been defined yet
- the current work has no up-to-date project document or planning handoff
- required research for the current role has not been completed
- external verification is required but has not been performed
- an existing project lacks minimum usable documentation and backfill has not been completed
- bugfix work lacks a recorded repro path, expected/actual result, root cause summary, or regression scope where required
- historical-data/schema mismatch exists but no migration decision or migration artifact has been recorded
- requirement retrospective, self-review, or self-correction fields are missing from the terminal archive

The pipeline should not stop merely to request confirmation when:

- the next role is already determined
- the current handoff is sufficient
- no material branching decision remains
- the current role can finish from existing facts and approved constraints
- the workflow is not attempting to cross from `solution-designer` into `implementer`

The pipeline must always stop for explicit solution approval before implementation when:

- the latest valid role is `solution-designer`
- the next role would be `implementer`
- a proposed solution changes user-facing behavior, architecture, dependencies, data handling, platform capabilities, or delivery scope

For this approval stop:

- present the solution to the user in Chinese before running the implementer gate or editing code
- include the implementation scope, target files/modules, verification plan, and main tradeoffs
- ask the user to approve, reject, or request changes
- record `需要用户确认：是` in the solution handoff
- record the user's approval in the project document or next handoff before implementation begins
- the implementer gate must fail unless the `solution-designer` handoff contains `用户方案批准` with explicit approval

When the pipeline does need to stop for confirmation because a real decision remains open:

- the current role must provide a concrete recommendation
- the current role must explain the reason for that recommendation
- the current role must surface the main tradeoff or risk that prevents automatic continuation
- the pipeline must not stop with a bare question when a recommendation can be made from existing facts
- the handoff must explicitly record `需要用户确认：是`
- the handoff must not leave `推荐方案 / 推荐原因 / 主要权衡` empty

When no confirmation is needed:

- record `需要用户确认：否`
- record `推荐方案：无`
- record `推荐原因：无`
- record `主要权衡：无`

## Recovery Rules

If the pipeline is blocked:

1. identify the last valid role
2. name the missing artifact
3. route back to the exact role that must repair the gap

Do not repair the gap inside the orchestrator.
Do not solve the blockage by inventing a new workflow.
If the blockage is only handoff formatting shape, normalize the handoff document first before treating the requirement itself as blocked.

## Project Placement Rule

For any new website, app, tool, or standalone deliverable:

1. choose the project folder during requirement or architecture stages
2. keep related implementation files inside that folder
3. avoid scattering project files across repository root

Root-level placement is allowed only when the user explicitly requests it and the handoff records that exception.

If the default container directory for new projects does not exist yet, create it during normal setup. Its absence is not a valid reason to block the workflow once the landing zone is approved.

For work inside an existing project:

1. identify whether the change belongs to an existing module or a new subproject folder
2. record that landing zone in the handoff before implementation
3. keep implementation inside the approved existing path or approved new subfolder

## Documentation-First Rule

For every active development task:

1. write or update the current project document before implementation
2. keep the document aligned with the latest handoff state
3. if the plan, scope, or landing zone changes, update the document first

The purpose is to ensure continuity across sessions and prevent the workflow from depending on agent memory.

## Existing Project Documentation Backfill Rule

For an existing project with no usable documentation:

1. stop normal downstream development
2. create minimum viable documentation from repository facts
3. record known facts, landing zone, scope, unknowns, and risks
4. treat that backfill document as a required workflow artifact
5. then continue the normal workflow

Do not use missing documentation as an excuse to rely on memory or guess intent.

Follow the backfill process in:

- `agents/references/documentation-backfill-playbook.md`

This backfill may be created during `requirement-analyst` or `architect`, but downstream roles may not proceed until it exists.

## Research-First Rule

For every role:

1. complete internal project research before formal output
2. complete external research before formal output
3. record the verified inputs and research findings in the role output

Internal research includes:

- current project document
- prior handoffs
- repository files
- existing implementation behavior

External research should always be completed. At minimum, verify whether any current outside facts, mainstream approaches, or mature implementations affect the role's output, including:

- third-party libraries or frameworks that may have changed
- browser or platform behavior
- SEO, deployment, distribution, or compatibility rules
- APIs, standards, or toolchain behavior that may be outdated

When external research is required, cover up to three layers as needed by the role:

1. official current facts and rules
2. current mainstream approaches used by the ecosystem
3. mature best-practice or reference implementations that inform a high-quality solution

If external research finds no meaningful new difference, record that conclusion explicitly.
Do not rely on memory alone when there is meaningful risk of outdated information.

Follow the external research process in:

- `agents/references/external-research-playbook.md`

## Automatic Progression Rule

Default to automatic progression.

Advance to the next role without asking when:

1. the workflow state clearly determines the next role
2. the needed inputs already exist
3. there is no significant unresolved branch

Ask only when:

1. the product or technical direction is still ambiguous
2. multiple non-equivalent paths remain open
3. a decision would change scope, structure, or external promises
4. the current role cannot produce a valid output from the available facts and handoffs

## Enforcement Recommendation

Before implementation, execute the repository workflow gate by following `agents/scripts/workflow-gate-checklist.md`.

Use the checklist to verify:

- current project document exists
- required frontmatter workflow fields exist
- handoff documents contain mandatory sections
- handoff documents contain the required Chinese sublabels
- handoff documents record current role id, handoff id, and requirement identifier explicitly
- handoff documents record required research and role-specific quality labels explicitly
- for non-`complete` stages, the current document's latest handoff block routes to the expected next role id for the validated stage
- for non-`complete` stages, the current document's latest handoff block declares the expected current role id for the validated stage
- for `complete` stage, the validated full handoff chain routes through all expected role ids from `requirement-analyst` through `knowledge-keeper` in order
- implementation targets stay inside the repository and match the approved scope
- existing-project work has completed required documentation backfill before downstream roles continue
- bugfix-mode handoffs include symptom, repro, expected/actual result, root cause summary, and regression scope when the validated stage requires them

## Enforcement Rule

Workflow enforcement is standardized on `agents/scripts/workflow-gate-checklist.md`.

Requirements:

1. execute the checklist in order
2. record explicit pass/fail results
3. repair failed workflow artifacts before proceeding
4. do not skip enforcement because automation is unavailable or inconvenient

Implementation may begin only after the checklist has been completed and recorded as passing for the current stage.

Use stage-specific gate validation as the workflow advances, and use the completion gate before declaring a requirement finished.
The checklist reads project-document frontmatter first, then validates that handoff content supports the declared status.
The implementation gate validates the full pre-implementation chain.
The completion gate validates the full 8-role chain in one project document and rejects partial closing-only inputs.
The workflow gate should enforce the handoff quality checker rules during normal workflow execution.
