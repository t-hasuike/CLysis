---
name: build-knowledge
description: 調査結果からドメイン知識を抽出し、input/domain/ に体系的に蓄積する。コードレビュー・調査完了後のナレッジ定着に使用。
argument-hint: <調査結果の要約 or ファイルパス> [カテゴリ]
---

# /build-knowledge スキル

> This is a generic skill from [decouple-legacy](https://github.com/t-hasuike/decouple-legacy-skills).
> Terminology can be customized via `config/terminology.md`.

## 概要

調査結果（/investigate, /service-spec, /impact-analysis, /code-review の出力）からドメイン知識を抽出し、`input/domain/` 配下にファイルとして蓄積する。

**重要**: ドメイン知識はプロジェクト固有の情報であり、Publicリポジトリには含まれない。各プロジェクトの `input/domain/` で独自管理する。

## なぜこのスキルが必要か

調査やレビューで得た知見は、その場限りで消えがち。このスキルにより:
- 調査結果を**再利用可能なドメイン知識**として定着させる
- 次回の調査・レビュー・実装時に**事前知識として参照**できる
- チーム全体の**ドメイン理解を蓄積・共有**できる

## 対象

$ARGUMENTS

## カテゴリ一覧

| カテゴリ | 内容 | ファイル命名例 |
|---------|------|-------------|
| business-rules | ビジネスルール・業務ロジック | `order_validation_rules.md` |
| data-structure | データ構造・DB設計・Enum定義 | `product_categories.md` |
| integration | 外部API連携・外部サービス仕様 | `payment_gateway_spec.md` |
| architecture | システム構成・Service責務・依存関係 | `service_responsibilities.md` |
| constraints | 技術的制約・既知の制限事項 | `legacy_constraints.md` |

## 実行手順

### Step 1: 調査結果の分析

入力された調査結果から以下を抽出:
- **確定した仕様・ビジネスルール**（推測ではなく確認済みの事実）
- **発見されたパターン**（コードの慣例、暗黙のルール）
- **制約・制限事項**（技術的制約、外部サービスの制限）

### Step 2: 既存ドメイン知識の確認

`input/domain/` 配下の既存ファイルを検索し、重複を回避:

```
input/domain/
├── [既存ファイル一覧を確認]
└── 新規作成 or 既存更新を判断
```

**判断基準**:
- 既存ファイルのスコープに含まれる → **既存ファイルに追記**
- 既存ファイルのスコープ外 → **新規ファイルを作成**
- 判断に迷う → 将軍（リーダー）に確認

### Step 3: ドメイン知識ファイルの生成・更新

#### 新規作成の場合

以下のフォーマットで `input/domain/` にファイルを作成:

```markdown
# [ドメイン知識タイトル]

> **Category**: [business-rules / data-structure / integration / architecture / constraints]
> **Created**: YYYY-MM-DD
> **Last Updated**: YYYY-MM-DD
> **Source**: [調査元（PR番号、調査レポート名等）]

## 概要

[1-3文の要約]

## 詳細

[ビジネスルール・仕様・データ構造等の詳細]

### [サブセクション]

[必要に応じてサブセクションで構造化]

## 注意事項

[使用時の注意点、例外ケース等]

## 変更履歴

| 日付 | 内容 | Source |
|------|------|--------|
| YYYY-MM-DD | 初版作成 | [調査元] |
```

#### 既存更新の場合

1. 既存ファイルの適切なセクションに追記
2. `Last Updated` を更新
3. 変更履歴に追記

### Step 4: 品質チェック

- [ ] 推測ではなく、確認済みの事実のみを記載したか
- [ ] 既存のドメイン知識と矛盾していないか（矛盾があれば将軍に報告）
- [ ] カテゴリ分類は適切か
- [ ] 他のスキル（/investigate, /code-review等）から参照しやすい形式か

## 報告形式

```
# ドメイン知識蓄積レポート

## 蓄積内容

| 操作 | ファイル | カテゴリ | 内容 |
|------|---------|---------|------|
| 新規作成 | input/domain/xxx.md | business-rules | ○○のビジネスルール |
| 追記 | input/domain/yyy.md | data-structure | △△のデータ構造追記 |

## 抽出元
- [調査レポート名 or PR番号]

## 次回の調査・レビューへの示唆
- [この知識が活きる場面の提案]
```

## パイプラインでの位置づけ

```
/investigate or /service-spec or /code-review
  → 調査・レビュー完了
  ↓
/build-knowledge [調査結果の要約]
  → ドメイン知識として定着
  ↓
次回の /investigate or /code-review
  → input/domain/ から事前知識として参照
```

**推奨タイミング**:
- コードレビュー完了後（新しいビジネスルールが判明した時）
- 影響分析完了後（システム構成・制約が明確になった時）
- 調査完了後（暗黙のルール・パターンを発見した時）

## 禁止事項

- 推測・未確認の情報をドメイン知識として記録しない
- 個人の感想・意見をドメイン知識に含めない
- コードのコピペをドメイン知識にしない（概念・ルールを抽出）

---

## I/O仕様

### INPUT
| 種別 | 内容 | 必須/任意 | 例 |
|------|------|-----------|-----|
| 調査結果 | スキル出力 or 要約テキスト | 必須 | `/investigate の出力`, `PR#123のレビューで判明した価格ルール` |
| カテゴリ | ドメイン知識のカテゴリ | 任意 | `business-rules`, `data-structure` |

### OUTPUT
| 種別 | 形式 | 出力先 |
|------|------|--------|
| ドメイン知識ファイル | Markdown | `input/domain/` 配下に新規作成 or 既存更新 |
| 蓄積レポート | Markdown | stdout（将軍への報告） |

### 前提条件
- `input/domain/` ディレクトリが存在すること
- 調査結果が確認済みの事実に基づいていること

### 後続スキル（パイプライン）
- なし（ドメイン知識は他の全スキルから参照される）

### 品質チェックポイント
- [ ] 確認済みの事実のみを記載したか
- [ ] 既存ドメイン知識と矛盾していないか
- [ ] カテゴリ分類は適切か
- [ ] 参照元（Source）を明記したか
