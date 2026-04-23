# Workflow Gate Standard Checklist

**Purpose:** This checklist is the only gate standard for workflow validation  
**Environment:** All operating systems (Windows / macOS / Linux)  
**When to run:** Before the pipeline advances to the next stage

---

## AI Execution Rules

- AI must execute this checklist item by item and must not decide from memory or impression.
- AI must read the current project document, the latest handoff for the current stage, and any required supporting context referenced by this checklist.
- If any required item fails, AI must repair the workflow artifact first before continuing implementation, review, testing, or archival.
- AI must not fake a passing gate by editing frontmatter state fields early, weakening handoff conclusions, or skipping missing items.
- AI must output one structured gate result after each gate run.

## Gate Output Template

```md
【门禁结论】
- 检查阶段：
- 检查结果：通过 / 不通过

【检查项结果】
- 项目文档存在性：通过 / 不通过
- frontmatter 完整性：通过 / 不通过
- 最新 handoff 完整性：通过 / 不通过
- 元数据一致性：通过 / 不通过
- 当前阶段前置条件：通过 / 不通过
- bugfix 必填项：通过 / 不适用 / 不通过
- completion 条件：通过 / 不适用 / 不通过

【失败项】
- 失败项 1：
- 影响：
- 修复建议：

【下一步】
- 可以继续到：
- 或必须先修复：
```

## Quick Start

**Read this before use:**
- This checklist is the only workflow gate standard and no longer depends on automation scripts.
- AI must check items in order; skipping steps can break the pipeline.
- If any item fails, it **must be fixed first** before work continues.
- AI must output a structured gate conclusion and explicitly mark pass / fail / not applicable.
- Estimated time: 5-15 minutes depending on project state.

---

## Part 1: Project Document Checks

### 1.1 Document Existence Check

**Steps:**
1. Open a terminal or command line.
2. Navigate to the project root directory.
3. Run: `ls -la <project>/docs/pipeline/ | tail -5`

**Validation points:**
- [ ] **Project document directory exists**:
  - For a real project, verify that `<project>/docs/pipeline/` exists.
  - For the rule system itself, verify that `agents/docs/context/workflow-system-context.md` exists.
- [ ] **There is an active requirement document**:
  - At least one document has `workflow_completion_passed: 0`.
  - The most recent unfinished document is the active requirement document.
- [ ] **Document path is correct**:
  - The document must live in the correct location and must not be scattered at repository root.
- [ ] **Real-project document placement is valid**:
  - Real-project pipeline documents must live under `<project>/docs/pipeline/`.
  - Real-project pipeline documents must not be written at repository root.
  - Real-project pipeline documents must not be written under `agents/`.
- [ ] **Scope / target is not out of bounds**:
  - The declared `项目落点`, target directories, and target file scope must stay inside the current project tree.
  - A pipeline document for project A must not point to project B's directory.
  - Handoff text such as expected landing zone or modification scope must not exceed the approved project boundary.
- [ ] **Rule-system documents and real-project documents are not mixed**:
  - Rule-system documents are only for maintaining `agents/` itself.
  - Real project work must not use a rule-system document as its project pipeline document.

**If this fails:**
```
ERROR: Project document is missing or incorrectly placed.
Fix:
1. Verify the project landing directory.
2. Verify that `docs/pipeline/` exists.
3. For a new project, create the required pipeline document first.
```

---

### 1.2 Frontmatter Completeness Check

**Steps:**
1. Open the project document and inspect the first 10 lines.
2. Verify there is a frontmatter block wrapped by `---`.
3. Check each required field one by one.

**Validation points:**
- [ ] **Base fields are complete**:
  ```yaml
  requirement_id: XXX-PROJECT-TOPIC-NNN
  workflow_project_type: new-project or existing-project
  workflow_work_type: feature/bugfix/task
  workflow_doc_backfilled: 0 or 1
  ```
- [ ] **Stage field is valid**:
  ```yaml
  workflow_current_stage: requirement-analyst/architect/code-investigator/
                       solution-designer/implementer/reviewer/tester/
                       knowledge-keeper/complete
  ```
