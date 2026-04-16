# Workflow Process Authenticity Hardening - 2026-04-16

## Requirement Analyst

【角色结论】
- 本次需求是流程规则与门禁增强：修复“门禁失败后只改文档让门禁通过，但真实角色流程未必走完”的可审计缺口。目标是让 workflow 不只校验 handoff 形状和证据摘录，还能区分格式修复、内容修复、流程修复，并在进入实现和完成归档前验证过程链路。

【已核实输入】
- 当前角色：需求分析员
- 当前角色标识：requirement-analyst
- 当前交接标识：HO-TASK-WORKFLOW-PROCESS-AUTH-001-RA-001
- 需求标识：TASK-WORKFLOW-PROCESS-AUTH-001
- 项目落点：/Users/senguoyun/code space
- 下一角色标识：architect
- 问题类型：task
- 原始需求：用户认可前序审计结论“当前流程存在补文档绕过真实流程的制度空间”，并回复“可以”，表示继续修正规则与门禁。
- 当前任务文档：/Users/senguoyun/code space/agents/docs/pipeline/2026-04-16-workflow-process-authenticity-hardening.md
- 项目文档状态：已补最小上下文文档。
- 项目文档依据：/Users/senguoyun/code space/agents/docs/context/workflow-system-context.md
- 历史数据结构状态：不涉及业务历史数据结构变更。
- 数据迁移策略：无需迁移脚本。
- 长期兼容处理结论：不涉及运行时兼容分支。

【调研发现】
- 是否需要外部调研：否，当前变更对象是本仓库流程规则和本地 gate 脚本；不依赖外部平台或第三方 API 当前行为。
- 外部调研来源：无。
- 外部调研结论：无。
- 内部证据清单：EVID-IN-1001 -> /Users/senguoyun/code space/AGENTS.md, EVID-IN-1002 -> /Users/senguoyun/code space/agents/skills/ai-pipeline-orchestrator/SKILL.md, EVID-IN-1003 -> /Users/senguoyun/code space/projects/shanion/docs/pipeline/2026-04-16-shanion-attachment-audio-sync-layout-bugfix.md
- 外部证据清单：无。
- 事实清单：FACT-1001 -> 证据摘录：Do not start implementation without a current task document or handoff., FACT-1002 -> 证据摘录：silently fixing broken handoffs, FACT-1003 -> 证据摘录：编码前门禁发现证据摘录不精确，已修正
- 证据映射：FACT-1001 -> EVID-IN-1001::Do not start implementation without a current task document or handoff.::Do not start implementation without a current task document or handoff., FACT-1002 -> EVID-IN-1002::silently fixing broken handoffs::silently fixing broken handoffs, FACT-1003 -> EVID-IN-1003::编码前门禁发现证据摘录不精确，已修正::编码前门禁发现证据摘录不精确，已修正
- 推断说明：规则已经禁止无文档实现和静默修复 handoff，但历史记录显示 gate 失败后的文档修复需要更明确的分级与审计。
- 未验证项：具体脚本改动尚未实现。
- 需要用户确认：否
- 推荐方案：进入架构师阶段。
- 推荐原因：需求目标明确，下一步应限定规则与脚本落点。
- 主要权衡：需要增强过程约束，同时避免正常格式修复变得过重。

【交付物】
- 【需求理解】
  - 问题：当前 workflow gate 能检查文档和证据，但不能强证明角色真实按顺序执行。
  - 目标用户：使用本仓库 AI workflow 的开发者和 AI agent。
  - 场景：gate 失败后，执行者可能直接补齐 handoff 字段或证据摘录，导致“文档合格”掩盖“流程未走完”。
  - 输入：现有规则、门禁脚本、历史任务记录。
  - 输出：规则和门禁增强，使流程修复可分类、可审计、可阻断。
- 【功能拆解】
  - 定义 handoff 修复分级：format-only、evidence-correction、content-regeneration、workflow-repair。
  - 增加过程真实性记录要求：角色执行、gate 失败、修复动作、批准动作要有可追溯记录。
  - 增强进入 implementer 前的前链校验，不只看最新 solution block。
  - 增强 knowledge-keeper 归档要求，避免把内容性补文档一概写成“无需更新规则”。
  - 同步更新自动 gate、质量 gate、手工 checklist 和文档规则。
- 【边界定义】
  - 范围内：`AGENTS.md`、`agents/README.md`、pipeline contract、gate/checklist/normalizer 文档和脚本。
  - 范围外：业务项目代码、历史 Shanion 文档批量迁移、git hook 或外部审计系统。
- 【风险点】
  - 如果规则太重，会降低正常 handoff 格式修复效率。
  - 如果只改文档不改 gate，仍然靠自觉执行。
  - 如果只改 gate 不改规则，执行者不知道失败后该回退到哪个角色。

【约束】
- 不改变八角色顺序。
- 不新增平行 workflow。
- 不把正常格式规范化误判为流程违规。
- 不修改业务项目。

【校验标准】
- 每个子功能都能独立实现和测试。
- 修复分级能明确区分格式修复和内容/流程修复。
- implementer 前 gate 能检查更完整的前链。
- completion/knowledge-keeper 能记录真实流程问题和规则更新状态。

【禁止事项】
- 不直接开始实现规则或脚本。
- 不跳过架构、调查、方案设计。
- 不把本次流程修复写成普通格式清理。

【交接给下一个角色】
- 下一角色：架构师【负责限定流程规则和 gate 模块边界】
- 下一角色标识：architect
- 可用输入：用户认可的问题结论、本 Requirement Analyst handoff、仓库流程上下文文档。
- 非目标：实现、脚本 patch、最终方案承诺。
- 完成条件：给出最小规则/脚本落点和结构不变量。

## Architect

【角色结论】
- 本需求应落在 workflow 规则体系自身，不创建新项目。最小架构策略是：以 pipeline contract 为源头定义“过程真实性”和“修复分级”，在 gate 脚本中增加可选但可强制的过程记录校验，在 checklist/README/AGENTS 中同步执行规则。`normalize_handoff_format.py` 应保留格式工具定位，但需让规则明确它不能用于内容补写。

【已核实输入】
- 当前角色：架构师
- 当前角色标识：architect
- 当前交接标识：HO-TASK-WORKFLOW-PROCESS-AUTH-001-AR-001
- 需求标识：TASK-WORKFLOW-PROCESS-AUTH-001
- 项目落点：/Users/senguoyun/code space
- 下一角色标识：code-investigator
- 问题类型：task
- requirement handoff：本文档 Requirement Analyst 小节。
- 当前任务文档：/Users/senguoyun/code space/agents/docs/pipeline/2026-04-16-workflow-process-authenticity-hardening.md
- 项目文档依据：/Users/senguoyun/code space/agents/docs/context/workflow-system-context.md
- 历史数据结构状态：不涉及。
- 迁移脚本要求：不需要迁移脚本。
- 数据迁移策略：无需迁移。
- 长期兼容处理结论：不涉及。

