#!/usr/bin/env python3
"""
Handoff quality checker for the AI engineering pipeline.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROLE_FORBIDDEN_PATTERNS = {
    "requirement-analyst": [
        r"(?i)\bdiff\b",
        r"代码实现",
        r"修改文件",
        r"接口设计",
    ],
    "architect": [
        r"具体代码",
        r"代码实现",
        r"直接编码",
    ],
    "code-investigator": [
        r"建议",
        r"推荐方案",
        r"应该修改",
        r"解决方案",
    ],
    "solution-designer": [
        r"```[\s\S]*?```",
        r"直接编码",
        r"完整代码",
    ],
    "implementer": [
        r"顺手重构",
        r"额外优化",
        r"新增页面",
    ],
    "reviewer": [
        r"已直接修复",
        r"我修改了",
        r"已改代码",
    ],
    "tester": [
        r"假设成功",
        r"应该没问题",
    ],
    "knowledge-keeper": [
        r"我猜",
        r"可能就是",
        r"应该是",
    ],
}

GENERIC_WEAK_PHRASES = [
    r"暂不展开",
    r"略",
    r"自行处理",
    r"查过了",
]

REQUIRED_QUALITY_LABELS = [
    "- 内部证据清单：",
    "- 外部证据清单：",
    "- 事实清单：",
    "- 证据映射：",
    "- 推断说明：",
    "- 未验证项：",
]

URL_RE = re.compile(r"^https?://\S+$")
FACT_LINE_RE = re.compile(r"(?m)^(FACT-\d+)\s*->\s*证据摘录：(.+?)\s*$")
INTERNAL_EVIDENCE_ITEM_RE = re.compile(r"^(EVID-IN-\d+)\s*->\s*(.+?)$")
EXTERNAL_EVIDENCE_ITEM_RE = re.compile(r"^(EVID-EX-\d+)\s*->\s*(.+?)\s*\|\s*(https?://\S+)$")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_last_handoff_block(text: str) -> str:
    positions = [match.start() for match in re.finditer(re.escape("【角色结论】"), text)]
    if not positions:
        return ""
    return text[positions[-1]:]


def extract_all_handoff_blocks(text: str) -> list[str]:
    positions = [match.start() for match in re.finditer(re.escape("【角色结论】"), text)]
    if not positions:
        return []
    blocks: list[str] = []
    for index, start in enumerate(positions):
        end = positions[index + 1] if index + 1 < len(positions) else len(text)
        blocks.append(text[start:end])
    return blocks


def extract_label_value(text: str, label: str) -> str | None:
    pattern = rf"(?m)^{re.escape(label)}\s*(.+?)\s*$"
    match = re.search(pattern, text)
    if match is None:
        return None
    return match.group(1).strip()


def repo_relative(path: Path, repo_root: Path) -> str:
    try:
        return str(path.resolve().relative_to(repo_root.resolve()))
    except ValueError:
        return str(path.resolve())


def split_items(value: str | None, item_prefixes: list[str] | None = None) -> list[str]:
    if value is None:
        return []
    normalized = value.replace("\r\n", "\n")
    if item_prefixes:
        pattern = r",\s*(?=(" + "|".join(re.escape(prefix) for prefix in item_prefixes) + r"))"
        normalized = re.sub(pattern, "\n", normalized)
    parts = [part.strip() for part in normalized.splitlines()]
    return [part for part in parts if part]


def extract_section(text: str, start_heading: str, end_headings: list[str]) -> str:
    start = text.find(start_heading)
    if start == -1:
        return ""
    start += len(start_heading)
    end_positions = [text.find(heading, start) for heading in end_headings]
    valid_positions = [position for position in end_positions if position != -1]
    end = min(valid_positions) if valid_positions else len(text)
    return text[start:end]


def parse_mapping_items(items_raw: list[str]) -> tuple[list[tuple[str, str, str, str]], list[str]]:
    items: list[tuple[str, str, str, str]] = []
    invalid: list[str] = []
    for raw in items_raw:
        if "->" not in raw:
            invalid.append(raw)
            continue
        fact_id, rest = raw.split("->", 1)
        parts = [part.strip() for part in rest.split("::")]
        if len(parts) != 3:
            invalid.append(raw)
            continue
        evidence_path, keyword, excerpt = parts
        items.append((fact_id.strip(), evidence_path.strip(), keyword.strip(), excerpt.strip()))
    return items, invalid


def parse_internal_evidence_items(items_raw: list[str]) -> tuple[dict[str, str], list[str], list[str]]:
    items: dict[str, str] = {}
    invalid: list[str] = []
    duplicates: list[str] = []
    for raw in items_raw:
        match = INTERNAL_EVIDENCE_ITEM_RE.match(raw)
        if not match:
            invalid.append(raw)
            continue
        evidence_id, target = match.groups()
        if evidence_id.strip() in items:
            duplicates.append(evidence_id.strip())
        items[evidence_id.strip()] = target.strip()
    return items, invalid, duplicates


def parse_external_evidence_items(items_raw: list[str]) -> tuple[dict[str, tuple[str, str]], list[str], list[str]]:
    items: dict[str, tuple[str, str]] = {}
    invalid: list[str] = []
    duplicates: list[str] = []
    for raw in items_raw:
        match = EXTERNAL_EVIDENCE_ITEM_RE.match(raw)
        if not match:
            invalid.append(raw)
            continue
        evidence_id, snapshot_path, url = match.groups()
        if evidence_id.strip() in items:
            duplicates.append(evidence_id.strip())
        items[evidence_id.strip()] = (snapshot_path.strip(), url.strip())
    return items, invalid, duplicates


def parse_fact_items(items_raw: list[str]) -> tuple[dict[str, str], list[str], list[str]]:
    items: dict[str, str] = {}
    invalid: list[str] = []
    duplicates: list[str] = []
    for raw in items_raw:
        match = FACT_LINE_RE.match(raw)
        if not match:
            invalid.append(raw)
            continue
        fact_id, fact_text = match.groups()
        if fact_id.strip() in items:
            duplicates.append(fact_id.strip())
        items[fact_id.strip()] = fact_text.strip()
    return items, invalid, duplicates


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check handoff content quality requirements."
    )
    parser.add_argument("--repo-root", default=".", help="Repository root.")
    parser.add_argument("--handoff-doc", required=True, help="Handoff doc to validate.")
    parser.add_argument("--project-path", required=True, help="Approved project path for evidence validation.")
    parser.add_argument(
        "--block-index",
        type=int,
        help="Optional zero-based handoff block index to validate. Defaults to latest block.",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    handoff_doc = (repo_root / args.handoff_doc).resolve() if not Path(args.handoff_doc).is_absolute() else Path(args.handoff_doc).resolve()
    project_path = (repo_root / args.project_path).resolve() if not Path(args.project_path).is_absolute() else Path(args.project_path).resolve()

    errors: list[str] = []

    if not handoff_doc.exists() or handoff_doc.is_dir():
        print(f"[FAIL] Handoff document not found or invalid: {handoff_doc}")
        return 1

    text = read_text(handoff_doc)
    blocks = extract_all_handoff_blocks(text)
    if not blocks:
        print(f"[FAIL] No handoff block found in {repo_relative(handoff_doc, repo_root)}")
        return 1
    if args.block_index is None:
        block = blocks[-1]
        block_label = "latest"
    else:
        if args.block_index < 0 or args.block_index >= len(blocks):
            print(
                "[FAIL] Requested handoff block index is out of range: "
                f"{args.block_index} for {repo_relative(handoff_doc, repo_root)}"
            )
            return 1
        block = blocks[args.block_index]
        block_label = str(args.block_index)

    role_id = extract_label_value(block, "- 当前角色标识：")
    role_display = extract_label_value(block, "- 当前角色：")
    if role_id is None:
        errors.append("Missing current role id metadata.")
    else:
        forbidden_patterns = ROLE_FORBIDDEN_PATTERNS.get(role_id, [])
        body_forbidden_scan = "\n".join(
            [
                extract_section(block, "【角色结论】", ["【已核实输入】"]),
                extract_section(block, "【调研发现】", ["【交付物】"]),
                extract_section(block, "【交付物】", ["【约束】"]),
                extract_section(block, "【约束】", ["【校验标准】"]),
                extract_section(block, "【校验标准】", ["【禁止事项】"]),
                extract_section(block, "【禁止事项】", ["【交接给下一个角色】"]),
            ]
        )
        for pattern in forbidden_patterns:
            if re.search(pattern, body_forbidden_scan):
                errors.append(f"Role id '{role_id}' contains forbidden content matching: {pattern}")

    missing_quality_labels = [label for label in REQUIRED_QUALITY_LABELS if label not in block]
    if missing_quality_labels:
        errors.append(
            "Missing required quality labels: " + ", ".join(missing_quality_labels)
        )

    external_required = extract_label_value(block, "- 是否需要外部调研：")
    external_sources = extract_label_value(block, "- 外部证据清单：")
    external_source_items = split_items(external_sources, ["EVID-EX-"])
    external_evidence_items, invalid_external_items, duplicate_external_ids = parse_external_evidence_items(external_source_items)
    if external_required in {"是", "需要", "yes", "true", "True"}:
        if external_sources in {None, "", "无", "未使用"}:
            errors.append("External research is required but external evidence sources are empty.")
        else:
            if invalid_external_items:
                errors.append(
                    "External evidence list contains malformed items: " + ", ".join(invalid_external_items)
                )
            if duplicate_external_ids:
                errors.append(
                    "External evidence list reuses duplicate ids: " + ", ".join(sorted(set(duplicate_external_ids)))
                )
            if not external_evidence_items:
                errors.append("External evidence list must use 'EVID-EX-编号 -> 本地快照路径 | URL' format.")
            for evidence_id, (snapshot_path, source_url) in external_evidence_items.items():
                snapshot_candidate = (repo_root / snapshot_path).resolve() if not Path(snapshot_path).is_absolute() else Path(snapshot_path).resolve()
                try:
                    snapshot_candidate.relative_to(repo_root)
                except ValueError:
                    errors.append(f"External evidence snapshot is outside repository: {snapshot_path}")
                    continue
                if not snapshot_candidate.exists() or snapshot_candidate.is_dir():
                    errors.append(f"External evidence snapshot does not exist as a file: {snapshot_path}")
                    continue
                try:
                    snapshot_candidate.relative_to(project_path)
                except ValueError:
                    errors.append(f"External evidence snapshot is outside approved project path: {snapshot_path}")
                if not URL_RE.match(source_url):
                    errors.append(f"External evidence source is not a concrete URL: {source_url}")

    internal_evidence = extract_label_value(block, "- 内部证据清单：")
    internal_evidence_raw_items = split_items(internal_evidence, ["EVID-IN-"])
    internal_evidence_items: dict[str, str] = {}
    if internal_evidence in {None, "", "无"}:
        errors.append("Internal evidence files must not be empty.")
    else:
        internal_evidence_items, invalid_internal_items, duplicate_internal_ids = parse_internal_evidence_items(internal_evidence_raw_items)
        if invalid_internal_items:
            errors.append(
                "Internal evidence list contains malformed items: " + ", ".join(invalid_internal_items)
            )
        if duplicate_internal_ids:
            errors.append(
                "Internal evidence list reuses duplicate ids: " + ", ".join(sorted(set(duplicate_internal_ids)))
            )
        if not internal_evidence_items:
            errors.append("Internal evidence list must use 'EVID-IN-编号 -> 文件路径' format.")
        for evidence_id, item in internal_evidence_items.items():
            if not evidence_id.startswith("EVID-IN-"):
                errors.append(f"Internal evidence id must use EVID-IN-* format: {evidence_id}")
            candidate = (repo_root / item).resolve() if not Path(item).is_absolute() else Path(item).resolve()
            try:
                candidate.relative_to(repo_root)
            except ValueError:
                errors.append(f"Internal evidence file is outside repository: {item}")
                continue
            if not candidate.exists() or candidate.is_dir():
                errors.append(f"Internal evidence file does not exist as a file: {item}")
                continue
            try:
                candidate.relative_to(project_path)
            except ValueError:
                errors.append(f"Internal evidence file is outside approved project path: {item}")

    verified_facts = extract_label_value(block, "- 事实清单：")
    evidence_mapping = extract_label_value(block, "- 证据映射：")
    inference = extract_label_value(block, "- 推断说明：")
    unknowns = extract_label_value(block, "- 未验证项：")
    fact_raw_items = split_items(verified_facts, ["FACT-"])
    fact_text_by_id, invalid_fact_items, duplicate_fact_ids = parse_fact_items(fact_raw_items)
    if verified_facts in {None, "", "无"}:
        errors.append("Verified facts must not be empty.")
    elif not fact_text_by_id:
        errors.append("Facts must use 'FACT-编号 -> 证据摘录：摘录内容' format for each fact.")
    elif invalid_fact_items:
        errors.append("Facts list contains malformed items: " + ", ".join(invalid_fact_items))
    if duplicate_fact_ids:
        errors.append("Facts list reuses duplicate ids: " + ", ".join(sorted(set(duplicate_fact_ids))))
    if evidence_mapping in {None, "", "无"}:
        errors.append("Evidence mapping must not be empty.")
    else:
        mapping_raw_items = split_items(evidence_mapping, ["FACT-"])
        parsed_mappings, invalid_mapping_items = parse_mapping_items(mapping_raw_items)
        if invalid_mapping_items:
            errors.append("Evidence mapping contains malformed items: " + ", ".join(invalid_mapping_items))
        if not parsed_mappings:
            errors.append(
                "Evidence mapping must use 'FACT-编号 -> EVID-编号::关键词::摘录' format."
            )
        else:
            all_evidence_items = {**internal_evidence_items, **external_evidence_items}
            fact_ids_in_verified = set(fact_text_by_id)
            mapped_fact_ids: set[str] = set()
            for fact_id, evidence_id, keyword, excerpt in parsed_mappings:
                if fact_id in mapped_fact_ids:
                    errors.append(f"Evidence mapping reuses duplicate fact identifier: {fact_id}")
                mapped_fact_ids.add(fact_id)
                if evidence_id not in all_evidence_items:
                    errors.append(
                        f"Evidence mapping references an unknown evidence id: {evidence_id}"
                    )
                    continue
                content = None
                evidence_target = None
                if evidence_id.startswith("EVID-IN-"):
                    evidence_path = all_evidence_items[evidence_id]
                    evidence_target = evidence_path
                    candidate = (repo_root / evidence_path).resolve() if not Path(evidence_path).is_absolute() else Path(evidence_path).resolve()
                    if not candidate.exists() or candidate.is_dir():
                        errors.append(f"Evidence mapping file does not exist as a file: {evidence_path}")
                        continue
                    content = read_text(candidate)
                elif evidence_id.startswith("EVID-EX-"):
                    snapshot_path, source_url = all_evidence_items[evidence_id]
                    evidence_target = snapshot_path
                    candidate = (repo_root / snapshot_path).resolve() if not Path(snapshot_path).is_absolute() else Path(snapshot_path).resolve()
                    if not candidate.exists() or candidate.is_dir():
                        errors.append(f"External evidence snapshot does not exist as a file: {snapshot_path}")
                        continue
                    content = read_text(candidate)
                if keyword in {"", "无"}:
                    errors.append(f"Evidence mapping keyword must not be empty for fact {fact_id}.")
                    continue
                if content is not None and keyword not in content:
                    errors.append(
                        f"Evidence mapping keyword '{keyword}' not found in evidence artifact {evidence_target}."
                    )
                if excerpt in {"", "无"}:
                    errors.append(f"Evidence mapping excerpt must not be empty for fact {fact_id}.")
                    continue
                if content is not None and excerpt not in content:
                    errors.append(
                        f"Evidence mapping excerpt '{excerpt}' not found in evidence artifact {evidence_target}."
                    )
                    continue
                fact_text = fact_text_by_id.get(fact_id)
                if fact_text is None:
                    errors.append(f"Evidence mapping references unknown fact identifier: {fact_id}")
                    continue
                expected_fact_text = excerpt
                if fact_text != expected_fact_text:
                    errors.append(
                        f"Verified fact {fact_id} must exactly match excerpt '{excerpt}' so unsupported extra claims cannot pass."
                    )
            if fact_ids_in_verified and fact_ids_in_verified != mapped_fact_ids:
                missing = sorted(fact_ids_in_verified - mapped_fact_ids)
                extra = sorted(mapped_fact_ids - fact_ids_in_verified)
                if missing:
                    errors.append(
                        "Verified facts missing evidence mappings for: " + ", ".join(missing)
                    )
                if extra:
                    errors.append(
                        "Evidence mappings reference unknown fact identifiers: " + ", ".join(extra)
                    )
    if inference is None:
        errors.append("Inference section must be present even if it says '无'.")
    if unknowns is None:
        errors.append("Unverified items section must be present even if it says '无'.")

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
    if role_id:
        print(f"- current role id: {role_id}")
    if role_display:
        print(f"- current role: {role_display}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