- [ ] **Pass-state fields are valid**:
  ```yaml
  workflow_solution_approved: 0 or 1
  workflow_pre_chain_verified: 0 or 1
  workflow_implementer_passed: 0 or 1
  workflow_reviewer_passed: 0 or 1
  workflow_tester_passed: 0 or 1
  workflow_knowledge_keeper_passed: 0 or 1
  workflow_completion_passed: 0 or 1
  ```

**If this fails:**
```
ERROR: Frontmatter fields are missing or invalid.
Fix:
1. Add missing fields.
2. Ensure all boolean-like workflow fields are only `0` or `1`.
3. Ensure `workflow_current_stage` is one of the allowed values.
```

**Quick verification commands:**
```bash
# Find the latest unfinished requirement document
ls -t <project>/docs/pipeline/*.md | head -1 | xargs grep -l "workflow_completion_passed: 0" || echo "No active requirement found"
# Inspect frontmatter-related fields
head -20 <project>/docs/pipeline/YYYY-MM-DD-*.md | grep -E "workflow_|requirement_id"
```

---

## Part 2: Handoff Content Checks

### 2.1 Latest Handoff Existence Check

**Steps:**
1. Open the project document directory: `<project>/docs/pipeline/`.
2. Find the latest unfinished requirement document (`workflow_completion_passed: 0`).
3. Inspect the last handoff block in that document.
4. Verify that its `当前角色标识` matches `workflow_current_stage`.

**Validation points:**
- [ ] **The active requirement document is correct**:
  - The latest document with `workflow_completion_passed: 0` is the active requirement.
  - Completed requirements (`workflow_completion_passed: 1`) are history, not the current work target.
- [ ] **The latest handoff matches the current role**:
  - If `workflow_current_stage: architect`, the latest handoff must be architect output.
  - If `workflow_current_stage: solution-designer`, the latest handoff must be solution-designer output.
- [ ] **Handoff format is correct**:
  - It contains the complete required Chinese headings.

**If this fails:**
```
ERROR: Handoff is missing or the role does not match.
Fix:
1. Verify the active requirement document.
2. Verify that the last handoff is truly the latest role output.
3. If the document is stale, update it with the latest valid handoff.
4. If the pipeline is broken, resume from the correct break point.
```

---

### 2.2 Handoff Structure Completeness Check

**Steps:**
1. Locate the latest handoff block.
2. Verify all required Chinese headings exist.

**Validation points:**
- [ ] **All required headings exist**:
  ```
  【角色结论】
  【已核实输入】
  【调研发现】
  【交付物】
  【约束】
  【校验标准】
  【禁止事项】
  【交接给下一个角色】
  ```
- [ ] **Heading order is correct**:
  - The headings must stay in this order and must not be rearranged or skipped.

**If this fails:**
```
ERROR: Handoff structure is incomplete.
Fix:
1. Add missing sections.
2. Restore the required order.
3. Ensure the handoff is structurally complete.
```

---

### 2.3 Handoff Metadata Check

**Steps:**
1. Inspect the metadata labels inside the handoff block.
2. Verify every required label exists.

**Validation points:**
- [ ] **Core metadata labels exist**:
  ```
  - 当前角色标识：
  - 当前交接标识：
  - 需求标识：
  - 下一角色标识：
  ```
- [ ] **Metadata values are correct**:
  - `需求标识` must exactly match frontmatter `requirement_id`.
  - `当前角色标识` must match `workflow_current_stage`.
  - `下一角色标识` must point to the next valid role in the pipeline.

**If this fails:**
```
ERROR: Metadata labels are missing or inconsistent.
Fix:
1. Add missing labels.
2. Correct inconsistent identifiers.
3. Ensure requirement IDs stay consistent across the document.
```

---

### 2.4 Handoff Transfer Information Check

**Steps:**
1. Inspect the `【交接给下一个角色】` section.
2. Verify all required transfer information exists.

**Validation points:**
- [ ] **Transfer information is complete**:
  ```
  - 下一角色：角色中文名【职责说明】
  - 可用输入：明确的输入列表
  - 非目标：明确不做什么
  - 完成条件：具体的完成标准
  ```

**If this fails:**
```
ERROR: Transfer information is incomplete.
Fix:
1. Add the missing transfer information.
2. Ensure the next role has a clear execution guide.
```

---

### 2.4.1 Role-Level Handoff Quality Check (Strict)

