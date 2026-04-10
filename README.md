# AI Workflow Repository

这个仓库当前主要用于维护 AI 开发体系本身，包括：

- `AGENTS.md`
- `agents/`
- workflow gate / quality checker / checklist
- role skills / templates / contract

## 仓库边界

这个仓库默认把“规则体系”和“具体业务项目”分开管理。

所有临时或独立项目统一放在 `projects/` 下，不作为规则仓库的一部分提交。

当前示例项目包括：

- `projects/exchange-rate-calculator/`
- `projects/shannian-site/`
- `projects/outside-docs/`

## 提交原则

- 规则相关提交：只提交 `AGENTS.md`、`agents/`、仓库根说明和规则脚本/文档
- 项目相关提交：默认放在 `projects/` 下并被统一忽略；如需纳入版本控制，应先明确调整 `.gitignore`

## 说明

如果后续你要新建项目，直接放到 `projects/<project-name>/` 即可，不需要每次单独改 ignore。

如果后续你要把某个项目也纳入当前仓库管理，再单独更新 `.gitignore` 并走一次项目级提交流程。
