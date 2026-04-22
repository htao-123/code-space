# Workflow Gate 标准检查清单

**定位：** 本清单是 workflow gate 的唯一检查依据  
**适用环境：** 所有操作系统（Windows/Mac/Linux）  
**检查频率：** 每次 pipeline 进入下一阶段前

---

## 🤖 AI 执行规则

- AI 必须逐项执行本清单，不得凭经验或印象直接判定通过。
- AI 必须读取当前项目文档、当前阶段对应 handoff，以及本清单要求的相关上下文。
- AI 若发现任一必需项失败，必须先修复 workflow artifact，再继续实现、审查、测试或归档。
- AI 不得通过提前修改 frontmatter 状态字段、弱化 handoff 结论或跳过缺失项来伪造门禁通过。
- AI 在每次 gate 结束后，都必须输出一份结构化门禁结果。

## 🧾 门禁输出模板

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

## 🚀 快速开始

**使用前必读：**
- ✅ 本清单是 workflow gate 的唯一标准，不再依赖自动脚本
- ✅ AI 必须按顺序检查，跳过任何步骤都可能导致 pipeline 破坏
- ✅ 如果某项检查失败，**必须先修复**才能继续下一步
- ✅ AI 必须输出结构化门禁结论，明确写出通过 / 不通过 / 不适用
- ⏱️ 预计耗时：5-15分钟（取决于项目状态）

---

## 📋 第一部分：项目文档检查

### 1.1 文档存在性检查

**步骤：**
1. 打开终端/命令行
2. 导航到项目根目录（包含 `agents/` 文件夹）
3. 运行：`ls -la <project>/docs/pipeline/ | tail -5`

**验证点：**
- [ ] **项目文档目录存在**：
  - 对于真实项目：检查 `<project>/docs/pipeline/` 目录是否存在
  - 对于规则系统：检查 `agents/docs/context/workflow-system-context.md` 是否存在
- [ ] **有活动需求的文档**：
  - 目录中存在至少一个 `workflow_completion_passed: 0` 的文档
  - 最新日期的未完成文档即为当前活动需求的文档
- [ ] **文档路径正确**：文档必须在正确的位置，不能在根目录散落
- [ ] **真实项目文档落点合法**：
  - 真实项目的 pipeline 文档必须位于 `<project>/docs/pipeline/`
  - 不允许把真实项目的 pipeline 文档写在仓库根目录
  - 不允许把真实项目的 pipeline 文档写在 `agents/` 目录下
- [ ] **scope / target 没有越界**：
  - 文档里声明的 `项目落点`、目标目录、目标文件范围必须位于当前项目树内
  - 不允许把 A 项目的 pipeline 文档指向 B 项目的目录
  - 不允许 handoff 中的“预计落点”“修改范围”超出已批准项目边界
- [ ] **规则系统与真实项目不混用**：
  - 规则系统文档只能用于 `agents/` 自身规则维护
  - 真实项目工作不能拿规则系统文档充当项目 pipeline 文档

**如果失败：**
```
🚨 错误：项目文档不存在或位置错误
📍 解决方案：
   1. 确认项目落点目录是否正确
   2. 检查是否遗漏了 docs/pipeline/ 目录
   3. 对于新项目，需要先创建 pipeline 文档
```

---

### 1.2 Frontmatter 完整性检查

**步骤：**
1. 打开项目文档，查看前10行
2. 确认是否有 `---` 包裹的 frontmatter 块
3. 逐一检查以下字段是否存在

**验证点：**
- [ ] **基础字段完整**：
  ```yaml
  requirement_id: XXX-PROJECT-TOPIC-NNN
  workflow_project_type: new-project 或 existing-project
  workflow_work_type: feature/bugfix/task
  workflow_doc_backfilled: 0 或 1
  ```
- [ ] **阶段字段正确**：
  ```yaml
  workflow_current_stage: requirement-analyst/architect/code-investigator/
                       solution-designer/implementer/reviewer/tester/
                       knowledge-keeper/complete
  ```
- [ ] **通过状态字段**：
  ```yaml
  workflow_solution_approved: 0 或 1
  workflow_pre_chain_verified: 0 或 1
  workflow_implementer_passed: 0 或 1
  workflow_reviewer_passed: 0 或 1
  workflow_tester_passed: 0 或 1
  workflow_knowledge_keeper_passed: 0 或 1
  workflow_completion_passed: 0 或 1
  ```