**Steps:**
1. Determine the role type from `当前角色标识`.
2. Check required labels, forbidden content, and quality boundaries for that role.
3. Any failed hard rule means the gate fails.

**Validation points:**
- [ ] **Solution Designer -> Implementer required transfer content**:
  - `【交接给下一个角色】` must explicitly contain `用户方案批准`.
  - The approval outcome must be explicit and must not be phrased as “待确认” or “建议后续再确认”.
- [ ] **Tester required labels**:
  - Tester handoff must explicitly include:
    - `- 运行时验证：`
    - `- 外部依赖验证：`
    - `- 未验证原因：`
  - It must not rely only on vague claims such as “已测试” or “已验证通过”.
- [ ] **Knowledge Keeper required labels**:
  - Knowledge-keeper handoff must explicitly include:
    - `- 需求复盘结论：`
    - `- 自我审查结论：`
    - `- 自我纠错项：`
- [ ] **Role boundaries are respected**:
  - `code-investigator` must not output the final solution or decide the recommendation on behalf of the user.
  - `solution-designer` must not replace design with full implementation code.
  - `tester` must not replace explicit verification with “probably fine” reasoning.
  - `knowledge-keeper` must not omit retrospective, self-review, or self-correction content.
- [ ] **Weak conclusions and placeholder text are forbidden**:
  - Do not use weak phrases such as “暂不展开”, “自行处理”, “查过了”, or “大概没问题”.
  - Do not leave placeholders such as “待补录”, “后续再补”, or “暂未整理”.

**If this fails:**
```
ERROR: Handoff role-level quality is insufficient.
Fix:
1. Add the required role-specific labels and conclusions.
2. Remove out-of-scope content, weak conclusions, and placeholders.
3. Ensure the handoff depth matches the role responsibility.
```

---

### 2.5 Research Findings Check (Important)

**Steps:**
1. Inspect the `【调研发现】` section for completeness and format.
2. Verify all required internal and external research fields exist.

**Validation points:**
- [ ] **Research content is complete**:
  ```
  Internal research:
  - 内部调研范围：specific investigated scope
  - 内部调研结论：internal findings
  - 外部调研范围：external verification scope
  - 官方事实结论：official documentation / API findings
  - 主流方案结论：mainstream ecosystem approaches
  - 最佳实现参考结论：mature reference implementation findings
  - 是否发现新增外部差异：explicit difference record

  Inference:
  - 推断说明：evidence-based inference
  - 未验证项：explicit unverified content
  - 需要用户确认：whether user confirmation is needed
  - 推荐方案：explicit recommendation
  - 推荐原因：reason for recommendation
  - 主要权衡：main tradeoffs
  ```
- [ ] **External research was actually executed**:
  - It must not say `待补录` or `待调研`.
  - It must record actual external research results.
  - Even “no new difference found” must be recorded explicitly.

**If this fails:**
```
ERROR: Research findings are incomplete or external research was not actually executed.
Fix:
1. Add complete internal and external research findings.
2. Remove placeholder text.
3. Ensure external research actually happened.
```

---

## Failure Handling Rules

- If any required item fails, repair the workflow artifact first, then rerun the appropriate gate.
- Do not fake a pass by editing frontmatter state fields.
- Do not treat missing handoff content, research, approval, or bugfix required fields as formatting-only issues.
- Do not continue into coding, review, testing, or archival after a failed gate.

## Part 3: Stage Rule Checks

### 3.1 Implementer Gate Pass Conditions

**Applies when:** `workflow_current_stage` is `implementer` or the pipeline is preparing to enter `implementer`

**Validation points:**
- [ ] **All preconditions are satisfied**:
  ```
  ✅ workflow_current_stage: solution-designer
  ✅ workflow_solution_approved: 1
  ✅ workflow_pre_chain_verified: 1
  ```
- [ ] **The pre-implementation chain is complete**:
  - Requirement Analyst -> Architect -> Code Investigator -> Solution Designer all exist.
  - Every handoff is complete and valid.
- [ ] **User approval exists**:
  - The solution-designer handoff contains `用户方案批准：用户明确批准` or an equivalent explicit approval statement.

