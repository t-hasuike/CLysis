---
name: project-guide
description: タスクに応じたプロジェクトドキュメントの参照ガイドを提示する。任務開始時・影響調査時に使用。
argument-hint: <タスク概要>
---

> This is a generic skill from [decouple-legacy](https://github.com/t-hasuike/decouple-legacy-skills).
> Terminology can be customized via `config/terminology.md`.

# /project-guide スキル

## 概要

タスクの性質を分析し、input/project/ および input/domain/ から最適な参照順序を提示するガイドスキル。
将軍チームが「今の任務に必要な知識」に最短で辿り着けるようにする。

※ See config/terminology.md for term customization

## 使い方

/project-guide [タスク概要]

### 汎用的な使用例（どのレガシーシステムでも使える）

| 例 | タスク種別 |
|----|-----------|
| /project-guide 注文処理のバグ調査 | バグ修正 |
| /project-guide 新しいAPI エンドポイント追加 | 新機能追加 |
| /project-guide 外部API連携先の仕様変更対応 | 仕様変更 |
| /project-guide バッチ処理の仕様把握 | 調査・分析 |
| /project-guide ローカル開発環境の構築 | 環境構築 |
| /project-guide 重複コードの共通化 | リファクタリング |

### プロジェクト固有の使用例

プロジェクト固有の使用例・キーワードマッピング・注意事項は `PROJECT_EXAMPLES.md` を参照してください。
このファイルはプロジェクトごとに作成し、ドメイン固有の設定を記載します。

## 調査対象

$ARGUMENTS

## 実行手順

### Step 1: タスク種別の判定

タスク概要から以下のいずれかに分類:

| 種別 | 判定基準 |
|------|---------|
| 新機能追加 | カテゴリ追加、画面追加、API追加等 |
| バグ修正 | エラー修正、不具合対応 |
| 仕様変更 | ルール変更、外部API変更 |
| 調査・分析 | 影響調査、仕様把握、コードリーディング |
| 環境構築 | ローカル開発環境、Docker、DB |
| リファクタリング | コード改善、技術的負債解消 |

### Step 2: 参照ガイドの生成

以下のフォーマットで出力:

```
# プロジェクトガイド - [タスク概要]

## 推奨参照順序

### Phase 1: システム理解(必読)
[タスク種別に関わらず必ず提示]
1. input/project/overview.md - プロジェクト全体像
2. input/project/repositories.md - リポジトリ責務の境界

### Phase 2: タスク固有の知識
[タスク種別に応じて動的に選択]

### Phase 3: 実装準備
[該当する場合のみ提示]

### Phase 4: 影響分析
[変更を伴う場合のみ提示]

## 関連ドメイン知識
[input/domain/ から該当するファイルを提示]

## 注意事項
[environment.md の「よくある罠」から該当箇所を抽出]
```

### Step 3: タスク種別ごとのガイドマッピング

#### 新機能追加
- **Phase 2**: environment.md(ビジネスルール)→ service_responsibilities.md(関連Service)→ tech_stack.md(技術制約)
- **Phase 3**: typical_change_patterns.md(類似パターン確認)→ schema_database.md(DB確認)
- **Phase 4**: impact_analysis_template.md → impact_analysis_example.md

#### バグ修正
- **Phase 2**: service_responsibilities.md(原因箇所の特定)→ environment.md(ビジネスルール確認)
- **Phase 3**: schema_database.md(データ確認)→ non_functional_requirements.md(制約確認)
- **Phase 4**: なし(修正範囲が限定的な場合)

#### 仕様変更
- **Phase 2**: environment.md(現行仕様)→ service_responsibilities.md(影響Service)→ diagrams/data_flow.md(データフロー)
- **Phase 3**: typical_change_patterns.md → schema_database.md
- **Phase 4**: impact_analysis_template.md → impact_analysis_example.md

#### 調査・分析
- **Phase 2**: service_responsibilities.md → diagrams/system_overview.md → diagrams/data_flow.md → diagrams/io_interfaces.md
- **Phase 3**: schema_database.md → environment.md
- **Phase 4**: なし

#### 環境構築
- **Phase 2**: local_dev.md → tech_stack.md
- **Phase 3**: なし
- **Phase 4**: なし
- **補足**: input/local_dev/ 配下の詳細ナレッジを参照

#### リファクタリング
- **Phase 2**: service_responsibilities.md(責務確認)→ non_functional_requirements.md(制約)→ todo_list.md(既知課題)
- **Phase 3**: typical_change_patterns.md → schema_database.md
- **Phase 4**: impact_analysis_template.md

### Step 4: ドメイン知識のマッピング

タスク概要のキーワードに基づき、input/domain/ から関連ファイルを提示する。

**プロジェクト固有のマッピング**: `PROJECT_EXAMPLES.md` にキーワード→ファイルのマッピングを定義してください。

### Step 5: 注意事項の抽出

environment.md の「よくある罠・注意点」セクションから、タスクに関連する注意事項を抽出して提示。

**共通注意事項(常に提示)**:
- プロジェクト固有のソフトデリート条件（例: delflag='0'）を全クエリに含める
- プロジェクト固有の型安全ルール（例: PHP strict_types）の確認
- 複数リポジトリの重複コード同期

**プロジェクト固有の注意事項**: `PROJECT_EXAMPLES.md` に記載してください。

## ドキュメント品質評価との連携

タスク完了後、output/ に出力したドキュメントを input/assessment/legacy_document_quality.md の基準で評価することを推奨。

**「次の行動に移せる」5Wチェック**:
- **What**: 変更対象を特定できている
- **Where**: ファイルパス:行番号を把握できている
- **How**: 実装方法を判断できている
- **Risk**: 影響範囲・副作用を評価できている
- **Next**: Phase分割した計画がある

## 報告形式

```
# プロジェクトガイド - [タスク概要]

> **タスク種別**: [新機能追加 / バグ修正 / 仕様変更 等]
> **作成日**: YYYY-MM-DD

---

## 推奨参照順序

### Phase 1: システム理解(必読)
1. `input/project/overview.md` - プロジェクト全体像
2. `input/project/repositories.md` - リポジトリ責務の境界

### Phase 2: タスク固有の知識
1. `input/project/environment.md` - [参照理由]
2. `input/project/service_responsibilities.md` - [参照理由]
...

### Phase 3: 実装準備
1. `input/project/typical_change_patterns.md` - [参照理由]
2. `input/project/schema_database.md` - [参照理由]
...

### Phase 4: 影響分析
1. `input/project/impact_analysis_template.md` - [参照理由]
2. `input/project/impact_analysis_example.md` - [参照理由]

---

## 関連ドメイン知識

- `input/domain/xxx.md` - [関連理由]

---

## 注意事項

### 共通(必須)
- プロジェクト固有のソフトデリート条件（例: delflag='0'）を全クエリに含める
- プロジェクト固有の型安全ルール（例: PHP strict_types）必須
- 複数リポジトリの重複コード同期

### タスク固有
- [タスク固有の注意事項を environment.md から抽出]
```

## 禁止事項

- 推測でドキュメントを指定しない(実際に input/ 配下を確認してから提示)
- ファイル変更を行わない(ガイド提示が主任務)

---

## I/O仕様

### INPUT
| 種別 | 内容 | 必須/任意 | 例 |
|------|------|-----------|-----|
| タスク概要 | 実施するタスクの説明 | 必須 | `注文処理のバグ調査`, `新APIエンドポイント追加` |

### OUTPUT
| 種別 | 形式 | 出力先 |
|------|------|--------|
| 参照ガイド | ドキュメント参照順序・関連ファイル一覧 | stdout（将軍への報告） |

### 前提条件
- input/project/ のドキュメントが存在すること
- input/domain/ のドメイン知識が存在すること

### 後続スキル（パイプライン）
- `/investigate` — ガイドで特定した対象の詳細調査
- `/service-spec` — ガイドで特定したServiceの仕様作成
- `/impact-analysis` — ガイドで特定した影響範囲の分析

### 品質チェックポイント
- [ ] タスク種別を正しく分類したか
- [ ] 参照順序に論理的な根拠があるか
- [ ] 関連するドメイン知識を漏れなく提示したか
