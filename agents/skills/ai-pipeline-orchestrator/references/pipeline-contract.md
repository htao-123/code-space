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

## Mandatory Handoff Shape

Every role output must contain:

```md
【角色结论】
【交付物】
【约束】
【校验标准】
【禁止事项】
【交接给下一个角色】
```

If any heading is missing, the handoff is incomplete and the pipeline must stop.

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

## Minimum Checks By Role

### requirement-analyst

- clarifies scope
- splits work into implementable sub-functions
- marks non-goals and ambiguities

### architect

- identifies affected modules
- maps input to output flow
- defines structural invariants

### code-investigator

- traces real call chains
- cites relevant files
- distinguishes fact from unknown

### solution-designer

- states root cause layer
- proposes minimum viable change
- defines impact range and fallback handling

### implementer

- stays inside approved file scope
- follows the design handoff
- avoids unrelated refactors

### reviewer

- flags bugs and regressions
- checks scope drift
- records residual risk

### tester

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

## Recovery Rules

If the pipeline is blocked:

1. identify the last valid role
2. name the missing artifact
3. route back to the exact role that must repair the gap

Do not repair the gap inside the orchestrator.