**If this fails:**
```
ERROR: Implementation gate conditions are not satisfied.
Fix:
1. Ensure all prerequisite stages are complete.
2. Ensure the solution has explicit user approval.
3. Add any missing handoffs.
```

---

### 3.2 Reviewer Gate Check

**Applies when:** `workflow_current_stage` is `reviewer` or the pipeline is preparing to enter `reviewer`

**Validation points:**
- [ ] **Preconditions are satisfied**:
  ```
  ✅ workflow_current_stage: implementer
  ✅ workflow_implementer_passed: 1
  ```
- [ ] **Implementation is complete**:
  - All planned code changes are finished.
  - Commit intent or implementation record clearly describes the change.
  - The code has passed a basic analysis check such as `dart analyze` or an equivalent check.
- [ ] **Review-fix-review loop is closed**:
  - If P0/P1 findings exist, the gate fails and the pipeline must return to implementer.
  - P2 findings are fixed by default.
  - Any deferred P2 has explicit deferral reason, risk record, and user approval.
  - Fixes made after review have been re-reviewed.
  - `workflow_reviewer_passed: 1` is set only after there are no blocking findings.

**If this fails:**
```
ERROR: Reviewer gate conditions are not satisfied.
Fix:
1. Ensure implementation is complete.
2. Run the relevant analysis check and fix basic issues.
3. Return blocking findings to implementer and re-review the fixes.
4. Finish all planned code changes.
```

---

### 3.3 Tester Gate Check

**Applies when:** `workflow_current_stage` is `tester` or the pipeline is preparing to enter `tester`

**Validation points:**
- [ ] **Preconditions are satisfied**:
  ```
  ✅ workflow_current_stage: reviewer
  ✅ workflow_reviewer_passed: 1
  ```
- [ ] **Testing validation is complete**:
  - `【交付物】` contains `【测试用例】`, `【测试结果】`, and the required testing conclusion fields.
  - Normal path, failure path, and boundary path are all covered.
  - Concrete test cases or verification methods are recorded.
  - `运行时验证 / 外部依赖验证 / 未验证原因` are explicitly recorded.

**If this fails:**
```
ERROR: Tester gate conditions are not satisfied.
Fix:
1. Ensure review is complete.
2. Add missing test coverage.
3. Record concrete verification methods and required testing labels.
```

---

### 3.4 Knowledge Keeper Gate Check

**Applies when:** `workflow_current_stage` is `knowledge-keeper` or the pipeline is preparing to enter `knowledge-keeper`

**Validation points:**
- [ ] **Preconditions are satisfied**:
  ```
  ✅ workflow_current_stage: tester
  ✅ workflow_tester_passed: 1
  ```
- [ ] **Archive content is complete**:
  - Problem records, lessons, and future precautions are recorded.
  - `需求复盘结论 / 自我审查结论 / 自我纠错项` are explicitly included.

**If this fails:**
```
ERROR: Knowledge-keeper gate conditions are not satisfied.
Fix:
1. Ensure testing is complete.
2. Add the missing archive content.
3. Ensure retrospective and self-review records are complete.
```

---

## Part 4: Completion Rule Checks

### 4.1 Completion Gate Check

**Applies when:** the workflow is preparing to set `workflow_completion_passed: 1`

**Validation points:**
- [ ] **The full 8-role chain exists**:
  - All handoffs from `requirement-analyst` through `knowledge-keeper` exist.
  - Every handoff satisfies the checks in this checklist.
  - The chain is continuous and unbroken.
- [ ] **All required gate flags have passed**:
  ```
  ✅ workflow_solution_approved: 1
  ✅ workflow_pre_chain_verified: 1
  ✅ workflow_implementer_passed: 1
  ✅ workflow_reviewer_passed: 1
  ✅ workflow_tester_passed: 1
  ✅ workflow_knowledge_keeper_passed: 1
  ```
- [ ] **Final state is correct**:
  - `workflow_current_stage: knowledge-keeper`
  - All required fixes and improvements are recorded in the handoff chain.

**If this fails:**
```
ERROR: Completion gate conditions are not satisfied.
Fix:
1. Ensure all 8 roles are complete.
2. Verify all gate conditions are satisfied.
3. Add any missing chain segments.
```

---

## Part 5: Special Scenario Checks

### 5.1 Bugfix Mode Extra Check

