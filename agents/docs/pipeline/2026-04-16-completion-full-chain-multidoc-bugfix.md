# Completion Full Chain Multi-Doc Bugfix

## Requirement Analyst

【角色结论】
- 本轮需求是 bugfix：修复 completion gate 在多 `--handoff-doc` 调用时仍可回退到 implementer/reviewer/tester/knowledge-keeper 四段 closing chain 的漏洞，并清理规则文档中残留的 closing-chain 旧口径。

【已核实输入】
- 当前角色：需求分析师
- 当前角色标识：requirement-analyst
- 当前交接标识：HO-BUGFIX-COMPLETION-FULL-CHAIN-MULTIDOC-001-RA-001
- 需求标识：BUGFIX-COMPLETION-FULL-CHAIN-MULTIDOC-001
- 项目落点：/Users/senguoyun/code space
- 下一角色标识：architect
- 问题类型：bugfix
- 复现步骤：审查 `agents/scripts/check_workflow_gate.py` 的 `complete` stage 分支，发现只有 `len(handoff_docs) == 1` 时才走完整 8 角色链；多文档时仍落回 `STAGE_EXPECTATIONS["complete"]` 的 4 角色校验。
- 预期结果：completion gate 无论如何调用，都不能只验证 closing chain；规则文档也不再提示 closing-chain-only completion。
- 实际结果：当前代码和文档仍存在旧路径和旧文案。

【调研发现】
- 是否需要外部调研：否。
- 外部调研来源：无。
- 外部调研结论：无。
- 内部证据清单：EVID-IN-2101 -> /Users/senguoyun/code space/agents/scripts/check_workflow_gate.py, EVID-IN-2102 -> /Users/senguoyun/code space/AGENTS.md, EVID-IN-2103 -> /Users/senguoyun/code space/agents/README.md, EVID-IN-2104 -> /Users/senguoyun/code space/agents/skills/ai-pipeline-orchestrator/references/pipeline-contract.md, EVID-IN-2105 -> /Users/senguoyun/code space/agents/scripts/workflow-gate-checklist.md
- 外部证据清单：无。
- 事实清单：FACT-2101 -> 证据摘录：if args.stage == "complete":, FACT-2102 -> 证据摘录：complete stage requires exactly one --handoff-doc containing the full, FACT-2103 -> 证据摘录：Completion must validate one task document containing the full 8-role chain, FACT-2104 -> 证据摘录：The completion gate validates one task document containing the full 8-role chain
- 证据映射：FACT-2101 -> EVID-IN-2101::stage == "complete"::if args.stage == "complete":, FACT-2102 -> EVID-IN-2101::requires exactly one::complete stage requires exactly one --handoff-doc containing the full, FACT-2103 -> EVID-IN-2102::Completion must validate::Completion must validate one task document containing the full 8-role chain, FACT-2104 -> EVID-IN-2103::completion gate validates::The completion gate validates one task document containing the full 8-role chain
- 推断说明：漏洞范围集中在 workflow gate completion 调用策略和规则文案，不涉及业务代码。
- 未验证项：实现后需用多文档 completion 负向用例验证。
- 需要用户确认：否
- 推荐方案：无
- 推荐原因：无
- 主要权衡：无

【交付物】
- 【范围】
  - 修复 `check_workflow_gate.py` completion 多文档旧路径。
  - 清理 `AGENTS.md`、`agents/README.md`、`pipeline-contract.md`、`workflow-gate-checklist.md` 中的 closing-chain 旧口径。
- 【非目标】
  - 不引入外部 ledger。
  - 不重构全部 stage expectation 模型。

【约束】
- 必须保持当前完整 8 角色链校验。
- 修复后 completion gate 应拒绝仅传 4 个 closing handoff docs 的调用。

【校验标准】
- implementer gate 通过后才编码。
- 多文档 completion gate 负向测试应失败并提示完整链要求。
- 单文档完整链 completion gate 应继续通过。

【禁止事项】
- 不把文档更新当作唯一修复。
- 不保留 completion closing-chain-only 调用路径。

【交接给下一个角色】
- 下一角色：架构师【负责确认修复落点和调用策略】
- 下一角色标识：architect
- 可用输入：用户 findings、当前 gate 代码、规则文档。
- 非目标：业务代码变更。
- 完成条件：给出最小结构修复范围。

## Architect

【角色结论】
- 修复落点应集中在 gate 调用策略：completion stage 强制单一任务文档作为完整链来源，拒绝多文档 completion 调用；文档口径统一为完整 8 角色链。这样比支持 8 个分散 handoff docs 更稳，因为当前 workflow 文档和 repair record 都以 task doc 为归档单位。

