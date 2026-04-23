# AI Engineering Skills

This directory contains a constrained AI engineering workflow built from reusable skills.

## Recommended Entry

Start with [ai-pipeline-orchestrator](./skills/ai-pipeline-orchestrator/SKILL.md) when you want the workflow to decide the correct next step and prevent skipping required gates.

## Hard Rule

Do not invent a parallel process, shortcut, or "better" workflow outside this system.
Do not merge multiple roles into one execution step.
Do not skip a role because it seems obvious.
Every requirement must run the full workflow to completion.
Do not continue when the immediately prior valid handoff is missing.
Do not scatter a new project across the repository root; place it in a dedicated project folder first.
Do not start development before writing the current project document.
Do not ask for confirmation when the workflow, handoffs, and repository facts already determine the next step.
Use Chinese when reporting roles and workflow progress to the user.
For every role, do not produce formal output before completing internal research and external research.
When the work could be invalidated by outdated external information, external research is mandatory.
External research must cover not only official current facts, but also current mainstream approaches and mature best-practice implementations when they affect the role's decision.
If an existing project lacks usable documentation, do not code first; create minimum viable documentation first.
If documentation backfill is required, downstream roles may continue only after the backfill artifact exists.
Bug fixes must use the same role pipeline under a required `bugfix` mode, not ad hoc patching.
When historical data and the new version's data structure diverge, do not keep the system alive through default compatibility branches; prefer an explicit migration script that upgrades historical data into the new structure.
Every completed requirement must end with a requirement retrospective.
Every completed requirement must record self-review and self-correction in the terminal knowledge-keeper handoff.
If project execution exposes a real workflow-rule or process problem, handle it as a separate rule-system change under `agents/` rather than writing workflow governance fields into the project document.
Rule-side workflow governance must be recorded in the fixed `## Rule Governance` section of `agents/docs/context/workflow-system-context.md`.
Workflow status lives in project-document frontmatter, not in brittle prose matching.
AI writes frontmatter workflow fields only when the rule-defined condition is already satisfied.
Implementation entry must validate the full requirement -> architecture -> investigation -> solution chain.
Completion must validate the full requirement -> architecture -> investigation -> solution -> implementation -> review -> test -> archive chain.
When this workflow is applied to a real project, that project must keep all pipeline documents under `<project>/docs/pipeline/`.
For real projects, all pipeline documents use the unified structure: `<project>/docs/pipeline/YYYY-MM-DD-<project>-<topic>-<work-type>.md`.
Each pipeline document maps to exactly one `requirement_id` and serves as both the current working document and historical record.
The active requirement is the most recent pipeline document with `workflow_completion_passed: 0`.
Completed requirements have `workflow_completion_passed: 1` and serve as historical records.
When a new independent requirement starts, create a new pipeline document under `<project>/docs/pipeline/` with a unique `requirement_id`.
When the work is a continuation of the same requirement, continue updating the same pipeline document and append evolution history as needed.
During research, read the current requirement's pipeline document first as the primary input.
Use historical pipeline documents only when you need prior decisions, stage evolution, earlier handoffs, or evidence indexes for the same or related requirements.
Historical documents are secondary research inputs and must not replace the current requirement's pipeline document as the default gate-facing source of truth.
Use these naming rules for real-project workflow artifacts:
- pipeline document: `<project>/docs/pipeline/YYYY-MM-DD-<project>-<topic>-<work-type>.md`
- requirement id: `<WORKTYPE>-<PROJECT>-<TOPIC>-NNN`
- internal evidence: `<project>/references/internal/<topic>-<artifact>-YYYY-MM-DD.md`
- external research: `<project>/references/external/<topic>-research-YYYY-MM-DD.md`
The current requirement's pipeline document should keep current state, current conclusions, and evidence indexes; long-form raw evidence belongs in `references/internal` or `references/external` by default.
Rules-side historical workflow documents should not accumulate under `agents/docs/`.
`agents/docs/` is reserved for current reusable context, not for rule-system self-edit history.

If an agent or user request conflicts with this workflow, the conflict must be stated explicitly before any work continues.

## Skills

### Orchestrator

- [ai-pipeline-orchestrator](./skills/ai-pipeline-orchestrator/SKILL.md)
  - Controls the full pipeline
  - Decides the next valid role
  - Blocks skipped or incomplete handoffs

### Core Roles

1. [requirement-analyst](./skills/requirement-analyst/SKILL.md)
   - Clarifies scope, boundaries, risks, and functional breakdown
2. [architect](./skills/architect/SKILL.md)
   - Maps the request to modules, data flow, and structural constraints
3. [code-investigator](./skills/code-investigator/SKILL.md)
   - Collects repository facts, call chains, and similar implementations
4. [solution-designer](./skills/solution-designer/SKILL.md)
   - Designs the minimum viable change from validated facts
5. [implementer](./skills/implementer/SKILL.md)
   - Implements the approved solution inside the allowed file scope
6. [reviewer](./skills/reviewer/SKILL.md)
   - Reviews for bugs, regressions, and scope violations
7. [tester](./skills/tester/SKILL.md)
   - Verifies normal, failure, and edge-case behavior
   - Must explicitly record runtime verification, external-dependency verification, and any unverified reason
8. [knowledge-keeper](./skills/knowledge-keeper/SKILL.md)
   - Archives validated conclusions and reusable lessons
   - Must also record requirement retrospective, self-review, and self-correction

## Required Order

