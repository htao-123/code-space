# Workflow Gate Checklist

Use this checklist only when the automatic gate script cannot run because of local environment limitations.

## When To Use

- `python3` is unavailable
- the gate script cannot execute in the current environment
- the runtime is missing and cannot be repaired quickly

Do not use this checklist just for convenience. Prefer the automatic gate whenever possible.

## Manual Checks

Mark each item before implementation begins.

### 1. Current Task Document

- [ ] A current task document or planning document exists
- [ ] It matches the latest understanding of scope
- [ ] If the task changed, the document was updated first

### 2. Workflow Handoffs

- [ ] The latest required handoff exists
- [ ] It contains all required sections:
  - `【角色结论】`
  - `【交付物】`
  - `【约束】`
  - `【校验标准】`
  - `【禁止事项】`
  - `【交接给下一个角色】`

### 3. Project Placement

- [ ] The approved project folder or landing zone is explicit
- [ ] New-project work is not scattered at repository root
- [ ] Existing-project work has an approved existing path or approved subfolder

### 4. Implementation Scope

- [ ] Target files or directories are named explicitly
- [ ] The targets are inside the approved project path
- [ ] The implementer is not coding outside the approved scope

### 5. Record The Fallback

- [ ] The task document records that automatic gate execution was unavailable
- [ ] The task document records that this manual checklist was used instead

## Completion Rule

Implementation may start only when every applicable checkbox is complete.
