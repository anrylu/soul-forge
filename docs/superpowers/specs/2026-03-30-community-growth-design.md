# Soul Forge Community Growth Design

**Goal:** Build open source community influence (GitHub stars, contributors, active community) with minimal effort for maximum impact.

**Strategy:** README改造 + 社群基礎設施 + 一次性發佈，按順序執行。

---

## Phase 1: README 改造（專案即產品頁）

將 README 從技術文件風格改為產品 landing page 風格。

### 1.1 Hero 區塊

- **Tagline:** `Summon AI agents with personality. RPG-style character creation for Claude Code, Gemini, Copilot & more.`
- **Demo GIF:** 緊接 tagline 下方，展示 `/sf-summon` 互動流程到 party 協作輸出
- **Badge 列:** PyPI version、Python version、License、CI status、Platforms supported

### 1.2 「3 步上手」區塊

```bash
uvx soul-forge init    # 選擇你的平台
/sf-summon             # 召喚你的第一個角色
/sf-party              # 查看你的隊伍
```

讓人在 10 秒內知道怎麼開始。

### 1.3 Why Soul Forge（價值主張）

用 3-4 個 bullet point 說明核心賣點，聚焦「這能幫你什麼」而非功能列表：

- 一個 prompt 同時觸發多個專家 agent，各自用不同風格回應
- RPG 角色系統讓 AI agent 管理變得直覺有趣
- 跨 5 個平台統一管理，不被任何工具綁定
- 純 prompt-based，不需要 API key 或外部服務

### 1.4 保留現有內容

現有的 command reference、platform support table、development guide 保留，移到頁面下方。

### 1.5 多語言 README 同步

README.zh-tw.md、README.zh-cn.md、README.ja.md 同步更新相同結構。

---

## Phase 2: 社群基礎設施

### 2.1 GitHub Actions CI

- 單一 workflow：push/PR 時執行 `pytest`
- 目的是讓 CI badge 亮綠燈作為信任指標
- 不需要複雜的 matrix build 或 deploy pipeline

### 2.2 CONTRIBUTING.md

內容：
- 開發環境 setup（uv install, pytest）
- PR 規範（簡潔即可）
- 標明「Good First Issues」方向：
  - 新增 expertise template（只需寫一個 markdown 檔）
  - 新增語言支援
  - 改進現有 template

### 2.3 Issue / PR Templates

- `.github/ISSUE_TEMPLATE/bug-report.md`
- `.github/ISSUE_TEMPLATE/feature-request.md`
- `.github/ISSUE_TEMPLATE/new-template.md`（社群貢獻角色/專業模板）
- `.github/PULL_REQUEST_TEMPLATE.md`

### 2.4 Examples 目錄

`examples/` 放 2-3 個預配好的 party 範例：

- **全端開發隊：** frontend-dev + backend-dev + code-reviewer
- **動漫語言教學隊：** english-teacher + japanese-teacher（用動漫角色人格）

讓新用戶可以直接複製體驗，不需從零開始。

---

## Phase 3: 發佈準備

### 3.1 Demo GIF 錄製

- 使用 terminal 錄製工具（vhs 或 asciinema）
- 30-45 秒流程：`uvx soul-forge init` → `/sf-summon` → party 協作效果
- 同時用於 README hero 和社群發文

### 3.2 發佈文案

**Reddit（r/ClaudeAI, r/ChatGPTCoding）：**
- Show-off 風格，開頭放 GIF
- 強調「用 RPG 的方式管理你的 AI agent 隊伍」
- 附帶簡短使用說明

**Hacker News（Show HN）：**
- 偏技術角度
- 強調：跨平台、pure prompt-based、no API dependency
- 標題格式：`Show HN: Soul Forge – RPG-style character creation for AI coding agents`

### 3.3 明確不做的事

- ❌ 官網/landing page — README 即 landing page
- ❌ Discord/Slack server — 太早，用 GitHub Discussions
- ❌ Blog — 發佈文即第一篇內容
- ❌ 影片 tutorial — GIF 足以傳達核心概念

---

## 執行順序

1. Phase 1（README 改造）→ 2. Phase 2（社群基礎設施）→ 3. Phase 3（發佈準備）

Phase 1 和 Phase 2 可以部分平行，但 Phase 3 必須等前兩者完成。
