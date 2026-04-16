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

- 流程复盘结论：当前未记录新的规则流程问题；若后续真实项目暴露规则缺陷，应在对应规则变更中更新本节。
- 值得保留的做法：项目文档与规则治理分离；规则系统自改只更新当前规则与当前上下文；workflow 状态以 frontmatter 为主。
- 需要修正或移除的规则：无
- 规则更新状态：当前已完成“项目文档不承载规则治理字段，规则治理统一落到本节”的收口。
