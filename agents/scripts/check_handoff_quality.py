#!/usr/bin/env python3
"""
Simplified handoff quality checker for the frontmatter-based workflow model.
"""

from __future__ import annotations

import argparse
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

REQUIRED_RESEARCH_LABELS = [
    "- 内部调研范围：",
    "- 内部调研结论：",
    "- 外部调研范围：",
    "- 外部调研来源：",
    "- 官方事实结论：",
    "- 主流方案结论：",
    "- 最佳实现参考结论：",
    "- 是否发现新增外部差异：",
    "- 推断说明：",
    "- 未验证项：",
    "- 需要用户确认：",
    "- 推荐方案：",
    "- 推荐原因：",
    "- 主要权衡：",
]

ROLE_FORBIDDEN_PATTERNS = {
    "requirement-analyst": [r"(?i)\bdiff\b", r"代码实现", r"修改文件"],
    "architect": [r"具体代码", r"直接编码"],
    "code-investigator": [r"建议", r"推荐方案", r"解决方案"],
    "solution-designer": [r"```[\s\S]*?```", r"直接编码", r"完整代码"],
    "implementer": [r"顺手重构", r"额外优化", r"新增页面"],
    "reviewer": [r"已直接修复", r"我修改了", r"已改代码"],
    "tester": [r"假设成功", r"应该没问题"],
    "knowledge-keeper": [r"我猜", r"可能就是"],
}

GENERIC_WEAK_PHRASES = [
    r"暂不展开",
    r"自行处理",
    r"查过了",
]

METADATA_ONLY_LABELS = [
    "- 当前角色：",
    "- 当前角色标识：",
    "- 当前交接标识：",
    "- 需求标识：",
    "- 下一角色标识：",
    "- 是否需要外部调研：",
    "- 外部调研来源：",
    "- 外部调研结论：",
    "- 未验证项：",
    "- 需要用户确认：",
    "- 推荐方案：",
    "- 推荐原因：",
    "- 主要权衡：",
]

TESTER_REQUIRED_LABELS = [
    "- 运行时验证：",
    "- 外部依赖验证：",
    "- 未验证原因：",
]

KNOWLEDGE_KEEPER_REQUIRED_LABELS = [
    "- 需求复盘结论：",
    "- 自我审查结论：",
    "- 自我纠错项：",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def repo_relative(path: Path, repo_root: Path) -> str:
    try:
        return str(path.resolve().relative_to(repo_root.resolve()))
    except ValueError:
        return str(path.resolve())


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
        if not line or ":" not in line:
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


def extract_label_value(text: str, label: str) -> str | None:
    pattern = rf"(?m)^\s*{re.escape(label)}\s*(.+?)\s*$"
    match = re.search(pattern, text)
    if match is None:
        return None
    return match.group(1).strip()


def extract_last_handoff_block(text: str) -> str:
    blocks = extract_all_handoff_blocks(text)
    return blocks[-1] if blocks else ""


def remove_metadata_only_lines(text: str) -> str:
    kept: list[str] = []
    for line in text.splitlines():
        stripped = line.lstrip()
        if any(stripped.startswith(label) for label in METADATA_ONLY_LABELS):
            continue
        kept.append(line)
    return "\n".join(kept)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check frontmatter-era handoff quality.")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--handoff-doc", required=True)
    parser.add_argument("--block-index", type=int)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    handoff_doc = (repo_root / args.handoff_doc).resolve() if not Path(args.handoff_doc).is_absolute() else Path(args.handoff_doc).resolve()

    errors: list[str] = []
    if not handoff_doc.exists() or handoff_doc.is_dir():
        print(f"[FAIL] Handoff document not found or invalid: {handoff_doc}")
        return 1

    text = read_text(handoff_doc)
    frontmatter, body = extract_frontmatter(text)
    if "requirement_id" not in frontmatter:
        errors.append("Task document frontmatter must include requirement_id.")
    if "workflow_current_stage" not in frontmatter:
        errors.append("Task document frontmatter must include workflow_current_stage.")

    blocks = extract_all_handoff_blocks(body)
    if not blocks:
        errors.append("Handoff document does not contain any handoff blocks.")
        block = ""
        block_label = repo_relative(handoff_doc, repo_root)
    else:
        if args.block_index is None:
            block = extract_last_handoff_block(body)
            index = len(blocks) - 1
        else:
            if args.block_index < 0 or args.block_index >= len(blocks):
                print(f"[FAIL] block-index out of range for {handoff_doc}")
                return 1
            index = args.block_index
            block = blocks[index]
        block_label = f"{repo_relative(handoff_doc, repo_root)}#handoff-{index + 1}"

    if block:
        missing_headings = [heading for heading in REQUIRED_HEADINGS if heading not in block]
        if missing_headings:
            errors.append(f"Handoff block missing required sections: {', '.join(missing_headings)}")

        missing_handoff_labels = [label for label in REQUIRED_HANDOFF_SUBLABELS if extract_label_value(block, label) is None]
        if missing_handoff_labels:
            errors.append(f"Handoff block missing required handoff labels: {', '.join(missing_handoff_labels)}")

        missing_metadata = [label for label in REQUIRED_METADATA_LABELS if extract_label_value(block, label) is None]
        if missing_metadata:
            errors.append(f"Handoff block missing required metadata labels: {', '.join(missing_metadata)}")

        missing_research = [label for label in REQUIRED_RESEARCH_LABELS if extract_label_value(block, label) is None]
        if missing_research:
            errors.append(f"Handoff block missing required research labels: {', '.join(missing_research)}")

        role_id = extract_label_value(block, "- 当前角色标识：")
        if role_id:
            body_forbidden_scan = remove_metadata_only_lines(block)
            for pattern in ROLE_FORBIDDEN_PATTERNS.get(role_id, []):
                if re.search(pattern, body_forbidden_scan):
                    errors.append(f"Role id '{role_id}' contains forbidden content matching: {pattern}")

            if role_id == "tester":
                missing = [label for label in TESTER_REQUIRED_LABELS if extract_label_value(block, label) is None]
                if missing:
                    errors.append(f"Tester handoff missing required labels: {', '.join(missing)}")
            if role_id == "knowledge-keeper":
                missing = [
                    label for label in KNOWLEDGE_KEEPER_REQUIRED_LABELS if extract_label_value(block, label) is None
                ]
                if missing:
                    errors.append(f"Knowledge-keeper handoff missing required labels: {', '.join(missing)}")
            if role_id == "solution-designer":
                next_role = extract_label_value(block, "- 下一角色标识：")
                approval = extract_label_value(block, "- 用户方案批准：")
                if next_role == "implementer" and approval is None:
                    errors.append("Solution-designer handoff that routes to implementer must record 用户方案批准。")

        for phrase in GENERIC_WEAK_PHRASES:
            if re.search(phrase, block):
                errors.append(f"Found weak or non-verifiable phrase: {phrase}")

    if errors:
        print("[FAIL] Handoff quality check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("[PASS] Handoff quality check passed.")
    print(f"- handoff document: {repo_relative(handoff_doc, repo_root)}")
    print(f"- validated block: {block_label}")
    role_id = extract_label_value(block, "- 当前角色标识：") if block else None
    if role_id:
        print(f"- current role id: {role_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
