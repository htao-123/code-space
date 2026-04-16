# Workflow System Context

- 项目落点：/Users/senguoyun/code space
- 文档状态：backfilled
- 创建日期：2026-04-16

## Scope

This repository maintains the AI engineering workflow itself, including root workflow rules, role skills, the pipeline contract, gate scripts, handoff quality checks, normalization helpers, and manual gate fallback checklist.

## Relevant Modules

- `AGENTS.md`: repository-level workflow requirements.
- `agents/README.md`: workflow overview and shared rules.
- `agents/skills/ai-pipeline-orchestrator/SKILL.md`: orchestration entry and skip-prevention contract.
- `agents/skills/ai-pipeline-orchestrator/references/pipeline-contract.md`: source-of-truth pipeline contract.
- `agents/scripts/check_workflow_gate.py`: stage gate checker.
- `agents/scripts/check_handoff_quality.py`: handoff content and evidence quality checker.
- `agents/scripts/normalize_handoff_format.py`: formatting-only handoff normalizer.
- `agents/scripts/workflow-gate-checklist.md`: manual fallback checklist.

## Known Facts

- Workflow execution is document-first and must use the eight-role pipeline for non-trivial changes.
- The gate checker validates structured handoff fields, role ids, evidence ids, and quality fields.
- The quality checker reads the current handoff Markdown and validates that declared evidence maps to real file contents.
- Historical task documents show several cases where gate failures were repaired by editing handoff content or evidence formatting.

## Unknowns And Risks

- The current gate cannot prove that a role actually executed at the time claimed; it mainly validates the current artifact state.
- The current documentation rules do not clearly distinguish formatting-only normalization from content repair or workflow repair.
- Adding process authenticity checks must avoid making normal formatting fixes too heavy.