**如果失败：**
```
🚨 错误：frontmatter 字段缺失或类型错误
📍 解决方案：
   1. 添加缺失的字段
   2. 确保 boolean 字段只能是 0 或 1
   3. 确保 workflow_current_stage 值在允许列表内
```

**快速验证命令：**
```bash
# 查找最新的未完成需求文档
ls -t <project>/docs/pipeline/*.md | head -1 | xargs grep -l "workflow_completion_passed: 0" || echo "No active requirement found"
# 提取 frontmatter 检查
head -20 <project>/docs/pipeline/YYYY-MM-DD-*.md | grep -E "workflow_|requirement_id"
```

---

## 📋 第二部分：Handoff 内容检查

### 2.1 最新 Handoff 存在性检查

**步骤：**
1. 打开项目文档目录：`<project>/docs/pipeline/`
2. 找到最新的未完成需求文档（`workflow_completion_passed: 0`）
3. 查看该文档末尾的最后一个 handoff 块
4. 确认其 `当前角色标识` 是否与 `workflow_current_stage` 匹配

**验证点：**
- [ ] **活动需求文档正确**：
  - 最新日期且 `workflow_completion_passed: 0` 的文档是当前活动需求
  - 已完成需求（`workflow_completion_passed: 1`）不作为当前工作目标
- [ ] **最新 handoff 的角色匹配**：
  - 如果 `workflow_current_stage: architect`，最新 handoff 应该是 `Architect` 的输出
  - 如果 `workflow_current_stage: solution-designer`，最新 handoff 应该是 `Solution Designer` 的输出
- [ ] **Handoff 格式正确**：包含完整的中文标题

**如果失败：**
```
🚨 错误：handoff 缺失或角色不匹配
📍 解决方案：
   1. 确认活动需求文档是否正确（未完成且最新）
   2. 确认最新的 handoff 块确实是最新的角色输出
   3. 如果文档是旧的，需要更新到最新的 handoff
   4. 如果 pipeline 断裂，需要从断点继续
```

---

### 2.2 Handoff 结构完整性检查

**步骤：**
1. 定位到最新的 handoff 块
2. 检查是否包含所有必需的中文标题

**验证点：**
- [ ] **必需标题全部存在**：
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
- [ ] **标题顺序正确**：必须按上述顺序，不能颠倒或跳过

**如果失败：**
```
🚨 错误：handoff 结构不完整
📍 解决方案：
   1. 添加缺失的标题段
   2. 调整标题顺序
   3. 确保 handoff 完整性
```

---

### 2.3 Handoff 元数据检查

**步骤：**
1. 检查每个 handoff 块中的元数据标签
2. 确认所有必需标签都存在

**验证点：**
- [ ] **核心元数据标签**：
  ```
  - 当前角色标识：
  - 当前交接标识：
  - 需求标识：
  - 下一角色标识：
  ```
- [ ] **标签值正确性**：
  - `需求标识` 必须与 frontmatter 中的 `requirement_id` 完全一致
  - `当前角色标识` 必须与 `workflow_current_stage` 对应
  - `下一角色标识` 必须指向 pipeline 的下一个角色

**如果失败：**
```
🚨 错误：元数据标签缺失或不匹配
📍 解决方案：
   1. 添加缺失的标签
   2. 修正不一致的标识符
   3. 确保需求 ID 在整个文档中保持一致
```

---

### 2.4 Handoff 交接信息检查

**步骤：**
1. 在每个 handoff 的 `【交接给下一个角色】` 部分检查
2. 确认包含所有必需的交接信息

**验证点：**
- [ ] **交接信息完整**：
  ```
  - 下一角色：角色中文名【职责说明】
  - 可用输入：明确的输入列表
  - 非目标：明确不做什么
  - 完成条件：具体的完成标准
  ```

**如果失败：**
```
🚨 错误：交接信息不完整
📍 解决方案：
   1. 补充缺失的交接信息
   2. 确保下一角色有清晰的指导
```

---

### 2.4.1 角色级 Handoff 质量检查（严格）

