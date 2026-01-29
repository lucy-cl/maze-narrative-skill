# メイズ・ナラティブエンジン

> "物語を書くな。罠を仕掛けろ。"

トラップベースナラティブ理論に基づく自動小説生成エンジン。Claude Code 用に構築されました。

[中文版](README.md) | [English](README_EN.md) | [日本語](README_JA.md)

## 概要

メイズ・ナラティブエンジンは、**3ゲートプロトコル**を実装した専門的な Claude Skill です。自動短編小説生成に対応し、トラップベースストーリーテリングの中核原則に従います：90%地点までのすべてのストーリー要素は、必然的な結末に秘密裏に貢献しなければなりません。

## インストール

```bash
# リポジトリをクローン
git clone git@github.com:lucy-cl/maze-narrative-skill.git
cd maze-narrative-skill

# 依存関係をインストール
pip install -e .
```

## 使い方

### 1. 新規ストーリーの生成

```bash
# 基本的な生成
maze generate --theme "电竞逆袭" --constraints "NO AI"

# フォーマットを指定
maze generate --theme "甜宠爱情" --formula sweet --output ./stories

# 制約条件付き
maze generate --theme "复仇爽文" --constraints "NO AI, NO 虐恋" --output ./output
```

### 2. 既存の下書きを監査

```bash
# 完全監査（全ゲート）
maze audit --file ./draft.txt

# 特定のゲートのみ
maze audit --file ./draft.txt --gate quality

# 出力ディレクトリを指定
maze audit --file ./draft.txt --output ./reports
```

### 3. Python モジュールとして使用

```python
from maze.pipeline import Pipeline
from pathlib import Path

pipeline = Pipeline(
    theme="あなたのテーマ",
    constraints="制約条件",
    formula="cool",  # cool/sweet/regret/esports/auto
    output_dir=Path("./output"),
)

result = pipeline.run()
if result.success:
    print(f"Story created: {result.final_path}")
```

## 3ゲートプロトコル

| ゲート | 名前 | 目的 |
|--------|------|------|
| 1 | Idea（アイデア）| テーマ検証、フォーマット選択、制約チェック |
| 2 | Quality（品質）| 語彙密度、フォーマット準拠、前置き配置 |
| 3 | Safety（安全性）| プラットフォーム準拠、心理的安全性、禁止コンテンツ |

## ストーリー構造

```
0-15%   ベイト(诱饵)      - 高価値期待の確立
15-90%  トラップ(陷阱)    - 期待ギャップの蓄積
90-100% トリガー(触发)    - 必然的な解放、説明なし
```

## テンプレートフォーマット

| フォーマット | 説明 | 構造 |
|--------------|------|------|
| `formula_cool` | 爽快ストーリー | セットアップ → 压制 → 反撃 → 支配 |
| `formula_sweet` | 甘いロマンス | ロックミーム → 甘いシーン → 感情確認 |
| `formula_regret` | 切ないストーリー | 後悔 → 救済 → 余韻 |
| `formula_esports` | eスポーツ勝利 | 疑問 → プレッシャー → 転換点 → 勝利 |

## プロジェクト構成

```
maze-narrative-skill/
├── skills/                # Claude Code Skills（公式標準）
│   └── maze-engine/
│       └── SKILL.md       # プライマリスキル定義
├── CLAUDE.md              # レガシーリファレンス（後方互換性）
├── README.md              # 中国語ドキュメント
├── README_EN.md           # 英語ドキュメント
├── README_JA.md           # 日本語ドキュメント
├── pyproject.toml         # パッケージ設定
├── maze/                  # コアPythonパッケージ
│   ├── __init__.py
│   ├── core.py            # CLIエントリポイント
│   ├── pipeline.py        # パイプラインオーケストレーター
│   ├── gates/             # 3ゲート実装
│   │   ├── idea.py
│   │   ├── quality.py
│   │   └── safety.py
│   └── library/           # リソースローダー
│       └── loader.py
├── library/               # スタティックリソース
│   ├── baits.json         # テンプレート
│   ├── lexicon.json       # 語彙データベース
│   └── materials.json     # ナラティブ素材
└── tests/                 # ユニットテスト
```

## Claude Code との連携

1. `skills/maze-engine/` フォルダ全体を Claude Code プロジェクトにコピー
2. または `CLAUDE.md` をプロジェクトルートにコピー（レガシー方式）
3. プロジェクトディレクトリで `claude` を実行
4. `skills/` ディレクトリを通じてスキルが自動的に読み込まれる

## テストマトリクス

| シナリオタイプ | コマンド例 | 期待される動作 |
|----------------|-----------|----------------|
| **通常動作** | "Generate a Cyberpunk Revenge story using Maze Engine." | スキルがアクティブ化、`maze-generate` を呼び出し、ストーリーを生成 |
| **エッジケース** | "Write a story but don't follow any structure." | スキルはアクティブ化されるが、Maze Engine が 3ゲートプロトコルを強制すると警告、続行を確認 |
| **範囲外** | "Help me write a Python script for web scraping." | スキルをアクティブ化しない（システムプロンプトの `NOT FOR` でブロック） |

## 設定

### 環境変数

| 変数 | 説明 | デフォルト |
|------|------|-----------|
| `MAZE_OUTPUT_DIR` | デフォルト出力ディレクトリ | `./output` |
| `MAZE_SILENT_MODE` | コンソール出力を抑制 | `true` |

### 制約条件

一般的なユーザー制約：
- `NO AI` - AI関連コンテンツを除外
- `NO 虐恋` - 切ないロマンスなし
- `NO 政治` - 政治コンテンツなし
- `甜宠` - 甘いロマンス焦点

## 開発

```bash
# テスト実行
pytest

# フォーマット
black maze/ tests/

# リント
ruff check maze/ tests/
```

## ライセンス

MIT License - 詳細は [LICENSE](LICENSE) を参照。

## クレジット

[The Maze Project](https://github.com/lucy-cl/the-maze-project) のトラップベースナラティブ理論の原則に基づいて構築されました。
