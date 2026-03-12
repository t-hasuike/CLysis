---
description: レガシーシステムの影響調査を体系的に実行する。project-guide → investigate → service-spec → impact-analysis のスキルチェーンを順次実行する。
argument-hint: "<変更内容の説明>"
---

# /investigate-flow — 影響調査フロー

## 概要

新機能追加・仕様変更時に、影響範囲を体系的に調査するワークフロー。
4つのスキルを順次実行し、最終的にADR形式の影響分析レポートを出力する。

## ワークフロー

### Step 1: 参照ガイドの取得

**project-guide** skill を適用:

- タスク概要を分析し、参照すべきドキュメントの順序を特定する
- input/project/ および input/domain/ から最適な参照順序を提示する

$ARGUMENTS

> **確認**: 「殿、参照ガイドを整えました。次の段（調査）に進んでよろしいか？」

### Step 2: コードベース調査

**investigate** skill を適用:

- Step 1 で特定したドキュメントを事前に読み込む
- 対象のクラス・機能を Serena のシンボリック検索で探索する
- ファイルパス:行番号を明記した調査報告を作成する

> **確認**: 「殿、調査結果が揃いました。次の段（仕様整理）に進んでよろしいか？」

### Step 3: Service仕様の整理

**service-spec** skill を適用:

- Step 2 で発見した高影響 Service の仕様を詳細に整理する
- メソッド一覧・依存関係・ビジネスルールを文書化する
- 複数 Service にまたがる場合は **service-spec (CROSS)** skill も適用する

> **確認**: 「殿、仕様の整理が完了しました。次の段（影響分析）に進んでよろしいか？」

### Step 4: 影響分析

**impact-analysis** skill を適用:

- Step 2-3 の結果をもとに、ADR形式の影響分析レポートを作成する
- リスク評価・Phase分割した実装計画を含む

### Step 5: 次の行動の提案

- 「殿、修正に着手されるなら `/implement` をお使いくだされ」
- 「さらに深掘りが必要であれば `/deep-dive` をお使いくだされ」
- 「ドメイン知識として蓄積するなら `/build-knowledge` をお使いくだされ」
