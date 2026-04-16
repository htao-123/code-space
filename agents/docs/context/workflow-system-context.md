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

- 流程复盘结论：真实项目的 current project document 路径此前只要求“在项目路径里”，但没有明确默认文件名和历史文档位置，导致迁移后 gate 输入和历史文档位置出现歧义；现已补充为固定的单 current + 多历史规则。
- 值得保留的做法：项目文档与规则治理分离；规则系统自改只更新当前规则与当前上下文；workflow 状态以 frontmatter 为主；当前文档固定路径、历史文档固定目录。
- 需要修正或移除的规则：将“current project document 只需位于项目路径内”的宽泛表述收紧为明确约定：`<project>/current-project.md` 作为默认 gate 输入，`<project>/docs/pipeline/` 作为历史需求文档目录。
- 规则更新状态：已完成真实项目文档布局与命名规则收口，默认采用 `current-project.md`、`docs/pipeline/`、`references/internal/`、`references/external/` 结构。
