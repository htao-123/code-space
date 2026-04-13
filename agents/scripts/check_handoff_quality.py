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
    r"(?m)^\s*-\s*略\s*$",
    r"(?m)^\s*略\s*$",
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
    pattern = rf"(?m)^\s*{re.escape(label)}\s*(.+?)\s*$"
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


def extract_top_level_bullet_block(text: str, label: str) -> str:
    pattern = re.compile(
        rf"(?m)^{re.escape(label)}\s*$\n(?P<body>(?:^(?:  |\t).*(?:\n|$))*)"
    )
    match = pattern.search(text)
    if match is None:
        return ""
    return match.group("body").strip()


def has_meaningful_content(text: str) -> bool:
    if text.strip() == "":
        return False
    normalized = text.strip()
    return normalized not in {"无", "未填写", "待补充", "待确认", "N/A", "n/a"}


def infer_external_dependency(
    block: str,
    fact_text_by_id: dict[str, str],
    internal_evidence_items: dict[str, str],
    external_evidence_items: dict[str, tuple[str, str]],
    repo_root: Path,
) -> bool:
    dependency_patterns = [
        r"https?://",
        r"\bfetch\(",
        r"\bAPI_BASE\b",
        r"外部 API",
        r"网络请求",
        r"浏览器运行时",
        r"/latest",
        r"/currencies",
    ]
    searchable_parts = [block, *fact_text_by_id.values()]
    for evidence_path in internal_evidence_items.values():
        candidate = (repo_root / evidence_path).resolve() if not Path(evidence_path).is_absolute() else Path(evidence_path).resolve()
        if candidate.exists() and candidate.is_file():
            searchable_parts.append(read_text(candidate))
    for snapshot_path, source_url in external_evidence_items.values():
        candidate = (repo_root / snapshot_path).resolve() if not Path(snapshot_path).is_absolute() else Path(snapshot_path).resolve()
        searchable_parts.append(source_url)
        if candidate.exists() and candidate.is_file():
            searchable_parts.append(read_text(candidate))
    searchable = "\n".join(searchable_parts)
    return any(re.search(pattern, searchable, re.IGNORECASE) for pattern in dependency_patterns)


def has_passing_test_case(test_results_section: str, case_ref: str) -> bool:
    match = re.search(r"用例\s*(\d+)", case_ref)
    if match is None:
        return False
    case_number = match.group(1)
    return re.search(rf"用例\s*{re.escape(case_number)}\s*:\s*pass\b", test_results_section, re.IGNORECASE) is not None


def indicates_schema_mismatch(value: str | None) -> bool:
    if value is None:
        return False
    return bool(re.search(r"(不一致|需要迁移|mismatch|diverge)", value, re.IGNORECASE))


