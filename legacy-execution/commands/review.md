---
description: Pull Requestのコード品質・ビジネスロジック整合性をレビューする。project-guide → code-review のスキルチェーンを実行する。
argument-hint: "<PR番号> <リポジトリ名>"
---

# /review — PRレビューフロー

## 概要

PRのコード品質とビジネスロジックの整合性をレビューするワークフロー。

## ワークフロー

### Step 1: コンテキストの準備

**project-guide** skill を適用:

- PRレビューに必要なドメイン知識・プロジェクト情報を特定する
- input/domain/ から関連するドメイン知識を事前に読み込む

$ARGUMENTS

> **確認**: 「殿、レビューの準備が整いました。レビューに進んでよろしいか？」

### Step 2: コードレビュー

**code-review** skill を適用:

- コード品質（可読性・保守性・セキュリティ）を評価する
- ビジネスロジックの整合性を検証する
- 承認（Approve）/ 修正要求（Request Changes）/ コメント（Comment）の判断を下す

### Step 3: 次の行動の提案

- 「殿、修正が必要な場合は `/implement` で修正提案を作成できます」
