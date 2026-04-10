[English](/README.md) | [繁體中文](/README.zh-tw.md) | [简体中文](/README.zh-cn.md) | [日本語](/README.ja.md)

# Soul Forge

**賦予 AI Agent 獨特人格。** RPG 風格角色創建系統，支援 Claude Code、Gemini CLI、Copilot 等平台。

[![PyPI version](https://img.shields.io/pypi/v/agentsoulforge)](https://pypi.org/project/agentsoulforge/)
[![Python](https://img.shields.io/pypi/pyversions/agentsoulforge)](https://pypi.org/project/agentsoulforge/)
[![CI](https://github.com/anrylu/soul-forge/actions/workflows/ci.yml/badge.svg)](https://github.com/anrylu/soul-forge/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 3 步上手

```bash
uvx agentsoulforge init    # 選擇你的平台
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
uvx agentsoulforge init

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
