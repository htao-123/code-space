#!/usr/bin/env python3
"""
Workflow gate checker for the AI engineering pipeline.
"""

from __future__ import annotations

import argparse
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


def repo_relative(path: Path, repo_root: Path) -> str:
    try:
        return str(path.resolve().relative_to(repo_root.resolve()))
    except ValueError:
        return str(path.resolve())


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def check_file_exists(path: Path, label: str, errors: list[str], repo_root: Path) -> None:
    if not path.exists():
        errors.append(f"{label} not found: {repo_relative(path, repo_root)}")
    elif path.is_dir():
        errors.append(f"{label} is a directory, expected file: {repo_relative(path, repo_root)}")


def check_handoff_doc(path: Path, errors: list[str], repo_root: Path) -> None:
    check_file_exists(path, "Handoff document", errors, repo_root)
    if errors and not path.exists():
        return

    text = read_text(path)
    missing = [heading for heading in REQUIRED_HEADINGS if heading not in text]
    if missing:
        errors.append(
            "Handoff document missing required sections in "
            f"{repo_relative(path, repo_root)}: {', '.join(missing)}"
        )

    missing_sublabels = [label for label in REQUIRED_HANDOFF_SUBLABELS if label not in text]
    if missing_sublabels:
        errors.append(
            "Handoff document missing required Chinese handoff labels in "
            f"{repo_relative(path, repo_root)}: {', '.join(missing_sublabels)}"
        )

    missing_research = [label for label in REQUIRED_RESEARCH_LABELS if label not in text]
    if missing_research:
        errors.append(
            "Handoff document missing required research records in "
            f"{repo_relative(path, repo_root)}: {', '.join(missing_research)}"
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
        if not str(target.resolve()).startswith(str(project_path.resolve())):
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
        choices=["general", "implementer"],
        default="general",
        help="Workflow stage to validate. 'implementer' applies stricter pre-coding checks.",
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
        if args.documentation_status == "backfilled":
            if backfill_doc is None:
                errors.append(
                    "Existing project with backfilled documentation requires --backfill-doc."
                )
            else:
                check_file_exists(backfill_doc, "Backfill document", errors, repo_root)
                ensure_within_repo(backfill_doc, repo_root, "Backfill document", errors)

    if args.project_type == "new-project" and args.documentation_status is not None:
        errors.append("New-project work must not pass --documentation-status.")

    if args.backfill_doc and args.documentation_status != "backfilled":
        errors.append("--backfill-doc may be used only when --documentation-status=backfilled.")

    for handoff_doc in handoff_docs:
        check_handoff_doc(handoff_doc, errors, repo_root)

    if args.stage == "implementer":
        if not handoff_docs:
            errors.append(
                "Implementer stage requires at least one --handoff-doc with a valid structured handoff."
            )
        if not target_paths:
            errors.append(
                "Implementer stage requires at least one --target-path so coding scope can be checked."
            )

    if target_paths:
        check_target_paths(target_paths, project_path, errors, repo_root)

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
