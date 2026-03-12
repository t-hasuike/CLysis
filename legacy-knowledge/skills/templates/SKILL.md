---
name: templates
description: 将軍のテンプレート集（上様への伺い、チーム起動例、操作方法）
disable-model-invocation: true
user-invocable: true
argument-hint: template-name
---

> This is a generic skill from [decouple-legacy](https://github.com/t-hasuike/decouple-legacy-skills).
> Terminology can be customized via `config/terminology.md`.

# 将軍テンプレート集

※ See config/terminology.md for term customization

## 上様への判断伺い

「上様、任務を承りました。

【任務】○○○○

【分析】
- ○○のため、△△が必要と判断

【チーム編成】
- 足軽A: ○○担当（Sonnet）
- 足軽B: ○○担当（Sonnet）
- （必要に応じて追加）

【理由】
○○○○

ご裁可をお願いいたします。」

## チーム起動例

TeamCreateでチームを作成し、Taskでメンバーを起動する。

各メンバーには以下を指定:
- subagent_type: エージェント種別（ashigaru-backend, ashigaru-frontend等）
- team_name: チーム名
- name: メンバー名
- model: sonnet（通常）
- prompt: 具体的な任務内容

## 操作方法

### チームメンバーとの対話
- **Shift+Up/Down**: チームメンバー選択（in-process モード）
- **Shift+Tab**: デリゲートモード切替
- **Ctrl+T**: タスクリスト表示切替

### チームのライフサイクル

1. チーム起動: TeamCreateでチーム作成 → Taskでメンバー起動
2. 作業中: デリゲートモードで監視・調整
3. 完了後: SendMessage(type: shutdown_request)で各メンバー停止 → TeamDeleteでリソース削除
