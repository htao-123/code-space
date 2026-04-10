# Workflow Gate Checklist

Use this checklist only when the automatic gate script cannot run because of local environment limitations.

## When To Use

- `python3` is unavailable
- the gate script cannot execute in the current environment
- the runtime is missing and cannot be repaired quickly

Do not use this checklist just for convenience. Prefer the automatic gate whenever possible.

## Manual Checks

Mark each item before implementation begins.

### 1. Current Task Document

- [ ] A current task document or planning document exists
- [ ] It matches the latest understanding of scope
- [ ] If the task changed, the document was updated first

### 2. Workflow Handoffs

- [ ] The latest required handoff exists
- [ ] It contains all required sections:
  - `【已核实输入】`
  - `【调研发现】`
  - `【角色结论】`
  - `【交付物】`
  - `【约束】`
  - `【校验标准】`
  - `【禁止事项】`
  - `【交接给下一个角色】`
- [ ] It contains the required Chinese handoff labels:
  - `- 下一角色：`
  - `- 可用输入：`
  - `- 非目标：`
  - `- 完成条件：`
- [ ] It records external research explicitly:
  - `- 是否需要外部调研`
  - `- 外部调研来源`
  - `- 外部调研结论`
- [ ] It records required handoff metadata explicitly:
  - `- 当前角色：`
  - `- 需求标识：`
  - `- 项目落点：`
- [ ] The latest handoff block, not an older block in the same file, is the one being validated
- [ ] The latest handoff block routes to the expected next role for the current stage
- [ ] The latest handoff block declares the expected current role for the current stage

### 3. Project Placement

- [ ] The approved project folder or landing zone is explicit
- [ ] New-project work is not scattered at repository root
- [ ] Existing-project work has an approved existing path or approved subfolder
- [ ] For existing-project work, documentation state is explicit: `documented` or `backfilled`
- [ ] If the existing project is already documented, the exact documentation artifact is named
- [ ] That documentation artifact declares the same approved `项目落点`
- [ ] If the existing project required backfill, the backfill document exists and is recorded as a workflow artifact
- [ ] That backfill document declares the same approved `项目落点`

### 4. Implementation Scope

- [ ] Target files or directories are named explicitly
- [ ] The targets are inside the approved project path
- [ ] The implementer is not coding outside the approved scope

### 5. Record The Fallback

- [ ] The task document records that automatic gate execution was unavailable
- [ ] The task document records that this manual checklist was used instead

## Completion Rule

Implementation may start only when every applicable checkbox is complete.

Before treating a requirement as finished, confirm that the latest handoff block routes to:

- `- 下一角色：无`

Also confirm that the closing chain exists and is ordered:

- implementer handoff -> `- 下一角色：审核员`
- reviewer handoff -> `- 下一角色：测试员`
- tester handoff -> `- 下一角色：知识归档员`
- knowledge-keeper handoff -> `- 下一角色：无`
- all four closing handoffs share the same `需求标识`
- all four closing handoffs share the same `项目落点`
