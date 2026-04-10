# External Research Playbook

This playbook defines how to perform required external research during workflow roles 2-8.

## Purpose

Use external research to prevent outdated technical, platform, API, standards, deployment, SEO, browser, or library assumptions from leaking into the workflow.

External research is not casual browsing. It is targeted verification of facts that may materially affect correctness.

## When External Research Is Mandatory

External research must be performed when the current role depends on facts that may have changed, including:

- third-party libraries or frameworks
- browser or platform behavior
- deployment or hosting constraints
- SEO, indexing, metadata, or sharing behavior
- API behavior or toolchain behavior
- standards, compatibility, or official platform rules

If there is meaningful risk that memory may be outdated, external research is mandatory.

## Research Sequence

### 1. Define The Research Question

Before browsing, write down:

- what needs verification
- why it affects the current role
- what decision depends on it

Good example:

- "Need to verify whether the current framework still recommends approach X before the solution designer commits to it."

Bad example:

- "Search around and see what people say."

### 2. Prefer Primary Sources

Search priority:

1. official documentation
2. official release notes or changelogs
3. official platform policy or standards pages
4. official blog or migration guides

Use secondary sources only when primary sources are insufficient, and mark them as secondary.

### 3. Keep Research Narrow

Only research facts that affect the current role's decision.

Do not over-browse.
Do not collect unrelated trend material.
Do not browse broadly when one or two official sources can answer the question.

### 4. Record The Result

The role output should include:

- whether external research was required
- what was verified
- which conclusion matters for the role's decision

If relevant, include source names or links in the task document or commentary.

### 5. Distinguish Fact From Inference

Mark:

- what is directly verified from sources
- what is your inference from those sources

Do not present inferences as verified facts.

## Role-Specific Guidance

### 建筑师

Use external research to verify:

- whether the proposed platform or architecture assumption is still valid
- whether current platform rules or constraints affect module placement

### 侦查员

Use external research only when code facts alone are not enough and current outside behavior directly affects interpretation.

### 方案设计师

Use external research to verify:

- whether a proposed solution is outdated
- whether a better official pattern now exists
- whether a chosen technical approach is still recommended

### 开发者

Use external research to verify:

- current APIs
- current framework syntax or usage
- implementation details likely to drift over time

### 审核员

Use external research to verify:

- known deprecations
- compatibility constraints
- outdated usage patterns

### 测试员

Use external research to verify:

- current platform behavior
- compatibility boundaries
- official support expectations when needed

## If External Research Cannot Be Performed

If external research is required but cannot be performed:

1. record that the role is externally blocked
2. state which fact remains unverified
3. do not silently proceed as if the fact were confirmed

The workflow may continue only if the remaining uncertainty is explicitly acceptable for the current role; otherwise the role should stop and report the blocker.