**Applies when:** `workflow_work_type: bugfix`

**Validation points:**
- [ ] **Bugfix-specific fields exist**:
  ```
  问题类型：bugfix
  复现步骤：specific reproduction steps
  预期结果：expected result
  实际结果：actual result
  根因摘要：root cause summary
  回归检查范围：regression scope
  ```
- [ ] **All downstream required content exists**:
  - Root-cause summary
  - Regression scope
  - Fix verification

**If this fails:**
```
ERROR: Bugfix-mode information is incomplete.
Fix:
1. Add all required bugfix fields.
2. Ensure root-cause analysis is explicit.
3. Ensure regression scope is explicit.
```

---

### 5.2 Data Migration Check

**Applies when:** historical data structure changes are involved

**Validation points:**
- [ ] **Migration strategy is explicit**:
  - The old structure is recorded.
  - The new structure is recorded.
  - The migration path is defined.
  - The compatibility decision is explained, including why runtime compatibility is not the default.
- [ ] **Migration artifact exists when needed**:
  - If migration is required, the script or migration entrypoint exists.
  - The migration entry is defined.
  - Rollback or recovery thinking is recorded.

**If this fails:**
```
ERROR: Data migration handling is insufficient.
Fix:
1. Record the real data-structure differences.
2. Define a concrete migration path.
3. Avoid default permanent runtime compatibility branches.
```

---

## Part 6: Environment-Specific Checks

### 6.1 Windows Environment Check

**Special considerations:**
- [ ] **Path separator handling**: use `/` consistently where the workflow expects repository-style paths.
- [ ] **Command execution environment**: if commands are needed, use Git Bash or PowerShell.
- [ ] **Permissions**: verify the environment can read and update workflow documents.

### 6.2 Linux / macOS Environment Check

**Special considerations:**
- [ ] **Permissions**: verify the environment can read and update workflow documents.
- [ ] **Dependencies**: verify Git is available when history or document location inspection is needed.
- [ ] **Equivalent execution**: if example commands are unavailable, use an equivalent method instead of skipping the gate.

---

## Troubleshooting Guide

### Issue 1: Cannot find the project document

**Symptoms:**
```
ls: cannot access '<project>/docs/pipeline/': No such file or directory
or: No active requirement found (all documents have workflow_completion_passed: 1)
```

**Fix:**
1. Verify the project path.
2. Verify you are in the correct project.
3. For a new project, create `docs/pipeline/` and the first pipeline document.
4. If all requirements are completed, create a new pipeline document for the new requirement.

---

### Issue 2: Frontmatter format problems

**Symptoms:**
- frontmatter field value types are invalid
- required fields are missing

**Fix:**
1. Check field value types (`0` / `1` only for workflow flag fields).
2. Add missing fields based on this checklist.
3. Ensure `workflow_current_stage` is in the allowed list.

---

### Issue 3: Handoff content is incomplete

**Symptoms:**
- required headings are missing
- metadata labels are missing
- research findings are incomplete

**Fix:**
1. Follow Part 2 of this checklist.
2. Add all required headings and labels.
3. Ensure external research actually happened.
4. Remove all placeholder content.

---

### Issue 4: Stage conditions are not satisfied

**Symptoms:**
- the pipeline cannot safely enter the next stage
- the gate fails

**Fix:**
1. Verify the current stage state.
2. Verify all prerequisites are satisfied.
3. Add any missing handoffs or required content.

---

## Completion Confirmation

After all checks above pass:

- [ ] It is safe to enter the next stage.
- [ ] All relevant gate conditions are satisfied.
- [ ] Document quality and completeness have been validated.

**Next step:**
- Decide whether the workflow can safely continue based on the current `workflow_current_stage` and the gate result.
- If the gate passes, the pipeline may move to the next role.
- If the gate fails, the missing items must be fixed first.

---

## Important Reminders

1. **Do not skip checks**: even when things look correct, check each required item.
2. **Do not assume**: verify facts instead of assuming they are correct.
3. **Stay strict**: this checklist is the formal gate standard.
4. **Record checklist defects**: if the checklist itself has a problem, report and fix it.

---

**Last updated:** 2026-04-22  
**Execution note:** This checklist is the gate execution mechanism.  
**Maintainer:** AI Pipeline System
