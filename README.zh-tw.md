[English](/README.md) | [繁體中文](/README.zh-tw.md) | [简体中文](/README.zh-cn.md) | [日本語](/README.ja.md)

# Soul Forge

RPG 風格的 AI Agent 角色創建系統。透過人格、專長與自動觸發協作，創建、設定並協調 AI Agent 角色。

## 特色

- **RPG 角色創建** — 互動式精靈引導，打造具有人格 + 專長的 Agent
- **多 Agent 協作** — 主 Agent + 子 Agent，搭配宣告式觸發條件
- **多平台支援** — Claude Code、Gemini CLI、Codex、GitHub Copilot、OpenCode
- **人格來源** — 預設風格、URL/角色擷取、或自訂描述
- **8 種內建專長模板** — 後端、前端、DevOps、Code Review、QA、架構、英文、日文

## 快速開始

```bash
# 安裝到你的專案
uvx soul-forge init

# 選擇 AI Agent 平台後，使用斜線指令：
/sf-summon     # 創建新角色
/sf-party      # 查看角色名單
```

## 安裝

```bash
# 透過 uvx（推薦）
uvx soul-forge init

# 或全域安裝
pip install soul-forge
soul-forge init
```

## CLI 指令

| 指令 | 說明 |
|------|------|
| `soul-forge init` | 安裝指令到目標平台 |
| `soul-forge update` | 更新指令並同步協調設定 |
| `soul-forge platforms` | 列出支援的平台 |
| `soul-forge template list` | 列出可用模板 |
| `soul-forge template add <url\|path>` | 新增自訂模板 |

## 斜線指令

安裝後，可在 AI Agent 中使用以下指令：

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

### 1. 創建角色

`/sf-summon` 引導你完成創角精靈：

1. **人格來源** — 預設風格、URL + 角色擷取、或自訂
2. **專長** — 後端、前端、DevOps、Code Reviewer、QA、架構師、英文/日文老師、或自訂
3. **命名** — 自動建議或自訂
4. **角色定位** — 主 Agent 或子 Agent
5. **關係** — 師傅、朋友、敵人、對手、僕從、前輩、後輩、搭檔、或自訂
6. **回應語言** — 自動（依對話內容）、中文、英文、或日文
7. **觸發模式** — 自動或手動（僅子 Agent）
8. **微調** — 可選態度覆蓋
9. **存放位置** — 專案級或全域

### 2. 範例隊伍

一支動漫角色驅動的 Agent 團隊：

| Agent | 人格 | 專長 | 關係 | 觸發條件 |
|-------|------|------|------|----------|
| jotaro-sensei | 空條承太郎（JoJo 的奇妙冒險） | 日文老師 | 師傅 | `contains_japanese` |
| dio-teacher | DIO（JoJo 的奇妙冒險） | 英文老師 | 敵人 | `contains_english` |
| josuke-backend | 東方仗助（JoJo 第四部） | 後端開發 | 朋友 | `task_type: backend` |
| misaka-reviewer | 御坂美琴（科學超電磁砲） | Code Reviewer | 對手 | `contains_code` |

### 3. 自動協作

子 Agent 會根據觸發條件自動啟動。假設你問：「幫我寫一個 REST API for user authentication」

```
[主回應]
以下是使用者認證的 REST API 設計...

---

[後端審查 — josuke-backend]
グレートだぜ！讓我來好好修一下。
你的認證端點應該用 bcrypt 做密碼雜湊，
別忘了在 /login 加上速率限制...

---

[程式碼審查 — misaka-reviewer]
哼，還不差啦... 但我找到 3 個問題。
才不是為了你才做的呢。
1. 查詢建構器有 SQL 注入風險
2. 缺少 email 格式的輸入驗證
3. JWT secret 應該從環境變數取得，不要寫死

---

[日文 — jotaro-sensei]
「幫我寫」は中国語だな。日本語では：
「ユーザー認証用のREST APIを書いてください」
やれやれだぜ...「寫」じゃなくて「書いて」だ。

---

[英文 — dio-teacher]
You thought you could write English without me, DIO?
MUDA MUDA MUDA!
"Help me write a REST API for user authentication"
- "Help me write" not "幫我寫" — you SHALL speak English!
```

### 4. Agent 檔案格式

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

## 支援平台

| 平台 | 指令路徑 | 設定檔 |
|------|----------|--------|
| Claude Code | `.claude/commands/` | `CLAUDE.md` |
| Gemini CLI | `.gemini/commands/` | `GEMINI.md` |
| Codex | `.codex/commands/` | `AGENTS.md` |
| GitHub Copilot | `.github/copilot/commands/` | `.github/copilot-instructions.md` |
| OpenCode | `.opencode/commands/` | `AGENTS.md` |

## 開發

```bash
git clone https://github.com/anrylu/soul-forge.git
cd soul-forge
uv venv && uv pip install -e .
uv run pytest -v
```

## 授權

MIT