**步骤：**
1. 根据最新 handoff 的 `当前角色标识` 判断角色类型
2. 对照该角色的强制字段、禁止事项、质量边界逐项检查
3. 任一角色级硬规则不满足，都视为 gate 不通过

**验证点：**
- [ ] **Solution Designer → Implementer 交接强制项**：
  - `【交接给下一个角色】` 中必须明确写出 `用户方案批准`
  - 必须明确说明批准结论，不允许写成“待确认”“建议后续再确认”
- [ ] **Tester 强制项**：
  - tester handoff 必须显式包含：
    - `- 运行时验证：`
    - `- 外部依赖验证：`
    - `- 未验证原因：`
  - 不能只写“已测试”“已验证通过”这类笼统描述
- [ ] **Knowledge Keeper 强制项**：
  - knowledge-keeper handoff 必须显式包含：
    - `- 需求复盘结论：`
    - `- 自我审查结论：`
    - `- 自我纠错项：`
- [ ] **角色禁止事项边界明确**：
  - `code-investigator` 不应输出最终解决方案或直接替用户拍板推荐方案
  - `solution-designer` 不应直接写成完整实现代码或用实现细节替代方案设计
  - `tester` 不应用“未验证但默认没问题”替代明确验证结论
  - `knowledge-keeper` 不应省略复盘、自审与纠错沉淀
- [ ] **弱结论与占位表述禁止**：
  - 不允许使用“暂不展开”“自行处理”“查过了”“大概没问题”这类弱化结论
  - 不允许保留“待补录”“后续再补”“暂未整理”这类占位语句

**如果失败：**
```
🚨 错误：handoff 角色级质量不达标
📍 解决方案：
   1. 按角色补齐强制标签和结论
   2. 移除越权内容、弱结论和占位语句
   3. 确保 handoff 的内容深度与当前角色职责一致
```

---

### 2.5 调研发现检查（重要）

**步骤：**
1. 检查 `【调研发现】` 部分的完整性和格式
2. 确认包含内外部调研的所有必需字段

**验证点：**
- [ ] **调研完整性**：
  ```
  内部调研：
  - 内部调研范围：具体调查范围
  - 内部调研结论：调查结果
  - 外部调研范围：外部验证范围
  - 官方事实结论：官方文档/API验证结果
  - 主流方案结论：主流生态系统做法
  - 最佳实现参考结论：成熟参考实现
  - 是否发现新增外部差异：明确的发现记录
  
  推断部分：
  - 推断说明：基于证据的推论
  - 未验证项：明确标记未验证内容
  - 需要用户确认：是否需要用户批准
  - 推荐方案：明确的推荐
  - 推荐原因：推荐理由
  - 主要权衡：权衡考虑
  ```
- [ ] **外部调研真实执行**：
  - 不能写"待补录"、"待调研"
  - 必须记录实际的调研结果
  - 即使"无发现"也要明确记录

**如果失败：**
```
🚨 错误：调研发现不完整或未执行外部调研
📍 解决方案：
   1. 补充完整的内外部调研
   2. 移除"待补录"占位符
   3. 确保外部调研已经真实执行
```

---

## ❌ 检查失败时的处理规则

- 若任一必需项不通过，必须先修复对应 workflow artifact，再重新从相关阶段执行完整 gate。
- 不允许通过修改 frontmatter 状态字段来“补通过”。
- 不允许把缺失的 handoff、调研、批准、bugfix 必填项视为格式问题直接忽略。
- 不允许在门禁失败时直接进入编码、审查、测试或归档。

## 📋 第三部分：阶段规则检查

### 3.1 Implementer Gate 通过条件

**适用场景：** 当 `workflow_current_stage` 是 `implementer` 或准备进入 `implementer` 时

**验证点：**
- [ ] **前置条件全部满足**：
  ```
  ✅ workflow_current_stage: solution-designer
  ✅ workflow_solution_approved: 1
  ✅ workflow_pre_chain_verified: 1
  ```
- [ ] **前置链条完整**：
  - Requirement Analyst → Architect → Code Investigator → Solution Designer 全部存在
  - 每个 handoff 都是完整和有效的
- [ ] **用户批准存在**：
  - `Solution Designer` 的 handoff 中包含 `用户方案批准：用户明确批准` 或类似内容

