# External Research Playbook

This playbook defines how to perform required external research during every workflow role.

## Purpose

Use external research to prevent outdated technical, platform, API, standards, deployment, SEO, browser, or library assumptions from leaking into the workflow.

External research is not casual browsing. It is targeted verification of facts that may materially affect correctness, and when relevant it also identifies current mainstream approaches and mature best-practice implementations.

## External Research Requirement

External research must be performed for every role before formal output. At minimum, verify whether any current outside facts, mainstream approaches, or mature implementations affect the current role, including:

- third-party libraries or frameworks
- browser or platform behavior
- deployment or hosting constraints
- SEO, indexing, metadata, or sharing behavior
- API behavior or toolchain behavior
- standards, compatibility, or official platform rules

If research finds no meaningful outside difference for the current role, record that conclusion explicitly rather than skipping the step.

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

### 2. Cover Three Research Layers

Check up to three layers depending on what the current role needs:

1. official current facts
2. mainstream current approaches
3. mature best-practice or reference implementations

Do not stop at only one layer when the role's decision depends on broader solution quality.

### 3. Prefer Primary Sources For Official Facts

Search priority:

1. official documentation
2. official release notes or changelogs
3. official platform policy or standards pages
4. official blog or migration guides

Use secondary sources only when primary sources are insufficient, and mark them as secondary.

For mainstream approaches and mature implementations, prefer:

- widely used ecosystem documentation
- maintainer guidance
- well-adopted community patterns
- credible reference implementations or high-quality open-source examples

### 4. Keep Research Narrow

Only research facts that affect the current role's decision.

Do not over-browse.
Do not collect unrelated trend material.
Do not browse broadly when one or two official sources can answer the question.

### 5. Record The Result

The role output should include:

- whether external research was required
- what was verified
- what the mainstream current approaches are when relevant
- which implementation patterns are worth following when relevant
- which conclusion matters for the role's decision

If relevant, include source names or links in the task document or commentary.

### 6. Distinguish Fact From Recommendation

Mark:

- what is directly verified from sources
- what is mainstream but not an official requirement
- what is your recommended implementation pattern based on those sources

Do not present inferences as verified facts.

## Role-Specific Guidance

### 建筑师

Use external research to verify:

- whether the proposed platform or architecture assumption is still valid
- whether current platform rules or constraints affect module placement
- which architecture approach is currently mainstream for the relevant ecosystem

### 侦查员

Use external research only when code facts alone are not enough and current outside behavior directly affects interpretation.

### 方案设计师

Use external research to verify:

- whether a proposed solution is outdated
- whether a better official pattern now exists
- whether a chosen technical approach is still recommended
- which current implementation pattern is most mature and maintainable

### 开发者

Use external research to verify:

- current APIs
- current framework syntax or usage
- implementation details likely to drift over time
- how mature implementations typically structure the same pattern when that affects code quality

### 审核员

Use external research to verify:

- known deprecations
- compatibility constraints
- outdated usage patterns
- whether the implementation follows a current mainstream pattern or an obsolete one

### 测试员

Use external research to verify:

- current platform behavior
- compatibility boundaries
- official support expectations when needed
- what successful real-world validation patterns look like for the same kind of feature

## If External Research Cannot Be Performed

If required external research cannot be performed:

1. record that the role is externally blocked
2. state which fact remains unverified
3. do not silently proceed as if the fact were confirmed

The workflow may continue only if the remaining uncertainty is explicitly acceptable for the current role; otherwise the role should stop and report the blocker.
