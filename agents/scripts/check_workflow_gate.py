#!/usr/bin/env python3
"""
Workflow gate checker for the frontmatter-based AI engineering pipeline.
"""

from __future__ import annotations

import argparse
import subprocess
import re
import sys
from pathlib import Path


REQUIRED_HEADINGS = [
    "【角色结论】",
    "【已核实输入】",
    "【调研发现】",
    "【交付物】",
    "【约束】",
    "【校验标准】",
    "【禁止事项】",
    "【交接给下一个角色】",
]

REQUIRED_HANDOFF_SUBLABELS = [
    "- 下一角色：",
    "- 可用输入：",
    "- 非目标：",
    "- 完成条件：",
]

REQUIRED_METADATA_LABELS = [
    "- 当前角色标识：",
    "- 当前交接标识：",
    "- 需求标识：",
    "- 下一角色标识：",
]

STAGE_ORDER = [
    "requirement-analyst",
    "architect",
    "code-investigator",
    "solution-designer",
    "implementer",
    "reviewer",
    "tester",
    "knowledge-keeper",
    "complete",
]

FRONTMATTER_REQUIRED_FIELDS = [
    "requirement_id",
    "workflow_project_type",
    "workflow_work_type",
    "workflow_doc_backfilled",
    "workflow_current_stage",
    "workflow_solution_approved",
    "workflow_pre_chain_verified",
    "workflow_implementer_passed",
    "workflow_reviewer_passed",
    "workflow_tester_passed",
    "workflow_knowledge_keeper_passed",
    "workflow_completion_passed",
]

FLAG_FIELDS = [
    "workflow_doc_backfilled",
    "workflow_solution_approved",
    "workflow_pre_chain_verified",
    "workflow_implementer_passed",
    "workflow_reviewer_passed",
    "workflow_tester_passed",
    "workflow_knowledge_keeper_passed",
    "workflow_completion_passed",
]

PRE_CHAIN_CURRENT = [
    "requirement-analyst",
    "architect",
    "code-investigator",
    "solution-designer",
]

PRE_CHAIN_NEXT = [
    "architect",
    "code-investigator",
    "solution-designer",
    "implementer",
]

FULL_CHAIN_CURRENT = [
    "requirement-analyst",
    "architect",
    "code-investigator",
    "solution-designer",
    "implementer",
    "reviewer",
    "tester",
    "knowledge-keeper",
]

FULL_CHAIN_NEXT = [
    "architect",
    "code-investigator",
    "solution-designer",
    "implementer",
    "reviewer",
    "tester",
    "knowledge-keeper",
    "terminal",
]

STAGE_EXPECTED_CURRENT_ROLE = {
    "implementer": "solution-designer",
    "reviewer": "implementer",
    "tester": "reviewer",
    "knowledge-keeper": "tester",
}

PROJECT_TYPES = {"new-project", "existing-project"}
WORK_TYPES = {"feature", "bugfix", "task"}

BUGFIX_BASE_LABELS = [
    "- 问题类型：",
    "- 复现步骤：",
    "- 预期结果：",
    "- 实际结果：",
]

BUGFIX_DOWNSTREAM_LABELS = [
    "- 根因摘要：",
    "- 回归检查范围：",
]

RULE_GOVERNANCE_REQUIRED_LABELS = [
    "- 流程复盘结论：",
    "- 值得保留的做法：",
    "- 需要修正或移除的规则：",
    "- 规则更新状态：",
]


def repo_relative(path: Path, repo_root: Path) -> str:
    try:
        return str(path.resolve().relative_to(repo_root.resolve()))
    except ValueError:
        return str(path.resolve())


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    frontmatter_text = text[4:end]
    body = text[end + 5 :]
    data: dict[str, str] = {}
    for raw_line in frontmatter_text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip("'\"")
    return data, body


