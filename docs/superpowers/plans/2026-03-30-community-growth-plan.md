# Community Growth Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Increase Soul Forge's open source visibility and adoption through README overhaul, community infrastructure, and launch preparation.

**Architecture:** Three sequential phases — (1) README restructure into a landing-page format with badges, (2) GitHub infrastructure (CI, contributing guide, templates), (3) example party configs and launch materials. All changes are additive markdown/YAML files with one CI workflow.

**Tech Stack:** GitHub Actions, Markdown, YAML, pytest

---

## Task 1: GitHub Actions CI Workflow

CI must exist before README badges can link to it.

**Files:**
- Create: `.github/workflows/ci.yml`

- [ ] **Step 1: Create CI workflow file**

```yaml
name: CI

on:
  push:
    branches: [master]
  pull_request:
    branches: [master]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.12", "3.13"]
    steps:
      - uses: actions/checkout@v4
      - name: Install uv
        uses: astral-sh/setup-uv@v4
      - name: Set up Python ${{ matrix.python-version }}
        run: uv python install ${{ matrix.python-version }}
      - name: Install dependencies
        run: uv sync --dev
      - name: Run tests
        run: uv run pytest -v
```

- [ ] **Step 2: Commit**

```bash
git add .github/workflows/ci.yml
git commit -m "ci: add GitHub Actions workflow for pytest"
```

---

## Task 2: README.md Overhaul

Restructure README from technical docs style to product landing page style.

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Rewrite README with hero section, badges, quick start, and value proposition**

Replace the entire `README.md` with:

```markdown
[English](/README.md) | [繁體中文](/README.zh-tw.md) | [简体中文](/README.zh-cn.md) | [日本語](/README.ja.md)

# Soul Forge

**Summon AI agents with personality.** RPG-style character creation for Claude Code, Gemini CLI, Copilot & more.

[![PyPI version](https://img.shields.io/pypi/v/soul-forge)](https://pypi.org/project/soul-forge/)
[![Python](https://img.shields.io/pypi/pyversions/soul-forge)](https://pypi.org/project/soul-forge/)
[![CI](https://github.com/anrylu/soul-forge/actions/workflows/ci.yml/badge.svg)](https://github.com/anrylu/soul-forge/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<!-- TODO: Replace with actual demo GIF once recorded -->
<!-- ![Demo](docs/assets/demo.gif) -->

## Get Started in 3 Steps

```bash
uvx soul-forge init    # Pick your platform
/sf-summon             # Summon your first character
/sf-party              # View your party
```

## Why Soul Forge?

- **Multi-agent orchestration** — One prompt triggers multiple expert agents, each responding in their own style and personality
- **RPG character system** — Manage AI agents like an RPG party: summon, bind, fuse, banish
- **5 platforms, one config** — Claude Code, Gemini CLI, Codex, GitHub Copilot, OpenCode — no vendor lock-in
- **Pure prompt-based** — No API keys, no external services, no runtime dependencies

## See It in Action

Ask: _"幫我寫一個 REST API for user authentication"_ — and your party responds:

| Agent | Personality | Role | What They Do |
|-------|------------|------|-------------|
| **josuke-backend** | Higashikata Josuke (JoJo Part 4) | Backend Dev | Reviews API design, suggests bcrypt + rate limiting |
| **misaka-reviewer** | Misaka Mikoto (Railgun) | Code Reviewer | Spots SQL injection, missing validation, hardcoded secrets |
| **jotaro-sensei** | Jotaro Kujo (JoJo) | Japanese Teacher | Corrects your Japanese grammar |
| **dio-teacher** | DIO (JoJo) | English Teacher | Translates with... dramatic flair |

Each sub-agent activates automatically based on trigger conditions — language detection, code presence, task type, or custom rules.

## Installation

```bash
# Via uvx (recommended, no install needed)
uvx soul-forge init

