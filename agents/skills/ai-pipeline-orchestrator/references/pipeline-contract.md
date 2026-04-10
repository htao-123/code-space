# Pipeline Contract

This document defines the shared contract across the 8 role skills.

## Role Order

1. `requirement-analyst`
2. `architect`
3. `code-investigator`
4. `solution-designer`
5. `implementer`
6. `reviewer`
7. `tester`
8. `knowledge-keeper`

No role may skip forward.
No role may merge with another role.
No agent may replace this workflow with a self-invented process.
No agent may decide that the workflow is optional just because the task feels simple.
No new project or substantial subproject may be scattered across repository root when it should live in a dedicated folder.
No implementation may begin until the current task is documented in a handoff or task document.
No agent should pause for redundant confirmation when the next workflow step is already determined by the current handoff state.
Every requirement must run through the full workflow until `knowledge-keeper`, unless the user explicitly abandons the workflow.
User-facing workflow communication should use Chinese role names and Chinese progression language.
For roles 2-8, research is mandatory before formal output.
If an existing project lacks usable documentation, minimum documentation backfill is mandatory before normal development continues.

## Mandatory Handoff Shape

Every role output must contain:

```md
【角色结论】
【已核实输入】
【调研发现】
【交付物】
【约束】
【校验标准】
【禁止事项】
【交接给下一个角色】
```

If any heading is missing, the handoff is incomplete and the pipeline must stop.

Inside `【交接给下一个角色】`, use Chinese labels:

```md
- 下一角色：角色中文名【该角色职责说明】
- 可用输入：
- 非目标：
- 完成条件：
```

## Allowed Transition Table

| Current role | Next role |
| --- | --- |
| `requirement-analyst` | `architect` |
| `architect` | `code-investigator` |
| `code-investigator` | `solution-designer` |
| `solution-designer` | `implementer` |
| `implementer` | `reviewer` |
| `reviewer` | `tester` |
| `tester` | `knowledge-keeper` |
| `knowledge-keeper` | terminal |

## Input Discipline

The next role may use only:

- the original user request
- the latest valid handoff
- repository facts explicitly allowed by that role

The next role may not:

- import assumptions from older incomplete drafts
- bypass prior constraints
- invent missing evidence
- invent a shortcut workflow outside this contract
- combine two role responsibilities "for convenience"
- begin implementing a new project before its folder placement is defined
- rely on unstated memory when the current task document has not been created or updated
- skip required internal research
- skip required external verification when current facts may have changed
- continue coding in an existing undocumented project before minimum documentation has been backfilled

## Minimum Checks By Role

### requirement-analyst

- clarifies scope
- splits work into implementable sub-functions
- marks non-goals and ambiguities

### architect

- verifies current project structure before deciding the landing zone
- identifies affected modules
- maps input to output flow
- defines structural invariants

### code-investigator

- researches internal code facts before drawing conclusions
- traces real call chains
- cites relevant files
- distinguishes fact from unknown

### solution-designer

- verifies whether the proposed solution depends on current external facts
- states root cause layer
- proposes minimum viable change
- defines impact range and fallback handling

### implementer

- verifies current implementation references and APIs before coding
- stays inside approved file scope
- follows the design handoff
- avoids unrelated refactors

### reviewer

- verifies review assumptions against current code and relevant current external standards when needed
- flags bugs and regressions
- checks scope drift
- records residual risk

### tester

- verifies test approach against the approved scope and any relevant current platform behavior
- covers normal path
- covers failure path
- covers edge or boundary path

### knowledge-keeper

- records symptom, root cause, fix
- records validated lessons
- marks remaining uncertainty

## Stop Conditions

The pipeline must stop when:

- the next required handoff does not exist
- the previous handoff is incomplete
- the user asks to skip a mandatory gate
- current work conflicts with prior constraints
- implementation or review evidence is missing for later stages
- any agent attempts to improvise an alternative process outside this contract
- a new project is being created but no dedicated folder has been defined yet
- the current task has no up-to-date handoff or planning document
- required research for the current role has not been completed
- external verification is required but has not been performed
- an existing project lacks minimum usable documentation and backfill has not been completed

The pipeline should not stop merely to request confirmation when:

- the next role is already determined
- the current handoff is sufficient
- no material branching decision remains
- the current role can finish from existing facts and approved constraints

## Recovery Rules

If the pipeline is blocked:

1. identify the last valid role
2. name the missing artifact
3. route back to the exact role that must repair the gap

Do not repair the gap inside the orchestrator.
Do not solve the blockage by inventing a new workflow.

## Project Placement Rule

For any new website, app, tool, or standalone deliverable:

1. choose the project folder during requirement or architecture stages
2. keep related implementation files inside that folder
3. avoid scattering project files across repository root

Root-level placement is allowed only when the user explicitly requests it and the handoff records that exception.

For work inside an existing project:

1. identify whether the change belongs to an existing module or a new subproject folder
2. record that landing zone in the handoff before implementation
3. keep implementation inside the approved existing path or approved new subfolder

## Documentation-First Rule

For every active development task:

1. write or update the current task document before implementation
2. keep the document aligned with the latest handoff state
3. if the plan, scope, or landing zone changes, update the document first

The purpose is to ensure continuity across sessions and prevent the workflow from depending on agent memory.

## Existing Project Documentation Backfill Rule

For an existing project with no usable documentation:

1. stop normal downstream development
2. create minimum viable documentation from repository facts
3. record known facts, landing zone, scope, unknowns, and risks
4. treat that backfill document as a required workflow artifact
5. then continue the normal workflow

Do not use missing documentation as an excuse to rely on memory or guess intent.

Follow the backfill process in:

- `agents/references/documentation-backfill-playbook.md`

This backfill may be created during `requirement-analyst` or `architect`, but downstream roles may not proceed until it exists.

## Research-First Rule

For roles 2-8:

1. complete internal project research before formal output
2. complete external research when current outside facts could affect correctness
3. record the verified inputs and research findings in the role output

Internal research includes:

- current task document
- prior handoffs
- repository files
- existing implementation behavior

External research is mandatory when the work depends on:

- third-party libraries or frameworks that may have changed
- browser or platform behavior
- SEO, deployment, distribution, or compatibility rules
- APIs, standards, or toolchain behavior that may be outdated

Do not rely on memory alone when there is meaningful risk of outdated information.

Follow the external research process in:

- `agents/references/external-research-playbook.md`

## Automatic Progression Rule

Default to automatic progression.

Advance to the next role without asking when:

1. the workflow state clearly determines the next role
2. the needed inputs already exist
3. there is no significant unresolved branch

Ask only when:

1. the product or technical direction is still ambiguous
2. multiple non-equivalent paths remain open
3. a decision would change scope, structure, or external promises
4. the current role cannot produce a valid output from the available facts and handoffs

## Enforcement Recommendation

Before implementation, run the repository gate checker:

```bash
python3 agents/scripts/check_workflow_gate.py --help
```

Use it to verify:

- current task document exists
- project path or landing zone is defined
- handoff documents contain mandatory sections
- handoff documents contain the required Chinese sublabels
- handoff documents record external research explicitly
- implementation targets stay inside the approved project path
- existing-project work declares documentation state and any required backfill artifact

## Enforcement Fallback Rule

Automatic gate first, manual checklist second.

If the gate script cannot run because the environment is missing a required runtime or command:

1. report the exact failure
2. perform a lightweight preflight when possible
3. fall back to the manual checklist

The workflow must not skip enforcement just because automation is unavailable.

Implementation may begin only after one of these is true:

- the automatic gate passes
- the manual checklist has been completed and recorded in the task document