1. requirement-analyst
2. architect
3. code-investigator
4. solution-designer
5. implementer
6. reviewer
7. tester
8. knowledge-keeper

Do not skip steps unless the immediately prior valid handoff already exists.

## Shared Rules

- Every role must output:

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

- Every handoff block must also record these metadata labels:

```md
- 当前角色标识：
- 当前交接标识：
- 需求标识：
- 下一角色标识：
```

- Each role may use only the original request, the latest valid handoff, and any repository facts explicitly allowed by that role.
- The orchestrator is the source of truth for deciding the next step.
- No agent may replace this workflow with its own improvised process.
- If there is any doubt, fall back to the orchestrator instead of continuing free-form.
- New builds or substantial subprojects must live in a dedicated folder instead of the repository root.
- Development is document-first: create or update the pipeline document before implementation so the workflow does not depend on memory.
- For real project work, all pipeline documents belong under `<project>/docs/pipeline/`.
- Each pipeline document maps to exactly one `requirement_id`.
- The active requirement is the most recent pipeline document with `workflow_completion_passed: 0`.
- New independent requirements create a new pipeline document with a unique `requirement_id`.
- Internal evidence should default to `<project>/references/internal/<topic>-<artifact>-YYYY-MM-DD.md`.
- External research should default to `<project>/references/external/<topic>-research-YYYY-MM-DD.md`.
- For rule-system changes under `agents/`, update current rules directly and do not create rule-side workflow history documents.
- Workflow execution should be automatic by default; pause only for real ambiguity, missing information, or meaningful branching decisions.
- The transition from `solution-designer` to `implementer` is a mandatory approval gate: present the solution to the user and wait for explicit approval before running the implementer gate or editing code.
- Only the current role's unresolved ambiguity may justify stopping for user confirmation.
- When stopping for confirmation because the current role is genuinely uncertain, do not ask a bare question; give a recommendation and explain why that recommendation is preferred.
- Record that stop explicitly in the handoff with `需要用户确认 / 推荐方案 / 推荐原因 / 主要权衡`; if no confirmation is needed, record `否 / 无 / 无 / 无`.
- Research is two-layered: internal project research first, external research second for every role.
- Existing undocumented projects must go through a documentation backfill step before normal development continues.
- When documentation backfill is required, the backfill artifact becomes a required input for later roles.
- If the default new-project container folder (for example `projects/`) does not exist yet, create it during normal setup rather than blocking the workflow.
- Historical-data/schema mismatch should default to migration scripts rather than long-lived compatibility handling inside runtime logic.

## Useful References

- [Pipeline Contract](./skills/ai-pipeline-orchestrator/references/pipeline-contract.md)
- [Workflow Gate Checklist](./scripts/workflow-gate-checklist.md)
  - Single source of truth for workflow gate validation
- [External Research Playbook](./references/external-research-playbook.md)
- [Documentation Backfill Playbook](./references/documentation-backfill-playbook.md)

Workflow gate execution is checklist-only.
The checklist validates workflow state from project-document frontmatter first, then validates that handoff content supports that declared state.
For real projects, use the current requirement's pipeline document (the most recent `<project>/docs/pipeline/YYYY-MM-DD-*.md` with `workflow_completion_passed: 0`) as the default gate target.
Historical pipeline documents with `workflow_completion_passed: 1` remain valid history, but they are not the default gate target for new work.
The implementation gate validates `workflow_current_stage=solution-designer`, `workflow_solution_approved=1`, `workflow_pre_chain_verified=1`, and a complete pre-implementation chain.
The completion gate validates one pipeline document containing the full 8-role chain from requirement-analyst through knowledge-keeper.
The checklist must still enforce the handoff quality checker rules during normal workflow execution.
Use these frontmatter fields as the minimum workflow state:
`requirement_id`, `workflow_project_type`, `workflow_work_type`, `workflow_doc_backfilled`, `workflow_current_stage`, `workflow_solution_approved`, `workflow_pre_chain_verified`, `workflow_implementer_passed`, `workflow_reviewer_passed`, `workflow_tester_passed`, `workflow_knowledge_keeper_passed`, `workflow_completion_passed`.

## Output Templates

Each role has its own fill-in template in `references/output-template.md` under that skill directory.

## Bugfix Mode

Use the normal 8-role pipeline for bug fixes, but mark the handoff chain explicitly with:

```md
- 问题类型：bugfix
- 复现步骤：
- 预期结果：
- 实际结果：
```

For bug-fix downstream stages, also require:

```md
- 根因摘要：
- 回归检查范围：
```

Bugfix mode expectations:

- `requirement-analyst` defines symptom, repro, expected vs actual behavior, and impact
- `architect` and `code-investigator` keep the repair scope narrow and evidence-based
- `solution-designer` must state the root cause summary
- `implementer` must repair the validated root cause only
- `reviewer` checks whether the change fixes root cause rather than masking the symptom
- `tester` must cover original repro, fix validation, and nearby regression scope
- `tester` must not treat static checks as a substitute for validating real success paths when external APIs, browser runtime, or network requests are involved
- `knowledge-keeper` archives symptom, root cause, fix, and recurrence prevention notes

When an existing project lacks usable documentation, follow:

- [Documentation Backfill Playbook](./references/documentation-backfill-playbook.md)

When workflow needs to read and continue using an existing project's older project document, and that document predates the current frontmatter-first workflow, manually normalize it according to the Documentation Backfill Playbook before continuing.

When current external facts may affect correctness, follow:

- [External Research Playbook](./references/external-research-playbook.md)
