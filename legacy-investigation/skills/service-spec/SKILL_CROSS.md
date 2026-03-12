---
name: service-spec (CROSS)
description: Cross-repository service specification analysis. Documents features spanning multiple repositories, focusing on data flow, synchronization points, and consistency rules.
argument-hint: <Feature name> <Repository A> <Repository B>
---

> This is a generic skill from [decouple-legacy](https://github.com/t-hasuike/decouple-legacy-skills).
> Terminology can be customized via `config/terminology.md`.

# [機能名：例 一括処理] 横断仕様サマリー

## 1. ビジネスドメイン概要
[この機能が解決するビジネス上の課題と、全体像を3行で]
- **主な登場人物 (Actors)**: システム管理者、エンドユーザー、外部システム
- **関連ドメイン**: input/domain/ 配下のドメイン知識

## 2. システム構成・コンポーネント図

| コンポーネント | リポジトリ | 主要な役割 |
|--------------|-----------|-----------|
| `OrderService` | backend | 注文データの集約・判定 |
| `NotificationSync` | frontend   | フロントへの通知 |

---

## 3. 横断処理フロー（シーケンス）
1. **[Core]** `ProcessingService::execute()` が対象データを抽出
2. **[Core]** `DataModel` を更新し、処理指示を作成
3. **[API]** 外部APIへリクエスト
4. **[Frontend]** Webhook経由で `UpdateService` を叩き、ステータス同期

---

## 4. 影響範囲・依存関係（マトリクス）
[既存の「依存しているクラス」を機能単位に拡張]

### 関連Service/Model一覧
- [ ] `app/Services/Processing/MainService.php` (ロジック核)
- [ ] `app/Models/Data.php` (Scope: `eligibleForProcessing` 追加)

---

## 5. データの整合性と差分（重要）
- **Source of Truth**: ステータスは `backend` が保持
- **同期タイミング**: 処理完了時に非同期Jobで `frontend` へ反映
- **不整合時の挙動**: Backend側を優先し、Frontend側は再同期バッチでリカバリ

---

## 6. 特記事項・技術的負債
[既存の「ハードコード」「負債」セクションをそのまま利用]

---

## I/O仕様

### INPUT
| 種別 | 内容 | 必須/任意 | 例 |
|------|------|-----------|-----|
| 機能名 | Cross-repository feature name | 必須 | `一括処理`, `Order sync` |
| リポジトリA | First repository | 必須 | `backend`, `core` |
| リポジトリB | Second repository | 必須 | `frontend`, `api` |

### OUTPUT
| 種別 | 形式 | 出力先 |
|------|------|--------|
| 横断仕様サマリー | Cross-repository specification document with data flow, sync points, and consistency rules | stdout（将軍への報告） |

### 前提条件
- Serena MCP が起動していること
- 両方のリポジトリにアクセス可能であること
- /investigate または /service-spec で各リポジトリの単体仕様を把握済みであること推奨

### 後続スキル（パイプライン）
- `/impact-analysis` — Cross-repository change impact analysis
- `/build-knowledge` — Persist cross-repository patterns to domain knowledge

### 品質チェックポイント
- [ ] データの整合性ルールを明記したか
- [ ] Source of Truthを明確にしたか
- [ ] 同期タイミング・不整合時の挙動を記載したか
- [ ] 両リポジトリの実装を確認したか（推測ではなく）
