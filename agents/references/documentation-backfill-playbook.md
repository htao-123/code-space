# Documentation Backfill Playbook

This playbook defines how to proceed when an existing project lacks usable documentation.

## Purpose

Prevent development from depending on memory or guesswork when working inside an undocumented existing project.

## When To Use

Use this playbook when:

- the project already exists
- there is no usable README, task document, or handoff chain for the current work
- the current change cannot be safely placed using existing documentation

## Principle

Do not code first.
Backfill the minimum documentation needed to let the workflow continue safely.

## Minimum Viable Documentation

Create enough documentation to support the current requirement. At minimum, capture:

- current task scope
- approved landing zone
- relevant modules or files
- known repository facts
- key unknowns
- risks or ambiguity

## Backfill Sequence

### 1. Inspect Repository Facts

Use repository evidence such as:

- directory structure
- entry files
- configuration files
- existing page or module names
- git history when useful

Do not infer intent without evidence.

### 2. Create The Current Task Document

Write a current task document that at least records:

- what is being changed
- where it is expected to land
- what is already known
- what still needs confirmation

The document should explicitly include:

- `- 需求标识：...`
- `- 项目落点：...`

### 3. Mark Unknowns Explicitly

Do not hide uncertainty.

If you cannot determine:

- the correct module
- the right entry point
- whether the work belongs to an existing module or a new subfolder

record that explicitly.

### 4. Resume Normal Workflow

Once the minimum document exists, continue with the normal role sequence.

## Stop Conditions

Stop and ask the user only when repository facts are insufficient to determine:

- the landing zone
- the relevant module boundary
- the current requirement scope

If those facts can be backfilled from the repository, do that first instead of asking immediately.
