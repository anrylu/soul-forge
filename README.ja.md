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
