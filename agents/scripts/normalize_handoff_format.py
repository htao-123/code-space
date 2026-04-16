#!/usr/bin/env python3
"""
Normalize handoff formatting into gate-friendly shapes.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ITEM_PREFIXES_BY_LABEL = {
    "- 内部证据清单：": ["EVID-IN-"],
    "- 外部证据清单：": ["EVID-EX-"],
    "- 事实清单：": ["FACT-"],
    "- 证据映射：": ["FACT-"],
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def append_format_repair_record(text: str) -> str:
    record = (
        "\n\n## Repair Record - Handoff Format Normalization\n\n"
        "- 修复类型：format-only\n"
        "- 修复处理：使用 normalize_handoff_format.py 仅规范 handoff 列表/分隔符/换行格式。\n"
        "- 负责角色：normalizer\n"
        "- 是否改变需求含义：否\n"
        "- 是否改变实现行为：否\n"
        "- 后续验证：重新运行对应 stage workflow gate。\n"
    )
    return text.rstrip() + record


def split_items(value: str, prefixes: list[str]) -> list[str]:
    normalized = value.replace("\r\n", "\n")
    normalized = re.sub(r",\s*(?=(" + "|".join(re.escape(prefix) for prefix in prefixes) + r"))", "\n", normalized)
    parts = [part.strip() for part in normalized.splitlines()]
    return [part for part in parts if part]


def normalize_internal_item(item: str) -> str:
    match = re.match(r"^(EVID-IN-\d+)\s*(?:->|:)\s*(.+?)\s*$", item)
    if not match:
        return item.strip()
    evidence_id, target = match.groups()
    return f"{evidence_id} -> {target.strip()}"


def normalize_external_item(item: str) -> str:
    match = re.match(r"^(EVID-EX-\d+)\s*(?:->|:)\s*(.+?)\s*\|\s*(https?://\S+)\s*$", item)
    if not match:
        return item.strip()
    evidence_id, snapshot_path, url = match.groups()
    return f"{evidence_id} -> {snapshot_path.strip()} | {url.strip()}"


def normalize_fact_item(item: str) -> str:
    match = re.match(r"^(FACT-\d+)\s*(?:->|:)\s*(.+?)\s*$", item)
    if not match:
        return item.strip()
    fact_id, fact_text = match.groups()
    fact_text = fact_text.strip()
    if not fact_text.startswith("证据摘录："):
        fact_text = f"证据摘录：{fact_text}"
    return f"{fact_id} -> {fact_text}"


def normalize_mapping_item(item: str) -> str:
    match = re.match(r"^(FACT-\d+)\s*(?:->|:)\s*(.+?)\s*$", item)
    if not match:
        return item.strip()
    fact_id, rest = match.groups()
    parts = [part.strip() for part in rest.split("::")]
    if len(parts) != 3:
        return f"{fact_id} -> {rest.strip()}"
    evidence_id, keyword, excerpt = parts
    return f"{fact_id} -> {evidence_id}::{keyword}::{excerpt}"


def normalize_items_for_label(label: str, raw_value: str) -> str:
    prefixes = ITEM_PREFIXES_BY_LABEL[label]
    items = split_items(raw_value, prefixes)
    normalized_items: list[str] = []
    for item in items:
        if label == "- 内部证据清单：":
            normalized_items.append(normalize_internal_item(item))
        elif label == "- 外部证据清单：":
            normalized_items.append(normalize_external_item(item))
        elif label == "- 事实清单：":
            normalized_items.append(normalize_fact_item(item))
        elif label == "- 证据映射：":
            normalized_items.append(normalize_mapping_item(item))
    return ", ".join(normalized_items)


def normalize_block(block: str) -> str:
    lines = block.splitlines()
    output: list[str] = []
    index = 0
    labels = set(ITEM_PREFIXES_BY_LABEL)

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        matched_label = next((label for label in labels if stripped.startswith(label)), None)
        if matched_label is None:
            output.append(line.rstrip())
            index += 1
            continue

        current_indent = re.match(r"^\s*", line).group(0)
        same_line_value = stripped[len(matched_label):].strip()
        values: list[str] = [same_line_value] if same_line_value else []
        index += 1
        while index < len(lines):
            next_line = lines[index]
            next_stripped = next_line.strip()
            if next_stripped == "":
                index += 1
                continue
            if next_line.startswith(current_indent + "  ") or next_line.startswith(current_indent + "\t"):
                values.append(next_stripped.lstrip("-").strip())
                index += 1
                continue
            break

        normalized_value = normalize_items_for_label(matched_label, "\n".join(values))
        output.append(f"{current_indent}{matched_label} {normalized_value}".rstrip())

    normalized = "\n".join(output)
    if block.endswith("\n"):
        normalized += "\n"
    return normalized


def extract_blocks(text: str) -> tuple[list[str], list[str], list[str]]:
    heading = "【角色结论】"
    positions = [match.start() for match in re.finditer(re.escape(heading), text)]
    if not positions:
        return [text], [], []

    prefixes: list[str] = []
    blocks: list[str] = []
    suffixes: list[str] = []

    cursor = 0
    for i, start in enumerate(positions):
        end = positions[i + 1] if i + 1 < len(positions) else len(text)
        prefixes.append(text[cursor:start])
        blocks.append(text[start:end])
        cursor = end
    suffixes = [""] * len(blocks)
    return prefixes, blocks, suffixes


def normalize_document(text: str) -> str:
    heading = "【角色结论】"
    positions = [match.start() for match in re.finditer(re.escape(heading), text)]
    if not positions:
        return normalize_block(text)

    rebuilt: list[str] = []
    cursor = 0
    for i, start in enumerate(positions):
        end = positions[i + 1] if i + 1 < len(positions) else len(text)
        rebuilt.append(text[cursor:start])
        rebuilt.append(normalize_block(text[start:end]))
        cursor = end
    return "".join(rebuilt)


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize handoff formatting into gate-friendly shapes.")
    parser.add_argument("--handoff-doc", required=True, help="Path to the handoff document.")
    parser.add_argument("--repo-root", default=".", help="Repository root.")
    parser.add_argument(
        "--write",
        action="store_true",
        help=(
            "Write the normalized result back to the file. Use only for format-only repairs; "
            "do not use this to add evidence, approval, role conclusions, test results, or retrospectives."
        ),
    )
    parser.add_argument(
        "--repair-type",
        choices=["format-only"],
        help="Required with --write. Only format-only repair may be normalized in place.",
    )
    parser.add_argument(
        "--ack-format-only",
        action="store_true",
        help="Required with --write to acknowledge that no facts, approvals, conclusions, or test results are being changed.",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    handoff_doc = (repo_root / args.handoff_doc).resolve() if not Path(args.handoff_doc).is_absolute() else Path(args.handoff_doc).resolve()
    if not handoff_doc.exists() or handoff_doc.is_dir():
        print(f"[FAIL] Handoff document not found or invalid: {handoff_doc}")
        return 1

    original = read_text(handoff_doc)
    normalized = normalize_document(original)

    if args.write:
        if args.repair_type != "format-only" or not args.ack_format_only:
            print("[FAIL] --write requires --repair-type format-only and --ack-format-only.")
            print()
            print("Suggested repair record:")
            print()
            print("## Repair Record - Handoff Format Normalization")
            print()
            print("- 修复类型：format-only")
            print("- 修复处理：使用 normalize_handoff_format.py 仅规范 handoff 列表/分隔符/换行格式。")
            print("- 负责角色：")
            print("- 是否改变需求含义：否")
            print("- 是否改变实现行为：否")
            print("- 后续验证：重新运行对应 stage workflow gate。")
            return 1
        write_text(handoff_doc, append_format_repair_record(normalized))
        print(f"[PASS] Normalized handoff document in place: {handoff_doc}")
        print("[INFO] Appended a task-level format-only Repair Record.")
    else:
        sys.stdout.write(normalized)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
