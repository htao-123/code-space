# Workflow Gate Checklist

Use this checklist only when the automatic gate script cannot run because the local environment cannot execute `python3`.

## Manual Checks

### 1. Project Document

- [ ] A current project document exists
- [ ] The document starts with frontmatter
- [ ] Frontmatter includes:
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
- [ ] Every workflow boolean field is `0` or `1`
- [ ] `workflow_current_stage` is one of:
  - `requirement-analyst`
  - `architect`
  - `code-investigator`
  - `solution-designer`
  - `implementer`
  - `reviewer`
  - `tester`
  - `knowledge-keeper`
  - `complete`

### 2. Handoff Shape

- [ ] The latest required handoff exists
- [ ] Each handoff contains:
  - `【角色结论】`
  - `【已核实输入】`
  - `【调研发现】`
  - `【交付物】`
  - `【约束】`
  - `【校验标准】`
  - `【禁止事项】`
  - `【交接给下一个角色】`
- [ ] Each handoff includes:
  - `- 当前角色标识：`
  - `- 当前交接标识：`
  - `- 需求标识：`
  - `- 下一角色标识：`
- [ ] Each handoff includes:
  - `- 下一角色：`
  - `- 可用输入：`
  - `- 非目标：`
  - `- 完成条件：`
- [ ] Each handoff includes:
  - `- 内部调研范围：`
  - `- 内部调研结论：`
  - `- 外部调研范围：`
  - `- 外部调研来源：`
  - `- 官方事实结论：`
  - `- 主流方案结论：`
  - `- 最佳实现参考结论：`
  - `- 是否发现新增外部差异：`
  - `- 推断说明：`
  - `- 未验证项：`
  - `- 需要用户确认：`
  - `- 推荐方案：`
  - `- 推荐原因：`
  - `- 主要权衡：`

### 3. Stage Rules

- [ ] `implementer` gate only runs when:
  - `workflow_current_stage: solution-designer`
  - `workflow_solution_approved: 1`
  - `workflow_pre_chain_verified: 1`
  - and the full pre-implementation chain exists
- [ ] `reviewer` gate only runs when:
  - `workflow_current_stage: implementer`
  - `workflow_implementer_passed: 1`
- [ ] `tester` gate only runs when:
  - `workflow_current_stage: reviewer`
  - `workflow_reviewer_passed: 1`
- [ ] `knowledge-keeper` gate only runs when:
  - `workflow_current_stage: tester`
  - `workflow_tester_passed: 1`
- [ ] `complete` gate only runs when:
  - `workflow_current_stage: knowledge-keeper`
  - `workflow_knowledge_keeper_passed: 1`
  - and the full 8-role chain exists in one project document

### 4. Content Quality

- [ ] If the current handoff is `solution-designer -> implementer`, it records `- 用户方案批准：`
- [ ] If the current handoff is `tester`, it records:
  - `- 运行时验证：`
  - `- 外部依赖验证：`
  - `- 未验证原因：`
- [ ] If the current handoff is `knowledge-keeper`, it records:
  - `- 需求复盘结论：`
  - `- 自我审查结论：`
  - `- 自我纠错项：`

### 5. Completion Rule

- [ ] Before setting `workflow_completion_passed: 1`, run the completion gate
- [ ] `workflow_completion_passed` stays `0` until completion actually passes
- [ ] After completion passes, AI may update:
  - `workflow_current_stage: complete`
  - `workflow_completion_passed: 1`
