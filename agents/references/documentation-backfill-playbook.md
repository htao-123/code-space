# Documentation Backfill Playbook

This playbook defines how to proceed when an existing project lacks usable documentation.

## Purpose

Prevent development from depending on memory or guesswork when working inside an undocumented existing project.

## When To Use

Use this playbook when:

- the project already exists
- there is no usable README, project document, or handoff chain for the current work
- the current change cannot be safely placed using existing documentation

If workflow needs to read and continue using a project document, and that document still uses the older pre-frontmatter workflow shape, first normalize it manually into the current frontmatter-first workflow shape.

Manual normalization must include at least:

- adding the required workflow frontmatter fields
- converting legacy handoff blocks to the current mandatory heading set
-补齐 metadata labels、调研标签与阶段所需字段
- ensuring the document lives under `<project>/docs/pipeline/` for real project work

Then continue with the backfill or normal workflow checks using the normalized project document.

For real projects, after upgrade or backfill, place all pipeline documents under:

```bash
<project>/docs/pipeline/YYYY-MM-DD-<project>-<topic>-<work-type>.md
```

The active requirement is the most recent pipeline document with `workflow_completion_passed: 0`.
Completed requirements have `workflow_completion_passed: 1` and serve as historical records.

## Principle

Do not code first.
Backfill the minimum documentation needed to let the workflow continue safely.

## Minimum Viable Documentation

Create enough documentation to support the current requirement. At minimum, capture:

- current task scope
- approved landing zone
- relevant modules or files
- known repository facts
- key unknowns
- risks or ambiguity

## Backfill Sequence

### 1. Inspect Repository Facts

Use repository evidence such as:

- directory structure
- entry files
- configuration files
- existing page or module names
- git history when useful

Do not infer intent without evidence.

### 2. Create The Current Task Document

Write a current project document that at least records:

- what is being changed
- where it is expected to land
- what is already known
- what still needs confirmation

The document should explicitly include:

- `- 需求标识：...`
- `- 项目落点：...`

For real projects, use these naming rules by default:

- pipeline document: `<project>/docs/pipeline/YYYY-MM-DD-<project>-<topic>-<work-type>.md`
- internal evidence: `<project>/references/internal/<topic>-<artifact>-YYYY-MM-DD.md`
- external research: `<project>/references/external/<topic>-research-YYYY-MM-DD.md`

The active requirement is identified by:
- Most recent filename date (YYYY-MM-DD prefix)
- `workflow_completion_passed: 0` in frontmatter


### 2.5 Normalize Legacy Project Documents

When an older project document predates the current workflow shape, normalize it manually before using it as gate input.

Normalization checklist:

- move the document into `<project>/docs/pipeline/` before treating it as active real-project workflow input
- add frontmatter with the current required workflow fields:
  - `requirement_id`
  - `workflow_project_type`
  - `workflow_work_type`
  - `workflow_doc_backfilled`
  - `workflow_current_stage`
  - `workflow_solution_approved`
  - `workflow_pre_chain_verified`
  - `workflow_implementer_passed`
  - `workflow_reviewer_passed`
  - `workflow_tester_passed`
  - `workflow_knowledge_keeper_passed`
  - `workflow_completion_passed`
- normalize frontmatter defaults:
  - all workflow pass fields must be `0` or `1`
  - `workflow_current_stage` must use the current role ids:
    - `requirement-analyst`
    - `architect`
    - `code-investigator`
    - `solution-designer`
    - `implementer`
    - `reviewer`
    - `tester`
    - `knowledge-keeper`
    - `complete`
  - `requirement_id` must match the active requirement across the whole document
- map any legacy role display names or old role ids into the current role ids before continuing
- ensure every handoff block contains, in this exact order:
  - `【角色结论】`
  - `【已核实输入】`
  - `【调研发现】`
  - `【交付物】`
  - `【约束】`
  - `【校验标准】`
  - `【禁止事项】`
  - `【交接给下一个角色】`
- ensure every handoff block also records:
  - `- 当前角色标识：`
  - `- 当前交接标识：`
  - `- 需求标识：`
  - `- 下一角色标识：`
- inject stage-required labels when they are missing:
  - tester must include:
    - `- 运行时验证：`
    - `- 外部依赖验证：`
    - `- 未验证原因：`
  - knowledge-keeper must include:
    - `- 需求复盘结论：`
    - `- 自我审查结论：`
    - `- 自我纠错项：`
  - solution-designer handing off to implementer must include:
    - `- 用户方案批准：`
- if `workflow_work_type: bugfix`, ensure the document also records:
  - `问题类型：bugfix`
  - `复现步骤：`
  - `预期结果：`
  - `实际结果：`
  - `根因摘要：`
  - `回归检查范围：`
- remove obsolete workflow structure that conflicts with the current pipeline contract, including old heading shapes, outdated metadata labels, and stale placeholders such as `待补录`

Do not treat a legacy document as valid gate input until the normalization has been completed.

### 3. Mark Unknowns Explicitly

Do not hide uncertainty.

If you cannot determine:

- the correct module
- the right entry point
- whether the work belongs to an existing module or a new subfolder

record that explicitly.

### 4. Resume Normal Workflow

Once the minimum document exists, continue with the normal role sequence.

## Stop Conditions

Stop and ask the user only when repository facts are insufficient to determine:

- the landing zone
- the relevant module boundary
- the current requirement scope

If those facts can be backfilled from the repository, do that first instead of asking immediately.
