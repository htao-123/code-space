# Reviewer Output Template

```md
【角色结论】
- 用一句话总结实现是否通过审查，以及最大风险是什么。

【交付物】
- 【问题列表】
  - 问题 1:
  - 严重性:
  - 证据:
  - 问题 2:
  - 严重性:
  - 证据:
- 【风险评估】
  - 残余风险 1:
  - 残余风险 2:

【约束】
- tester 必须覆盖主要风险和未决问题
- 不得把 review 通过当作功能正确的证明

【校验标准】
- 所有改动区域都已检查
- 发现项基于证据
- 即使无 bug 也写清残余风险

【禁止事项】
- 不静默改代码
- 不重写设计
- 不做空泛通过结论

【交接给下一个角色】
- Next role: tester
- allowed inputs: 原始需求 + solution handoff + changed code + 本 handoff
- done when: 每个主要风险都有测试或阻塞说明
```