def extract_all_handoff_blocks(text: str) -> list[str]:
    positions = [match.start() for match in re.finditer(re.escape("【角色结论】"), text)]
    if not positions:
        return []
    blocks: list[str] = []
    for index, start in enumerate(positions):
        end = positions[index + 1] if index + 1 < len(positions) else len(text)
        next_heading = text.find("\n## ", start)
        if next_heading != -1 and next_heading < end:
            end = next_heading
        blocks.append(text[start:end])
    return blocks


def extract_last_handoff_block(text: str) -> str:
    blocks = extract_all_handoff_blocks(text)
    return blocks[-1] if blocks else ""


def extract_label_value(text: str, label: str) -> str | None:
    pattern = rf"(?m)^\s*{re.escape(label)}\s*(.+?)\s*$"
    match = re.search(pattern, text)
    if match is None:
        return None
    return match.group(1).strip()


def check_file_exists(path: Path, label: str, errors: list[str], repo_root: Path) -> None:
    if not path.exists():
        errors.append(f"{label} not found: {repo_relative(path, repo_root)}")
    elif path.is_dir():
        errors.append(f"{label} is a directory, expected file: {repo_relative(path, repo_root)}")


def ensure_within_repo(path: Path, repo_root: Path, label: str, errors: list[str]) -> None:
    try:
        path.resolve().relative_to(repo_root.resolve())
    except ValueError:
        errors.append(f"{label} must be inside repository root: {path}")


def path_is_within(path: Path, ancestor: Path) -> bool:
    try:
        path.resolve().relative_to(ancestor.resolve())
        return True
    except ValueError:
        return False


def is_rule_system_change(repo_root: Path, task_doc: Path, target_paths: list[Path]) -> bool:
    agents_root = (repo_root / "agents").resolve()
    if target_paths:
        return all(path_is_within(target, agents_root) for target in target_paths)
    return path_is_within(task_doc, agents_root)


def project_doc_scope(task_doc: Path, repo_root: Path) -> Path:
    scope = task_doc.resolve().parent
    if scope.name.lower() in {"docs", "doc", "documentation"} and scope != repo_root.resolve():
        return scope.parent
    return scope


def validate_project_doc_location(
    repo_root: Path,
    task_doc: Path,
    target_paths: list[Path],
    rule_system_change: bool,
    errors: list[str],
) -> None:
    agents_root = (repo_root / "agents").resolve()
    if rule_system_change:
        return
    if path_is_within(task_doc, agents_root):
        errors.append(
            "Real-project pipeline documents must not live under agents/; "
            f"move it into the real project path: {repo_relative(task_doc, repo_root)}"
        )
    if not target_paths:
        return
    doc_scope = project_doc_scope(task_doc, repo_root)
    if doc_scope == repo_root.resolve():
        errors.append(
            "Real-project pipeline documents must live inside the real project tree, "
            f"not at repository root: {repo_relative(task_doc, repo_root)}. "
            "Recommended path: <project>/docs/pipeline/YYYY-MM-DD-<project>-<topic>-<work-type>.md"
        )
        return
    aligned = False
    for target in target_paths:
        target_scope = target.resolve() if target.is_dir() else target.resolve().parent
        if path_is_within(target_scope, doc_scope) or path_is_within(doc_scope, target_scope):
            aligned = True
            break
    if not aligned:
        errors.append(
            "Pipeline document must live in the same project tree as at least one validated target path: "
            f"{repo_relative(task_doc, repo_root)}. "
            "Recommended path: <project>/docs/pipeline/YYYY-MM-DD-<project>-<topic>-<work-type>.md"
        )


def validate_handoff_docs(
    repo_root: Path,
    handoff_docs: list[Path],
    errors: list[str],
) -> None:
    for doc in handoff_docs:
        check_file_exists(doc, "Handoff document", errors, repo_root)
        ensure_within_repo(doc, repo_root, "Handoff document", errors)


