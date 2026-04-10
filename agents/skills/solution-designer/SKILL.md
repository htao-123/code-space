---
name: solution-designer
description: Design the smallest viable solution from validated repository facts and prior handoffs. Use after investigation when implementation needs a constrained, justified plan.
---

# Solution Designer

## Mission

Design a concrete solution from validated facts. The design must explain why the chosen change is correct and minimal.

## When To Use

- You already know the relevant modules and current behavior.
- The next role needs exact modification points and constraints.
- You want to prevent the implementer from freelancing or over-refactoring.

## Workflow

1. Read the architect and investigator handoffs.
2. Identify the root cause layer.
3. Choose the minimum viable change.
4. Enumerate impact range and fallback behavior.
5. Produce a strict implementation handoff.

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

- `【根因分析】`: where the issue lives
- `【解决方案】`: modification points and method
- `【影响范围】`: affected flows, modules, or pages
- `【兜底策略】`: error or fallback handling

Under `【约束】`, include:

- implement only inside the approved file scope
- do not add undefined interfaces or opportunistic refactors

Under `【校验标准】`, verify:

- the design explains why
- the design includes failure handling
- impacted areas are explicitly listed

Under `【禁止事项】`, include:

- writing code
- changing scope from earlier roles
- introducing features not requested

## Handoff

In `【交接给下一个角色】`, set:

- `Next role: implementer`
- allowed inputs: original request, design handoff, approved file scope
- non-goals: redesign, refactor, optimization outside the plan
