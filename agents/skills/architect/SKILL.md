---
name: architect
description: Decide where a requested change belongs in the existing system and produce a minimal-change architecture handoff. Use after requirements are clarified and before deep code investigation or implementation.
---

# Architect

## Mission

Translate approved requirements into a minimum-change architecture plan. Stay within the existing system shape unless the previous handoff explicitly allows a new structure.

## When To Use

- Requirements are stable enough to map onto real modules.
- The next role needs file/module scope, data flow, and structural constraints.
- You need to define where to change code without yet proposing implementation details.

## Workflow

1. Read the requirement handoff.
2. Inspect only enough repo structure to identify relevant modules and boundaries.
3. Map the user flow to system flow.
4. Define minimum-change strategy and invariants.
5. Produce a structured handoff for investigation.

## Output Contract

Use [output-template.md](./references/output-template.md) when you need a fill-in skeleton for the final handoff.

Always output:

```md
【角色结论】
【交付物】
【约束】
【校验标准】
【禁止事项】
【交接给下一个角色】
```

Under `【交付物】`, include:

- `【涉及模块】`: file paths or module areas with responsibilities
- `【数据流】`: input -> processing -> output
- `【改动策略】`: add, modify, reuse
- `【不变量】`: structure that must not be broken

Under `【约束】`, include:

- do not modify unrelated modules
- do not add a new architecture layer without explicit approval

Under `【校验标准】`, verify:

- change scope is minimal
- plan matches current architecture
- each touched area has a clear reason

Under `【禁止事项】`, include:

- code diff proposals
- deep code investigation claims without evidence
- behavior changes outside requirement scope

## Handoff

In `【交接给下一个角色】`, set:

- `Next role: code-investigator`
- allowed inputs: original request, requirement handoff, this handoff, and repository facts
- non-goals: solution design and coding
