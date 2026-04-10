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
【交付物】
【约束】
【校验标准】
【禁止事项】
【交接给下一个角色】
```

- Each role may use only the original request, the latest valid handoff, and any repository facts explicitly allowed by that role.
- The orchestrator is the source of truth for deciding the next step.
- No agent may replace this workflow with its own improvised process.
- If there is any doubt, fall back to the orchestrator instead of continuing free-form.
- New builds or substantial subprojects must live in a dedicated folder instead of the repository root.
- Development is document-first: create or update the current task document before implementation so the workflow does not depend on memory.
- Workflow execution should be automatic by default; pause only for real ambiguity, missing information, or meaningful branching decisions.
- Only the current role's unresolved ambiguity may justify stopping for user confirmation.

## Useful References

- [Pipeline Contract](./skills/ai-pipeline-orchestrator/references/pipeline-contract.md)
- [Pipeline Demo](./skills/ai-pipeline-orchestrator/references/pipeline-demo.md)
- [Workflow Gate Checker](./scripts/check_workflow_gate.py)
- [Workflow Gate Checklist](./scripts/workflow-gate-checklist.md)

## Output Templates

Each role has its own fill-in template in `references/output-template.md` under that skill directory.
