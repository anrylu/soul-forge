[English](/README.md) | [繁體中文](/README.zh-tw.md) | [简体中文](/README.zh-cn.md) | [日本語](/README.ja.md)

# Soul Forge

RPGスタイルのAI Agentキャラクター作成システム。パーソナリティ、専門分野、自動トリガー連携でAI Agentペルソナを作成・設定・オーケストレーション。

## 特徴

- **RPGキャラクター作成** — インタラクティブなウィザードでパーソナリティ＋専門分野を持つAgentを鍛造
- **マルチAgent連携** — メインAgent＋サブAgent、宣言的トリガー条件付き
- **マルチプラットフォーム対応** — Claude Code、Gemini CLI、Codex、GitHub Copilot、OpenCode
- **パーソナリティソース** — プリセットスタイル、URL/キャラクター抽出、カスタム記述
- **8種類の専門テンプレート** — バックエンド、フロントエンド、DevOps、コードレビュー、QA、アーキテクチャ、英語、日本語

## クイックスタート

```bash
# プロジェクトにインストール
uvx soul-forge init

# AI Agentプラットフォームを選択後、スラッシュコマンドを使用：
/sf-summon     # 新しいキャラクターを作成
/sf-party      # Agentの一覧を表示
```

## インストール

```bash
# uvx経由（推奨）
uvx soul-forge init

# またはグローバルインストール
pip install soul-forge
soul-forge init
```

## CLIコマンド

| コマンド | 説明 |
|----------|------|
| `soul-forge init` | 対象プラットフォームにコマンドをインストール |
| `soul-forge update` | コマンドを更新しオーケストレーションを同期 |
| `soul-forge platforms` | サポートプラットフォームの一覧 |
| `soul-forge template list` | 利用可能なテンプレートの一覧 |
| `soul-forge template add <url\|path>` | カスタムテンプレートを追加 |

## スラッシュコマンド

インストール後、AI Agentで以下のコマンドが使用可能：

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

### 1. キャラクター作成

`/sf-summon` でウィザードを進行：

1. **パーソナリティソース** — プリセット、URL＋キャラクター抽出、カスタム
2. **専門分野** — バックエンド、フロントエンド、DevOps、コードレビュアー、QA、アーキテクト、英語/日本語教師、カスタム
3. **命名** — 自動提案またはカスタム
4. **役割** — メインAgentまたはサブAgent
5. **関係性** — 師匠、友人、敵、ライバル、従者、先輩、後輩、パートナー、カスタム
6. **応答言語** — 自動（会話に合わせる）、中国語、英語、日本語
7. **トリガーモード** — 自動または手動（サブAgentのみ）
8. **微調整** — オプションの態度オーバーライド
9. **保存先** — プロジェクトレベルまたはグローバル

### 2. パーティの例

アニメキャラクターで構成されたAgentチーム：

| Agent | パーソナリティ | 専門分野 | 関係性 | トリガー |
|-------|---------------|----------|--------|----------|
| jotaro-sensei | 空条承太郎（ジョジョの奇妙な冒険） | 日本語教師 | 師匠 | `contains_japanese` |
| dio-teacher | DIO（ジョジョの奇妙な冒険） | 英語教師 | 敵 | `contains_english` |
| josuke-backend | 東方仗助（ジョジョ第4部） | バックエンド開発 | 友人 | `task_type: backend` |
| misaka-reviewer | 御坂美琴（とある科学の超電磁砲） | コードレビュアー | ライバル | `contains_code` |

### 3. 自動オーケストレーション

自動トリガー付きのサブAgentは条件に基づいて起動。例えば「幫我寫一個 REST API for user authentication」と聞くと：

```
[メイン応答]
ユーザー認証のREST API設計です...

---

[バックエンドレビュー — josuke-backend]
グレートだぜ！俺がキレイに直してやるよ。
認証エンドポイントはbcryptでパスワードハッシュすべきだし、
/loginにレート制限も忘れんなよ...

---

[コードレビュー — misaka-reviewer]
ふん、悪くはないわね... でも3つ問題を見つけたわ。
別にアンタのためにやってるわけじゃないんだからね。
1. クエリビルダーにSQLインジェクションのリスク
2. メール形式の入力バリデーションが未実装
3. JWTシークレットは環境変数から取得すべき、ハードコードはダメ

---

[日本語 — jotaro-sensei]
「幫我寫」は中国語だな。日本語では：
「ユーザー認証用のREST APIを書いてください」
やれやれだぜ...「寫」じゃなくて「書いて」だ。

---

[英語 — dio-teacher]
You thought you could write English without me, DIO?
MUDA MUDA MUDA!
"Help me write a REST API for user authentication"
- "Help me write" not "幫我寫" — you SHALL speak English!
```

### 4. Agentファイル形式

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

## 対応プラットフォーム

| プラットフォーム | コマンドパス | 設定ファイル |
|-----------------|-------------|-------------|
| Claude Code | `.claude/commands/` | `CLAUDE.md` |
| Gemini CLI | `.gemini/commands/` | `GEMINI.md` |
| Codex | `.codex/commands/` | `AGENTS.md` |
| GitHub Copilot | `.github/copilot/commands/` | `.github/copilot-instructions.md` |
| OpenCode | `.opencode/commands/` | `AGENTS.md` |

## 開発

```bash
git clone https://github.com/anrylu/soul-forge.git
cd soul-forge
uv venv && uv pip install -e .
uv run pytest -v
```

## ライセンス

MIT
