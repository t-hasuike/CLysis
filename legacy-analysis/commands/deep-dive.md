---
description: レガシーシステムの全体像を俯瞰的に分析する。システム相関図・DFD・I/Oインタフェース図を段階的に作成する。
argument-hint: "<分析対象のシステム・サブシステム名>"
---

# /deep-dive — システム深掘り分析

## 概要

レガシーシステムの全体像を俯瞰するためのワークフロー。
legacy-analyze skill の Phase 0-3 を順次実行し、システム相関図・DFD・I/Oインタフェース図を作成する。

## ワークフロー

### Step 1: Phase 0 — 土台構築

**legacy-analyze** skill を適用（Phase 0）:

- Auto-collect from README, docker-compose.yml, dependency management files (.env.example)
- Extract repository roles, technology stack, and dependencies
- Ask 9 clarifying questions about business domain and context
- Generate initial system overview diagram and "Known/Unknown" list

$ARGUMENTS

> **確認**: 「殿、システム概要の把握が完了しました。次の段（相関図）に進んでよろしいか？」

### Step 2: Phase 1 — 具体から掘る

**legacy-analyze** skill を適用（Phase 1 [change theme]）:

- Select a specific change theme (e.g., "add a new product category")
- Trace impact across repositories using /impact-analysis
- Document cross-repository connections, hidden outputs, hardcoded values
- Update system overview diagram and DFD fragments
- Refine "Known/Unknown" list

> **確認**: 「殿、相関図ができました。次の段（DFD）に進んでよろしいか？」

### Step 3: Phase 2 — 監査で嘘を排除

**legacy-analyze** skill を適用（Phase 2）:

- metsuke (Inspector) audits Phase 1 deliverables for accuracy
- Verify all method names, class names, file paths exist
- Cross-check code snippets against actual implementation
- Validate application of project-specific rules (e.g., soft-delete conditions)
- Correct findings and deliver audited artifacts

> **確認**: 「殿、DFDが完成しました。次の段（I/O図）に進んでよろしいか？」

### Step 4: Phase 3 — 抽象に戻す

**legacy-analyze** skill を適用（Phase 3）:

- Integrate Phase 1-2 fragments into three consolidated maps
- Update system overview diagram with new connections
- Add data flows to DFD
- Document I/O interfaces and external connections
- Persist domain knowledge to input/domain/
- Update "Known/Unknown" list

### Step 5: 次の行動の提案

- 「殿、ドメイン知識として蓄積するなら `/build-knowledge` をお使いくだされ」
- 「特定の機能を詳しく調べるなら `/understand` をお使いくだされ」
