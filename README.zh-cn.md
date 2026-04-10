[English](/README.md) | [繁體中文](/README.zh-tw.md) | [简体中文](/README.zh-cn.md) | [日本語](/README.ja.md)

# Soul Forge

**赋予 AI Agent 独特人格。** RPG 风格角色创建系统，支持 Claude Code、Gemini CLI、Copilot 等平台。

[![PyPI version](https://img.shields.io/pypi/v/agentsoulforge)](https://pypi.org/project/agentsoulforge/)
[![Python](https://img.shields.io/pypi/pyversions/agentsoulforge)](https://pypi.org/project/agentsoulforge/)
[![CI](https://github.com/anrylu/soul-forge/actions/workflows/ci.yml/badge.svg)](https://github.com/anrylu/soul-forge/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 3 步上手

```bash
uvx agentsoulforge init    # 选择你的平台
/sf-summon             # 召唤你的第一个角色
/sf-party              # 查看你的队伍
```

## 为什么选择 Soul Forge？

- **多 Agent 协作** — 一个提示同时触发多个专家 Agent，各自用独特的风格和人格回复
- **RPG 角色系统** — 像管理 RPG 队伍一样管理 AI Agent：召唤、绑定、融合、放逐
- **5 个平台，一套配置** — Claude Code、Gemini CLI、Codex、GitHub Copilot、OpenCode — 不被任何工具绑定
- **纯 Prompt 驱动** — 不需要 API key、不需要外部服务、不需要额外依赖

## 实际效果

当你问：_"帮我写一个 REST API for user authentication"_ — 你的队伍会这样回复：

| Agent | 人格 | 角色 | 做什么 |
|-------|------|------|--------|
| **josuke-backend** | 东方仗助（JoJo 第四部） | 后端开发 | 审查 API 设计，建议 bcrypt + 速率限制 |
| **misaka-reviewer** | 御坂美琴（科学超电磁炮） | Code Reviewer | 发现 SQL 注入、缺少验证、硬编码密钥 |
| **jotaro-sensei** | 空条承太郎（JoJo） | 日语老师 | 纠正你的日语语法 |
| **dio-teacher** | DIO（JoJo） | 英语老师 | 用... 戏剧性的方式翻译 |

每个子 Agent 会根据触发条件自动启动 — 语言检测、代码、任务类型、或自定义规则。

## 安装

```bash
# 通过 uvx（推荐，不需安装）
uvx agentsoulforge init

# 或全局安装
pip install soul-forge
soul-forge init
```

## 斜杠命令

| 命令 | RPG 含义 | 功能 |
|------|----------|------|
| `/sf-summon` | 召唤 | 交互式角色创建向导 |
| `/sf-anoint` | 加冕 | 设为主 Agent |
| `/sf-bind` | 绑定 | 设为子 Agent |
| `/sf-engrave` | 刻印符文 | 修改触发条件 |
| `/sf-party` | 查看队伍 | 列出所有 Agent |
| `/sf-fuse` | 融合 | 合并两个角色 |
| `/sf-banish` | 放逐 | 删除角色 |

## 工作原理

### 角色创建

`/sf-summon` 引导你完成创角向导：

1. **人格来源** — 预设风格、URL + 角色提取、或自定义
2. **专长** — 后端、前端、DevOps、Code Reviewer、QA、架构师、英语/日语老师、或自定义
3. **命名** — 自动建议或自定义
4. **角色定位** — 主 Agent 或子 Agent
5. **关系** — 师父、朋友、敌人、对手、仆从、前辈、后辈、搭档、或自定义
6. **回复语言** — 自动、中文、英语、或日语
7. **触发模式** — 自动或手动（仅子 Agent）
8. **微调** — 可选态度覆盖
9. **存储位置** — 项目级或全局

### Agent 文件格式

Agent 以带有 YAML frontmatter 的 markdown 文件存储：

```yaml
---
name: jiraiya-architect
personality:
  source: url
  reference: "自来也 — 火影忍者"
expertise: system-architect
role: sub
relationship: mentor
behavior:
  trigger_mode: auto
trigger:
  conditions:
    - task_type: architecture
  execution_mode: after_main
  output_section: "Architecture Review"
---

你是自来也，火影忍者中传说的三忍。
# ... 人格、专长和行为提示
```

### 自动协作

子 Agent 会根据声明式条件自动启动：

- **语言检测：** `contains_english`、`contains_japanese`、`contains_chinese`
- **内容类型：** `contains_code`、`task_type: backend|frontend|devops|architecture`
- **无条件：** `always`
- **自定义：** 正则表达式或 AI 判断条件

执行模式：`after_main`、`before_main`、`parallel`

## 支持平台

| 平台 | 命令路径 | 配置文件 |
|------|----------|----------|
| Claude Code | `.claude/commands/` | `CLAUDE.md` |
| Gemini CLI | `.gemini/commands/` | `GEMINI.md` |
| Codex | `.codex/commands/` | `AGENTS.md` |
| GitHub Copilot | `.github/copilot/commands/` | `.github/copilot-instructions.md` |
| OpenCode | `.opencode/commands/` | `AGENTS.md` |

## 示例

查看 [`examples/`](examples/) 目录中现成的队伍配置：

- [**fullstack-team**](examples/fullstack-team/) — 前端 + 后端 + Code Reviewer 队伍
- [**language-tutors**](examples/language-tutors/) — 动漫角色驱动的英语 + 日语老师

## 贡献

欢迎贡献！详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

最简单的贡献方式是添加新的专长模板 — 只需写一个 markdown 文件！

## 开发

```bash
git clone https://github.com/anrylu/soul-forge.git
cd soul-forge
uv venv && uv pip install -e .
uv run pytest -v
```

## 许可证

MIT