**如果失败：**
```
🚨 错误：implementation gate 条件不满足
📍 解决方案：
   1. 确认所有前置阶段都已完成
   2. 确认方案已获得用户明确批准
   3. 补充任何缺失的 handoff
```

---

### 3.2 Reviewer Gate 检查

**适用场景：** 当 `workflow_current_stage` 是 `reviewer` 或准备进入 `reviewer` 时

**验证点：**
- [ ] **前置条件满足**：
  ```
  ✅ workflow_current_stage: implementer
  ✅ workflow_implementer_passed: 1
  ```
- [ ] **实现已完成**：
  - 所有计划的代码修改都已完成
  - 提交信息清晰描述了所做的更改
  - 代码通过了基本的分析检查（`dart analyze` 或等价）

**如果失败：**
```
🚨 错误：reviewer gate 条件不满足
📍 解决方案：
   1. 确认实现阶段已经完成
   2. 运行代码分析工具修复基本问题
   3. 完成所有计划的代码修改
```

---

### 3.3 Tester Gate 检查

**适用场景：** 当 `workflow_current_stage` 是 `tester` 或准备进入 `tester` 时

**验证点：**
- [ ] **前置条件满足**：
  ```
  ✅ workflow_current_stage: reviewer
  ✅ workflow_reviewer_passed: 1
  ```
- [ ] **测试验证完整**：
  - `【交付物】` 中包含 `【测试用例】`、`【测试结果】` 以及测试结论所需字段
  - 正常路径、失败路径、边界条件都已覆盖
  - 记录了具体的测试案例或验证方法
  - 明确记录 `运行时验证 / 外部依赖验证 / 未验证原因`

**如果失败：**
```
🚨 错误：tester gate 条件不满足
📍 解决方案：
   1. 确认审查阶段已完成
   2. 补充测试验证的覆盖范围
   3. 记录具体的验证方法
```

---

### 3.4 Knowledge Keeper Gate 检查

**适用场景：** 当 `workflow_current_stage` 是 `knowledge-keeper` 或准备进入 `knowledge-keeper` 时

**验证点：**
- [ ] **前置条件满足**：
  ```
  ✅ workflow_current_stage: tester
  ✅ workflow_tester_passed: 1
  ```
- [ ] **归档内容完整**：
  - 问题记录、经验总结、未来注意事项都已记录
  - 显式包含 `需求复盘结论 / 自我审查结论 / 自我纠错项`

**如果失败：**
```
🚨 错误：knowledge-keeper gate 条件不满足
📍 解决方案：
   1. 确认测试阶段已完成
   2. 补充归档所需的所有内容
   3. 确保复盘和审查记录完整
```

---

## 📋 第四部分：完成规则检查

### 4.1 Completion Gate 检查

**适用场景：** 当准备设置 `workflow_completion_passed: 1` 时

**验证点：**
- [ ] **完整的 8 角色链条**：
  - 从 `requirement-analyst` 到 `knowledge-keeper` 的所有 handoff 都存在
  - 每个 handoff 都满足本清单的所有检查项
  - 链条是连续的，没有断裂或跳跃
- [ ] **所有 gate 都已通过**：
  ```
  ✅ workflow_solution_approved: 1
  ✅ workflow_pre_chain_verified: 1
  ✅ workflow_implementer_passed: 1
  ✅ workflow_reviewer_passed: 1
  ✅ workflow_tester_passed: 1
  ✅ workflow_knowledge_keeper_passed: 1
  ```
- [ ] **最终状态正确**：
  - `workflow_current_stage: knowledge-keeper`
  - 所有修复和改进都已记录在 handoff 中

**如果失败：**
```
🚨 错误：completion gate 条件不满足
📍 解决方案：
   1. 确认所有 8 个角色都已完成
   2. 验证所有 gate 条件都已满足
   3. 补充任何缺失的环节
```

---

## 📋 第五部分：特殊场景检查

### 5.1 Bugfix 模式额外检查

**适用场景：** 当 `workflow_work_type: bugfix` 时

**验证点：**
- [ ] **Bugfix 特有字段存在**：
  ```
  问题类型：bugfix
  复现步骤：具体的复现步骤
  预期结果：预期应该看到什么
  实际结果：实际看到了什么
  根因摘要：问题的根本原因
  回归检查范围：需要检查的影响范围
  ```
