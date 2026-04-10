# AI Workflow Repository

这个仓库当前主要用于维护 AI 开发体系本身，包括：

- `AGENTS.md`
- `agents/`
- workflow gate / quality checker / checklist
- role skills / templates / contract

## AI 开发体系概览

这套体系的核心目标不是“让 AI 直接写代码”，而是让 AI 严格遵守工程流程。

标准角色顺序是：

1. `requirement-analyst`
2. `architect`
3. `code-investigator`
4. `solution-designer`
5. `implementer`
6. `reviewer`
7. `tester`
8. `knowledge-keeper`

总控入口是：

- `ai-pipeline-orchestrator`

它负责决定当前应该进入哪个角色、阻止跳步、阻止缺 handoff 继续往下走。

## 大致流程

每个需求都应按这个顺序推进：

1. `需求分析师`
   把需求收敛清楚，写明范围、边界、风险和目标。
2. `建筑师`
   确定项目落点、模块边界和结构约束。
3. `侦查员`
   只查事实，不给方案，确认调用链、代码证据和现有实现。
4. `方案设计师`
   基于证据给出最小可行方案，并明确影响范围与兜底策略。
5. `开发者`
   只按批准方案实现，不扩需求、不顺手重构。
6. `审核员`
   像 code review 一样找 bug、回归风险和越界修改。
7. `测试员`
   验证正常路径、失败路径和边界情况。
8. `知识归档员`
   沉淀现象、根因、修复方式和复用经验。

## 规则重点

- 不能跳步骤
- 不能合并角色
- 文档先行，不能靠记忆开发
- 新项目默认放到 `projects/<project-name>/`
- 规则仓库和具体项目仓库分开管理
- 需要时必须做外部调研，不能只靠旧记忆
- bug 修复也必须走同一套流程，只是使用 `bugfix mode`

## 仓库边界

这个仓库默认把“规则体系”和“具体业务项目”分开管理。

所有临时或独立项目统一放在 `projects/` 下，不作为规则仓库的一部分提交。

当前示例项目包括：

- `projects/exchange-rate-calculator/`
- `projects/shannian-site/`
- `projects/outside-docs/`

## 提交原则

- 规则相关提交：只提交 `AGENTS.md`、`agents/`、仓库根说明和规则脚本/文档
- 项目相关提交：默认放在 `projects/` 下并被统一忽略；如需纳入版本控制，应先明确调整 `.gitignore`

## 说明

如果后续你要新建项目，直接放到 `projects/<project-name>/` 即可，不需要每次单独改 ignore。

如果后续你要把某个项目也纳入当前仓库管理，再单独更新 `.gitignore` 并走一次项目级提交流程。
