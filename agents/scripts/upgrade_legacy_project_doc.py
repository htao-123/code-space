#!/usr/bin/env python3
"""
Upgrade a legacy project document into the current frontmatter-first workflow shape.
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

ROLE_DISPLAY_TO_ID = {
    "需求分析师": "requirement-analyst",
    "建筑师": "architect",
    "架构师": "architect",
    "代码调查员": "code-investigator",
    "方案设计师": "solution-designer",
    "开发者": "implementer",
    "审查员": "reviewer",
    "测试员": "tester",
    "知识归档员": "knowledge-keeper",
}

ROLE_ID_TO_NEXT = {
    "requirement-analyst": "architect",
    "architect": "code-investigator",
    "code-investigator": "solution-designer",
    "solution-designer": "implementer",
    "implementer": "reviewer",
    "reviewer": "tester",
    "tester": "knowledge-keeper",
    "knowledge-keeper": "terminal",
}

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

RESEARCH_DEFAULTS = {
    "- 内部调研范围：": "待补录",
    "- 内部调研结论：": "待补录",
    "- 外部调研范围：": "待补录",
    "- 外部调研来源：": "待补录",
    "- 官方事实结论：": "待补录",
    "- 主流方案结论：": "待补录",
    "- 最佳实现参考结论：": "待补录",
    "- 是否发现新增外部差异：": "待补录",
    "- 推断说明：": "待补录",
    "- 未验证项：": "无",
    "- 需要用户确认：": "否",
    "- 推荐方案：": "无",
    "- 推荐原因：": "无",
    "- 主要权衡：": "无",
}

TESTER_DEFAULTS = {
    "- 运行时验证：": "待补录",
    "- 外部依赖验证：": "待补录",
    "- 未验证原因：": "无",
}

KNOWLEDGE_KEEPER_DEFAULTS = {
    "- 需求复盘结论：": "待补录",
    "- 自我审查结论：": "待补录",
    "- 自我纠错项：": "待补录",
}

BUGFIX_BASE_DEFAULTS = {
    "- 问题类型：": "bugfix",
    "- 复现步骤：": "待补录",
    "- 预期结果：": "待补录",
    "- 实际结果：": "待补录",
}

BUGFIX_DOWNSTREAM_DEFAULTS = {
    "- 根因摘要：": "待补录",
    "- 回归检查范围：": "待补录",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


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


def dump_frontmatter(data: dict[str, str]) -> str:
    order = [
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
    lines = ["---"]
    for key in order:
        if key in data:
            lines.append(f"{key}: {data[key]}")
    extra_keys = [key for key in data.keys() if key not in order]
    for key in extra_keys:
        lines.append(f"{key}: {data[key]}")
    lines.append("---")
    return "\n".join(lines) + "\n"


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


def replace_blocks(original_body: str, new_blocks: list[str]) -> str:
    positions = [match.start() for match in re.finditer(re.escape("【角色结论】"), original_body)]
    if not positions or len(positions) != len(new_blocks):
        return original_body
    parts: list[str] = []
    cursor = 0
    for index, start in enumerate(positions):
        end = positions[index + 1] if index + 1 < len(positions) else len(original_body)
        next_heading = original_body.find("\n## ", start)
        if next_heading != -1 and next_heading < end:
            end = next_heading
        parts.append(original_body[cursor:start])
        parts.append(new_blocks[index])
        cursor = end
    parts.append(original_body[cursor:])
    return "".join(parts)


def extract_label_value(text: str, label: str) -> str | None:
    pattern = rf"(?m)^\s*{re.escape(label)}\s*(.+?)\s*$"
    match = re.search(pattern, text)
    if match is None:
        return None
    return match.group(1).strip()


def find_section_span(block: str, heading: str) -> tuple[int, int] | None:
    start = block.find(heading)
    if start == -1:
        return None
    content_start = start + len(heading)
    end = len(block)
    for candidate in REQUIRED_HEADINGS:
        if candidate == heading:
            continue
        pos = block.find(candidate, content_start)
        if pos != -1 and pos < end:
            end = pos
    return start, end


def extract_section_content(block: str, heading: str) -> str:
    span = find_section_span(block, heading)
    if span is None:
        return ""
    start, end = span
    section = block[start + len(heading) : end]
    return section.strip("\n")


def rebuild_block(block: str) -> str:
    rebuilt_sections: list[str] = []
    for heading in REQUIRED_HEADINGS:
        content = extract_section_content(block, heading)
        section = heading
        if content:
            section += "\n" + content.rstrip("\n")
        rebuilt_sections.append(section.rstrip())
    return "\n\n".join(rebuilt_sections).rstrip() + "\n"


def ensure_section_exists(block: str, heading: str) -> str:
    if heading in block:
        return block
    if block and not block.endswith("\n"):
        block += "\n"
    return block + f"{heading}\n"


def ensure_label_in_section(block: str, heading: str, label: str, value: str) -> str:
    block = ensure_section_exists(block, heading)
    span = find_section_span(block, heading)
    if span is None:
        return block
    start, end = span
    section = block[start:end]
    if extract_label_value(section, label) is not None:
        return block
    insert = f"{label} {value}\n"
    if not section.endswith("\n"):
        section += "\n"
    section += insert
    return block[:start] + section + block[end:]


def infer_role_id(block: str) -> str | None:
    current_role_id = extract_label_value(block, "- 当前角色标识：")
    if current_role_id:
        return current_role_id
    display = extract_label_value(block, "- 当前角色：")
    if display:
        display = display.split("【", 1)[0].strip()
        return ROLE_DISPLAY_TO_ID.get(display)
    return None


def infer_next_role_id(block: str, current_role_id: str | None) -> str | None:
    next_role_id = extract_label_value(block, "- 下一角色标识：")
    if next_role_id:
        return next_role_id
    next_role_display = extract_label_value(block, "- 下一角色：")
    if next_role_display:
        display = next_role_display.split("【", 1)[0].strip()
        if display in {"无", "terminal"}:
            return "terminal"
        return ROLE_DISPLAY_TO_ID.get(display)
    if current_role_id:
        return ROLE_ID_TO_NEXT.get(current_role_id)
    return None


def derive_requirement_id(frontmatter: dict[str, str], blocks: list[str], doc_path: Path) -> str:
    if frontmatter.get("requirement_id"):
        return frontmatter["requirement_id"]
    for block in blocks:
        requirement_id = extract_label_value(block, "- 需求标识：")
        if requirement_id:
            return requirement_id
    stem = re.sub(r"[^A-Za-z0-9]+", "-", doc_path.stem).strip("-").upper()
    return f"LEGACY-{stem or 'DOC'}"


def normalize_block(
    block: str,
    requirement_id: str,
    block_index: int,
    work_type: str,
) -> str:
    block = rebuild_block(block)
    current_role_id = infer_role_id(block)
    next_role_id = infer_next_role_id(block, current_role_id)
    if current_role_id:
        block = ensure_label_in_section(block, "【已核实输入】", "- 当前角色标识：", current_role_id)
    if next_role_id:
        block = ensure_label_in_section(block, "【已核实输入】", "- 下一角色标识：", next_role_id)
    block = ensure_label_in_section(block, "【已核实输入】", "- 需求标识：", requirement_id)
    if current_role_id:
        block = ensure_label_in_section(
            block,
            "【已核实输入】",
            "- 当前交接标识：",
            f"{requirement_id}-{current_role_id}-{block_index + 1}",
        )

    for label, value in RESEARCH_DEFAULTS.items():
        block = ensure_label_in_section(block, "【调研发现】", label, value)

    if current_role_id == "tester":
        for label, value in TESTER_DEFAULTS.items():
            block = ensure_label_in_section(block, "【交付物】", label, value)

    if current_role_id == "knowledge-keeper":
        for label, value in KNOWLEDGE_KEEPER_DEFAULTS.items():
            block = ensure_label_in_section(block, "【调研发现】", label, value)

    if work_type == "bugfix":
        for label, value in BUGFIX_BASE_DEFAULTS.items():
            block = ensure_label_in_section(block, "【已核实输入】", label, value)
        if current_role_id in {"solution-designer", "implementer", "reviewer", "tester", "knowledge-keeper"}:
            for label, value in BUGFIX_DOWNSTREAM_DEFAULTS.items():
                block = ensure_label_in_section(block, "【已核实输入】", label, value)

    if current_role_id == "solution-designer" and next_role_id == "implementer":
        block = ensure_label_in_section(block, "【调研发现】", "- 用户方案批准：", "待补录")

    return block


def infer_current_stage(frontmatter: dict[str, str], blocks: list[str]) -> str:
    existing = frontmatter.get("workflow_current_stage")
    if existing:
        return existing
    for block in reversed(blocks):
        role_id = infer_role_id(block)
        if role_id:
            return role_id
    return "requirement-analyst"


def infer_work_type(frontmatter: dict[str, str], blocks: list[str], explicit: str | None) -> str:
    if explicit:
        return explicit
    if frontmatter.get("workflow_work_type"):
        return frontmatter["workflow_work_type"]
    for block in blocks:
        if extract_label_value(block, "- 问题类型：") == "bugfix":
            return "bugfix"
    return "feature"


def infer_project_type(frontmatter: dict[str, str], explicit: str | None) -> str:
    if explicit:
        return explicit
    if frontmatter.get("workflow_project_type"):
        return frontmatter["workflow_project_type"]
    return "existing-project"


def flag_for_stage(stage: str, threshold: str) -> str:
    return "1" if STAGE_ORDER.index(stage) >= STAGE_ORDER.index(threshold) else "0"


def infer_solution_approved(blocks: list[str], stage: str, existing: str | None) -> str:
    if existing in {"0", "1"}:
        return existing
    for block in blocks:
        if infer_role_id(block) == "solution-designer" and infer_next_role_id(block, "solution-designer") == "implementer":
            approval = extract_label_value(block, "- 用户方案批准：")
            if approval and approval not in {"否", "无", "待补录", "待确认", "未批准", "0"}:
                return "1"
    return "1" if STAGE_ORDER.index(stage) > STAGE_ORDER.index("solution-designer") else "0"


def infer_pre_chain_verified(blocks: list[str], solution_approved: str, existing: str | None) -> str:
    if existing in {"0", "1"}:
        return existing
    sequence = ["requirement-analyst", "architect", "code-investigator", "solution-designer"]
    roles = [infer_role_id(block) for block in blocks]
    cursor = 0
    for role in roles:
        if role == sequence[cursor]:
            cursor += 1
            if cursor == len(sequence):
                break
    return "1" if cursor == len(sequence) and solution_approved == "1" else "0"


def build_frontmatter(
    frontmatter: dict[str, str],
    requirement_id: str,
    project_type: str,
    work_type: str,
    doc_backfilled: str,
    current_stage: str,
    blocks: list[str],
) -> dict[str, str]:
    data = dict(frontmatter)
    data["requirement_id"] = requirement_id
    data["workflow_project_type"] = project_type
    data["workflow_work_type"] = work_type
    data["workflow_doc_backfilled"] = doc_backfilled
    data["workflow_current_stage"] = current_stage

    solution_approved = infer_solution_approved(blocks, current_stage, data.get("workflow_solution_approved"))
    pre_chain_verified = infer_pre_chain_verified(blocks, solution_approved, data.get("workflow_pre_chain_verified"))
    data["workflow_solution_approved"] = solution_approved
    data["workflow_pre_chain_verified"] = pre_chain_verified
    data["workflow_implementer_passed"] = data.get("workflow_implementer_passed") or flag_for_stage(current_stage, "implementer")
    data["workflow_reviewer_passed"] = data.get("workflow_reviewer_passed") or flag_for_stage(current_stage, "reviewer")
    data["workflow_tester_passed"] = data.get("workflow_tester_passed") or flag_for_stage(current_stage, "tester")
    data["workflow_knowledge_keeper_passed"] = data.get("workflow_knowledge_keeper_passed") or (
        "1" if current_stage in {"knowledge-keeper", "complete"} else "0"
    )
    data["workflow_completion_passed"] = data.get("workflow_completion_passed") or ("1" if current_stage == "complete" else "0")
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description="Upgrade a legacy project document to the current workflow shape.")
    parser.add_argument("--project-doc", required=True)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--project-type", choices=["new-project", "existing-project"])
    parser.add_argument("--work-type", choices=["feature", "bugfix", "task"])
    parser.add_argument("--doc-backfilled", choices=["0", "1"], default="0")
    args = parser.parse_args()

    project_doc = Path(args.project_doc).resolve()
    if not project_doc.exists() or project_doc.is_dir():
        print(f"[FAIL] Invalid project document: {project_doc}")
        return 1

    original = read_text(project_doc)
    frontmatter, body = extract_frontmatter(original)
    blocks = extract_all_handoff_blocks(body)
    if not blocks:
        print("[FAIL] Project document does not contain any handoff blocks.")
        return 1

    requirement_id = derive_requirement_id(frontmatter, blocks, project_doc)
    project_type = infer_project_type(frontmatter, args.project_type)
    work_type = infer_work_type(frontmatter, blocks, args.work_type)

    new_blocks = [
        normalize_block(block, requirement_id, index, work_type)
        for index, block in enumerate(blocks)
    ]
    new_body = replace_blocks(body, new_blocks)
    current_stage = infer_current_stage(frontmatter, new_blocks)
    new_frontmatter = build_frontmatter(
        frontmatter,
        requirement_id,
        project_type,
        work_type,
        args.doc_backfilled,
        current_stage,
        new_blocks,
    )

    upgraded = dump_frontmatter(new_frontmatter) + new_body.lstrip("\n")

    print("[OK] Legacy project document upgrade prepared.")
    print(f"- project document: {project_doc}")
    print(f"- requirement_id: {new_frontmatter['requirement_id']}")
    print(f"- workflow_project_type: {new_frontmatter['workflow_project_type']}")
    print(f"- workflow_work_type: {new_frontmatter['workflow_work_type']}")
    print(f"- workflow_doc_backfilled: {new_frontmatter['workflow_doc_backfilled']}")
    print(f"- workflow_current_stage: {new_frontmatter['workflow_current_stage']}")
    print(f"- blocks upgraded: {len(new_blocks)}")

    if args.write:
        write_text(project_doc, upgraded)
        print("[WRITE] Project document updated in place.")
    else:
        sys.stdout.write("\n")
        sys.stdout.write(upgraded)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