def validate_frontmatter(
    frontmatter: dict[str, str],
    errors: list[str],
    task_doc: Path,
    repo_root: Path,
) -> None:
    missing = [field for field in FRONTMATTER_REQUIRED_FIELDS if field not in frontmatter]
    if missing:
        errors.append(
            f"Project document missing required frontmatter fields in {repo_relative(task_doc, repo_root)}: "
            f"{', '.join(missing)}"
        )
    stage = frontmatter.get("workflow_current_stage")
    if stage and stage not in STAGE_ORDER:
        errors.append(
            f"Project document has invalid workflow_current_stage in {repo_relative(task_doc, repo_root)}: {stage}"
        )
    project_type = frontmatter.get("workflow_project_type")
    if project_type and project_type not in PROJECT_TYPES:
        errors.append(
            f"Project document has invalid workflow_project_type in {repo_relative(task_doc, repo_root)}: {project_type}"
        )
    work_type = frontmatter.get("workflow_work_type")
    if work_type and work_type not in WORK_TYPES:
        errors.append(
            f"Project document has invalid workflow_work_type in {repo_relative(task_doc, repo_root)}: {work_type}"
        )
    for field in FLAG_FIELDS:
        value = frontmatter.get(field)
        if value is None:
            continue
        if value not in {"0", "1"}:
            errors.append(
                f"Project document has invalid {field} in {repo_relative(task_doc, repo_root)}: "
                "expected 0 or 1."
            )


def validate_handoff_block(
    block: str,
    errors: list[str],
    location_label: str,
    requirement_id: str,
    expected_current_role: str | None = None,
    expected_next_role: str | None = None,
) -> dict[str, str] | None:
    missing_headings = [heading for heading in REQUIRED_HEADINGS if heading not in block]
    if missing_headings:
        errors.append(
            f"Handoff block missing required sections in {location_label}: {', '.join(missing_headings)}"
        )

    missing_labels = [label for label in REQUIRED_HANDOFF_SUBLABELS if extract_label_value(block, label) is None]
    if missing_labels:
        errors.append(
            f"Handoff block missing required handoff labels in {location_label}: {', '.join(missing_labels)}"
        )

    missing_metadata = [label for label in REQUIRED_METADATA_LABELS if extract_label_value(block, label) is None]
    if missing_metadata:
        errors.append(
            f"Handoff block missing required metadata labels in {location_label}: {', '.join(missing_metadata)}"
        )

    current_role_id = extract_label_value(block, "- 当前角色标识：")
    next_role_id = extract_label_value(block, "- 下一角色标识：")
    block_requirement_id = extract_label_value(block, "- 需求标识：")
    handoff_id = extract_label_value(block, "- 当前交接标识：")

    if block_requirement_id and block_requirement_id != requirement_id:
        errors.append(
            f"Handoff block requirement_id mismatch in {location_label}: "
            f"expected {requirement_id}, got {block_requirement_id}"
        )

    if expected_current_role and current_role_id != expected_current_role:
        errors.append(
            f"Handoff block current role mismatch in {location_label}: "
            f"expected {expected_current_role}, got {current_role_id or 'missing'}"
        )

    if expected_next_role and next_role_id != expected_next_role:
        errors.append(
            f"Handoff block next role mismatch in {location_label}: "
            f"expected {expected_next_role}, got {next_role_id or 'missing'}"
        )

    if current_role_id is None or next_role_id is None or handoff_id is None:
        return None

    return {
        "current_role_id": current_role_id,
        "next_role_id": next_role_id,
        "requirement_id": block_requirement_id or "",
        "handoff_id": handoff_id,
    }


def find_latest_role_chain(blocks: list[str], current_roles: list[str], next_roles: list[str]) -> list[int]:
    selected_reversed: list[int] = []
    before_index = len(blocks)
    for current_role, next_role in zip(reversed(current_roles), reversed(next_roles)):
        found_index = None
        for index in range(before_index - 1, -1, -1):
            block = blocks[index]
            if (
                extract_label_value(block, "- 当前角色标识：") == current_role
                and extract_label_value(block, "- 下一角色标识：") == next_role
            ):
                found_index = index
                break
        if found_index is None:
            return []
        selected_reversed.append(found_index)
        before_index = found_index
    return list(reversed(selected_reversed))