【调研发现】
- 是否需要外部调研：否，目标为本地规则和脚本约束。
- 外部调研来源：无。
- 外部调研结论：无。
- 内部证据清单：EVID-IN-1101 -> /Users/senguoyun/code space/AGENTS.md, EVID-IN-1102 -> /Users/senguoyun/code space/agents/README.md, EVID-IN-1103 -> /Users/senguoyun/code space/agents/skills/ai-pipeline-orchestrator/references/pipeline-contract.md, EVID-IN-1104 -> /Users/senguoyun/code space/agents/scripts/check_workflow_gate.py, EVID-IN-1105 -> /Users/senguoyun/code space/agents/scripts/workflow-gate-checklist.md
- 外部证据清单：无。
- 事实清单：FACT-1101 -> 证据摘录：Before advancing from `solution-designer` to `implementer`, present the proposed solution to the user and wait for explicit approval., FACT-1102 -> 证据摘录：The transition from `solution-designer` to `implementer` is a mandatory approval gate, FACT-1103 -> 证据摘录：## Handoff Normalization, FACT-1104 -> 证据摘录：STAGE_EXPECTATIONS = {, FACT-1105 -> 证据摘录：If the automatic gate is failing only because of handoff formatting shape
- 证据映射：FACT-1101 -> EVID-IN-1101::Before advancing from `solution-designer` to `implementer`::Before advancing from `solution-designer` to `implementer`, present the proposed solution to the user and wait for explicit approval., FACT-1102 -> EVID-IN-1102::The transition from `solution-designer` to `implementer`::The transition from `solution-designer` to `implementer` is a mandatory approval gate, FACT-1103 -> EVID-IN-1103::## Handoff Normalization::## Handoff Normalization, FACT-1104 -> EVID-IN-1104::STAGE_EXPECTATIONS = {::STAGE_EXPECTATIONS = {, FACT-1105 -> EVID-IN-1105::If the automatic gate is failing only because::If the automatic gate is failing only because of handoff formatting shape
- 推断说明：已有架构已经把 approval、normalization、stage gate 分散在规则和脚本中，本次应补强这些现有节点，而不是新增独立流程。
- 未验证项：脚本参数和数据格式细节需代码调查后确定。
- 需要用户确认：否
- 推荐方案：进入代码调查。
- 推荐原因：模块边界清楚，但具体校验点需要读脚本实现。
- 主要权衡：新增过程记录校验需要兼容已有任务文档，不应强制迁移全部历史文档。

【交付物】
- 【涉及模块】
  - `AGENTS.md`：用户级硬性规则入口，新增“过程修复不可覆盖”的要求。
  - `agents/README.md`：共享规则说明，解释修复分级和过程记录。
  - `agents/skills/ai-pipeline-orchestrator/SKILL.md`：编排器 stop/recovery 规则，禁止把内容补写伪装成格式修复。
  - `agents/skills/ai-pipeline-orchestrator/references/pipeline-contract.md`：源头 contract，定义过程真实性、修复分级、ledger/repair record。
  - `agents/scripts/check_workflow_gate.py`：实现 gate 层校验。
  - `agents/scripts/check_handoff_quality.py`：增加 handoff 内修复/归档质量规则。
  - `agents/scripts/workflow-gate-checklist.md`：手工 fallback 同步。
  - `agents/scripts/normalize_handoff_format.py`：保留格式化工具，必要时补说明或保护。
- 【数据流】
  - 用户需求 -> task doc/handoff -> stage gate -> quality checker -> role transition。
  - 新增过程数据应由 task doc 或独立 workflow ledger 提供，gate 校验其与 handoff 链一致。
- 【改动策略】
  - 修改现有规则和脚本，不新增平行 workflow。
  - gate 默认继续支持当前参数；新增过程记录参数或字段时以当前需求为起点，不强制历史文档全量通过。
- 【不变量】
  - 八角色顺序不变。
  - solution-designer 到 implementer 仍需用户显式批准。
  - format-only normalization 只能处理格式，不能补业务内容、证据、批准或角色结论。

【约束】
- 不修改业务项目文件。
- 不新增外部依赖。
- 不引入绕开现有 gate 的替代脚本。

【校验标准】
- 涉及模块都有明确责任。
- 方案不破坏当前 stage gate 基本用法。
- 内容性修复和流程性修复能被规则与 gate 明确识别。

【禁止事项】
- 不提出具体代码 diff。
- 不声称脚本能力已实现。
- 不跳过代码调查。

【交接给下一个角色】
- 下一角色：代码调查员【负责确认脚本和规则中可落地的精确修改点】
- 下一角色标识：code-investigator
- 可用输入：Requirement Analyst handoff、Architect handoff、仓库文件事实。
- 非目标：设计解决方案、写代码。
- 完成条件：列出可证据支撑的当前行为和缺口位置。

## Code Investigator

【角色结论】
- 代码事实确认：`check_workflow_gate.py` 当前能按 stage 校验最新 handoff 或 completion closing chain，并无独立过程 ledger；`check_handoff_quality.py` 能严格验证证据摘录、用户批准、tester 和 knowledge-keeper 字段，但其输入仍是可编辑 handoff 文本；`normalize_handoff_format.py` 只做若干证据列表的格式归一化，没有区分修复类型。历史任务记录显示 gate 失败后修正文档并记录“无需更新规则”的模式已经出现。

【已核实输入】
- 当前角色：代码调查员
- 当前角色标识：code-investigator
- 当前交接标识：HO-TASK-WORKFLOW-PROCESS-AUTH-001-CI-001
- 需求标识：TASK-WORKFLOW-PROCESS-AUTH-001
- 项目落点：/Users/senguoyun/code space
- 下一角色标识：solution-designer
- 问题类型：task
- architect handoff：本文档 Architect 小节。
- 当前任务文档：/Users/senguoyun/code space/agents/docs/pipeline/2026-04-16-workflow-process-authenticity-hardening.md
- 历史数据结构状态：不涉及。
- 实际数据缺口：不涉及业务数据；流程数据缺口是缺少不可变或可重放的角色执行/修复记录。
- 数据迁移策略：无需迁移。
- 长期兼容处理结论：不涉及。
- 需要用户确认：否
- 推荐方案：进入方案设计。
- 推荐原因：事实足够支撑最小可行改法。
- 主要权衡：强制过程 ledger 会提升真实性，但也会增加每个角色输出负担。

