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

1. Complete internal research on the requirement handoff, current project document, repo structure, and existing boundaries.
2. Complete external research and record official facts, mainstream approaches, and mature reference patterns that affect architecture.
3. Inspect only enough repo structure to identify relevant modules and boundaries.
4. Map the user flow to system flow.
5. Define minimum-change strategy and invariants.
6. Produce a structured handoff for investigation.

## Output Contract

Use [output-template.md](./references/output-template.md) when you need a fill-in skeleton for the final handoff.

Always output:

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

`【已核实输入】` and `【调研发现】` must include the metadata, research, unknown, confirmation, and schema/migration labels required by the pipeline contract. `【调研发现】` must explicitly separate internal research and external research results. Update `workflow_current_stage` to `architect` only after the architect handoff is complete.

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

- `下一角色：侦查员【负责收集代码事实、调用链与现有实现证据】`
- `可用输入：` original request, requirement handoff, this handoff, and repository facts
- `非目标：` solution design and coding
- `完成条件：` investigator has a valid module and boundary scope
