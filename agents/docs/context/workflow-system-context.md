# Workflow System Context

## Scope

This repository maintains the AI engineering workflow itself, including root workflow rules, role skills, the pipeline contract, the frontmatter-first gate script, the handoff quality checker, and the manual gate fallback checklist.

## Relevant Modules

- `AGENTS.md`: repository-level workflow requirements.
- `agents/README.md`: workflow overview and shared rules.
- `agents/skills/ai-pipeline-orchestrator/SKILL.md`: orchestration entry and skip-prevention contract.
- `agents/skills/ai-pipeline-orchestrator/references/pipeline-contract.md`: source-of-truth pipeline contract.
- `agents/scripts/check_workflow_gate.py`: stage gate checker.
- `agents/scripts/check_handoff_quality.py`: handoff structure and role-quality checker.
- `agents/scripts/upgrade_legacy_project_doc.py`: legacy project-document upgrader for pre-frontmatter docs.
- `agents/scripts/workflow-gate-checklist.md`: manual fallback checklist.

## Known Facts

- Workflow execution is document-first and must use the eight-role pipeline for non-trivial changes.
- Workflow status is declared in project-document frontmatter rather than inferred from brittle prose.
- The gate checker validates frontmatter workflow fields, role ids, requirement identifiers, handoff order, and stage-specific completion conditions.
- The quality checker validates current handoff structure plus tester and knowledge-keeper role-specific required labels.

## Unknowns And Risks

- The current gate still validates artifact state, not real historical execution time.
- Template, context, and rule text must stay aligned with the frontmatter-first model or they will reintroduce dual-track workflow behavior.

## Rule Governance

- 流程复盘结论：真实项目此前采用 current-project.md 与 docs/pipeline/ 双文档系统，造成管理复杂性和概念混淆；现已统一为单一 docs/pipeline/ 结构，通过 workflow_completion_passed 字段区分活动需求与历史需求。
- 值得保留的做法：项目文档与规则治理分离；规则系统自改只更新当前规则与当前上下文；workflow 状态以 frontmatter 为主；统一文档结构简化管理。
- 需要修正或移除的规则：将双文档系统改为单一文档结构；所有项目文档统一位于 `<project>/docs/pipeline/` 目录；活动需求为最新日期且 `workflow_completion_passed: 0` 的文档；已完成需求为 `workflow_completion_passed: 1` 的文档。
- 规则更新状态：已完成简化，移除 current-project.md 双重文档系统，统一采用 docs/pipeline/ 结构，通过 frontmatter 字段自动区分活动和历史需求。