- [ ] **所有下游阶段都包含**：
  - 根因摘要
  - 回归检查范围
  - 修复验证

**如果失败：**
```
🚨 错误：bugfix 模式信息不完整
📍 解决方案：
   1. 补充 bugfix 特有的所有字段
   2. 确保根因分析清晰
   3. 明确回归检查范围
```

---

### 5.2 数据迁移检查

**适用场景：** 当涉及历史数据结构变更时

**验证点：**
- [ ] **迁移策略明确**：
  - 旧数据结构已记录
  - 新数据结构已设计
  - 迁移路径已定义
  - 兼容性处理已说明（为什么不用运行时兼容）
- [ ] **迁移脚本存在**：
  - 如果需要迁移，脚本已创建
  - 迁移入口已定义
  - 回滚策略已考虑

**如果失败：**
```
🚨 错误：数据迁移处理不当
📍 解决方案：
   1. 明确记录数据结构差异
   2. 设计明确的迁移路径
   3. 避免默认的永久运行时兼容分支
```

---

## 📋 第六部分：环境特定检查

### 6.1 Windows 环境检查

**特殊考虑：**
- [ ] **路径分隔符**：确认使用 `/` 而非 `\`
- [ ] **命令执行**：如果需要运行命令，使用 Git Bash 或 PowerShell
- [ ] **文件权限**：确认有读写权限

### 6.2 Linux/Mac 环境检查

**特殊考虑：**
- [ ] **权限**：确认当前环境可读取和修改 workflow 文档
- [ ] **依赖**：确认 Git 已安装，便于查看历史和定位相关文档
- [ ] **命令可替代性**：若示例命令不可用，必须用等价方式完成检查，不能因此跳过门禁

---

## 🔧 故障排除指南

### 问题 1：找不到项目文档

**症状：**
```
ls: cannot access '<project>/docs/pipeline/': No such file or directory
或：No active requirement found (所有文档都是 workflow_completion_passed: 1)
```

**解决方案：**
1. 确认项目路径是否正确
2. 检查是否在正确的项目目录中
3. 对于新项目，可能需要先创建 docs/pipeline/ 目录和第一个 pipeline 文档
4. 如果所有需求都已完成，需要为新的需求创建新的 pipeline 文档

---

### 问题 2：Frontmatter 格式错误

**症状：**
- Frontmatter 字段值类型不正确
- 缺少必需的字段

**解决方案：**
1. 检查字段值的类型（boolean 只能是 0 或 1）
2. 对照本清单补充缺失字段
3. 确保 `workflow_current_stage` 值在允许列表中

---

### 问题 3：Handoff 内容不完整

**症状：**
- 缺少必需的标题
- 元数据标签缺失
- 调研发现不完整

**解决方案：**
1. 参考本清单的第二部分
2. 补充所有必需的标题和标签
3. 确保外部调研已真实执行
4. 移除所有"待补录"占位符

---

### 问题 4：Stage 条件不满足

**症状：**
- Pipeline 无法进入下一阶段
- Gate 检查失败

**解决方案：**
1. 确认当前阶段状态正确
2. 验证所有前置条件都满足
3. 补充任何缺失的 handoff 或内容

---

## 📝 检查完成确认

当上述所有检查都通过后：

- [ ] **可以安全进入下一阶段**
- [ ] **所有 gate 条件已满足**
- [ ] **文档质量和完整性已验证**

**下一步：**
- 根据当前 `workflow_current_stage` 和通过检查的情况，决定是否可以继续 pipeline
- 如果通过，可以安全地进入下一个角色
- 如果未通过，需要先修复问题再继续

---

## ⚠️ 重要提醒

1. **不要跳过检查**：即使看起来"没问题"，也要逐项检查
2. **不要假设**：不要假设某些内容"应该是对的"，要实际验证
3. **严格遵循**：这个清单本身就是正式门禁标准，不能降低标准
4. **记录问题**：如果发现检查清单本身的问题，及时反馈改进

---

**最后更新：** 2026-04-17  
**执行说明：** 本清单由 AI 直接执行并记录结果，不再依赖自动 gate 脚本。  
**维护者：** AI Pipeline System