【已核实输入】
- 当前角色：架构师
- 当前角色标识：architect
- 当前交接标识：HO-BUGFIX-COMPLETION-FULL-CHAIN-MULTIDOC-001-ARCH-001
- 需求标识：BUGFIX-COMPLETION-FULL-CHAIN-MULTIDOC-001
- 项目落点：/Users/senguoyun/code space
- 下一角色标识：code-investigator
- 问题类型：bugfix
- 复现步骤：沿用 Requirement Analyst。
- 预期结果：completion gate 不再接受 4 段 closing chain 多文档模式。
- 实际结果：当前 `complete` stage 仍有多文档旧路径。
- 根因摘要：`complete` 的完整链逻辑只绑定 `len(handoff_docs) == 1` 分支，旧 `STAGE_EXPECTATIONS["complete"]` 仍可被多文档调用触发。
- 回归检查范围：completion stage、quality_targets、错误提示、规则文档。
- 历史数据结构状态：不涉及。
- 迁移脚本要求：不涉及。

【调研发现】
- 是否需要外部调研：否。
- 外部调研来源：无。
- 外部调研结论：无。
- 内部证据清单：EVID-IN-2201 -> /Users/senguoyun/code space/agents/scripts/check_workflow_gate.py, EVID-IN-2202 -> /Users/senguoyun/code space/agents/skills/ai-pipeline-orchestrator/references/pipeline-contract.md
- 外部证据清单：无。
- 事实清单：FACT-2201 -> 证据摘录：FULL_CHAIN_CURRENT_ROLE_IDS = [, FACT-2202 -> 证据摘录：Completion may pass only after the full chain has been validated, FACT-2203 -> 证据摘录：if args.stage == "complete":
- 证据映射：FACT-2201 -> EVID-IN-2201::FULL_CHAIN_CURRENT_ROLE_IDS::FULL_CHAIN_CURRENT_ROLE_IDS = [, FACT-2202 -> EVID-IN-2202::Completion may pass::Completion may pass only after the full chain has been validated, FACT-2203 -> EVID-IN-2201::stage == "complete"::if args.stage == "complete":
- 推断说明：强制 completion 单文档与现有 task-level repair record 设计一致。
- 未验证项：实现后需确认多文档 complete 不再进入旧期望数组。
- 需要用户确认：否
- 推荐方案：无
- 推荐原因：无
- 主要权衡：无

【交付物】
- 【结构方案】
  - 在 `check_workflow_gate.py` 中让 `args.stage == "complete"` 且 `len(handoff_docs) != 1` 直接报错。
  - completion 单文档继续使用 `FULL_CHAIN_CURRENT_ROLE_IDS/FULL_CHAIN_NEXT_ROLE_IDS`。
  - 清理 `closing handoff chain` 相关错误提示和文档旧口径。
- 【影响范围】
  - 影响 completion gate 调用方式。
  - 不影响 implementer/reviewer/tester/knowledge-keeper 单步 stage。

【约束】
- 不支持 4 文档 completion。
- 不新增依赖。

【校验标准】
- 多文档 completion 负向测试失败。
- 单文档完整链 completion 正向测试通过。

【禁止事项】
- 不恢复旧 closing-chain-only 模式。
- 不改变角色顺序。

【交接给下一个角色】
- 下一角色：代码调查员【负责确认具体旧路径和文档残留】
- 下一角色标识：code-investigator
- 可用输入：架构结论、相关文件。
- 非目标：编码。
- 完成条件：列出精确修改点。

## Code Investigator

【角色结论】
- 旧路径明确存在：`complete` 单文档分支设置 `expectations = None`，但多文档时会继续使用 `STAGE_EXPECTATIONS["complete"]` 中的 4 角色数组；同时多处文档仍写着 closing chain。

【已核实输入】
- 当前角色：代码调查员
- 当前角色标识：code-investigator
- 当前交接标识：HO-BUGFIX-COMPLETION-FULL-CHAIN-MULTIDOC-001-CI-001
- 需求标识：BUGFIX-COMPLETION-FULL-CHAIN-MULTIDOC-001
- 项目落点：/Users/senguoyun/code space
- 下一角色标识：solution-designer
- 问题类型：bugfix
- 复现步骤：读取 `check_workflow_gate.py` completion stage 代码和 `rg` 搜索 closing-chain 文案。
- 预期结果：完整链路径应覆盖所有 completion 调用。
- 实际结果：多文档 completion 仍可使用 4 角色 closing chain。
- 根因摘要：旧 `STAGE_EXPECTATIONS["complete"]` 未被移除或屏蔽，多文档 completion 未被拒绝。
- 回归检查范围：`check_workflow_gate.py` lines around completion dispatch；规则文档所有 closing-chain 命中。
- 历史数据结构状态：不涉及。
- 实际数据缺口：不涉及。

【调研发现】
- 是否需要外部调研：否。
- 外部调研来源：无。
- 外部调研结论：无。
- 内部证据清单：EVID-IN-2301 -> /Users/senguoyun/code space/agents/scripts/check_workflow_gate.py, EVID-IN-2302 -> /Users/senguoyun/code space/AGENTS.md, EVID-IN-2303 -> /Users/senguoyun/code space/agents/README.md, EVID-IN-2304 -> /Users/senguoyun/code space/agents/skills/ai-pipeline-orchestrator/references/pipeline-contract.md, EVID-IN-2305 -> /Users/senguoyun/code space/agents/scripts/workflow-gate-checklist.md
- 外部证据清单：无。
- 事实清单：FACT-2301 -> 证据摘录："current_role_ids": ["implementer", "reviewer", "tester", "knowledge-keeper"], FACT-2302 -> 证据摘录：if expectations is not None:, FACT-2303 -> 证据摘录：The completion gate validates one task document containing the full 8-role chain, FACT-2304 -> 证据摘录：Also confirm that the validated full 8-role chain exists in one task document and is ordered
- 证据映射：FACT-2301 -> EVID-IN-2301::knowledge-keeper::"current_role_ids": ["implementer", "reviewer", "tester", "knowledge-keeper"], FACT-2302 -> EVID-IN-2301::expectations is not None::if expectations is not None:, FACT-2303 -> EVID-IN-2303::completion gate validates::The completion gate validates one task document containing the full 8-role chain, FACT-2304 -> EVID-IN-2305::full 8-role chain::Also confirm that the validated full 8-role chain exists in one task document and is ordered
- 推断说明：只改文档不足以阻止旧路径；必须在脚本层拒绝多文档 completion 或改成 8 文档完整链。
- 未验证项：待实现后跑负向命令。
- 需要用户确认：否
- 推荐方案：无
- 推荐原因：无
- 主要权衡：无

【交付物】
- 【精确修改点】
  - `check_workflow_gate.py`：在 completion stage 增加 `len(handoff_docs) != 1` 的 hard fail，并确保不会继续使用 4 段 `STAGE_EXPECTATIONS["complete"]`。
  - `check_workflow_gate.py`：错误信息从 closing handoff chain 改为 full handoff chain。
  - 文档：将 completion closing chain 旧说法全部改成 full 8-role chain。

【约束】
- 不改业务逻辑。
- 不改其他 stage 的正常多文档行为，除 completion 外。

【校验标准】
- `rg` 不再命中旧的 completion closing-chain-only 口径。
- completion 多文档调用失败。

【禁止事项】
- 不用人工约定代替脚本 hard fail。

【交接给下一个角色】
- 下一角色：方案设计师【负责形成可审批修复方案】
- 下一角色标识：solution-designer
- 可用输入：调查结论、用户 findings。
- 非目标：编码。
- 完成条件：输出需用户批准的最小修复方案。

## Solution Designer

【角色结论】
- 推荐方案：completion stage 强制只接受一个任务文档，并且该文档必须包含可重放的完整 8 角色链；同时删除/改写脚本和规则文档中的 closing-chain 旧提示。这是最小且最稳的修复。

【已核实输入】
- 当前角色：方案设计师
- 当前角色标识：solution-designer
- 当前交接标识：HO-BUGFIX-COMPLETION-FULL-CHAIN-MULTIDOC-001-SD-001
- 需求标识：BUGFIX-COMPLETION-FULL-CHAIN-MULTIDOC-001
- 项目落点：/Users/senguoyun/code space
- 下一角色标识：implementer
- 问题类型：bugfix
- 复现步骤：沿用 Code Investigator。
- 预期结果：completion gate 不能再用 4 文档 closing chain 通过。
- 实际结果：待实现。
- 根因摘要：completion 多文档路径没有被完整链逻辑覆盖。
- 回归检查范围：`check_workflow_gate.py`、`AGENTS.md`、`agents/README.md`、`pipeline-contract.md`、`workflow-gate-checklist.md`、当前任务文档 gate。
- 历史数据结构状态：不涉及。
- 数据迁移策略：无需迁移。
- 长期兼容处理结论：不涉及。
- 用户方案批准：已批准，用户回复“批准”。

【调研发现】
- 是否需要外部调研：否。
- 外部调研来源：无。
- 外部调研结论：无。
- 内部证据清单：EVID-IN-2401 -> /Users/senguoyun/code space/agents/scripts/check_workflow_gate.py, EVID-IN-2402 -> /Users/senguoyun/code space/AGENTS.md, EVID-IN-2403 -> /Users/senguoyun/code space/agents/README.md, EVID-IN-2404 -> /Users/senguoyun/code space/agents/scripts/workflow-gate-checklist.md
- 外部证据清单：无。
- 事实清单：FACT-2401 -> 证据摘录：if args.stage == "complete":, FACT-2402 -> 证据摘录：complete stage requires exactly one --handoff-doc containing the full, FACT-2403 -> 证据摘录：Completion must validate one task document containing the full 8-role chain, FACT-2404 -> 证据摘录：The completion gate validates one task document containing the full 8-role chain
- 证据映射：FACT-2401 -> EVID-IN-2401::stage == "complete"::if args.stage == "complete":, FACT-2402 -> EVID-IN-2401::requires exactly one::complete stage requires exactly one --handoff-doc containing the full, FACT-2403 -> EVID-IN-2402::Completion must validate::Completion must validate one task document containing the full 8-role chain, FACT-2404 -> EVID-IN-2403::completion gate validates::The completion gate validates one task document containing the full 8-role chain
- 推断说明：拒绝多文档 completion 比支持 8 个分散文档更符合当前 task-level repair record 和完整任务文档归档模式。
- 未验证项：实现后需跑 implementer/reviewer/tester/complete gates，以及多文档负向测试。
- 需要用户确认：是
- 推荐方案：让 `--stage complete` 只接受一个 `--handoff-doc`；该文档内必须能找到完整 8 角色链。同步清理所有 completion closing-chain 旧文案。
- 推荐原因：直接关闭已发现绕过路径，避免调用者继续传 4 个 closing docs 通过 completion。
- 主要权衡：不再支持分散在多个 handoff doc 的 completion 调用；但这与当前任务文档归档和 repair record 设计一致，约束更清晰。

【交付物】
- 【拟修改文件】
  - `agents/scripts/check_workflow_gate.py`
  - `AGENTS.md`
  - `agents/README.md`
  - `agents/skills/ai-pipeline-orchestrator/references/pipeline-contract.md`
  - `agents/scripts/workflow-gate-checklist.md`
  - 本任务文档
- 【拟验证】
  - implementer gate。
  - Python 语法检查。
  - `--stage complete` 单任务文档正向通过。
  - `--stage complete` 多 `--handoff-doc` 负向失败。
  - `rg` 确认 completion closing-chain 旧口径清理。

【约束】
- 未获用户批准前不编码。
- 不引入外部依赖。
- 不改业务代码。

【校验标准】
- 用户批准后再进入 implementer。
- 修复后 completion 多文档旧路径不可达。

【禁止事项】
- 不保留 4 文档 closing-chain-only completion 入口。
- 不跳过 reviewer/tester/knowledge-keeper。

【交接给下一个角色】
- 下一角色：开发者【负责在批准后实施最小修复】
- 下一角色标识：implementer
- 可用输入：本 solution handoff、用户批准、代码调查事实。
- 非目标：外部审计系统、业务代码变更。
- 完成条件：完成修复并通过验证。

## Implementer

【角色结论】
- 已完成修复：completion stage 现在强制只接受一个 `--handoff-doc`，该文档必须包含完整 8 角色链；多文档 completion 会直接失败，不再落回 4 段旧路径。规则文档中的 completion closing-chain 旧口径已清理。

【已核实输入】
- 当前角色：开发者
- 当前角色标识：implementer
- 当前交接标识：HO-BUGFIX-COMPLETION-FULL-CHAIN-MULTIDOC-001-IMP-001
- 需求标识：BUGFIX-COMPLETION-FULL-CHAIN-MULTIDOC-001
- 项目落点：/Users/senguoyun/code space
- 下一角色标识：reviewer
- 问题类型：bugfix
- 复现步骤：沿用 Code Investigator；重点验证 `--stage complete` 多 `--handoff-doc` 不再使用 4 角色旧路径。
- 预期结果：completion gate 只接受单一完整任务文档；规则文档不再保留 completion closing-chain 旧口径。
- 实际结果：已实现，待 reviewer 审查。
- 根因摘要：completion 多文档路径没有进入 `FULL_CHAIN_CURRENT_ROLE_IDS/FULL_CHAIN_NEXT_ROLE_IDS` 校验，仍会使用旧的 4 角色 stage expectations。
- 回归检查范围：`check_workflow_gate.py` completion dispatch、规则文档 completion 文案、当前 bugfix 任务文档 gate。
- solution-designer handoff：本文档 Solution Designer 小节，用户已批准。
- 当前任务文档：/Users/senguoyun/code space/agents/docs/pipeline/2026-04-16-completion-full-chain-multidoc-bugfix.md
- 历史数据结构状态：不涉及。
- 数据迁移策略：无需迁移。
- 迁移实现状态：不涉及。
- 长期兼容处理结论：不涉及。
- 兼容分支状态：不涉及。

【调研发现】
- 是否需要外部调研：否。
- 外部调研来源：无。
- 外部调研结论：无。
- 内部证据清单：EVID-IN-2501 -> /Users/senguoyun/code space/agents/scripts/check_workflow_gate.py, EVID-IN-2502 -> /Users/senguoyun/code space/AGENTS.md, EVID-IN-2503 -> /Users/senguoyun/code space/agents/README.md, EVID-IN-2504 -> /Users/senguoyun/code space/agents/skills/ai-pipeline-orchestrator/references/pipeline-contract.md, EVID-IN-2505 -> /Users/senguoyun/code space/agents/scripts/workflow-gate-checklist.md
- 外部证据清单：无。
- 事实清单：FACT-2501 -> 证据摘录：if args.stage == "complete":, FACT-2502 -> 证据摘录：complete stage requires exactly one --handoff-doc containing the full, FACT-2503 -> 证据摘录：do not pass only implementer/reviewer/tester/knowledge-keeper handoff docs., FACT-2504 -> 证据摘录：Completion must validate one task document containing the full 8-role chain, FACT-2505 -> 证据摘录：The completion gate validates one task document containing the full 8-role chain
- 证据映射：FACT-2501 -> EVID-IN-2501::stage == "complete"::if args.stage == "complete":, FACT-2502 -> EVID-IN-2501::requires exactly one::complete stage requires exactly one --handoff-doc containing the full, FACT-2503 -> EVID-IN-2501::do not pass only::do not pass only implementer/reviewer/tester/knowledge-keeper handoff docs., FACT-2504 -> EVID-IN-2502::Completion must validate::Completion must validate one task document containing the full 8-role chain, FACT-2505 -> EVID-IN-2503::completion gate validates::The completion gate validates one task document containing the full 8-role chain
- 推断说明：hard fail 多文档 completion 后，旧 4 文档 closing-only 调用路径不可达。
- 未验证项：还需 reviewer 审查、tester 执行多文档负向和单文档正向 completion 验证。
- 需要用户确认：否
- 推荐方案：无
- 推荐原因：无
- 主要权衡：无

【交付物】
- 【代码变更】
  - `check_workflow_gate.py`：`args.stage == "complete"` 时先检查 `len(handoff_docs) == 1`；否则报错并跳过旧 stage expectations。
  - `check_workflow_gate.py`：completion 缺链错误提示改为 full 8-role chain。
  - 规则文档：统一要求 completion 使用一个任务文档里的完整 8 角色链，不接受只传 implementer/reviewer/tester/knowledge-keeper。
- 【验证记录】
  - implementer gate：通过。
  - Python 语法检查：`env PYTHONPYCACHEPREFIX=/tmp/codex-pycache python3 -m py_compile agents/scripts/check_workflow_gate.py` 通过。
  - 规则文档关键词扫描：目标规则文件和 gate 脚本中不再命中 completion closing-chain 旧口径。

【约束】
- 未修改业务代码。
- 未引入外部依赖。
- 未支持分散 8 文档 completion，保持单任务文档归档模型。

【校验标准】
- reviewer gate 通过。
- tester 验证多文档 completion 失败。
- complete gate 使用单任务文档完整链通过。

【禁止事项】
- 不保留 4 文档 completion 旧路径。
- 不把规则文案更新当作唯一修复。

【交接给下一个角色】
- 下一角色：审查者【负责复核旧路径是否完全关闭，规则文档是否一致】
- 下一角色标识：reviewer
- 可用输入：本 implementer handoff、代码 diff、用户 findings。
- 非目标：新增外部审计系统。
- 完成条件：输出审查结论并交给 tester。

## Reviewer

【角色结论】
- 审查结论：通过。completion 多文档旧路径已被 hard fail 关闭，目标规则文件中 completion closing-chain 旧口径已清零；未发现新的阻塞问题。

【已核实输入】
- 当前角色：审查者
- 当前角色标识：reviewer
- 当前交接标识：HO-BUGFIX-COMPLETION-FULL-CHAIN-MULTIDOC-001-REV-001
- 需求标识：BUGFIX-COMPLETION-FULL-CHAIN-MULTIDOC-001
- 项目落点：/Users/senguoyun/code space
- 下一角色标识：tester
- 问题类型：bugfix
- 复现步骤：审查 `git diff`、搜索旧口径关键词、确认 completion stage 分支。
- 预期结果：旧的 4 文档 completion 路径不可达；规则文档不再诱导 closing-chain-only completion。
- 实际结果：符合预期，待 tester 运行正负向命令。
- 根因摘要：completion 多文档路径曾绕过完整 8 角色链校验。
- 回归检查范围：`check_workflow_gate.py` completion dispatch、规则文档 completion 说明。
- implementer handoff：本文档 Implementer 小节。
- 当前任务文档：/Users/senguoyun/code space/agents/docs/pipeline/2026-04-16-completion-full-chain-multidoc-bugfix.md

【调研发现】
- 是否需要外部调研：否。
- 外部调研来源：无。
- 外部调研结论：无。
- 内部证据清单：EVID-IN-2601 -> /Users/senguoyun/code space/agents/scripts/check_workflow_gate.py, EVID-IN-2602 -> /Users/senguoyun/code space/AGENTS.md, EVID-IN-2603 -> /Users/senguoyun/code space/agents/README.md, EVID-IN-2604 -> /Users/senguoyun/code space/agents/skills/ai-pipeline-orchestrator/references/pipeline-contract.md, EVID-IN-2605 -> /Users/senguoyun/code space/agents/scripts/workflow-gate-checklist.md
- 外部证据清单：无。
- 事实清单：FACT-2601 -> 证据摘录：if args.stage == "complete":, FACT-2602 -> 证据摘录：complete stage requires exactly one --handoff-doc containing the full, FACT-2603 -> 证据摘录：Completion must validate one task document containing the full 8-role chain, FACT-2604 -> 证据摘录：The completion gate validates one task document containing the full 8-role chain, FACT-2605 -> 证据摘录：validated full 8-role chain exists in one task document
- 证据映射：FACT-2601 -> EVID-IN-2601::stage == "complete"::if args.stage == "complete":, FACT-2602 -> EVID-IN-2601::requires exactly one::complete stage requires exactly one --handoff-doc containing the full, FACT-2603 -> EVID-IN-2602::Completion must validate::Completion must validate one task document containing the full 8-role chain, FACT-2604 -> EVID-IN-2603::completion gate validates::The completion gate validates one task document containing the full 8-role chain, FACT-2605 -> EVID-IN-2605::full 8-role chain::validated full 8-role chain exists in one task document
- 推断说明：因为 completion 分支在多文档时设置 `expectations = None` 并记录错误，后续旧 `STAGE_EXPECTATIONS["complete"]` 不会继续校验 4 文档。
- 未验证项：还需 tester 执行多文档 completion 负向命令和单文档 completion 正向命令。
- 需要用户确认：否
- 推荐方案：无
- 推荐原因：无
- 主要权衡：无

【交付物】
- 【审查结果】
  - Finding 1：已修复，completion 多文档调用直接失败。
  - Finding 2：已修复，目标规则文件中旧口径关键词扫描无命中。
- 【剩余风险】
  - 历史任务文档中作为问题描述出现的旧词不会清理；本次只清理可执行规则和 gate 脚本。

【约束】
- 未改业务代码。
- 未引入新依赖。

【校验标准】
- tester gate 通过。
- 多文档 completion 负向测试失败。
- 单文档完整链 completion 正向测试通过。

【禁止事项】
- 不跳过测试。
- 不恢复 4 文档 completion。

【交接给下一个角色】
- 下一角色：测试者【负责执行正负向门禁验证】
- 下一角色标识：tester
- 可用输入：reviewer 结论、实现 diff、用户 findings。
- 非目标：新增修复范围。
- 完成条件：输出测试结果并交给 knowledge-keeper。

## Tester

【角色结论】
- 测试结论：通过当前阶段验证。语法检查通过；目标规则文件旧口径扫描无命中；多 `--handoff-doc` completion 调用按预期失败并提示必须使用一个包含完整 8 角色链的任务文档。当前需求自身的 completion 正向验证需在 knowledge-keeper handoff 追加后执行。

【已核实输入】
- 当前角色：测试者
- 当前角色标识：tester
- 当前交接标识：HO-BUGFIX-COMPLETION-FULL-CHAIN-MULTIDOC-001-TEST-001
- 需求标识：BUGFIX-COMPLETION-FULL-CHAIN-MULTIDOC-001
- 项目落点：/Users/senguoyun/code space
- 下一角色标识：knowledge-keeper
- 问题类型：bugfix
- 复现步骤：执行 tester gate、Python 语法检查、旧口径关键词扫描、多文档 completion 负向命令。
- 预期结果：脚本可编译；目标规则文件不含旧口径；多文档 completion 失败；本任务 completion 正向在 knowledge-keeper 后通过。
- 实际结果：前三项通过；本任务 completion 正向待 knowledge-keeper 后执行。
- 根因摘要：completion 多文档路径曾允许 4 角色旧链绕过完整 8 角色链校验。
- 回归检查范围：`check_workflow_gate.py` completion 分支、规则文档 completion 口径、多文档 completion 负向行为。
- 运行时验证：
  - 命令验证：已运行 tester stage gate、`py_compile`、旧口径关键词扫描、多文档 completion 负向命令。
  - 结果：pass。
- 外部依赖验证：
  - 是否涉及外部 API / 浏览器运行时 / 网络请求: 否
  - 成功路径是否已真实验证: 不涉及
  - 成功路径证据: 不涉及
  - 说明：本需求仅修改本地 workflow 脚本和规则文档。
- 未验证原因：
  - 无
- reviewer handoff：本文档 Reviewer 小节。
- 当前任务文档：/Users/senguoyun/code space/agents/docs/pipeline/2026-04-16-completion-full-chain-multidoc-bugfix.md

【调研发现】
- 是否需要外部调研：否。
- 外部调研来源：无。
- 外部调研结论：无。
- 内部证据清单：EVID-IN-2701 -> /Users/senguoyun/code space/agents/scripts/check_workflow_gate.py, EVID-IN-2702 -> /Users/senguoyun/code space/AGENTS.md, EVID-IN-2703 -> /Users/senguoyun/code space/agents/README.md, EVID-IN-2704 -> /Users/senguoyun/code space/agents/scripts/workflow-gate-checklist.md
- 外部证据清单：无。
- 事实清单：FACT-2701 -> 证据摘录：complete stage requires exactly one --handoff-doc containing the full, FACT-2702 -> 证据摘录：do not pass only implementer/reviewer/tester/knowledge-keeper handoff docs., FACT-2703 -> 证据摘录：Completion must validate one task document containing the full 8-role chain, FACT-2704 -> 证据摘录：The completion gate validates one task document containing the full 8-role chain, FACT-2705 -> 证据摘录：validated full 8-role chain exists in one task document
- 证据映射：FACT-2701 -> EVID-IN-2701::requires exactly one::complete stage requires exactly one --handoff-doc containing the full, FACT-2702 -> EVID-IN-2701::do not pass only::do not pass only implementer/reviewer/tester/knowledge-keeper handoff docs., FACT-2703 -> EVID-IN-2702::Completion must validate::Completion must validate one task document containing the full 8-role chain, FACT-2704 -> EVID-IN-2703::completion gate validates::The completion gate validates one task document containing the full 8-role chain, FACT-2705 -> EVID-IN-2704::full 8-role chain::validated full 8-role chain exists in one task document
- 推断说明：负向命令返回失败且错误信息来自新增 hard fail，说明旧多文档 completion 入口已关闭。
- 未验证项：本任务 complete stage 正向验证需 knowledge-keeper handoff 后执行。
- 需要用户确认：否
- 推荐方案：无
- 推荐原因：无
- 主要权衡：无

【交付物】
- 【测试结果】
  - 用例 1：`python3 agents/scripts/check_workflow_gate.py ... --stage tester ...` -> pass。
  - 用例 2：`env PYTHONPYCACHEPREFIX=/tmp/codex-pycache python3 -m py_compile agents/scripts/check_workflow_gate.py` -> pass。
  - 用例 3：旧口径 `rg` 扫描目标规则文件和 gate 脚本 -> pass，无命中。
  - 用例 4：`--stage complete` 传 4 个 `--handoff-doc` -> expected fail，错误提示要求 exactly one full 8-role handoff chain。
- 【未验证项】
  - 当前任务 complete stage 正向验证待 knowledge-keeper handoff 后执行。

【约束】
- 未执行外部服务测试，因为本需求不涉及外部服务。
- 未用历史任务文档作为正向依据，因为历史文档里的旧证据摘录会被当前更严格文案变更影响。

【校验标准】
- knowledge-keeper gate 通过。
- 当前任务 completion gate 通过。

【禁止事项】
- 不把负向测试当成最终 completion 正向。
- 不跳过 knowledge-keeper。

【交接给下一个角色】
- 下一角色：知识归档者【负责归档复盘并运行 completion gate】
- 下一角色标识：knowledge-keeper
- 可用输入：tester 结果、reviewer 结论、用户 findings。
- 非目标：继续扩大代码改动。
- 完成条件：归档完成并通过 completion gate。

## Knowledge Keeper

【角色结论】
- 归档结论：本轮 bugfix 已完成，completion gate 的多文档旧路径被关闭，规则文档口径已统一为“一个任务文档里的完整 8 角色链”。当前任务可以进入 completion gate。

【已核实输入】
- 当前角色：知识归档者
- 当前角色标识：knowledge-keeper
- 当前交接标识：HO-BUGFIX-COMPLETION-FULL-CHAIN-MULTIDOC-001-KK-001
- 需求标识：BUGFIX-COMPLETION-FULL-CHAIN-MULTIDOC-001
- 项目落点：/Users/senguoyun/code space
- 下一角色标识：terminal
- 问题类型：bugfix
- 复现步骤：沿用本任务前序 findings，检查 completion 调用策略和规则文档文案。
- 预期结果：多文档 completion 失败，单任务文档完整 8 角色链 completion 通过；归档记录需求复盘、自审纠错、流程复盘、规则更新状态。
- 实际结果：多文档 completion 负向已通过；当前任务 completion 正向待本步后执行。
- 根因摘要：旧 `STAGE_EXPECTATIONS["complete"]` 在多文档调用时仍可触发，且规则文档残留 closing-chain 旧口径。
- 回归检查范围：completion stage dispatch、错误提示、规则文档 completion 说明、当前任务完整链。
- 修复类型：workflow-repair
- 修复处理：本轮通过脚本 hard fail 和文档统一口径修复多文档 completion 旧路径；未对业务代码做改动。
- tester handoff：本文档 Tester 小节。
- 当前任务文档：/Users/senguoyun/code space/agents/docs/pipeline/2026-04-16-completion-full-chain-multidoc-bugfix.md

【调研发现】
- 是否需要外部调研：否。
- 外部调研来源：无。
- 外部调研结论：无。
- 内部证据清单：EVID-IN-2801 -> /Users/senguoyun/code space/agents/scripts/check_workflow_gate.py, EVID-IN-2802 -> /Users/senguoyun/code space/AGENTS.md, EVID-IN-2803 -> /Users/senguoyun/code space/agents/README.md, EVID-IN-2804 -> /Users/senguoyun/code space/agents/skills/ai-pipeline-orchestrator/references/pipeline-contract.md, EVID-IN-2805 -> /Users/senguoyun/code space/agents/scripts/workflow-gate-checklist.md
- 外部证据清单：无。
- 事实清单：FACT-2801 -> 证据摘录：complete stage requires exactly one --handoff-doc containing the full, FACT-2802 -> 证据摘录：complete stage requires a full 8-role handoff chain from, FACT-2803 -> 证据摘录：Completion must validate one task document containing the full 8-role chain, FACT-2804 -> 证据摘录：The completion gate validates one task document containing the full 8-role chain, FACT-2805 -> 证据摘录：validated full 8-role chain exists in one task document
- 证据映射：FACT-2801 -> EVID-IN-2801::requires exactly one::complete stage requires exactly one --handoff-doc containing the full, FACT-2802 -> EVID-IN-2801::full 8-role handoff chain::complete stage requires a full 8-role handoff chain from, FACT-2803 -> EVID-IN-2802::Completion must validate::Completion must validate one task document containing the full 8-role chain, FACT-2804 -> EVID-IN-2803::completion gate validates::The completion gate validates one task document containing the full 8-role chain, FACT-2805 -> EVID-IN-2805::full 8-role chain::validated full 8-role chain exists in one task document
- 推断说明：completion gate 现在既要求单一任务文档，又要求可重放完整 8 角色链；这与 task-level repair record 设计一致。
- 未验证项：无；本步后执行当前任务 completion gate。
- 需要用户确认：否
- 推荐方案：无
- 推荐原因：无
- 主要权衡：无

【交付物】
- 【需求复盘】
  - 需求复盘结论：已修复 completion 多文档回退到 4 角色 closing-only 校验的问题，并清理了会诱导旧调用方式的规则文档口径。
  - 已完成范围：脚本 hard fail、多文档 completion 拒绝、规则文档统一为完整 8 角色链。
- 【自我审查】
  - 自我审查结论：本轮修复没有扩大到业务代码，修改集中且直接命中用户 findings。
  - 自我纠错项：将残留的“not only closing chain”式表述继续收敛为纯“完整 8 角色链”表述，避免搜索残留和误导。
- 【流程复盘】
  - 流程复盘结论：这次流程再次暴露了“脚本已修一半、文档口径未完全同步”的问题，且 completion 特殊分支在多参数路径上容易留下旧行为。
  - 值得保留的做法：在 reviewer 阶段用关键词扫描确认规则文档口径已统一；用负向命令验证 hard fail。
  - 需要修正或移除的规则：已修正 completion 必须使用一个任务文档中的完整 8 角色链；已移除 completion closing-chain 旧口径。
  - 规则更新状态：已完成。
- 【验证摘要】
  - implementer/reviewer/tester/knowledge-keeper gates：pass。
  - 多文档 completion 负向：pass（预期失败）。
  - 当前任务 completion 正向：待执行。

【约束】
- 未新增外部依赖。
- 未引入外部 ledger。
- 未修改业务代码。

【校验标准】
- 当前任务 completion gate 通过。
- 当前任务完整 8 角色链共享同一 `需求标识` 与 `项目落点`。

【禁止事项】
- 不把归档当成跳过 completion。
- 不恢复 completion 多文档模式。

【交接给下一个角色】
- 下一角色：终端归档【负责运行当前任务 completion gate 并结束本需求】
- 下一角色标识：terminal
- 可用输入：完整任务文档、tester 结果、reviewer 结论。
- 非目标：继续扩大改动。
- 完成条件：completion gate 通过并向用户汇报。

## Repair Record - Completion Evidence Refresh After Full-Chain Replay

- 修复类型：evidence-correction
- 修复处理：completion gate 会重放当前任务文档的完整 8 角色链，前半段 Requirement/Architect/Code Investigator/Solution Designer handoff 中仍保留修复前的旧证据摘录（如 `len(handoff_docs) == 1`、closing-chain 文案）；已统一刷新为当前代码和规则文件里仍可匹配的 `if args.stage == "complete":`、`requires exactly one`、`Completion must validate one task document containing the full 8-role chain` 等摘录。
- 负责角色：knowledge-keeper
- 是否改变需求含义：否
- 是否改变实现行为：否
- 后续验证：重新运行当前任务 completion gate。
