---
name: tester
description: Verify behavior with test cases and execution evidence, including success, failure, and edge-case coverage. Use after review when the pipeline needs proof instead of assumptions.
---

# Tester

## Mission

Prove whether the change actually works. Reproduce the target behavior, validate fixes, and test failure paths.

## When To Use

- The code is implemented and reviewed, but behavior still needs proof.
- A bugfix must be reproduced and retested.
- Failure paths or edge cases are easy to overlook.

## Workflow

1. Complete internal research on the design handoff, review handoff, current project document, and available validation paths.
2. Complete external research and record official facts, mainstream approaches, and mature validation patterns relevant to testing.
3. Define normal, abnormal, and boundary test cases.
4. Run available tests or document blockers.
5. Record pass, fail, or blocked with evidence.
6. Hand off only validated conclusions.

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

`【已核实输入】` and `【调研发现】` must include the metadata, research, unknown, confirmation, runtime verification, external-dependency verification, and unverified-reason labels required by the pipeline contract. `【调研发现】` must explicitly separate internal research and external research results. After tester handoff is complete, update `workflow_current_stage: tester` and `workflow_tester_passed: 1`.

Under `【交付物】`, include:

- `【测试用例】`: normal, abnormal, and boundary cases
- `【测试结果】`: pass, fail, blocked with evidence

Under `【约束】`, include:

- archive only validated conclusions
- carry forward any blocked or unverified risks

Under `【校验标准】`, verify:

- key path is covered
- failure path is covered
- original issue can be reproduced or clearly cannot be reproduced

Under `【禁止事项】`, include:

- assuming success
- omitting failed cases
- hiding environment blockers

## Handoff

In `【交接给下一个角色】`, set:

- `下一角色：知识归档员【负责沉淀问题记录、修复方式与可复用经验】`
- `可用输入：` original request, design handoff, review handoff, this handoff
- `非目标：` inventing results that were not tested
- `完成条件：` validated facts and unverified items are both explicit