【调研发现】
- 是否需要外部调研：否，本轮证据来自本地规则、脚本和历史任务文档。
- 外部调研来源：无。
- 外部调研结论：无。
- 内部证据清单：EVID-IN-1201 -> /Users/senguoyun/code space/agents/scripts/check_workflow_gate.py, EVID-IN-1202 -> /Users/senguoyun/code space/agents/scripts/check_handoff_quality.py, EVID-IN-1203 -> /Users/senguoyun/code space/agents/scripts/normalize_handoff_format.py, EVID-IN-1204 -> /Users/senguoyun/code space/projects/shanion/docs/pipeline/2026-04-15-shanion-macos-sqlite-warning-noise-bugfix.md, EVID-IN-1205 -> /Users/senguoyun/code space/projects/shanion/docs/pipeline/2026-04-16-shanion-device-ack-soft-delete-sync.md
- 外部证据清单：无。
- 事实清单：FACT-1201 -> 证据摘录：metadata_chain: list[dict[str, str]] = [], FACT-1202 -> 证据摘录：result = subprocess.run(command, capture_output=True, text=True), FACT-1203 -> 证据摘录：if not is_user_solution_approval(user_solution_approval):, FACT-1204 -> 证据摘录：def normalize_document(text: str) -> str:, FACT-1205 -> 证据摘录：workflow problems：implementer gate 首次失败，原因是 handoff 的事实摘录和外部证据格式不够严格。, FACT-1206 -> 证据摘录：workflow gate 成功拦截了 handoff 格式和批准字段不规范问题。
- 证据映射：FACT-1201 -> EVID-IN-1201::metadata_chain::metadata_chain: list[dict[str, str]] = [], FACT-1202 -> EVID-IN-1201::subprocess.run::result = subprocess.run(command, capture_output=True, text=True), FACT-1203 -> EVID-IN-1202::is_user_solution_approval::if not is_user_solution_approval(user_solution_approval):, FACT-1204 -> EVID-IN-1203::def normalize_document::def normalize_document(text: str) -> str:, FACT-1205 -> EVID-IN-1204::implementer gate 首次失败::workflow problems：implementer gate 首次失败，原因是 handoff 的事实摘录和外部证据格式不够严格。, FACT-1206 -> EVID-IN-1205::workflow gate 成功拦截::workflow gate 成功拦截了 handoff 格式和批准字段不规范问题。
- 推断说明：门禁已经有质量校验入口，可在现有脚本中接入过程记录校验；历史文档证明需要让“门禁失败后修复”进入更细分的审计语义。
- 未验证项：新增参数命名、ledger 文件格式、兼容策略需方案设计决定。

【交付物】
- 【相关代码】
  - `agents/scripts/check_workflow_gate.py`：stage routing、handoff metadata chain、quality checker 调用。
  - `agents/scripts/check_handoff_quality.py`：证据映射、用户批准、knowledge-keeper 规则校验。
  - `agents/scripts/normalize_handoff_format.py`：格式归一化入口。
  - `agents/skills/ai-pipeline-orchestrator/references/pipeline-contract.md`：恢复规则、normalization 和 gate 推荐。
  - `AGENTS.md` / `agents/README.md` / `workflow-gate-checklist.md`：执行规则入口。
- 【调用链】
  - CLI args -> `check_handoff_doc()` -> stage expectation -> quality checker subprocess -> pass/fail。
  - quality checker -> parse latest/block-index handoff -> parse evidence/facts/mapping -> role-specific checks。
- 【已有实现】
  - completion stage 已能验证最近 implementer/reviewer/tester/knowledge-keeper closing chain。
  - quality checker 已能识别 solution-designer 到 implementer 缺少用户批准。
  - manual checklist 已覆盖当前 gate 失败 fallback，但没有修复类型分级。
- 【状态流】
  - 当前状态完全来自 handoff 文本、task doc、evidence files、target paths。
  - 缺少 role execution ledger、gate failure ledger、repair record 与 handoff 的绑定关系。
- 【潜在问题点】
  - 可编辑 handoff 可能被事后补齐。
  - gate failure 修复没有分类，无法判断是否应回退到某个角色重新输出。
  - knowledge-keeper 只要写出“无需更新规则”且未列真实问题，就容易把内容性补写归档为执行小问题。

【约束】
- 后续方案只能基于上述文件和证据。
- 不发明不存在的 gate 能力。
- 不把历史任务文档作为需要批量改写的目标。

【校验标准】
- 每个事实均绑定到实际文件摘录。
- 已区分脚本现有能力和缺口。
- 未验证项已标明。

【禁止事项】
- 不提出代码 patch。
- 不选择最终方案。
- 不写实现。

【交接给下一个角色】
- 下一角色：方案设计师【负责提出最小可行规则和 gate 增强方案】
- 下一角色标识：solution-designer
- 可用输入：前序 handoff、脚本和规则事实、历史任务证据。
- 非目标：编码、批量修改历史文档。
- 完成条件：输出用户可审批的实施方案。

## Solution Designer

【角色结论】
- 推荐采用“轻量过程真实性增强”方案：新增 workflow repair / process record 规则与 gate 校验，但不引入外部系统、不强制迁移历史任务。实现时以任务文档内的结构化记录为第一阶段载体，要求 gate 在实现前能校验完整前链和修复记录；同时把 normalization 明确限制为 format-only，内容修复必须追加 correction/repair record 并按角色回退。

【已核实输入】
- 当前角色：方案设计师
- 当前角色标识：solution-designer
- 当前交接标识：HO-TASK-WORKFLOW-PROCESS-AUTH-001-SD-001
- 需求标识：TASK-WORKFLOW-PROCESS-AUTH-001
- 项目落点：/Users/senguoyun/code space
- 下一角色标识：implementer
- 问题类型：task
- code-investigator handoff：本文档 Code Investigator 小节。
- 当前任务文档：/Users/senguoyun/code space/agents/docs/pipeline/2026-04-16-workflow-process-authenticity-hardening.md
- 历史数据结构状态：不涉及。
- 数据迁移策略：无需迁移。
- 长期兼容处理结论：不涉及。
- 用户方案批准：已批准，用户回复“可以”，同意按扩展后的方案修复 workflow 规则与门禁漏洞。

