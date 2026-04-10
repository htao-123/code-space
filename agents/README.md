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
Do not start development before writing the current task's handoff or planning document.
Do not ask for confirmation when the workflow, handoffs, and repository facts already determine the next step.
Use Chinese when reporting roles and workflow progress to the user.
For roles 2-8, do not produce formal output before completing required research.
When the work could be invalidated by outdated external information, external research is mandatory.
If an existing project lacks usable documentation, do not code first; create minimum viable documentation first.
If documentation backfill is required, downstream roles may continue only after the backfill artifact exists.
Bug fixes must use the same role pipeline under a required `bugfix` mode, not ad hoc patching.

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
8. [knowledge-keeper](./skills/knowledge-keeper/SKILL.md)
   - Archives validated conclusions and reusable lessons

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
- 当前角色：
- 当前角色标识：
- 当前交接标识：
- 需求标识：
- 项目落点：
- 下一角色标识：
```

- Each role may use only the original request, the latest valid handoff, and any repository facts explicitly allowed by that role.
- The orchestrator is the source of truth for deciding the next step.
- No agent may replace this workflow with its own improvised process.
- If there is any doubt, fall back to the orchestrator instead of continuing free-form.
- New builds or substantial subprojects must live in a dedicated folder instead of the repository root.
- Development is document-first: create or update the current task document before implementation so the workflow does not depend on memory.
- Workflow execution should be automatic by default; pause only for real ambiguity, missing information, or meaningful branching decisions.
- Only the current role's unresolved ambiguity may justify stopping for user confirmation.
- Research is two-layered: internal project research first, external time-sensitive research when needed.
- Existing undocumented projects must go through a documentation backfill step before normal development continues.
- When documentation backfill is required, the backfill artifact becomes a required input for later roles.
- If the default new-project container folder (for example `projects/`) does not exist yet, create it during normal setup rather than blocking the workflow.

## Useful References

- [Pipeline Contract](./skills/ai-pipeline-orchestrator/references/pipeline-contract.md)
- [Pipeline Demo](./skills/ai-pipeline-orchestrator/references/pipeline-demo.md)
- [Workflow Gate Checker](./scripts/check_workflow_gate.py)
- [Handoff Quality Checker](./scripts/check_handoff_quality.py)
- [Workflow Gate Checklist](./scripts/workflow-gate-checklist.md)
- [External Research Playbook](./references/external-research-playbook.md)
- [Documentation Backfill Playbook](./references/documentation-backfill-playbook.md)

The gate checker supports stage-specific validation and a final completion gate. Use the matching stage instead of validating only implementation.
The completion gate is expected to validate the closing chain from implementer through knowledge-keeper.
The workflow gate also runs the handoff quality checker by default.
The quality checker is mandatory during normal workflow execution.
Relationship validation now prefers stable IDs over free-text matching.
Use `当前角色标识 / 下一角色标识 / 当前交接标识` for workflow routing.
Treat `当前角色` as display-only text, not a gate source of truth.
Use `FACT-* / EVID-IN-* / EVID-EX-*` identifiers for facts and evidence.
Use `EVID-EX-* -> 本地快照路径 | URL` for external evidence targets.
Write fact items as `FACT-001 -> 证据摘录：摘录内容`.
Write evidence mappings as `FACT-001 -> EVID-IN-001::keyword::摘录`.

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
- `knowledge-keeper` archives symptom, root cause, fix, and recurrence prevention notes

When an existing project lacks usable documentation, follow:

- [Documentation Backfill Playbook](./references/documentation-backfill-playbook.md)

When current external facts may affect correctness, follow:

- [External Research Playbook](./references/external-research-playbook.md)