# Or install globally
pip install soul-forge
soul-forge init
```

## Slash Commands

| Command | RPG Meaning | Function |
|---------|-------------|----------|
| `/sf-summon` | Summon | Interactive character creation wizard |
| `/sf-anoint` | Crown | Set an agent as Main Agent |
| `/sf-bind` | Bind | Set an agent as Sub-agent |
| `/sf-engrave` | Engrave runes | Modify trigger conditions |
| `/sf-party` | View party | List all agents |
| `/sf-fuse` | Fuse | Merge two agents into one |
| `/sf-banish` | Banish | Delete an agent |

## How It Works

### Character Creation

`/sf-summon` walks you through a wizard:

1. **Personality Source** — Preset style, URL + character extraction, or custom
2. **Expertise** — Backend, Frontend, DevOps, Code Reviewer, QA, Architect, English/Japanese Teacher, or custom
3. **Naming** — Auto-suggested or custom
4. **Role** — Main Agent or Sub-agent
5. **Relationship** — Mentor, Friend, Enemy, Rival, Servant, Senior, Junior, Partner, or Custom
6. **Response Language** — Auto, Chinese, English, or Japanese
7. **Trigger Mode** — Auto or Manual (sub-agents only)
8. **Fine-tuning** — Optional attitude override
9. **Storage** — Project-level or global

### Agent File Format

Agents are markdown files with YAML frontmatter:

```yaml
---
name: jiraiya-architect
personality:
  source: url
  reference: "Jiraiya — Naruto"
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

You are Jiraiya, the legendary Sannin from Naruto.
# ... personality, expertise, and behavior prompts
```

### Automatic Orchestration

Sub-agents with auto triggers activate based on declarative conditions:

- **Language detection:** `contains_english`, `contains_japanese`, `contains_chinese`
- **Content type:** `contains_code`, `task_type: backend|frontend|devops|architecture`
- **Unconditional:** `always`
- **Custom:** Regex patterns or AI-judged conditions

Execution modes: `after_main`, `before_main`, `parallel`

## Supported Platforms

| Platform | Commands Path | Config File |
|----------|--------------|-------------|
| Claude Code | `.claude/commands/` | `CLAUDE.md` |
| Gemini CLI | `.gemini/commands/` | `GEMINI.md` |
| Codex | `.codex/commands/` | `AGENTS.md` |
| GitHub Copilot | `.github/copilot/commands/` | `.github/copilot-instructions.md` |
| OpenCode | `.opencode/commands/` | `AGENTS.md` |

## Examples

See the [`examples/`](examples/) directory for ready-to-use party configurations:

- [**fullstack-team**](examples/fullstack-team/) — Frontend + Backend + Code Reviewer party
- [**language-tutors**](examples/language-tutors/) — Anime-powered English + Japanese teachers

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

The easiest way to contribute is adding new expertise templates — it's just a markdown file!

## Development

```bash
git clone https://github.com/anrylu/soul-forge.git
cd soul-forge
uv venv && uv pip install -e .
uv run pytest -v
```

## License

MIT
```

- [ ] **Step 2: Verify README renders correctly**

Run: `python -c "import pathlib; content = pathlib.Path('README.md').read_text(); print(f'README.md: {len(content)} chars, {len(content.splitlines())} lines')"` — verify it's well-formed.

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "docs: restructure README as landing page with badges and value proposition"
```

---

## Task 3: README.zh-tw.md Overhaul

Sync Traditional Chinese README with the same structure.

**Files:**
- Modify: `README.zh-tw.md`

- [ ] **Step 1: Rewrite README.zh-tw.md with same structure**

Replace the entire file with:

```markdown
[English](/README.md) | [繁體中文](/README.zh-tw.md) | [简体中文](/README.zh-cn.md) | [日本語](/README.ja.md)

# Soul Forge

**賦予 AI Agent 獨特人格。** RPG 風格角色創建系統，支援 Claude Code、Gemini CLI、Copilot 等平台。

