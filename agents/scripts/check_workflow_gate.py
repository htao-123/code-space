#!/usr/bin/env python3
"""
Workflow gate checker for the AI engineering pipeline.
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

REQUIRED_RESEARCH_LABELS = [
    "- 是否需要外部调研",
    "- 外部调研来源",
    "- 外部调研结论",
]

REQUIRED_METADATA_LABELS = [
    "- 当前角色标识：",
    "- 当前交接标识：",
    "- 需求标识：",
    "- 项目落点：",
    "- 下一角色标识：",
]

STAGE_EXPECTATIONS = {
    "implementer": {
        "current_role_ids": ["solution-designer"],
        "next_role_ids": ["implementer"],
    },
    "reviewer": {
        "current_role_ids": ["implementer"],
        "next_role_ids": ["reviewer"],
    },
    "tester": {
        "current_role_ids": ["reviewer"],
        "next_role_ids": ["tester"],
    },
    "knowledge-keeper": {
        "current_role_ids": ["tester"],
        "next_role_ids": ["knowledge-keeper"],
    },
    "complete": {
        "current_role_ids": ["implementer", "reviewer", "tester", "knowledge-keeper"],
        "next_role_ids": ["reviewer", "tester", "knowledge-keeper", "terminal"],
    },
}


def repo_relative(path: Path, repo_root: Path) -> str:
    try:
        return str(path.resolve().relative_to(repo_root.resolve()))
    except ValueError:
        return str(path.resolve())


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_last_handoff_block(text: str) -> str:
    positions = [match.start() for match in re.finditer(re.escape("【角色结论】"), text)]
    if not positions:
        return ""
    return text[positions[-1]:]


def extract_label_value(text: str, label: str) -> str | None:
    pattern = rf"(?m)^{re.escape(label)}\s*(.+?)\s*$"
    match = re.search(pattern, text)
    if match is None:
        return None
    return match.group(1).strip()


def resolve_declared_project_path(value: str, repo_root: Path) -> Path:
    candidate = Path(value)
    if candidate.is_absolute():
        return candidate.resolve()
    return (repo_root / candidate).resolve()


def check_file_exists(path: Path, label: str, errors: list[str], repo_root: Path) -> None:
    if not path.exists():
        errors.append(f"{label} not found: {repo_relative(path, repo_root)}")
    elif path.is_dir():
        errors.append(f"{label} is a directory, expected file: {repo_relative(path, repo_root)}")


def check_handoff_doc(
    path: Path,
    errors: list[str],
    repo_root: Path,
    approved_project_path: Path,
    expected_current_role_id: str | None = None,
    expected_next_role_id: str | None = None,
) -> dict[str, str] | None:
    check_file_exists(path, "Handoff document", errors, repo_root)
    if errors and not path.exists():
        return None

    text = read_text(path)
    block = extract_last_handoff_block(text)
    if not block:
        errors.append(
            f"Handoff document does not contain any handoff block: {repo_relative(path, repo_root)}"
        )
        return None

    missing = [heading for heading in REQUIRED_HEADINGS if heading not in block]
    if missing:
        errors.append(
            "Latest handoff block missing required sections in "
            f"{repo_relative(path, repo_root)}: {', '.join(missing)}"
        )

    heading_positions = [block.find(heading) for heading in REQUIRED_HEADINGS]
    if any(position == -1 for position in heading_positions):
        pass
    elif heading_positions != sorted(heading_positions):
        errors.append(
            "Latest handoff block has headings out of order in "
            f"{repo_relative(path, repo_root)}"
        )

    missing_sublabels = [label for label in REQUIRED_HANDOFF_SUBLABELS if label not in block]
    if missing_sublabels:
        errors.append(
            "Latest handoff block missing required Chinese handoff labels in "
            f"{repo_relative(path, repo_root)}: {', '.join(missing_sublabels)}"
        )

    missing_research = [label for label in REQUIRED_RESEARCH_LABELS if label not in block]
    if missing_research:
        errors.append(
            "Latest handoff block missing required research records in "
            f"{repo_relative(path, repo_root)}: {', '.join(missing_research)}"
        )

    missing_metadata = [label for label in REQUIRED_METADATA_LABELS if label not in block]
    if missing_metadata:
        errors.append(
            "Latest handoff block missing required metadata labels in "
            f"{repo_relative(path, repo_root)}: {', '.join(missing_metadata)}"
        )

    current_role_id = extract_label_value(block, "- 当前角色标识：")
    handoff_id = extract_label_value(block, "- 当前交接标识：")
    requirement_id = extract_label_value(block, "- 需求标识：")
    declared_project_path = extract_label_value(block, "- 项目落点：")
    next_role_id = extract_label_value(block, "- 下一角色标识：")

    if current_role_id is None:
        errors.append(
            f"Latest handoff block missing current role id metadata in {repo_relative(path, repo_root)}"
        )
    if handoff_id is None:
        errors.append(
            f"Latest handoff block missing handoff identifier in {repo_relative(path, repo_root)}"
        )
    if requirement_id is None:
        errors.append(
            f"Latest handoff block missing requirement identifier in {repo_relative(path, repo_root)}"
        )
    if declared_project_path is None:
        errors.append(
            f"Latest handoff block missing project path metadata in {repo_relative(path, repo_root)}"
        )
    else:
        resolved_declared_project_path = resolve_declared_project_path(declared_project_path, repo_root)
        if resolved_declared_project_path != approved_project_path.resolve():
            errors.append(
                "Latest handoff block project path does not match approved project path in "
                f"{repo_relative(path, repo_root)}: declared {declared_project_path}"
            )
    if next_role_id is None:
        errors.append(
            f"Latest handoff block missing next role id metadata in {repo_relative(path, repo_root)}"
        )

    if expected_current_role_id is not None and current_role_id is not None:
        if current_role_id != expected_current_role_id:
            errors.append(
                "Latest handoff block has the wrong current role id in "
                f"{repo_relative(path, repo_root)}: expected {expected_current_role_id}, got {current_role_id}"
            )

    if expected_next_role_id is not None and next_role_id is not None:
        if next_role_id != expected_next_role_id:
            errors.append(
                "Latest handoff block routes to the wrong next role id in "
                f"{repo_relative(path, repo_root)}: expected {expected_next_role_id}, got {next_role_id}"
            )

    if handoff_id is not None and requirement_id is not None and requirement_id not in handoff_id:
        errors.append(
            "Latest handoff block handoff identifier must include requirement identifier in "
            f"{repo_relative(path, repo_root)}: handoff {handoff_id}, requirement {requirement_id}"
        )

    if (
        current_role_id is None
        or handoff_id is None
        or requirement_id is None
        or declared_project_path is None
        or next_role_id is None
    ):
        return None

    return {
        "current_role_id": current_role_id,
        "handoff_id": handoff_id,
        "requirement_id": requirement_id,
        "project_path": declared_project_path,
        "next_role_id": next_role_id,
    }


def check_documentation_artifact(
    path: Path,
    label: str,
    errors: list[str],
    repo_root: Path,
    approved_project_path: Path,
) -> None:
    check_file_exists(path, label, errors, repo_root)
    if errors and not path.exists():
        return
    ensure_within_repo(path, repo_root, label, errors)
    text = read_text(path)
    declared_project_path = extract_label_value(text, "- 项目落点：")
    if declared_project_path is None:
        errors.append(
            f"{label} does not declare project path metadata: {repo_relative(path, repo_root)}"
        )
        return
    resolved_declared_project_path = resolve_declared_project_path(declared_project_path, repo_root)
    if resolved_declared_project_path != approved_project_path.resolve():
        errors.append(
            f"{label} project path does not match approved project path in {repo_relative(path, repo_root)}: "
            f"declared {declared_project_path}"
        )
    try:
        path.resolve().relative_to(approved_project_path.resolve())
    except ValueError:
        errors.append(
            f"{label} is not stored inside the approved project path: "
            f"{repo_relative(path, repo_root)} not under {repo_relative(approved_project_path, repo_root)}"
        )


def is_repo_root(path: Path, repo_root: Path) -> bool:
    return path.resolve() == repo_root.resolve()


def ensure_within_repo(path: Path, repo_root: Path, label: str, errors: list[str]) -> None:
    try:
        path.resolve().relative_to(repo_root.resolve())
    except ValueError:
        errors.append(f"{label} is outside repository: {path}")


def check_target_paths(targets: list[Path], project_path: Path, errors: list[str], repo_root: Path) -> None:
    for target in targets:
        ensure_within_repo(target, repo_root, "Target path", errors)
        try:
            target.resolve().relative_to(project_path.resolve())
        except ValueError:
            errors.append(
                "Target path is outside approved project path: "
                f"{repo_relative(target, repo_root)} not under {repo_relative(project_path, repo_root)}"
            )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check whether workflow prerequisites are satisfied before implementation."
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root. Defaults to current directory.",
    )
    parser.add_argument(
        "--task-doc",
        required=True,
        help="Path to the current task document or planning document.",
    )
    parser.add_argument(
        "--stage",
        choices=["general", "implementer", "reviewer", "tester", "knowledge-keeper", "complete"],
        default="general",
        help=(
            "Workflow stage to validate. "
            "'implementer' applies pre-coding checks, later stages validate role routing, "
            "and 'complete' verifies the requirement is closed by knowledge-keeper."
        ),
    )
    parser.add_argument(
        "--project-type",
        choices=["new-project", "existing-project"],
        required=True,
        help="Whether this work creates a new project/subproject or modifies an existing one.",
    )
    parser.add_argument(
        "--project-path",
        required=True,
        help="Approved project folder or landing zone for the work.",
    )
    parser.add_argument(
        "--documentation-status",
        choices=["documented", "backfilled"],
        help=(
            "Documentation state for existing-project work. "
            "Use 'documented' when usable docs already existed, or 'backfilled' when a new backfill artifact was created."
        ),
    )
    parser.add_argument(
        "--backfill-doc",
        help="Backfill document path required when --documentation-status=backfilled.",
    )
    parser.add_argument(
        "--documentation-doc",
        help="Existing documentation path required when --documentation-status=documented.",
    )
    parser.add_argument(
        "--handoff-doc",
        action="append",
        default=[],
        help="Handoff document to validate. Repeatable.",
    )
    parser.add_argument(
        "--target-path",
        action="append",
        default=[],
        help="Implementation target path to verify stays inside project-path. Repeatable.",
    )
    parser.add_argument(
        "--allow-root",
        action="store_true",
        help="Allow repository root placement. Use only for explicitly approved exceptions.",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    task_doc = (repo_root / args.task_doc).resolve() if not Path(args.task_doc).is_absolute() else Path(args.task_doc).resolve()
    project_path = (repo_root / args.project_path).resolve() if not Path(args.project_path).is_absolute() else Path(args.project_path).resolve()
    handoff_docs = [
        (repo_root / doc).resolve() if not Path(doc).is_absolute() else Path(doc).resolve()
        for doc in args.handoff_doc
    ]
    backfill_doc = None
    if args.backfill_doc:
        backfill_doc = (repo_root / args.backfill_doc).resolve() if not Path(args.backfill_doc).is_absolute() else Path(args.backfill_doc).resolve()
    documentation_doc = None
    if args.documentation_doc:
        documentation_doc = (repo_root / args.documentation_doc).resolve() if not Path(args.documentation_doc).is_absolute() else Path(args.documentation_doc).resolve()
    target_paths = [
        (repo_root / target).resolve() if not Path(target).is_absolute() else Path(target).resolve()
        for target in args.target_path
    ]

    errors: list[str] = []

    if not repo_root.exists():
        print(f"[FAIL] Repository root not found: {repo_root}")
        return 1

    check_file_exists(task_doc, "Task document", errors, repo_root)
    ensure_within_repo(task_doc, repo_root, "Task document", errors)

    if not project_path.exists():
      errors.append(f"Project path not found: {repo_relative(project_path, repo_root)}")
    ensure_within_repo(project_path, repo_root, "Project path", errors)

    if args.project_type == "new-project":
        if is_repo_root(project_path, repo_root) and not args.allow_root:
            errors.append(
                "New project may not use repository root as project-path without --allow-root."
            )

    if args.project_type == "existing-project":
        if args.documentation_status is None:
            errors.append(
                "Existing project work requires --documentation-status so the workflow can verify documented vs backfilled state."
            )
        if not project_path.exists():
            errors.append("Existing project landing zone must already exist.")
        if args.documentation_status == "documented":
            if documentation_doc is None:
                errors.append(
                    "Existing project with documented status requires --documentation-doc."
                )
            else:
                check_documentation_artifact(
                    documentation_doc,
                    "Documentation document",
                    errors,
                    repo_root,
                    project_path,
                )
        if args.documentation_status == "backfilled":
            if backfill_doc is None:
                errors.append(
                    "Existing project with backfilled documentation requires --backfill-doc."
                )
            else:
                check_documentation_artifact(
                    backfill_doc,
                    "Backfill document",
                    errors,
                    repo_root,
                    project_path,
                )

    if args.project_type == "new-project" and args.documentation_status is not None:
        errors.append("New-project work must not pass --documentation-status.")

    if args.backfill_doc and args.documentation_status != "backfilled":
        errors.append("--backfill-doc may be used only when --documentation-status=backfilled.")

    if args.documentation_doc and args.documentation_status != "documented":
        errors.append("--documentation-doc may be used only when --documentation-status=documented.")

    expectations = STAGE_EXPECTATIONS.get(args.stage)
    metadata_chain: list[dict[str, str]] = []
    if expectations:
        expected_current_role_ids = expectations["current_role_ids"]
        expected_next_role_ids = expectations["next_role_ids"]
        if len(expected_next_role_ids) == 1:
            expected_current_role_id_list = expected_current_role_ids * len(handoff_docs)
            expected_next_role_id_list = expected_next_role_ids * len(handoff_docs)
        else:
            expected_current_role_id_list = expected_current_role_ids
            expected_next_role_id_list = expected_next_role_ids
            if len(handoff_docs) != len(expected_next_role_ids):
                errors.append(
                    f"{args.stage} stage requires exactly {len(expected_next_role_ids)} --handoff-doc values "
                    "to validate the closing handoff chain."
                )
        for index, handoff_doc in enumerate(handoff_docs):
            expected_current_role_id = None
            expected_next_role_id = None
            if index < len(expected_current_role_id_list):
                expected_current_role_id = expected_current_role_id_list[index]
            if index < len(expected_next_role_id_list):
                expected_next_role_id = expected_next_role_id_list[index]
            metadata = check_handoff_doc(
                handoff_doc,
                errors,
                repo_root,
                project_path,
                expected_current_role_id=expected_current_role_id,
                expected_next_role_id=expected_next_role_id,
            )
            if metadata is not None:
                metadata_chain.append(metadata)
    else:
        for handoff_doc in handoff_docs:
            metadata = check_handoff_doc(
                handoff_doc,
                errors,
                repo_root,
                project_path,
            )
            if metadata is not None:
                metadata_chain.append(metadata)

    if args.stage == "complete" and metadata_chain:
        requirement_ids = {metadata["requirement_id"] for metadata in metadata_chain}
        if len(requirement_ids) != 1:
            errors.append(
                "Completion chain mixes multiple requirement identifiers: "
                f"{', '.join(sorted(requirement_ids))}"
            )
        declared_project_paths = {metadata["project_path"] for metadata in metadata_chain}
        if len(declared_project_paths) != 1:
            errors.append(
                "Completion chain mixes multiple declared project paths: "
                f"{', '.join(sorted(declared_project_paths))}"
            )
        handoff_ids = [metadata["handoff_id"] for metadata in metadata_chain]
        if len(set(handoff_ids)) != len(handoff_ids):
            errors.append("Completion chain reuses duplicate handoff identifiers.")

    if args.stage in {"implementer", "reviewer", "tester", "knowledge-keeper", "complete"}:
        if not handoff_docs:
            errors.append(
                f"{args.stage} stage requires at least one --handoff-doc with a valid structured handoff."
            )
    if args.stage in {"implementer", "reviewer", "tester", "knowledge-keeper"} and len(handoff_docs) != 1:
        errors.append(
            f"{args.stage} stage requires exactly one --handoff-doc so each gate run validates a single requirement transition."
        )

    if args.stage == "implementer":
        if not target_paths:
            errors.append(
                "Implementer stage requires at least one --target-path so coding scope can be checked."
            )

    if target_paths:
        check_target_paths(target_paths, project_path, errors, repo_root)

    quality_script = repo_root / "agents/scripts/check_handoff_quality.py"
    for handoff_doc in handoff_docs:
        result = subprocess.run(
            [
                sys.executable,
                str(quality_script),
                "--repo-root",
                str(repo_root),
                "--handoff-doc",
                str(handoff_doc),
                "--project-path",
                str(project_path),
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            detail = result.stdout.strip() or result.stderr.strip() or "unknown quality check failure"
            errors.append(
                f"Handoff quality check failed for {repo_relative(handoff_doc, repo_root)}: {detail}"
            )

    if errors:
        print("[FAIL] Workflow gate check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("[PASS] Workflow gate check passed.")
    print(f"- stage: {args.stage}")
    print(f"- task document: {repo_relative(task_doc, repo_root)}")
    print(f"- project type: {args.project_type}")
    print(f"- project path: {repo_relative(project_path, repo_root)}")
    if args.documentation_status:
        print(f"- documentation status: {args.documentation_status}")
    if documentation_doc:
        print(f"- documentation document: {repo_relative(documentation_doc, repo_root)}")
    if backfill_doc:
        print(f"- backfill document: {repo_relative(backfill_doc, repo_root)}")
    if handoff_docs:
        print("- validated handoff docs:")
        for handoff_doc in handoff_docs:
            print(f"  - {repo_relative(handoff_doc, repo_root)}")
    if target_paths:
        print("- validated target paths:")
        for target_path in target_paths:
            print(f"  - {repo_relative(target_path, repo_root)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