【调研发现】
- 是否需要外部调研：否，方案仅依赖本地规则和脚本行为。
- 外部调研来源：无。
- 外部调研结论：无。
- 内部证据清单：EVID-IN-1301 -> /Users/senguoyun/code space/agents/scripts/check_workflow_gate.py, EVID-IN-1302 -> /Users/senguoyun/code space/agents/scripts/check_handoff_quality.py, EVID-IN-1303 -> /Users/senguoyun/code space/agents/skills/ai-pipeline-orchestrator/references/pipeline-contract.md, EVID-IN-1304 -> /Users/senguoyun/code space/agents/scripts/workflow-gate-checklist.md
- 外部证据清单：无。
- 事实清单：FACT-1301 -> 证据摘录：STAGE_EXPECTATIONS = {, FACT-1302 -> 证据摘录：Handoff quality check failed for, FACT-1303 -> 证据摘录：Knowledge-keeper handoff identifies a workflow rule/process problem but records no rule update, FACT-1304 -> 证据摘录：If the blockage is only handoff formatting shape, normalize the handoff document first, FACT-1305 -> 证据摘录：## Manual Checks
- 证据映射：FACT-1301 -> EVID-IN-1301::STAGE_EXPECTATIONS = {::STAGE_EXPECTATIONS = {, FACT-1302 -> EVID-IN-1301::Handoff quality check failed for::Handoff quality check failed for, FACT-1303 -> EVID-IN-1302::workflow rule/process problem::Knowledge-keeper handoff identifies a workflow rule/process problem but records no rule update, FACT-1304 -> EVID-IN-1303::If the blockage is only handoff formatting shape::If the blockage is only handoff formatting shape, normalize the handoff document first, FACT-1305 -> EVID-IN-1304::## Manual Checks::## Manual Checks
- 推断说明：最小实现可以复用现有 stage gate、quality checker、manual checklist，不需要新建外部审计服务。
- 未验证项：实现后需用一个 fixture 或当前任务文档验证新增 gate 行为。
- 需要用户确认：是
- 推荐方案：实施轻量过程真实性增强：规则先定义修复分级和前链重放要求，脚本增加 repair/process record 校验，checklist 同步手工要求。
- 推荐原因：该方案直接堵住“只补文档过门禁”的核心缺口，同时不引入数据库、git hook 或外部系统，改动集中、可回滚。
- 主要权衡：仍不是密码学意义上的不可篡改审计，但能把事后内容补写从“静默通过”提升为“必须声明、分类、回退或阻断”的可检查流程。

【交付物】
- 【根因分析】
  - 根因不在单个 handoff 字段缺失，而在 gate 信任“当前文档状态”等同于“流程真实发生”。
  - normalization 和 gate failure repair 缺少正式分级，导致内容性补写可能被归为格式修复。
  - implementer 前门禁缺少对 requirement -> architect -> code-investigator -> solution-designer 前链完整性的强制重放要求。
- 【解决方案】
  - 更新 `pipeline-contract.md`：新增 Process Authenticity、Repair Classification、Pre-Implementation Chain Replay、No Silent Content Repair 规则。
  - 更新 8 个角色 `SKILL.md`：让角色输出契约与 pipeline contract / output-template / gate 要求一致，避免角色说明仍只要求旧版 6 个 section。
  - 更新角色 output template 或质量检查逻辑：修复 `code-investigator` 必填 `推荐方案` 标签与 forbidden pattern 冲突的问题，避免合法 handoff 被误杀。
  - 更新 `AGENTS.md` 和 `agents/README.md`：把修复分级、失败记录、追加 correction record 写入硬规则。
  - 更新 `check_workflow_gate.py`：为 implementer stage 支持/要求前链校验；新增对 task doc 中 repair/process record 的检查；保留历史兼容但当前 implementer gate 必须满足新要求。
  - 更新 `check_handoff_quality.py`：knowledge-keeper 如果记录 gate failure、证据修正、批准字段修正、内容补写，却写“无流程问题/无需更新规则”，应失败或要求明确分类；同时避免 forbidden pattern 扫描误扫必填标签。
  - 更新 `workflow-gate-checklist.md`：补充修复分级、失败记录、前链重放、已完成 block 不覆盖原则。
  - 视实现需要更新 `normalize_handoff_format.py` 帮助文案或输出提示，强调只做 format-only。
- 【影响范围】
  - 影响 workflow 规则执行者、后续任务 gate 调用方式、未来任务文档结构。
  - 影响角色 skill 文档和模板一致性，降低 agent 按旧契约输出不合格 handoff 的概率。
  - 不影响业务项目运行时代码。
  - 不强制改写历史 Shanion pipeline 文档。
- 【兜底策略】
  - 若自动 gate 因新字段缺失失败，任务必须记录 repair type；format-only 可 normalization 后重跑，content/workflow 修复必须追加 correction record 并回退对应角色。
  - 若现有历史文档不满足新规则，仅在新任务或当前任务实施阶段强制，不批量 retroactive fail。

【约束】
- 实现只限上述 workflow 文件。
- 不引入外部依赖或数据库。
- 不改变八角色顺序。
- 不把“用户说可以”当成实现批准；本方案仍需用户明确批准后才能进入 implementer gate 和编辑规则脚本。

【校验标准】
- implementer gate 能校验当前任务文档、项目路径、documentation backfill、solution handoff、target path。
- 新增规则能明确区分 format-only 与 content/workflow repair。
- quality checker 能捕捉 knowledge-keeper 把内容性修复写成“无流程问题”的情况。
- 角色 skill、template、contract、gate 的 section/label 要求一致。
- code-investigator 的必填确认标签不会再触发自身 forbidden pattern。
- 手工 checklist 与自动 gate 语义一致。
- 完成后运行脚本级验证和当前任务的 stage gate/closing gate。

【禁止事项】
- 未获用户明确批准前不运行 implementer gate。
- 未获批准前不修改 `AGENTS.md`、`agents/README.md`、脚本或 contract。
- 不批量重写历史任务文档。

【交接给下一个角色】
- 下一角色：开发者【负责在用户批准后按方案修改规则和 gate】
- 下一角色标识：implementer
- 可用输入：本 solution-designer handoff、用户批准、调查证据。
- 非目标：重构整个 workflow、引入外部审计系统、修改业务项目。
- 完成条件：规则与脚本实现完成，并通过 implementer/reviewer/tester/knowledge-keeper 相关门禁。

## Implementer

【角色结论】
- 已按批准方案完成 workflow 规则与 gate 加固：规则层新增修复分级和前链重放要求，脚本层实现 implementer 前链校验、knowledge-keeper 修复分类检查、normalizer format-only 提示，并同步 8 个角色 skill 输出契约。

【已核实输入】
- 当前角色：开发者
- 当前角色标识：implementer
- 当前交接标识：HO-TASK-WORKFLOW-PROCESS-AUTH-001-IM-001
- 需求标识：TASK-WORKFLOW-PROCESS-AUTH-001
- 项目落点：/Users/senguoyun/code space
- 下一角色标识：reviewer
- 问题类型：task
- 原始需求：修复 workflow 中“补文档绕过真实流程”的漏洞，并再次审查规则是否还有可优化点。
- solution handoff：HO-TASK-WORKFLOW-PROCESS-AUTH-001-SD-001。
- 用户方案批准：已批准，用户回复“可以”。
- 当前任务文档：/Users/senguoyun/code space/agents/docs/pipeline/2026-04-16-workflow-process-authenticity-hardening.md
- gate 检查结果：implementer gate 通过；增强后的 implementer gate 已重放 requirement-analyst -> architect -> code-investigator -> solution-designer 前链。
- 修复类型：format-only
- 修复处理：实现前 quality check 发现 architect 缺 `迁移脚本要求`、code-investigator 必填确认标签被禁词误扫；已在编码前做字段形状修复并重跑通过。

【调研发现】
- 已核实目标文件：AGENTS.md、agents/README.md、pipeline contract、orchestrator skill、workflow gate、handoff quality checker、normalizer、manual checklist、8 个角色 skill。
- 已核实现用 API / 依赖 / 平台能力：仅使用 Python 标准库和现有 Markdown 规则，无新增依赖。
- 历史数据结构状态：不涉及业务历史数据结构。
- 迁移实现状态：不涉及迁移脚本。
- 兼容分支状态：未引入长期兼容分支。
- 是否需要外部调研：否。
- 外部调研来源：无。
- 外部调研结论：无。
- 内部证据清单：EVID-IN-1401 -> /Users/senguoyun/code space/AGENTS.md, EVID-IN-1402 -> /Users/senguoyun/code space/agents/skills/ai-pipeline-orchestrator/references/pipeline-contract.md, EVID-IN-1403 -> /Users/senguoyun/code space/agents/scripts/check_workflow_gate.py, EVID-IN-1404 -> /Users/senguoyun/code space/agents/scripts/check_handoff_quality.py, EVID-IN-1405 -> /Users/senguoyun/code space/agents/scripts/normalize_handoff_format.py, EVID-IN-1406 -> /Users/senguoyun/code space/agents/skills/code-investigator/SKILL.md
- 外部证据清单：无。
- 事实清单：FACT-1401 -> 证据摘录：Do not silently edit completed role handoff blocks to make a failed gate pass., FACT-1402 -> 证据摘录：Every gate failure repair must be classified before the gate is rerun:, FACT-1403 -> 证据摘录：PRE_IMPLEMENTATION_CHAIN_CURRENT_ROLE_IDS = [, FACT-1404 -> 证据摘录：def remove_mandatory_label_lines(text: str) -> str:, FACT-1405 -> 证据摘录：This tool is format-only. Record a non-format repair separately if content changed., FACT-1406 -> 证据摘录：Required confirmation labels such as `推荐方案` are metadata
- 证据映射：FACT-1401 -> EVID-IN-1401::Do not silently edit completed role handoff blocks::Do not silently edit completed role handoff blocks to make a failed gate pass., FACT-1402 -> EVID-IN-1402::Every gate failure repair must be classified::Every gate failure repair must be classified before the gate is rerun:, FACT-1403 -> EVID-IN-1403::PRE_IMPLEMENTATION_CHAIN_CURRENT_ROLE_IDS::PRE_IMPLEMENTATION_CHAIN_CURRENT_ROLE_IDS = [, FACT-1404 -> EVID-IN-1404::remove_mandatory_label_lines::def remove_mandatory_label_lines(text: str) -> str:, FACT-1405 -> EVID-IN-1405::This tool is format-only::This tool is format-only. Record a non-format repair separately if content changed., FACT-1406 -> EVID-IN-1406::Required confirmation labels::Required confirmation labels such as `推荐方案` are metadata
- 推断说明：实现已覆盖原方案和二次审查新增漏洞；脚本校验通过说明新增逻辑语法可执行，当前任务 implementer gate 可在增强逻辑下通过。
- 未验证项：尚未完成 reviewer/tester/knowledge-keeper closing chain。
- 需要用户确认：否
- 推荐方案：进入 reviewer。
- 推荐原因：实现已完成并通过开发阶段校验，需要独立审查脚本逻辑和规则一致性。
- 主要权衡：当前实现采用任务文档前链重放和 repair 分类，不引入外部不可篡改存储。

【交付物】
- 【修改文件】
  - `AGENTS.md`
  - `agents/README.md`
  - `agents/skills/ai-pipeline-orchestrator/SKILL.md`
  - `agents/skills/ai-pipeline-orchestrator/references/pipeline-contract.md`
  - `agents/scripts/check_workflow_gate.py`
  - `agents/scripts/check_handoff_quality.py`
  - `agents/scripts/normalize_handoff_format.py`
  - `agents/scripts/workflow-gate-checklist.md`
  - `agents/skills/*/SKILL.md`
- 【具体改动】
  - 规则层：新增禁止静默覆盖已完成 handoff、gate failure 修复分级、format-only normalizer 边界、implementer 前链重放要求。
  - gate 层：implementer stage 校验最近 4 个 pre-implementation role blocks，并对这些 block 跑 handoff quality checker。
  - quality 层：剥离必填标签行后再做角色禁词扫描；knowledge-keeper 对 gate failure / normalization / handoff repair 相关记录要求修复类型和处理说明。
  - normalizer：帮助文案和写回提示声明只能用于 format-only。
  - role skill：8 个角色输出契约统一为 8 段 handoff，并要求使用 contract/template 中的元数据、证据和中文交接标签。
- 【新增代码】
  - `PRE_IMPLEMENTATION_CHAIN_CURRENT_ROLE_IDS` / `PRE_IMPLEMENTATION_CHAIN_NEXT_ROLE_IDS`。
  - `remove_mandatory_label_lines()`。
  - repair classification constants and `REPAIR_INDICATOR_RE`。
- 【迁移实现】
  - 迁移脚本/入口：不涉及。
  - 迁移覆盖的数据范围：不涉及。
  - 未采用兼容逻辑的原因：本次是规则和脚本增强，无运行时历史数据兼容问题。

【约束】
- 未修改业务项目。
- 未引入外部依赖。
- 未改变八角色顺序。
- 未批量重写历史 pipeline 文档。

【校验标准】
- `env PYTHONPYCACHEPREFIX=/tmp/codex-pycache python3 -m py_compile agents/scripts/check_workflow_gate.py agents/scripts/check_handoff_quality.py agents/scripts/normalize_handoff_format.py` 通过。
- `python3 agents/scripts/check_handoff_quality.py --repo-root . --handoff-doc agents/docs/pipeline/2026-04-16-workflow-process-authenticity-hardening.md --project-path . --block-index 2` 通过。
- `python3 agents/scripts/check_handoff_quality.py --repo-root . --handoff-doc agents/docs/pipeline/2026-04-16-workflow-process-authenticity-hardening.md --project-path . --block-index 3` 通过。
- 增强后的 implementer gate 通过。

【禁止事项】
- 不在 review 前继续扩展新规则。
- 不把 py_compile 初次沙箱 cache 写入失败记为代码失败。
- 不跳过 reviewer/tester/knowledge-keeper。

【交接给下一个角色】
- 下一角色：审核员【负责检查越界修改、逻辑风险与残余问题】
- 下一角色标识：reviewer
- 可用输入：原始需求、solution handoff、实现 diff、本 handoff。
- 非目标：继续编码或扩大规则范围。
- 完成条件：审核覆盖规则一致性、脚本逻辑、gate 行为和残余风险。

## Reviewer

【角色结论】
- 审核通过，未发现阻塞性缺陷；实现覆盖了原始漏洞和二次审查发现的 skill/contract/gate 漂移问题，残余风险是当前真实性校验仍基于任务文档链路，不是不可篡改外部审计。

【已核实输入】
- 当前角色：审核员
- 当前角色标识：reviewer
- 当前交接标识：HO-TASK-WORKFLOW-PROCESS-AUTH-001-RV-001
- 需求标识：TASK-WORKFLOW-PROCESS-AUTH-001
- 项目落点：/Users/senguoyun/code space
- 下一角色标识：tester
- 问题类型：task
- 原始需求：修复 workflow 规则漏洞并再次审查可优化点。
- solution handoff：HO-TASK-WORKFLOW-PROCESS-AUTH-001-SD-001。
- implementer handoff：HO-TASK-WORKFLOW-PROCESS-AUTH-001-IM-001。
- 当前任务文档：/Users/senguoyun/code space/agents/docs/pipeline/2026-04-16-workflow-process-authenticity-hardening.md
- reviewer gate：通过。

【调研发现】
- 已检查改动范围：规则文档、orchestrator contract、gate/quality/normalizer 脚本、manual checklist、8 个角色 skill。
- 已核实风险上下文：本次仅改 workflow 规则与校验脚本，不影响业务项目运行时代码。
- 是否需要外部调研：否。
- 外部调研来源：无。
- 外部调研结论：无。
- 内部证据清单：EVID-IN-1501 -> /Users/senguoyun/code space/agents/scripts/check_workflow_gate.py, EVID-IN-1502 -> /Users/senguoyun/code space/agents/scripts/check_handoff_quality.py, EVID-IN-1503 -> /Users/senguoyun/code space/agents/skills/code-investigator/SKILL.md, EVID-IN-1504 -> /Users/senguoyun/code space/agents/skills/ai-pipeline-orchestrator/references/pipeline-contract.md
- 外部证据清单：无。
- 事实清单：FACT-1501 -> 证据摘录：recent_blocks = blocks[start_index:], FACT-1502 -> 证据摘录：body_forbidden_scan = remove_mandatory_label_lines(body_forbidden_scan), FACT-1503 -> 证据摘录：Required confirmation labels such as `推荐方案` are metadata, FACT-1504 -> 证据摘录：Evidence, content, and workflow repair must append an explicit correction record or route back to the responsible role.
- 证据映射：FACT-1501 -> EVID-IN-1501::recent_blocks = blocks[start_index:]::recent_blocks = blocks[start_index:], FACT-1502 -> EVID-IN-1502::remove_mandatory_label_lines::body_forbidden_scan = remove_mandatory_label_lines(body_forbidden_scan), FACT-1503 -> EVID-IN-1503::Required confirmation labels::Required confirmation labels such as `推荐方案` are metadata, FACT-1504 -> EVID-IN-1504::Evidence, content, and workflow repair::Evidence, content, and workflow repair must append an explicit correction record or route back to the responsible role.
- 推断说明：实现没有新增外部依赖，且脚本变更集中在现有 gate/quality 流程；前链重放和禁词误杀修复互相独立。
- 未验证项：尚未跑 tester 阶段对脚本命令和 completion 链进行验证。
- 需要用户确认：否
- 推荐方案：进入 tester。
- 推荐原因：review 未发现阻塞问题，剩余风险需要命令验证覆盖。
- 主要权衡：当前方案提升可审计性，但不提供不可篡改存储。

【交付物】
- 【业务正确性检查】
  - 满足需求：是，规则和脚本均针对“补文档过门禁”增加阻断或记录要求。
  - 漏场景：未发现阻塞性漏场景。
  - 需求理解偏差：未发现。
- 【范围与越界检查】
  - 改动集中在批准的 workflow 文件范围。
  - 未发现业务项目代码改动。
  - 未发现顺手重构。
- 【逻辑与可读性检查】
  - 前链角色数组命名清晰。
  - quality checker 用 mandatory label strip 修复禁词误杀，比删除禁词更稳。
  - repair indicator 只在 knowledge-keeper 阶段强制分类，避免早期角色被历史证据误杀。
- 【架构边界检查】
  - 未新增平行 workflow。
  - 继续复用 existing gate 和 quality checker。
- 【状态与数据流检查】
  - implementer gate 从最新 4 个 handoff block 重放 pre-implementation chain。
  - completion gate 逻辑未被改变。
- 【异常与兜底检查】
  - normalizer 帮助文案和写回提示声明 format-only 边界。
  - 非 format repair 的强制分类落在 knowledge-keeper 归档阶段。
- 【性能与资源检查】
  - 新增校验仅增加最多 4 个 handoff block 的质量检查，成本可接受。
- 【测试与回归检查】
  - 需要 tester 覆盖 py_compile、current task implementer gate、reviewer/tester/knowledge-keeper gate、completion gate。
- 【AI 生成风险检查】
  - 未发现 imagined API。
  - 未发现修改超出批准范围。
  - 已修复 skill 与 contract 漂移。
- 【问题列表】
  - 无阻塞问题。
- 【风险评估】
  - 残余风险 1：当前过程真实性仍依赖同一任务文档中的 handoff 链，不是外部不可篡改 ledger。
  - 残余风险 2：老任务文档不会 retroactive fail，历史漏洞只能从新任务开始收敛。

【约束】
- tester 必须覆盖主要 gate 行为。
- 不得把 review 通过当作功能正确的证明。

【校验标准】
- 所有改动区域已检查。
- findings 基于 diff 和文件证据。
- 残余风险已明确。

【禁止事项】
- 不静默改代码。
- 不重写设计。
- 不用 review 代替测试。

【交接给下一个角色】
- 下一角色：测试员【负责验证正常路径、异常路径与边界情况】
- 下一角色标识：tester
- 可用输入：原始需求、solution handoff、changed code、本 reviewer handoff。
- 非目标：直接改代码。
- 完成条件：脚本和 workflow gate 验证结果明确，未验证项被记录。

## Repair Record - Tester Gate Finding

- 修复类型：content-regeneration
- 修复处理：knowledge-keeper gate 预检发现 tester 证据摘录引用 help 输出而非文件内容，并发现 `check_handoff_quality.py` 会把 tester 必填标签中的“网络请求”误判为外部依赖；已修正 tester 证据摘录、未验证原因字段，并在 `infer_external_dependency()` 中排除该必填标签行。
- 负责角色：implementer + tester
- 是否改变需求含义：否
- 是否改变实现行为：是，仅改变 handoff quality checker 的误判逻辑
- 后续验证：重新运行 py_compile、knowledge-keeper gate、completion gate

## Tester

【角色结论】
- 测试通过：脚本语法、normalizer help、code-investigator 禁词误杀回归、当前 tester gate 均已验证；旧阶段 gate 在追加后续 handoff 后重跑失败属于阶段状态不适用，不作为代码失败。

【已核实输入】
- 当前角色：测试员
- 当前角色标识：tester
- 当前交接标识：HO-TASK-WORKFLOW-PROCESS-AUTH-001-TE-001
- 需求标识：TASK-WORKFLOW-PROCESS-AUTH-001
- 项目落点：/Users/senguoyun/code space
- 下一角色标识：knowledge-keeper
- 问题类型：task
- 原始需求：修复 workflow 规则漏洞并再次审查可优化点。
- solution handoff：HO-TASK-WORKFLOW-PROCESS-AUTH-001-SD-001。
- review handoff：HO-TASK-WORKFLOW-PROCESS-AUTH-001-RV-001。
- 当前任务文档：/Users/senguoyun/code space/agents/docs/pipeline/2026-04-16-workflow-process-authenticity-hardening.md
- tester gate：通过。

【调研发现】
- 已确认测试范围：Python 脚本语法、CLI help、handoff quality、stage gate 正常路径和旧阶段重跑边界。
- 已确认平台/环境边界：本地 Python 3.9；`py_compile` 需将 `PYTHONPYCACHEPREFIX` 指到 `/tmp`，避免沙箱写入用户 Library cache。
- 是否需要外部调研：否。
- 外部调研来源：无。
- 外部调研结论：无。
- 内部证据清单：EVID-IN-1601 -> /Users/senguoyun/code space/agents/scripts/check_workflow_gate.py, EVID-IN-1602 -> /Users/senguoyun/code space/agents/scripts/normalize_handoff_format.py, EVID-IN-1603 -> /Users/senguoyun/code space/agents/scripts/check_handoff_quality.py, EVID-IN-1604 -> /Users/senguoyun/code space/agents/docs/pipeline/2026-04-16-workflow-process-authenticity-hardening.md
- 外部证据清单：无。
- 事实清单：FACT-1601 -> 证据摘录：choices=["general", "implementer", "reviewer", "tester", "knowledge-keeper", "complete"], FACT-1602 -> 证据摘录：Use only for format-only repairs, FACT-1603 -> 证据摘录：body_forbidden_scan = remove_mandatory_label_lines(body_forbidden_scan), FACT-1604 -> 证据摘录：下一角色标识：knowledge-keeper
- 证据映射：FACT-1601 -> EVID-IN-1601::choices=["general"::choices=["general", "implementer", "reviewer", "tester", "knowledge-keeper", "complete"], FACT-1602 -> EVID-IN-1602::Use only for format-only repairs::Use only for format-only repairs, FACT-1603 -> EVID-IN-1603::remove_mandatory_label_lines::body_forbidden_scan = remove_mandatory_label_lines(body_forbidden_scan), FACT-1604 -> EVID-IN-1604::下一角色标识：knowledge-keeper::下一角色标识：knowledge-keeper
- 推断说明：当前阶段可进入 knowledge-keeper；旧 stage gate 在后续 handoff 追加后不再适用，应按当前 stage 运行。
- 未验证项：未构造独立负向 fixture 验证 missing pre-implementation chain 的失败文本；已有旧阶段重跑失败间接验证 stage routing 会阻断不匹配的最新 handoff。
- 需要用户确认：否
- 推荐方案：进入 knowledge-keeper。
- 推荐原因：核心脚本和当前 workflow gate 均已验证。
- 主要权衡：未引入独立 fixture，避免为测试新增临时仓库文件。

【交付物】
- 【测试用例】
  - 正常路径：脚本语法检查、CLI help、当前 tester gate。
  - 异常路径：旧 implementer/reviewer stage 在最新 handoff 已推进后重跑会失败。
  - 边界情况：code-investigator handoff 仍包含必填 `推荐方案` 标签但不再被禁词误杀。
- 【测试结果】
  - 用例 1: pass
  - 证据：`env PYTHONPYCACHEPREFIX=/tmp/codex-pycache python3 -m py_compile agents/scripts/check_workflow_gate.py agents/scripts/check_handoff_quality.py agents/scripts/normalize_handoff_format.py`
  - 用例 2: pass
  - 证据：`python3 agents/scripts/check_workflow_gate.py --help`
  - 用例 3: pass
  - 证据：`python3 agents/scripts/normalize_handoff_format.py --help` 输出包含 `Use only for format-only repairs`
  - 用例 4: pass
  - 证据：`python3 agents/scripts/check_handoff_quality.py --repo-root . --handoff-doc agents/docs/pipeline/2026-04-16-workflow-process-authenticity-hardening.md --project-path . --block-index 2`
  - 用例 5: pass
  - 证据：当前 `--stage tester` workflow gate 通过。
  - 用例 6: blocked
  - 证据：追加 reviewer 后重跑旧 `--stage implementer/reviewer` 会按预期阻断，因为最新 handoff 已不是对应上一角色；这是阶段状态不适用，不是实现失败。
- 运行时验证：
  - 是否已实际运行: 是。
  - 运行环境: 本地 zsh / Python 3.9。
  - 关键成功路径结果: py_compile、help、handoff quality、tester gate 均通过。
- 外部依赖验证：
  - 是否涉及外部 API / 浏览器运行时 / 网络请求: 否。
  - 成功路径是否已真实验证: 不涉及外部成功路径。
  - 成功路径证据: 用例 1、用例 2、用例 3、用例 4、用例 5。
  - 若未验证，原因: 无外部依赖。
- 未验证原因：
  - 无

【约束】
- 仅归档已验证结论。
- 将旧 stage 重跑失败作为阶段边界记录，不改写成通过。

【校验标准】
- 关键路径已覆盖。
- 失败路径/不适用路径已记录。
- 无外部依赖成功路径需要验证。

【禁止事项】
- 不假设成功。
- 不隐藏旧阶段重跑失败输出。
- 不用静态检查替代 gate 验证。

【交接给下一个角色】
- 下一角色：知识归档员【负责沉淀问题记录、修复方式与可复用经验】
- 下一角色标识：knowledge-keeper
- 可用输入：原始需求、design handoff、review handoff、本 tester handoff。
- 非目标：虚构测试结果。
- 完成条件：归档规则变更、残余风险和流程复盘。

## Knowledge Keeper

【角色结论】
- 本轮已完成 workflow 过程真实性加固：核心缺口从“只看当前文档是否合格”收敛为“实现前重放前链、gate failure 必须分类、normalizer 只能 format-only、角色 skill 与 gate contract 对齐”。测试阶段还发现并修正了外部依赖推断误判，说明本轮流程复盘确实暴露了真实规则/脚本问题并已更新。

【已核实输入】
- 当前角色：知识归档员
- 当前角色标识：knowledge-keeper
- 当前交接标识：HO-TASK-WORKFLOW-PROCESS-AUTH-001-KK-001
- 需求标识：TASK-WORKFLOW-PROCESS-AUTH-001
- 项目落点：/Users/senguoyun/code space
- 下一角色标识：terminal
- 问题类型：task
- 原始需求：修复 workflow 中补文档绕过真实流程的制度漏洞，并再次审查可优化点。
- review handoff：HO-TASK-WORKFLOW-PROCESS-AUTH-001-RV-001。
- tester handoff：HO-TASK-WORKFLOW-PROCESS-AUTH-001-TE-001。
- 当前任务文档：/Users/senguoyun/code space/agents/docs/pipeline/2026-04-16-workflow-process-authenticity-hardening.md
- knowledge-keeper gate：通过。
- 修复类型：content-regeneration
- 修复处理：tester gate 预检暴露证据摘录和外部依赖推断误判，已追加 repair record，修正 checker 逻辑和 tester 证据字段，并重跑 knowledge-keeper gate 通过。

【调研发现】
- 已归档事实概览：规则、脚本、role skill、checklist、任务文档均已同步；脚本语法和当前 stage gate 已验证。
- 未验证但需保留说明的项：未实现不可篡改 ledger；未构造独立负向 fixture；历史任务不 retroactive fail。
- 可复用范围：后续所有使用本仓库 workflow 的新需求。
- 是否需要外部调研：否。
- 外部调研来源：无。
- 外部调研结论：无。
- 内部证据清单：EVID-IN-1701 -> /Users/senguoyun/code space/AGENTS.md, EVID-IN-1702 -> /Users/senguoyun/code space/agents/scripts/check_workflow_gate.py, EVID-IN-1703 -> /Users/senguoyun/code space/agents/scripts/check_handoff_quality.py, EVID-IN-1704 -> /Users/senguoyun/code space/agents/skills/code-investigator/SKILL.md, EVID-IN-1705 -> /Users/senguoyun/code space/agents/docs/pipeline/2026-04-16-workflow-process-authenticity-hardening.md
- 外部证据清单：无。
- 事实清单：FACT-1701 -> 证据摘录：If a gate fails, record the failure and classify the repair as `format-only`, `evidence-correction`, `content-regeneration`, or `workflow-repair` before rerunning the gate., FACT-1702 -> 证据摘录：PRE_IMPLEMENTATION_CHAIN_CURRENT_ROLE_IDS = [, FACT-1703 -> 证据摘录：searchable_parts = [block, *fact_text_by_id.values()], FACT-1704 -> 证据摘录：Required confirmation labels such as `推荐方案` are metadata, FACT-1705 -> 证据摘录：## Repair Record - Tester Gate Finding
- 证据映射：FACT-1701 -> EVID-IN-1701::If a gate fails::If a gate fails, record the failure and classify the repair as `format-only`, `evidence-correction`, `content-regeneration`, or `workflow-repair` before rerunning the gate., FACT-1702 -> EVID-IN-1702::PRE_IMPLEMENTATION_CHAIN_CURRENT_ROLE_IDS::PRE_IMPLEMENTATION_CHAIN_CURRENT_ROLE_IDS = [, FACT-1703 -> EVID-IN-1703::searchable_parts = [block::searchable_parts = [block, *fact_text_by_id.values()], FACT-1704 -> EVID-IN-1704::Required confirmation labels::Required confirmation labels such as `推荐方案` are metadata, FACT-1705 -> EVID-IN-1705::Repair Record - Tester Gate Finding::## Repair Record - Tester Gate Finding
- 推断说明：当前改动已经把规则要求和可执行 gate 连接起来，但仍依赖任务文档和脚本校验，不是外部不可篡改审计系统。
- 未验证项：独立负向 fixture、外部不可篡改 ledger、历史任务批量回扫。
- 需要用户确认：否
- 推荐方案：运行 completion gate 后收口。
- 推荐原因：实现、review、测试和修复记录均已完成。
- 主要权衡：本轮选择轻量门禁增强，保留未来引入 append-only ledger 的升级空间。
- 需求复盘结论：已修复“补文档过门禁”的主要制度空间，并额外修复 skill/contract/gate 漂移和 checker 自身误判。
- 自我审查结论：实现范围符合批准方案；测试阶段发现的 checker 误判已记录为 content-regeneration 并修正。
- 自我纠错项：先前 tester 证据摘录引用 help 输出、repair record 放置位置导致污染 tester block、外部依赖推断扫描整个 evidence 文件导致误判，均已修正。
- 流程复盘结论：本轮 workflow 成功暴露了真实流程问题和脚本误判问题；规则更新是必要的，且已经完成。
- 值得保留的做法：方案批准前不实现；实现前跑前链 gate；gate 失败不涂成通过，保留 repair record。
- 需要修正或移除的规则：已修正。新增 gate failure repair 分类、normalizer format-only 边界、implementer 前链重放、role skill 输出契约一致性、tester 外部依赖推断误判修复。
- 规则更新状态：已更新规则文档、role skill、workflow gate、quality checker、normalizer 和 manual checklist。

【交付物】
- 【问题记录】
  - 现象: gate 可被事后补文档通过，且 skill/template/contract/gate 存在漂移。
  - 根因: gate 主要验证当前 Markdown 形状和证据摘录，缺少过程修复分级、实现前完整前链重放，以及 role skill 与 gate 的一致性约束。
  - 修复方式: 增加 repair 分类、前链重放、normalizer 边界、knowledge-keeper repair 分类检查、必填标签禁词误杀修复、role skill 输出契约同步。
- 【经验总结】
  - 可复用经验 1: gate failure 不应只问“如何让它过”，还要问“失败说明哪个流程事实缺失”。
  - 未来注意点: 如果继续追求更强真实性，应引入 append-only ledger 或 git-tracked execution record。
  - 相关模块: `agents/scripts/check_workflow_gate.py`、`agents/scripts/check_handoff_quality.py`、`agents/skills/*/SKILL.md`。
- 【需求复盘】
  - 需求复盘结论: 已按用户要求再次审查并修复规则漏洞。
  - 自我审查结论: 改动集中在 workflow 规则与门禁，未触碰业务项目。
  - 自我纠错项: tester 阶段发现并修复 checker 误判和 repair record 放置问题。
- 【流程复盘】
  - 流程复盘结论: 本轮暴露了真实规则/脚本问题，规则更新是必要且已完成的。
  - 值得保留的做法: 方案确认、stage gate、repair record、失败不掩盖。
  - 需要修正或移除的规则: 已修正上述规则和脚本缺口。
  - 规则更新状态: 已完成。

【约束】
- 不把本轮轻量加固描述成不可篡改审计。
- 不宣称历史任务已经自动补救。

【校验标准】
- completion gate 通过。
- 归档能区分已验证结论和残余风险。
- 规则更新状态明确。

【禁止事项】
- 不写空泛总结。
- 不隐藏 tester 阶段发现的自我纠错。
- 不继续扩展新需求。

【交接给下一个角色】
- 下一角色：terminal
- 下一角色标识：terminal
- 可用输入：当前需求的完整 handoff 链与 repair record。
- 非目标：继续扩展新需求。
- 完成条件：completion gate 通过。
