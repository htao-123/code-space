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

1. Read the validated design, review, and test outcomes.
2. Distinguish facts from inference.
3. Summarize symptom, root cause, and fix.
4. Record reusable lessons and future watch-outs.
5. Produce a structured terminal handoff.

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

`【已核实输入】` and `【调研发现】` must include the metadata, research, evidence, fact mapping, inference, unknown, confirmation, requirement retrospective, self-review, self-correction, workflow retrospective, retained practices, rule-fix candidates, rule-update status, and any repair classification required by the pipeline contract.

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
- `完成条件：` completion gate can validate the closing chain