def validate_unique_handoff_ids(
    chain: list[dict[str, str]],
    errors: list[str],
    label: str,
) -> None:
    handoff_ids = [item["handoff_id"] for item in chain]
    if len(set(handoff_ids)) != len(handoff_ids):
        errors.append(f"{label} reuses duplicate handoff identifiers.")


def run_quality_check(repo_root: Path, handoff_doc: Path, block_index: int | None, label: str, errors: list[str]) -> None:
    quality_script = repo_root / "agents/scripts/check_handoff_quality.py"
    command = [sys.executable, str(quality_script), "--repo-root", str(repo_root), "--handoff-doc", str(handoff_doc)]
    if block_index is not None:
        command.extend(["--block-index", str(block_index)])
    completed = subprocess.run(command, capture_output=True, text=True)
    if completed.returncode != 0:
        detail = completed.stdout.strip() or completed.stderr.strip() or "unknown quality-check failure"
        errors.append(f"Handoff quality check failed for {label}: {detail}")


def stage_flag_name(stage: str) -> str | None:
    return {
        "reviewer": "workflow_implementer_passed",
        "tester": "workflow_reviewer_passed",
        "knowledge-keeper": "workflow_tester_passed",
    }.get(stage)


def validate_target_paths(
    repo_root: Path,
    target_paths: list[Path],
    project_type: str,
    stage: str,
    errors: list[str],
) -> None:
    if stage != "general" and not target_paths:
        errors.append(f"{stage} stage requires at least one --target-path.")
        return
    if project_type != "new-project":
        return
    for target in target_paths:
        resolved = target.resolve()
        if resolved == repo_root.resolve():
            errors.append("new-project work must not target repository root directly.")
        elif resolved.parent == repo_root.resolve() and resolved.suffix:
            errors.append(
                f"new-project work must use a dedicated folder, not a root-level file target: {repo_relative(target, repo_root)}"
            )


def validate_bugfix_blocks(
    blocks: list[str],
    errors: list[str],
    task_doc: Path,
    repo_root: Path,
) -> None:
    for index, block in enumerate(blocks):
        location = f"{repo_relative(task_doc, repo_root)}#handoff-{index + 1}"
        missing_base = [label for label in BUGFIX_BASE_LABELS if extract_label_value(block, label) is None]
        if missing_base:
            errors.append(f"Bugfix handoff missing required labels in {location}: {', '.join(missing_base)}")
            continue
        issue_type = extract_label_value(block, "- 问题类型：")
        if issue_type != "bugfix":
            errors.append(f"Bugfix handoff must record 问题类型：bugfix in {location}.")
        current_role = extract_label_value(block, "- 当前角色标识：")
        if current_role in {"solution-designer", "implementer", "reviewer", "tester", "knowledge-keeper"}:
            missing_downstream = [
                label for label in BUGFIX_DOWNSTREAM_LABELS if extract_label_value(block, label) is None
            ]
            if missing_downstream:
                errors.append(
                    f"Bugfix downstream handoff missing required labels in {location}: {', '.join(missing_downstream)}"
                )