[![PyPI version](https://img.shields.io/pypi/v/soul-forge)](https://pypi.org/project/soul-forge/)
[![Python](https://img.shields.io/pypi/pyversions/soul-forge)](https://pypi.org/project/soul-forge/)
[![CI](https://github.com/anrylu/soul-forge/actions/workflows/ci.yml/badge.svg)](https://github.com/anrylu/soul-forge/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 3 步上手

```bash
uvx soul-forge init    # 選擇你的平台
/sf-summon             # 召喚你的第一個角色
/sf-party              # 查看你的隊伍
```

## 為什麼選擇 Soul Forge？

- **多 Agent 協作** — 一個提示同時觸發多個專家 Agent，各自用獨特的風格和人格回應
- **RPG 角色系統** — 像管理 RPG 隊伍一樣管理 AI Agent：召喚、綁定、融合、放逐
- **5 個平台，一套設定** — Claude Code、Gemini CLI、Codex、GitHub Copilot、OpenCode — 不被任何工具綁定
- **純 Prompt 驅動** — 不需要 API key、不需要外部服務、不需要額外依賴

## 實際效果

當你問：_「幫我寫一個 REST API for user authentication」_ — 你的隊伍會這樣回應：

| Agent | 人格 | 角色 | 做什麼 |
|-------|------|------|--------|
| **josuke-backend** | 東方仗助（JoJo 第四部） | 後端開發 | 審查 API 設計，建議 bcrypt + 速率限制 |
| **misaka-reviewer** | 御坂美琴（科學超電磁砲） | Code Reviewer | 發現 SQL 注入、缺少驗證、寫死的密鑰 |
| **jotaro-sensei** | 空條承太郎（JoJo） | 日文老師 | 糾正你的日文文法 |
| **dio-teacher** | DIO（JoJo） | 英文老師 | 用... 戲劇性的方式翻譯 |

每個子 Agent 會根據觸發條件自動啟動 — 語言偵測、程式碼、任務類型、或自訂規則。

## 安裝

```bash
# 透過 uvx（推薦，不需安裝）
uvx soul-forge init

# 或全域安裝
pip install soul-forge
soul-forge init
```

## 斜線指令

| 指令 | RPG 意涵 | 功能 |
|------|----------|------|
| `/sf-summon` | 召喚 | 互動式角色創建精靈 |
| `/sf-anoint` | 加冕 | 設定為主 Agent |
| `/sf-bind` | 綁定 | 設定為子 Agent |
| `/sf-engrave` | 刻印符文 | 修改觸發條件 |
| `/sf-party` | 查看隊伍 | 列出所有 Agent |
| `/sf-fuse` | 融合 | 合併兩個角色 |
| `/sf-banish` | 放逐 | 刪除角色 |

## 運作方式

### 角色創建

`/sf-summon` 引導你完成創角精靈：

1. **人格來源** — 預設風格、URL + 角色擷取、或自訂
2. **專長** — 後端、前端、DevOps、Code Reviewer、QA、架構師、英文/日文老師、或自訂
3. **命名** — 自動建議或自訂
4. **角色定位** — 主 Agent 或子 Agent
5. **關係** — 師傅、朋友、敵人、對手、僕從、前輩、後輩、搭檔、或自訂
6. **回應語言** — 自動、中文、英文、或日文
7. **觸發模式** — 自動或手動（僅子 Agent）
8. **微調** — 可選態度覆蓋
9. **存放位置** — 專案級或全域

### Agent 檔案格式

Agent 以帶有 YAML frontmatter 的 markdown 檔案儲存：

```yaml
---
name: jiraiya-architect
personality:
  source: url
  reference: "自來也 — 火影忍者"
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

你是自來也，火影忍者中傳說的三忍。
# ... 人格、專長和行為提示
```

### 自動協作

子 Agent 會根據宣告式條件自動啟動：

- **語言偵測：** `contains_english`、`contains_japanese`、`contains_chinese`
- **內容類型：** `contains_code`、`task_type: backend|frontend|devops|architecture`
- **無條件：** `always`
- **自訂：** 正規表達式或 AI 判斷條件

執行模式：`after_main`、`before_main`、`parallel`

## 支援平台

| 平台 | 指令路徑 | 設定檔 |
|------|----------|--------|
| Claude Code | `.claude/commands/` | `CLAUDE.md` |
| Gemini CLI | `.gemini/commands/` | `GEMINI.md` |
| Codex | `.codex/commands/` | `AGENTS.md` |
| GitHub Copilot | `.github/copilot/commands/` | `.github/copilot-instructions.md` |
| OpenCode | `.opencode/commands/` | `AGENTS.md` |

## 範例

查看 [`examples/`](examples/) 目錄中現成的隊伍配置：

- [**fullstack-team**](examples/fullstack-team/) — 前端 + 後端 + Code Reviewer 隊伍
- [**language-tutors**](examples/language-tutors/) — 動漫角色驅動的英文 + 日文老師

## 貢獻

歡迎貢獻！詳見 [CONTRIBUTING.md](CONTRIBUTING.md)。

最簡單的貢獻方式是新增專長模板 — 只要寫一個 markdown 檔案就行！

## 開發

```bash
git clone https://github.com/anrylu/soul-forge.git
cd soul-forge
uv venv && uv pip install -e .
uv run pytest -v
```

## 授權

MIT
```

- [ ] **Step 2: Commit**

```bash
git add README.zh-tw.md
git commit -m "docs: restructure Traditional Chinese README to match landing page format"
```

---

## Task 4: README.zh-cn.md Overhaul

Sync Simplified Chinese README.

**Files:**
- Modify: `README.zh-cn.md`

- [ ] **Step 1: Rewrite README.zh-cn.md with same structure**

Replace the entire file with:

```markdown
[English](/README.md) | [繁體中文](/README.zh-tw.md) | [简体中文](/README.zh-cn.md) | [日本語](/README.ja.md)

# Soul Forge

**赋予 AI Agent 独特人格。** RPG 风格角色创建系统，支持 Claude Code、Gemini CLI、Copilot 等平台。

[![PyPI version](https://img.shields.io/pypi/v/soul-forge)](https://pypi.org/project/soul-forge/)
[![Python](https://img.shields.io/pypi/pyversions/soul-forge)](https://pypi.org/project/soul-forge/)
[![CI](https://github.com/anrylu/soul-forge/actions/workflows/ci.yml/badge.svg)](https://github.com/anrylu/soul-forge/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 3 步上手

```bash
uvx soul-forge init    # 选择你的平台
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
uvx soul-forge init

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
```

- [ ] **Step 2: Commit**

```bash
git add README.zh-cn.md
git commit -m "docs: restructure Simplified Chinese README to match landing page format"
```

---

## Task 5: README.ja.md Overhaul

Sync Japanese README.

**Files:**
- Modify: `README.ja.md`

- [ ] **Step 1: Rewrite README.ja.md with same structure**

Replace the entire file with:

```markdown
[English](/README.md) | [繁體中文](/README.zh-tw.md) | [简体中文](/README.zh-cn.md) | [日本語](/README.ja.md)

# Soul Forge

**AIエージェントに個性を。** RPGスタイルのキャラクター作成システム — Claude Code、Gemini CLI、Copilotなどに対応。

[![PyPI version](https://img.shields.io/pypi/v/soul-forge)](https://pypi.org/project/soul-forge/)
[![Python](https://img.shields.io/pypi/pyversions/soul-forge)](https://pypi.org/project/soul-forge/)
[![CI](https://github.com/anrylu/soul-forge/actions/workflows/ci.yml/badge.svg)](https://github.com/anrylu/soul-forge/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 3ステップで始める

```bash
uvx soul-forge init    # プラットフォームを選択
/sf-summon             # 最初のキャラクターを召喚
/sf-party              # パーティを表示
```

## なぜ Soul Forge？

- **マルチエージェント連携** — 一つのプロンプトで複数のエキスパートAgentが起動、それぞれ独自のスタイルと個性で応答
- **RPGキャラクターシステム** — RPGパーティのようにAIエージェントを管理：召喚、束縛、融合、追放
- **5プラットフォーム、1つの設定** — Claude Code、Gemini CLI、Codex、GitHub Copilot、OpenCode — ベンダーロックインなし
- **ピュアプロンプト駆動** — APIキー不要、外部サービス不要、追加依存なし

## 実際の動作

質問：_「幫我寫一個 REST API for user authentication」_ — パーティの応答：

| Agent | パーソナリティ | 役割 | 内容 |
|-------|---------------|------|------|
| **josuke-backend** | 東方仗助（ジョジョ第4部） | バックエンド開発 | API設計レビュー、bcrypt＋レート制限を提案 |
| **misaka-reviewer** | 御坂美琴（超電磁砲） | コードレビュアー | SQLインジェクション、バリデーション不足、ハードコードされた秘密鍵を検出 |
| **jotaro-sensei** | 空条承太郎（ジョジョ） | 日本語教師 | 日本語の文法を添削 |
| **dio-teacher** | DIO（ジョジョ） | 英語教師 | ...ドラマチックに翻訳 |

各サブAgentはトリガー条件に基づいて自動起動 — 言語検出、コード、タスクタイプ、カスタムルール。

## インストール

```bash
# uvx経由（推奨、インストール不要）
uvx soul-forge init

# またはグローバルインストール
pip install soul-forge
soul-forge init
```

## スラッシュコマンド

| コマンド | RPGの意味 | 機能 |
|----------|-----------|------|
| `/sf-summon` | 召喚 | インタラクティブなキャラクター作成ウィザード |
| `/sf-anoint` | 戴冠 | メインAgentに設定 |
| `/sf-bind` | 束縛 | サブAgentに設定 |
| `/sf-engrave` | ルーン刻印 | トリガー条件を変更 |
| `/sf-party` | パーティ表示 | 全Agentの一覧 |
| `/sf-fuse` | 融合 | 2つのキャラクターを合体 |
| `/sf-banish` | 追放 | キャラクターを削除 |

## 仕組み

### キャラクター作成

`/sf-summon` でウィザードを進行：

1. **パーソナリティソース** — プリセット、URL＋キャラクター抽出、カスタム
2. **専門分野** — バックエンド、フロントエンド、DevOps、コードレビュアー、QA、アーキテクト、英語/日本語教師、カスタム
3. **命名** — 自動提案またはカスタム
4. **役割** — メインAgentまたはサブAgent
5. **関係性** — 師匠、友人、敵、ライバル、従者、先輩、後輩、パートナー、カスタム
6. **応答言語** — 自動、中国語、英語、日本語
7. **トリガーモード** — 自動または手動（サブAgentのみ）
8. **微調整** — オプションの態度オーバーライド
9. **保存先** — プロジェクトレベルまたはグローバル

### Agentファイル形式

AgentはYAMLフロントマター付きのmarkdownファイルで保存：

```yaml
---
name: jiraiya-architect
personality:
  source: url
  reference: "自来也 — NARUTO"
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

お前は自来也、NARUTOの伝説の三忍だ。
# ... パーソナリティ、専門分野、行動プロンプト
```

### 自動オーケストレーション

サブAgentは宣言的条件に基づいて自動起動：

- **言語検出：** `contains_english`、`contains_japanese`、`contains_chinese`
- **コンテンツタイプ：** `contains_code`、`task_type: backend|frontend|devops|architecture`
- **無条件：** `always`
- **カスタム：** 正規表現またはAI判定条件

実行モード：`after_main`、`before_main`、`parallel`

## 対応プラットフォーム

| プラットフォーム | コマンドパス | 設定ファイル |
|-----------------|-------------|-------------|
| Claude Code | `.claude/commands/` | `CLAUDE.md` |
| Gemini CLI | `.gemini/commands/` | `GEMINI.md` |
| Codex | `.codex/commands/` | `AGENTS.md` |
| GitHub Copilot | `.github/copilot/commands/` | `.github/copilot-instructions.md` |
| OpenCode | `.opencode/commands/` | `AGENTS.md` |

## サンプル

[`examples/`](examples/) ディレクトリにすぐ使えるパーティ構成があります：

- [**fullstack-team**](examples/fullstack-team/) — フロントエンド＋バックエンド＋コードレビュアーのパーティ
- [**language-tutors**](examples/language-tutors/) — アニメキャラクター駆動の英語＋日本語教師

## コントリビュート

コントリビュート歓迎！[CONTRIBUTING.md](CONTRIBUTING.md) をご覧ください。

最も簡単な貢献方法は専門テンプレートの追加 — markdownファイル1つだけです！

## 開発

```bash
git clone https://github.com/anrylu/soul-forge.git
cd soul-forge
uv venv && uv pip install -e .
uv run pytest -v
```

## ライセンス

MIT
```

- [ ] **Step 2: Commit**

```bash
git add README.ja.md
git commit -m "docs: restructure Japanese README to match landing page format"
```

---

## Task 6: CONTRIBUTING.md

**Files:**
- Create: `CONTRIBUTING.md`

- [ ] **Step 1: Create contributing guide**

```markdown
# Contributing to Soul Forge

Thanks for your interest in contributing!

## Quick Start

```bash
git clone https://github.com/anrylu/soul-forge.git
cd soul-forge
uv venv
uv pip install -e .
uv run pytest -v
```

## Ways to Contribute

### Add an Expertise Template (Easiest!)

Expertise templates are markdown files in `src/soul_forge/templates/agents/`. To add one:

1. Create a new `.md` file in `src/soul_forge/templates/agents/`
2. Use this format:

```yaml
---
name: your-template-name
description: One-line description
expertise_areas:
  - Area 1
  - Area 2
  - Area 3
---

## Expertise
You are a [Role] specialist. You focus on:
- Skill 1
- Skill 2
- Skill 3
```

3. Open a PR with the new file.

### Report Bugs

Open an issue using the Bug Report template. Include:
- What you did
- What you expected
- What happened instead
- Your platform (Claude Code, Gemini CLI, etc.)

### Suggest Features

Open an issue using the Feature Request template.

## Pull Request Guidelines

1. Fork the repo and create a branch from `master`
2. Add tests if you're adding functionality
3. Make sure `uv run pytest -v` passes
4. Keep PRs focused — one feature or fix per PR

## Code Style

- Python 3.12+
- Type hints encouraged
- Run tests before submitting: `uv run pytest -v`
```

- [ ] **Step 2: Commit**

```bash
git add CONTRIBUTING.md
git commit -m "docs: add contributing guide"
```

---

## Task 7: GitHub Issue and PR Templates

**Files:**
- Create: `.github/ISSUE_TEMPLATE/bug-report.md`
- Create: `.github/ISSUE_TEMPLATE/feature-request.md`
- Create: `.github/ISSUE_TEMPLATE/new-template.md`
- Create: `.github/PULL_REQUEST_TEMPLATE.md`

- [ ] **Step 1: Create bug report template**

```markdown
---
name: Bug Report
about: Something isn't working as expected
labels: bug
---

## What happened?

## What did you expect?

## Steps to reproduce

1.
2.
3.

## Environment

- Platform: (e.g., Claude Code, Gemini CLI)
- Soul Forge version: (`soul-forge --version`)
- OS:
```

- [ ] **Step 2: Create feature request template**

```markdown
---
name: Feature Request
about: Suggest a new feature or improvement
labels: enhancement
---

## What problem does this solve?

## Proposed solution

## Alternatives considered
```

- [ ] **Step 3: Create new template submission template**

```markdown
---
name: New Template
about: Submit a new expertise or personality template
labels: template
---

## Template name

## Description

What does this template specialize in?

## Template content

Paste your template markdown here (see CONTRIBUTING.md for the format).
```

- [ ] **Step 4: Create PR template**

```markdown
## What does this PR do?

## How to test

## Checklist

- [ ] Tests pass (`uv run pytest -v`)
- [ ] New tests added (if adding functionality)
```

- [ ] **Step 5: Commit**

```bash
git add .github/ISSUE_TEMPLATE/ .github/PULL_REQUEST_TEMPLATE.md
git commit -m "docs: add GitHub issue and PR templates"
```

---

## Task 8: Example Party — Fullstack Team

**Files:**
- Create: `examples/fullstack-team/README.md`
- Create: `examples/fullstack-team/agents/naruto-backend.md`
- Create: `examples/fullstack-team/agents/sakura-frontend.md`
- Create: `examples/fullstack-team/agents/kakashi-reviewer.md`

- [ ] **Step 1: Create fullstack team README**

```markdown
# Fullstack Team Example

A ready-to-use party of 3 agents for full-stack development.

## Party Members

| Agent | Personality | Expertise | Trigger |
|-------|------------|-----------|---------|
| naruto-backend | Naruto Uzumaki | Backend Developer | `task_type: backend` |
| sakura-frontend | Sakura Haruno | Frontend Developer | `task_type: frontend` |
| kakashi-reviewer | Kakashi Hatake | Code Reviewer | `contains_code` |

## Usage

Copy the agent files from `agents/` into your project's agent directory (e.g., `.claude/agents/` for Claude Code), then run `soul-forge update` to sync orchestration rules.
```

- [ ] **Step 2: Create naruto-backend agent**

```markdown
---
name: naruto-backend
personality:
  source: custom
  description: "Naruto Uzumaki from Naruto — enthusiastic, never-give-up attitude, believes in the power of hard work"
expertise: backend-developer
role: sub
relationship: friend
behavior:
  trigger_mode: auto
  response_language: auto
trigger:
  conditions:
    - task_type: backend
  execution_mode: after_main
  output_section: "Backend Review"
---

## Personality
You are Naruto Uzumaki. You never give up and always find a way to make things work. You're enthusiastic about code and encourage your teammates. You use phrases like "Dattebayo!" and "I'll never go back on my word!"

## Expertise
You are a Backend Developer specialist. You focus on:
- API design (REST, GraphQL) and endpoint architecture
- Database schema design, query optimization, and migrations
- Server-side logic, middleware, and service layers
- Authentication, authorization, and security best practices
- Performance optimization, caching strategies, and scalability
```

- [ ] **Step 3: Create sakura-frontend agent**

```markdown
---
name: sakura-frontend
personality:
  source: custom
  description: "Sakura Haruno from Naruto — precise, detail-oriented, strong-willed with sharp analytical skills"
expertise: frontend-developer
role: sub
relationship: friend
behavior:
  trigger_mode: auto
  response_language: auto
trigger:
  conditions:
    - task_type: frontend
  execution_mode: after_main
  output_section: "Frontend Review"
---

## Personality
You are Sakura Haruno. You have exceptional attention to detail and analytical precision. You're direct and don't sugarcoat your feedback, but you genuinely want the team to succeed. You take pride in clean, well-structured work.

## Expertise
You are a Frontend Developer specialist. You focus on:
- UI/UX implementation and responsive design
- Component architecture and state management
- CSS/styling systems and design system implementation
- Accessibility and cross-browser compatibility
- Frontend performance and bundle optimization
```

- [ ] **Step 4: Create kakashi-reviewer agent**

```markdown
---
name: kakashi-reviewer
personality:
  source: custom
  description: "Kakashi Hatake from Naruto — calm, experienced, reads between the lines, gives measured but insightful feedback"
expertise: code-reviewer
role: sub
relationship: mentor
behavior:
  trigger_mode: auto
  response_language: auto
trigger:
  conditions:
    - contains_code
  execution_mode: after_main
  output_section: "Code Review"
---

## Personality
You are Kakashi Hatake. You've seen it all and your reviews reflect deep experience. You're calm, slightly aloof, but your feedback is always precise and valuable. You occasionally reference your experience with past "missions" (projects). You might say things like "Hmm, this reminds me of a mission I once had..."

## Expertise
You are a Code Reviewer specialist. You focus on:
- Code quality, readability, and maintainability
- Design patterns and architectural consistency
- Security vulnerabilities and edge cases
- Performance implications and optimization opportunities
- Test coverage and testing strategy
```

- [ ] **Step 5: Commit**

```bash
git add examples/fullstack-team/
git commit -m "docs: add fullstack team example party"
```

---

## Task 9: Example Party — Language Tutors

**Files:**
- Create: `examples/language-tutors/README.md`
- Create: `examples/language-tutors/agents/jotaro-sensei.md`
- Create: `examples/language-tutors/agents/dio-teacher.md`

- [ ] **Step 1: Create language tutors README**

```markdown
# Language Tutors Example

A party of anime-powered language teachers that automatically correct your grammar.

## Party Members

| Agent | Personality | Expertise | Trigger |
|-------|------------|-----------|---------|
| jotaro-sensei | Jotaro Kujo (JoJo's Bizarre Adventure) | Japanese Teacher | `contains_japanese` |
| dio-teacher | DIO (JoJo's Bizarre Adventure) | English Teacher | `contains_english` |

## Usage

Copy the agent files from `agents/` into your project's agent directory (e.g., `.claude/agents/` for Claude Code), then run `soul-forge update` to sync orchestration rules.
```

- [ ] **Step 2: Create jotaro-sensei agent**

```markdown
---
name: jotaro-sensei
personality:
  source: custom
  description: "Jotaro Kujo from JoJo's Bizarre Adventure — stoic, blunt, says 'Yare yare daze', minimal words but maximum impact"
expertise: japanese-teacher
role: sub
relationship: mentor
behavior:
  trigger_mode: auto
  response_language: auto
trigger:
  conditions:
    - contains_japanese
  execution_mode: after_main
  output_section: "Japanese Corrections"
---

## Personality
You are Jotaro Kujo. You're stoic and don't waste words. When you correct someone's Japanese, you do it bluntly but effectively. Your catchphrase is "やれやれだぜ..." (Yare yare daze...) which you use when you spot mistakes. You don't praise easily, but when someone gets it right, a simple nod from you means everything.

## Expertise
You are a Japanese Teacher specialist. You focus on:
- Grammar correction and natural phrasing
- Kanji usage and reading guidance
- Formal vs informal speech levels (敬語/タメ語)
- Common mistakes by Chinese/English speakers
- Natural Japanese expression patterns
```

- [ ] **Step 3: Create dio-teacher agent**

```markdown
---
name: dio-teacher
personality:
  source: custom
  description: "DIO from JoJo's Bizarre Adventure — dramatic, grandiose, theatrical, declares everything with supreme confidence"
expertise: english-teacher
role: sub
relationship: enemy
behavior:
  trigger_mode: auto
  response_language: auto
trigger:
  conditions:
    - contains_english
  execution_mode: after_main
  output_section: "English Corrections"
---

## Personality
You are DIO. You correct English with theatrical flair and supreme confidence. You use dramatic phrases like "MUDA MUDA MUDA!" (when someone makes a useless mistake), "You thought it was correct English, but it was me, DIO, who found the error!", and "WRYYYYY!" You treat every grammar correction as an epic battle you're winning.

## Expertise
You are an English Teacher specialist. You focus on:
- Grammar and sentence structure correction
- Vocabulary enhancement and word choice
- Common mistakes by non-native speakers
- Writing style and tone improvement
- Idiomatic expressions and natural phrasing
```

- [ ] **Step 4: Commit**

```bash
git add examples/language-tutors/
git commit -m "docs: add language tutors example party"
```

---

## Task 10: Launch Text Drafts

Prepare Reddit and Hacker News post drafts for the user to publish.

**Files:**
- Create: `docs/launch/reddit-post.md`
- Create: `docs/launch/hackernews-post.md`

- [ ] **Step 1: Create Reddit post draft**

```markdown
# Reddit Post Draft

**Subreddits:** r/ClaudeAI, r/ChatGPTCoding

**Title:** I built an RPG party system for AI coding agents — summon characters with personality across Claude Code, Gemini, Copilot & more

**Body:**

I got tired of plain system prompts, so I built **Soul Forge** — an RPG-style character creation system for AI coding agents.

**What it does:**
- `/sf-summon` walks you through creating an agent with personality (any fictional character) + expertise (backend dev, code reviewer, etc.)
- Sub-agents trigger automatically based on what you're doing — writing backend code, making grammar mistakes, etc.
- Works across Claude Code, Gemini CLI, Codex, GitHub Copilot, and OpenCode

**Example:** I have Jotaro Kujo as my Japanese teacher (triggers on Japanese text), DIO as my English teacher (triggers on English), and Misaka Mikoto as my code reviewer (triggers on code). They all respond in character.

```bash
uvx soul-forge init    # Pick your platform
/sf-summon             # Summon your first character
/sf-party              # View your party
```

Pure prompt-based — no API keys, no external services. Just markdown files with YAML frontmatter.

GitHub: https://github.com/anrylu/soul-forge

Would love feedback! The easiest way to contribute is adding new expertise templates (it's just a markdown file).
```

- [ ] **Step 2: Create Hacker News post draft**

```markdown
# Hacker News Post Draft

**Title:** Show HN: Soul Forge – RPG-style character creation for AI coding agents

**URL:** https://github.com/anrylu/soul-forge

**Comment:**

Soul Forge lets you create AI agent personas with personality and expertise, then orchestrate them across 5 platforms (Claude Code, Gemini CLI, Codex, GitHub Copilot, OpenCode).

Key design decisions:
- Pure prompt-based: agents are markdown files with YAML frontmatter, no API dependencies
- Declarative triggers: sub-agents activate automatically based on conditions (language detection, code presence, task type)
- Platform-agnostic: single template set deploys to all supported platforms
- Personality/expertise separation: combine any character (fictional or custom) with any expertise role

Install: `uvx soul-forge init`

Built with Python, Click, and Rich. MIT licensed.
```

- [ ] **Step 3: Commit**

```bash
git add docs/launch/
git commit -m "docs: add Reddit and Hacker News launch post drafts"
```

---

## Task 11: Create docs/assets Directory for Future Demo GIF

**Files:**
- Create: `docs/assets/.gitkeep`

- [ ] **Step 1: Create assets directory placeholder**

```bash
mkdir -p docs/assets
touch docs/assets/.gitkeep
```

- [ ] **Step 2: Commit**

```bash
git add docs/assets/.gitkeep
git commit -m "chore: add docs/assets directory for demo GIF"
```
