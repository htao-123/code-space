# AI Engineering Skills

This directory contains a constrained AI engineering workflow built from reusable skills.

## Recommended Entry

Start with [ai-pipeline-orchestrator](./skills/ai-pipeline-orchestrator/SKILL.md) when you want the workflow to decide the correct next step and prevent skipping required gates.

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

## Useful References

- [Pipeline Contract](./skills/ai-pipeline-orchestrator/references/pipeline-contract.md)
- [Pipeline Demo](./skills/ai-pipeline-orchestrator/references/pipeline-demo.md)

## Output Templates

Each role has its own fill-in template in `references/output-template.md` under that skill directory.
