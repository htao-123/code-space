---
name: knowledge-keeper
description: Archive the problem, root cause, fix, test outcome, and reusable lessons in a structured record. Use at the end of the pipeline to preserve validated knowledge for later sessions.
---

# Knowledge Keeper

## Mission

Capture reusable knowledge after implementation and validation are complete.

## When To Use

- The pipeline has reached the final archival stage.
- Another engineer or agent should be able to reuse the outcome later.
- You need a clean record of symptom, root cause, fix, and remaining risk.

## Workflow

1. Complete internal research on the validated design, review, test outcomes, and current project document.
2. Complete external research and record official facts, mainstream approaches, and mature reusable patterns relevant to archival conclusions.
3. Distinguish facts from inference.
4. Summarize symptom, root cause, and fix.
5. Record reusable lessons and future watch-outs.
6. Produce a structured terminal handoff.

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

`【已核实输入】` and `【调研发现】` must include the metadata, research, unknown, confirmation, requirement retrospective, self-review, and self-correction required by the pipeline contract. `【调研发现】` must explicitly separate internal research and external research results. After the archive handoff is complete, update `workflow_current_stage: knowledge-keeper` and `workflow_knowledge_keeper_passed: 1`. Only after the completion gate passes may AI update `workflow_current_stage: complete` and `workflow_completion_passed: 1`.

Under `【交付物】`, include:

- `【问题记录】`: symptom, root cause, fix
- `【经验总结】`: reusable lessons, future watch-outs, related modules

Under `【约束】`, include:

- only archive validated information
- mark blocked or uncertain results clearly

Under `【校验标准】`, verify:

- another engineer or agent could reuse this without re-discovery
- the record distinguishes fact from inference

Under `【禁止事项】`, include:

- vague summary
- unvalidated claims
- restating the whole conversation without structure

## Handoff

In `【交接给下一个角色】`, set:

- `下一角色：无【当前需求已完成完整流程】`
- `可用输入：` current requirement's complete handoff chain
- `非目标：` continuing into a new requirement
- `完成条件：` completion gate can validate the full 8-role chain
