# Workflow Gate Checklist

Use this checklist only when the automatic gate script cannot run because of local environment limitations.

## When To Use

- `python3` is unavailable
- the gate script cannot execute in the current environment
- the runtime is missing and cannot be repaired quickly

Do not use this checklist just for convenience. Prefer the automatic gate whenever possible.
If the automatic gate is failing only because of handoff formatting shape, normalize the handoff document first with `python3 agents/scripts/normalize_handoff_format.py --handoff-doc <doc> --write` before falling back to this checklist.

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
- [ ] It records quality evidence explicitly:
  - `- 内部证据清单：`
  - `- 外部证据清单：`
  - `- 事实清单：`
  - `- 证据映射：`
  - `- 推断说明：`
  - `- 未验证项：`
  - `- 需要用户确认：`
  - `- 推荐方案：`
  - `- 推荐原因：`
  - `- 主要权衡：`
- [ ] It records required handoff metadata explicitly:
  - `- 当前角色标识：`
  - `- 当前交接标识：`
  - `- 需求标识：`
  - `- 项目落点：`
  - `- 下一角色标识：`
- [ ] 非 `complete` 阶段校验的是当前文档的最新 handoff block；`complete` 阶段校验的是同一需求最近的收尾链 block
- [ ] 被校验的 handoff block `下一角色标识` matches the validated stage transition
- [ ] 被校验的 handoff block `当前角色标识` matches the validated stage transition
- [ ] The current `当前角色标识` content does not violate its role-specific禁止事项
- [ ] The handoff does not use weak phrases such as “查过了” without evidence
- [ ] `当前角色标识` and `下一角色标识` match the approved role transition
- [ ] `当前交接标识` is unique and includes the same `需求标识`
- [ ] `内部证据清单` uses `EVID-IN-* -> 文件路径` format and points to real files inside the approved project path
- [ ] `外部证据清单` uses `EVID-EX-* -> 本地快照路径 | URL` format when external research is required
- [ ] 外部证据快照文件存在且位于批准项目路径内
- [ ] `事实清单` uses `FACT-* -> 证据摘录：摘录内容` format
- [ ] `证据映射` binds each fact ID to `EVID-*::关键词::摘录`
- [ ] 非 `complete` 阶段的 gate 一次只校验一个 `--handoff-doc`
- [ ] 如果当前被校验 block 的 `当前角色标识` 是 `tester`，则必须记录：
  - `- 运行时验证：`
  - `- 外部依赖验证：`
  - `- 未验证原因：`
- [ ] 如果功能依赖外部 API、浏览器运行时或网络请求，测试结论不能只基于静态检查；必须完成真实成功路径验证，或明确记录未验证原因
- [ ] 如果外部成功路径被标记为“已真实验证”，则 `外部依赖验证` 必须绑定到一个具体 `用例 N`，且该用例在 `【测试结果】` 中为 `pass`
- [ ] 如果当前角色需要停下来请求用户确认，则 handoff 必须明确记录 `需要用户确认：是`，并给出 `推荐方案 / 推荐原因 / 主要权衡`
- [ ] 如果当前角色不需要用户确认，则 handoff 必须明确记录 `需要用户确认：否`

### 3. Project Placement

- [ ] The approved project folder or landing zone is explicit
- [ ] New-project work is not scattered at repository root
- [ ] Existing-project work has an approved existing path or approved subfolder
- [ ] For existing-project work, documentation state is explicit: `documented` or `backfilled`
- [ ] If the existing project is already documented, the exact documentation artifact is named
- [ ] That documentation artifact declares the same approved `项目落点`
- [ ] That documentation artifact is stored inside the approved project path
- [ ] If the existing project required backfill, the backfill document exists and is recorded as a workflow artifact
- [ ] That backfill document declares the same approved `项目落点`
- [ ] That backfill document is stored inside the approved project path

### 4. Implementation Scope

- [ ] Target files or directories are named explicitly
- [ ] The targets are inside the approved project path
- [ ] The implementer is not coding outside the approved scope

### 5. Record The Fallback

- [ ] The task document records that automatic gate execution was unavailable
- [ ] The task document records that this manual checklist was used instead

## Completion Rule

Implementation may start only when every applicable checkbox is complete.

Before treating a requirement as finished, confirm that the final block in the validated closing chain routes to:

- `- 下一角色：无`

Also confirm that the validated closing chain exists and is ordered:

- implementer handoff -> `- 下一角色：审核员`
- reviewer handoff -> `- 下一角色：测试员`
- tester handoff -> `- 下一角色：知识归档员`
- knowledge-keeper handoff -> `- 下一角色：无`
- all four closing handoffs share the same `需求标识`
- all four closing handoffs share the same `项目落点`