def validate_rule_governance_context(repo_root: Path, errors: list[str]) -> None:
    context_doc = (repo_root / "agents/docs/context/workflow-system-context.md").resolve()
    if not context_doc.exists():
        errors.append("Rule-system change requires agents/docs/context/workflow-system-context.md.")
        return
    text = read_text(context_doc)
    if "## Rule Governance" not in text:
        errors.append("workflow-system-context.md must contain a fixed ## Rule Governance section.")
    for label in RULE_GOVERNANCE_REQUIRED_LABELS:
        if extract_label_value(text, label) is None:
            errors.append(f"Rule Governance section missing required label in workflow-system-context.md: {label}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check workflow gate status against frontmatter and handoff chain.")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--task-doc", required=True)
    parser.add_argument(
        "--stage",
        required=True,
        choices=["general", "implementer", "reviewer", "tester", "knowledge-keeper", "complete"],
    )
    parser.add_argument("--handoff-doc", action="append", default=[])
    parser.add_argument("--target-path", action="append", default=[])
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    task_doc = (repo_root / args.task_doc).resolve() if not Path(args.task_doc).is_absolute() else Path(args.task_doc).resolve()
    handoff_docs = [
        (repo_root / doc).resolve() if not Path(doc).is_absolute() else Path(doc).resolve()
        for doc in args.handoff_doc
    ]
    target_paths = [
        (repo_root / target).resolve() if not Path(target).is_absolute() else Path(target).resolve()
        for target in args.target_path
    ]

    errors: list[str] = []

    if not repo_root.exists():
        print(f"[FAIL] Repository root not found: {repo_root}")
        return 1

    check_file_exists(task_doc, "Project document", errors, repo_root)
    ensure_within_repo(task_doc, repo_root, "Project document", errors)
    if handoff_docs:
        validate_handoff_docs(repo_root, handoff_docs, errors)
    if target_paths:
        for target in target_paths:
            ensure_within_repo(target, repo_root, "Target path", errors)

    if errors:
        print("[FAIL] Workflow gate check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    text = read_text(task_doc)
    frontmatter, body = extract_frontmatter(text)
    validate_frontmatter(frontmatter, errors, task_doc, repo_root)

    requirement_id = frontmatter.get("requirement_id", "")
    project_type = frontmatter.get("workflow_project_type", "")
    work_type = frontmatter.get("workflow_work_type", "")
    doc_backfilled = frontmatter.get("workflow_doc_backfilled", "")
    current_stage = frontmatter.get("workflow_current_stage", "")

    validate_target_paths(repo_root, target_paths, project_type, args.stage, errors)

    if project_type == "new-project" and doc_backfilled != "0":
        errors.append("new-project work requires workflow_doc_backfilled=0.")
    if project_type == "existing-project" and doc_backfilled not in {"0", "1"}:
        errors.append("existing-project work requires workflow_doc_backfilled to be 0 or 1.")

    blocks = extract_all_handoff_blocks(body)
    if not blocks:
        errors.append(f"Project document does not contain any handoff blocks: {repo_relative(task_doc, repo_root)}")

    if work_type == "bugfix":
        validate_bugfix_blocks(blocks, errors, task_doc, repo_root)

    rule_system_change = is_rule_system_change(repo_root, task_doc, target_paths)
    validate_project_doc_location(repo_root, task_doc, target_paths, rule_system_change, errors)
    if rule_system_change:
        validate_rule_governance_context(repo_root, errors)

    for index, block in enumerate(blocks):
        validate_handoff_block(
            block,
            errors,
            f"{repo_relative(task_doc, repo_root)}#handoff-{index + 1}",
            requirement_id,
        )

    if args.stage == "implementer":
        if current_stage != "solution-designer":
            errors.append("implementer stage requires workflow_current_stage=solution-designer.")
        if frontmatter.get("workflow_solution_approved") != "1":
            errors.append("implementer stage requires workflow_solution_approved=1.")
        if frontmatter.get("workflow_pre_chain_verified") != "1":
            errors.append("implementer stage requires workflow_pre_chain_verified=1.")
        chain_indexes = find_latest_role_chain(blocks, PRE_CHAIN_CURRENT, PRE_CHAIN_NEXT)
        if not chain_indexes:
            errors.append(
                "implementer stage requires a complete requirement-analyst -> architect -> "
                "code-investigator -> solution-designer chain."
            )
        else:
            chain_meta: list[dict[str, str]] = []
            for i, block_index in enumerate(chain_indexes):
                metadata = validate_handoff_block(
                    blocks[block_index],
                    errors,
                    f"{repo_relative(task_doc, repo_root)}#handoff-{block_index + 1}",
                    requirement_id,
                    PRE_CHAIN_CURRENT[i],
                    PRE_CHAIN_NEXT[i],
                )
                if metadata:
                    chain_meta.append(metadata)
            validate_unique_handoff_ids(chain_meta, errors, "Pre-implementation chain")
            for block_index in chain_indexes:
                run_quality_check(
                    repo_root,
                    task_doc,
                    block_index,
                    f"{repo_relative(task_doc, repo_root)}#handoff-{block_index + 1}",
                    errors,
                )

    elif args.stage in {"reviewer", "tester", "knowledge-keeper"}:
        expected_stage = STAGE_EXPECTED_CURRENT_ROLE[args.stage]
        expected_flag = stage_flag_name(args.stage)
        if current_stage != expected_stage:
            errors.append(f"{args.stage} stage requires workflow_current_stage={expected_stage}.")
        if expected_flag and frontmatter.get(expected_flag) != "1":
            errors.append(f"{args.stage} stage requires {expected_flag}=1.")
        latest_block = extract_last_handoff_block(body)
        metadata = validate_handoff_block(
            latest_block,
            errors,
            repo_relative(task_doc, repo_root),
            requirement_id,
            expected_stage,
            args.stage,
        )
        if metadata:
            run_quality_check(repo_root, task_doc, len(blocks) - 1, repo_relative(task_doc, repo_root), errors)

    elif args.stage == "complete":
        if len(handoff_docs) != 1:
            errors.append(
                "complete stage requires exactly one --handoff-doc containing the full 8-role chain."
            )
        elif handoff_docs[0].resolve() != task_doc.resolve():
            errors.append(
                "complete stage requires --handoff-doc to point to the same current project document passed via --task-doc."
            )
        if current_stage != "knowledge-keeper":
            errors.append("complete stage requires workflow_current_stage=knowledge-keeper before final pass.")
        if frontmatter.get("workflow_knowledge_keeper_passed") != "1":
            errors.append("complete stage requires workflow_knowledge_keeper_passed=1.")
        if frontmatter.get("workflow_completion_passed") == "1":
            errors.append("complete stage must run before AI writes workflow_completion_passed=1.")
        chain_indexes = find_latest_role_chain(blocks, FULL_CHAIN_CURRENT, FULL_CHAIN_NEXT)
        if not chain_indexes:
            errors.append(
                "complete stage requires a complete 8-role chain from requirement-analyst through knowledge-keeper."
            )
        else:
            chain_meta: list[dict[str, str]] = []
            for i, block_index in enumerate(chain_indexes):
                metadata = validate_handoff_block(
                    blocks[block_index],
                    errors,
                    f"{repo_relative(task_doc, repo_root)}#handoff-{block_index + 1}",
                    requirement_id,
                    FULL_CHAIN_CURRENT[i],
                    FULL_CHAIN_NEXT[i],
                )
                if metadata:
                    chain_meta.append(metadata)
            validate_unique_handoff_ids(chain_meta, errors, "Completion chain")
            for block_index in chain_indexes:
                run_quality_check(
                    repo_root,
                    task_doc,
                    block_index,
                    f"{repo_relative(task_doc, repo_root)}#handoff-{block_index + 1}",
                    errors,
                )

    elif args.stage == "general":
        latest_block = extract_last_handoff_block(body)
        if latest_block:
            run_quality_check(repo_root, task_doc, len(blocks) - 1, repo_relative(task_doc, repo_root), errors)

    if errors:
        print("[FAIL] Workflow gate check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("[PASS] Workflow gate check passed.")
    print(f"- stage: {args.stage}")
    print(f"- project document: {repo_relative(task_doc, repo_root)}")
    print(f"- project type: {project_type}")
    print(f"- work type: {work_type}")
    if handoff_docs:
        print("- validated handoff docs:")
        for doc in handoff_docs:
            print(f"  - {repo_relative(doc, repo_root)}")
    if target_paths:
        print("- validated target paths:")
        for target in target_paths:
            print(f"  - {repo_relative(target, repo_root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
