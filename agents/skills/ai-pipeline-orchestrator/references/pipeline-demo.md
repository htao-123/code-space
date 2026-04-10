# Pipeline Demo

This is a worked example showing how the orchestrator and the 8 role skills fit together.

## Example Request

> Add a debounce to the search box so repeated typing does not trigger a request on every keystroke.

## Step 1: Requirement Analyst

```md
【角色结论】
- The request is to reduce request frequency during typing without changing search results semantics.

【交付物】
- 【需求理解】
  - Problem: search requests fire too often while typing
  - Scenario: user types quickly in the search box
  - Input: text entered into search field
  - Output: delayed request after typing settles
- 【功能拆解】
  - detect search input changes
  - delay request trigger
  - preserve final query behavior
- 【边界定义】
  - In scope: request trigger timing
  - Out of scope: search ranking, UI redesign, API changes
- 【风险点】
  - unclear debounce duration
  - risk of breaking immediate search on submit

【约束】
- do not change search meaning
- do not add unrelated search features

【校验标准】
- debounce behavior is clearly scoped
- non-goals are explicit

【禁止事项】
- architecture design
- implementation details

【交接给下一个角色】
- Next role: architect
- allowed inputs: original request plus this handoff only
- non-goals: coding and file guesses
```

## Step 2: Architect

```md
【角色结论】
- The change belongs in the search input handling layer and request dispatch path.

【交付物】
- 【涉及模块】
  - search input component
  - search controller or state holder
  - request dispatch function
- 【数据流】
  - user input -> state update -> delayed trigger -> request dispatch
- 【改动策略】
  - modify existing search trigger path
- 【不变量】
  - keep API contract unchanged
  - keep explicit submit behavior intact

【约束】
- do not modify unrelated search result rendering
- do not add a new architecture layer

【校验标准】
- touched modules are minimal
- existing search structure remains intact

【禁止事项】
- code diffs
- implementation details

【交接给下一个角色】
- Next role: code-investigator
- allowed inputs: original request, requirement handoff, this handoff
- non-goals: proposing a fix
```

## Step 3: Code Investigator

```md
【角色结论】
- Search input currently triggers the request directly on every change.

【交付物】
- 【相关代码】
  - SearchBar widget handles `onChanged`
  - SearchController dispatches fetch call
  - SearchApi client performs request
- 【调用链】
  - SearchBar.onChanged -> SearchController.onQueryChanged -> fetchResults
- 【已有实现】
  - another filter panel already uses a delayed timer before reload
- 【状态流】
  - input text -> query state -> request invocation -> results state
- 【潜在问题点】
  - immediate dispatch on each keystroke
  - possible stale timer if not canceled on dispose

【约束】
- only use listed files unless new evidence appears
- do not invent missing logic

【校验标准】
- every claim is traceable to code
- unknowns are labeled

【禁止事项】
- proposing solutions
- writing code

【交接给下一个角色】
- Next role: solution-designer
- allowed inputs: original request, architect handoff, this handoff
- allowed files/modules: listed files only
```

## Step 4: Solution Designer

```md
【角色结论】
- The root cause is direct request dispatch inside the query change path.

【交付物】
- 【根因分析】
  - query changes call fetch immediately with no delay gate
- 【解决方案】
  - add a debounce timer in the controller
  - cancel prior timer on each query update
  - trigger immediate fetch only on explicit submit action
- 【影响范围】
  - search input flow
  - controller lifecycle cleanup
- 【兜底策略】
  - cancel timer on dispose
  - bypass debounce when user presses submit

【约束】
- change only approved search input/controller files
- do not modify API client or result rendering

【校验标准】
- design explains why
- fallback and cleanup are defined

【禁止事项】
- coding
- scope expansion

【交接给下一个角色】
- Next role: implementer
- allowed inputs: original request, this handoff, approved file scope
- non-goals: redesign
```

## Step 5: Implementer

```md
【角色结论】
- The approved debounce logic was implemented in the search controller path only.

【交付物】
- 【修改文件】
  - search_controller.dart
  - search_bar.dart
- 【具体改动】
  - added debounce timer management
  - canceled pending timer on new input
  - preserved immediate submit behavior
- 【新增代码】
  - timer field
  - dispose cleanup

【约束】
- review only against approved solution
- treat edits outside scope as violations

【校验标准】
- only approved files changed
- implementation matches design

【禁止事项】
- opportunistic refactor
- redesign

【交接给下一个角色】
- Next role: reviewer
- allowed inputs: original request, solution handoff, changed code, this handoff
- non-goals: rewriting requirements
```

## Step 6: Reviewer

```md
【角色结论】
- Implementation mostly matches the design, with one lifecycle risk to verify.

【交付物】
- 【问题列表】
  - ensure timer is canceled on controller dispose
- 【风险评估】
  - medium risk of delayed callback firing after teardown if cleanup is incomplete

【约束】
- tester must verify dispose path
- do not assume implementation is correct without execution evidence

【校验标准】
- changed files reviewed
- residual risk is explicit

【禁止事项】
- silently editing the code
- vague approval

【交接给下一个角色】
- Next role: tester
- allowed inputs: original request, solution handoff, changed code, this handoff
- done when: normal typing and teardown risk are both tested
```

## Step 7: Tester

```md
【角色结论】
- Debounced search works in the normal path and explicit submit still works.

【交付物】
- 【测试用例】
  - rapid typing triggers one delayed request
  - explicit submit triggers immediate request
  - closing the page cancels pending debounce
- 【测试结果】
  - pass: rapid typing
  - pass: explicit submit
  - pass: dispose cleanup

【约束】
- archive only validated outcomes
- carry forward any blocked environment notes

【校验标准】
- normal, failure, and lifecycle paths covered
- original issue is no longer reproducible

【禁止事项】
- assuming success
- hiding blocked cases

【交接给下一个角色】
- Next role: knowledge-keeper
- allowed inputs: original request, design handoff, review handoff, this handoff
- non-goals: inventing extra conclusions
```

## Step 8: Knowledge Keeper

```md
【角色结论】
- The root issue was eager request dispatch during input change.

【交付物】
- 【问题记录】
  - Symptom: search fired too frequently while typing
  - Root cause: request dispatch happened on each query change
  - Fix: controller-level debounce plus cleanup on dispose
- 【经验总结】
  - debounce belongs near request trigger, not inside API layer
  - lifecycle cleanup must be tested for timer-based fixes

【约束】
- archive validated information only
- mark uncertain items explicitly

【校验标准】
- another engineer can reuse the record
- facts and inferences are separated

【禁止事项】
- vague summary
- unvalidated claims

【交接给下一个角色】
- Terminal role
- Restart only from a new requirement
```

## Orchestrator Output Example

If the conversation currently ends after the architect handoff, the orchestrator should output:

```md
【当前状态】
- Last completed valid role: architect
- Pipeline state: in progress

【下一角色】
- code-investigator
- This is the only valid next role because architecture exists but evidence collection has not completed.

【可用输入】
- original user request
- latest architect handoff
- repository facts allowed for investigation

【缺失项】
- no code-investigator handoff yet

【执行规则】
- the next role may only use the listed inputs
- the next role may not propose solutions
- the next role must emit a full structured handoff

【停止条件】
- stop if required evidence cannot be collected
- stop if the investigator handoff is incomplete
```
