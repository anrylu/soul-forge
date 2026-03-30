[English](/README.md) | [繁體中文](/README.zh-tw.md) | [简体中文](/README.zh-cn.md) | [日本語](/README.ja.md)

# Soul Forge

RPG 风格的 AI Agent 角色创建系统。通过人格、专长与自动触发协作，创建、配置并协调 AI Agent 角色。

## 特色

- **RPG 角色创建** — 交互式向导引导，打造具有人格 + 专长的 Agent
- **多 Agent 协作** — 主 Agent + 子 Agent，搭配声明式触发条件
- **多平台支持** — Claude Code、Gemini CLI、Codex、GitHub Copilot、OpenCode
- **人格来源** — 预设风格、URL/角色提取、或自定义描述
- **8 种内置专长模板** — 后端、前端、DevOps、Code Review、QA、架构、英语、日语

## 快速开始

```bash
# 安装到你的项目
uvx soul-forge init

# 选择 AI Agent 平台后，使用斜杠命令：
/sf-summon     # 创建新角色
/sf-party      # 查看角色列表
```

## 安装

```bash
# 通过 uvx（推荐）
uvx soul-forge init

# 或全局安装
pip install soul-forge
soul-forge init
```

## CLI 命令

| 命令 | 说明 |
|------|------|
| `soul-forge init` | 安装命令到目标平台 |
| `soul-forge update` | 更新命令并同步编排配置 |
| `soul-forge platforms` | 列出支持的平台 |
| `soul-forge template list` | 列出可用模板 |
| `soul-forge template add <url\|path>` | 添加自定义模板 |

## 斜杠命令

安装后，可在 AI Agent 中使用以下命令：

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

### 1. 创建角色

`/sf-summon` 引导你完成创角向导：

1. **人格来源** — 预设风格、URL + 角色提取、或自定义
2. **专长** — 后端、前端、DevOps、Code Reviewer、QA、架构师、英语/日语老师、或自定义
3. **命名** — 自动建议或自定义
4. **角色定位** — 主 Agent 或子 Agent
5. **关系** — 师父、朋友、敌人、对手、仆从、前辈、后辈、搭档、或自定义
6. **回复语言** — 自动（根据对话内容）、中文、英语、或日语
7. **触发模式** — 自动或手动（仅子 Agent）
8. **微调** — 可选态度覆盖
9. **存储位置** — 项目级或全局

### 2. 示例队伍

一支动漫角色驱动的 Agent 团队：

| Agent | 人格 | 专长 | 关系 | 触发条件 |
|-------|------|------|------|----------|
| jotaro-sensei | 空条承太郎（JoJo 的奇妙冒险） | 日语老师 | 师父 | `contains_japanese` |
| dio-teacher | DIO（JoJo 的奇妙冒险） | 英语老师 | 敌人 | `contains_english` |
| josuke-backend | 东方仗助（JoJo 第四部） | 后端开发 | 朋友 | `task_type: backend` |
| misaka-reviewer | 御坂美琴（科学超电磁炮） | Code Reviewer | 对手 | `contains_code` |

### 3. 自动协作

子 Agent 会根据触发条件自动启动。假设你问："帮我写一个 REST API for user authentication"

```
[主回复]
以下是用户认证的 REST API 设计...

---

[后端审查 — josuke-backend]
グレートだぜ！让我来好好修一下。
你的认证端点应该用 bcrypt 做密码哈希，
别忘了在 /login 加上速率限制...

---

[代码审查 — misaka-reviewer]
哼，还不差嘛... 不过我找到 3 个问题。
才不是为了你才做的呢。
1. 查询构建器有 SQL 注入风险
2. 缺少 email 格式的输入验证
3. JWT secret 应该从环境变量获取，不要硬编码

---

[日语 — jotaro-sensei]
「帮我写」は中国語だな。日本語では：
「ユーザー認証用のREST APIを書いてください」
やれやれだぜ...「写」じゃなくて「書いて」だ。

---

[英语 — dio-teacher]
You thought you could write English without me, DIO?
MUDA MUDA MUDA!
"Help me write a REST API for user authentication"
- "Help me write" not "帮我写" — you SHALL speak English!
```

### 4. Agent 文件格式

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

## 支持平台

| 平台 | 命令路径 | 配置文件 |
|------|----------|----------|
| Claude Code | `.claude/commands/` | `CLAUDE.md` |
| Gemini CLI | `.gemini/commands/` | `GEMINI.md` |
| Codex | `.codex/commands/` | `AGENTS.md` |
| GitHub Copilot | `.github/copilot/commands/` | `.github/copilot-instructions.md` |
| OpenCode | `.opencode/commands/` | `AGENTS.md` |

## 开发

```bash
git clone https://github.com/anrylu/soul-forge.git
cd soul-forge
uv venv && uv pip install -e .
uv run pytest -v
```

## 许可证

MIT