def is_empty_or_not_applicable(value: str | None) -> bool:
    if value is None:
        return True
    normalized = value.strip()
    return normalized in {"", "无", "不涉及", "无需", "未填写", "待补充", "待确认"}


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

    if role_id == "architect":
        schema_status = extract_label_value(block, "- 历史数据结构状态：")
        migration_requirement = extract_label_value(block, "- 迁移脚本要求：")
        if is_empty_or_not_applicable(schema_status):
            errors.append("Architect handoff must explicitly record schema/history-data status.")
        if is_empty_or_not_applicable(migration_requirement):
            errors.append("Architect handoff must explicitly record whether a migration script is required.")
        if indicates_schema_mismatch(schema_status):
            if migration_requirement is None or not re.search(r"(需要|必须|迁移脚本)", migration_requirement):
                errors.append(
                    "Architect handoff identifies schema mismatch but does not require a migration script."
                )
            if migration_requirement and re.search(r"(兼容分支|长期兼容|运行时兼容)", migration_requirement) and not re.search(r"(不采用|不默认|禁止)", migration_requirement):
                errors.append(
                    "Architect handoff must not treat long-lived compatibility handling as the default response to schema mismatch."
                )

    if role_id == "code-investigator":
        schema_status = extract_label_value(block, "- 历史数据结构状态：")
        data_gap = extract_label_value(block, "- 实际数据缺口：")
        if is_empty_or_not_applicable(schema_status):
            errors.append("Code-investigator handoff must explicitly record schema/history-data status.")
        if indicates_schema_mismatch(schema_status) and is_empty_or_not_applicable(data_gap):
            errors.append(
                "Code-investigator handoff identifies schema mismatch but does not describe the real data gap migration must close."
            )

    if role_id == "solution-designer":
        schema_status = extract_label_value(block, "- 历史数据结构状态：")
        migration_strategy = extract_label_value(block, "- 数据迁移策略：")
        compatibility_conclusion = extract_label_value(block, "- 长期兼容处理结论：")
        if is_empty_or_not_applicable(schema_status):
            errors.append("Solution-designer handoff must explicitly record schema/history-data status.")
        if is_empty_or_not_applicable(migration_strategy):
            errors.append("Solution-designer handoff must explicitly record the migration strategy decision.")
        if is_empty_or_not_applicable(compatibility_conclusion):
            errors.append("Solution-designer handoff must explicitly record the long-lived compatibility conclusion.")
        if indicates_schema_mismatch(schema_status):
            if migration_strategy is None or not re.search(r"(迁移|migration)", migration_strategy, re.IGNORECASE):
                errors.append(
                    "Solution-designer handoff identifies schema mismatch but does not define an explicit migration strategy."
                )
            if compatibility_conclusion and not re.search(r"(不采用|不默认|不引入|禁止)", compatibility_conclusion):
                errors.append(
                    "Solution-designer handoff must explicitly reject long-lived compatibility handling when schema mismatch is being handled by migration."
                )

    if role_id == "implementer":
        schema_status = extract_label_value(block, "- 历史数据结构状态：")
        migration_implementation = extract_label_value(block, "- 迁移实现状态：")
        compatibility_branch_status = extract_label_value(block, "- 兼容分支状态：")
        if is_empty_or_not_applicable(schema_status):
            errors.append("Implementer handoff must explicitly record schema/history-data status.")
        if is_empty_or_not_applicable(migration_implementation):
            errors.append("Implementer handoff must explicitly record migration implementation status.")
        if is_empty_or_not_applicable(compatibility_branch_status):
            errors.append("Implementer handoff must explicitly record compatibility-branch status.")
        if indicates_schema_mismatch(schema_status):
            if migration_implementation is None or re.search(r"(未实现|不涉及|无需|待补充)", migration_implementation):
                errors.append(
                    "Implementer handoff identifies schema mismatch but does not record an implemented migration entrypoint or migration script."
                )
            if compatibility_branch_status and re.search(r"(已新增|已引入|保留兼容|运行时兼容)", compatibility_branch_status):
                errors.append(
                    "Implementer handoff must not introduce long-lived compatibility branches as the default response to schema mismatch."
                )

    if role_id == "tester":
        runtime_verification = extract_top_level_bullet_block(block, "- 运行时验证：")
        external_dependency_verification = extract_top_level_bullet_block(block, "- 外部依赖验证：")
        unverified_reason = extract_top_level_bullet_block(block, "- 未验证原因：")
        test_results_section = extract_section(block, "【交付物】", ["【约束】"])
        declared_external_dependency = extract_label_value(
            external_dependency_verification,
            "- 是否涉及外部 API / 浏览器运行时 / 网络请求:",
        )
        success_path_status = extract_label_value(
            external_dependency_verification,
            "- 成功路径是否已真实验证:",
        )
        success_path_evidence = extract_label_value(
            external_dependency_verification,
            "- 成功路径证据:",
        )

        if not has_meaningful_content(runtime_verification):
            errors.append("Tester handoff must provide substantive runtime verification details.")
        if not has_meaningful_content(external_dependency_verification):
            errors.append("Tester handoff must provide substantive external-dependency verification details.")
        if unverified_reason.strip() == "":
            errors.append("Tester handoff must provide an explicit unverified-reason field value.")

        external_dependency_involved = infer_external_dependency(
            block,
            fact_text_by_id,
            internal_evidence_items,
            external_evidence_items,
            repo_root,
        ) or external_required in {"是", "需要", "yes", "true", "True"}
        if external_dependency_involved and (
            declared_external_dependency is None
            or re.search(r"(不涉及|无外部依赖|否)", declared_external_dependency)
        ):
            errors.append(
                "Tester handoff marks external dependency as not involved, but the validated evidence indicates external APIs, browser runtime, or network requests are involved."
            )

        success_path_verified = bool(success_path_status and re.search(r"(已真实验证|已验证|pass|通过|是)", success_path_status))
        success_path_not_verified = bool(success_path_status and re.search(r"(未验证|blocked|阻塞|无法验证|未实际验证|否)", success_path_status))
        runtime_not_run = re.search(r"(未实际运行|未运行|blocked|阻塞|无法运行)", runtime_verification)

        if (success_path_not_verified or runtime_not_run) and unverified_reason.strip() in {"", "无"}:
            errors.append(
                "Tester handoff cannot mark runtime or external success-path verification incomplete while leaving unverified reason empty or '无'."
            )

        if (
            not success_path_not_verified
            and not runtime_not_run
            and unverified_reason.strip() not in {"", "无"}
            and has_meaningful_content(unverified_reason)
        ):
            errors.append(
                "Tester handoff should not record a non-empty unverified reason after claiming runtime and external success-path verification are complete."
            )

        if external_dependency_involved and success_path_status is None:
            errors.append("Tester handoff must explicitly declare whether the external success path was truly verified.")

        if success_path_verified:
            if success_path_evidence is None or not re.search(r"用例\s*\d+", success_path_evidence):
                errors.append(
                    "Tester handoff must bind external success-path verification to a concrete passing test case, e.g. '用例 1'."
                )
            elif not has_passing_test_case(test_results_section, success_path_evidence):
                errors.append(
                    "Tester handoff claims the external success path was truly verified, but the referenced test case is missing or not marked pass in the test-results section."
                )

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
