---
name: legacy-analyze
description: レガシーコードを「具体⇔抽象の反復」で段階的に理解するためのスキル。3つの地図（システム鳥瞰図・DFD・I/Oインターフェース）を「作る」のではなく「育てる」アプローチ。
argument-hint: "Phase 0 | Phase 1 [変更テーマ] | Phase 2 | Phase 3"
---

# /legacy-analyze — レガシーコード攻略スキル

> This is a generic skill from [decouple-legacy](https://github.com/t-hasuike/decouple-legacy-skills).
> Terminology can be customized via `config/terminology.md`.

## 概要
レガシーコードを「具体⇔抽象の反復」で段階的に理解するためのスキル。
3つの地図（システム鳥瞰図・DFD・I/Oインターフェース）を「作る」のではなく「育てる」アプローチ。

※ See config/terminology.md for term customization

## 前提条件
- プロジェクト基本情報（overview.md, repositories.md, tech_stack.md）が存在すること
  - デフォルト: `input/project/` 配下
  - 拡張構成: `knowledge/system/` 配下（5段階フェーズ構成）
- 図の管理場所が存在すること
  - デフォルト: `input/project/diagrams/`
  - 拡張構成: `knowledge/system/02_structure/` および `knowledge/system/03_behavior/`
- schema.duckdb（DBスキーマ）が利用可能であること

## Phase 0: 土台構築（初回のみ）

### 目的
コードから読み取れる「揺るがない事実」を自動収集し、人間に聞くべき最小限の質問を導き出す。

### 手順

**Step 1: 自動収集（人間の入力不要）**
各リポジトリの以下を自動収集:
- README.md
- docker-compose.yml / Dockerfile
- .env.example（.envは除外 — セキュリティ）
- 依存性管理ファイル（composer.json / package.json / go.mod / build.gradle 等）
- ルートディレクトリのファイル構成
- routes/（APIエンドポイント構成）

DBスキーマ（schema.duckdb）があればテーブル一覧・外部キー関係も抽出。

**Step 2: 「わかったこと」の整理**
自動収集から判明する情報を整理:
- 各リポジトリの技術スタック（フレームワーク、言語バージョン）
- 各リポジトリの役割（READMEから）
- リポジトリ間の連携の手がかり（.env.exampleのAPI_URL等）
- バッチ・インフラ系の構成

※ 検証結果: README/composer.json/package.json等から、全体の約65〜73%の情報が自動で判明する。

**Step 3: 「わからないこと」を質問として提示**
自動収集では判明しないビジネス文脈を、以下の9項目の質問として人間に提示:

```
以下の9項目を教えてください。残りは自動収集済みです:

1. サービスのビジネスドメイン（1〜2文で）
   → 何を誰に提供するサービスか

2. 対象ユーザーの呼称と具体的役割
   → READMEに「○○向け」という記述がありましたが、
     各ユーザーの具体的な役割を教えてください

3. ドメイン固有の用語の意味
   → 自動収集で見つかった固有名詞（プラン名等）の意味

4. ユーザー種別ごとの業種・属性
   → 「パートナー」等の呼称が指す具体的な業種

5. 重要度の評価
   → どのリポジトリが最重要か、変更頻度が高いか

6. レガシーシステムの位置づけ
   → 旧システムの移行状況、現在も使われているか

7. リポジトリ間連携方式の補足
   → 自動推定できなかった連携の確認

8. 組織名・ブランド名の文脈
   → READMEに登場する固有名詞の正式な意味

9. 本番ドメインの対応表（任意）
   → 各サービスが稼働しているURL
```

**Step 4: overview.md + 鳥瞰図の初版生成**
Step 2（自動収集結果）+ Step 3（人間の回答）を統合して:
- overview.md の初版を生成
- システム鳥瞰図の初版（mermaid）を生成
- 「わかったこと」リスト
- 「まだわからないこと」リスト（※これが最重要 -- Phase 1 で掘る対象）

### 重要な原則
- Step 1-2 は人間の入力なしで実行可能
- Step 3 の質問は自動収集結果に基づいて動的に生成する（固定質問ではない）
- 「何を聞けばいいかもわからない」状態を、AIが構造化する

## Phase 1: 具体から掘る（反復の核）

### 目的
具体的な変更テーマを1つ選び、芋づる式に追跡する。追跡の副産物として地図の断片を得る。

### 手順
1. ユーザーが変更テーマを指定（例:「新しい商品カテゴリを追加したい」）
2. /impact-analysis で影響範囲を追跡
3. 追跡過程で発見した以下を記録:
   - リポジトリ間連携（API呼び出し、共有DB、共有Enum等）
   - 隠れた出力（メール、CSV、バッチ処理、外部API連携）
   - ハードコード箇所
   - 技術的負債
4. 関連Serviceを /service-spec で仕様整理
5. リポジトリ横断の場合は /service-spec (CROSS) で差分分析
6. 出力:
   - 影響分析レポート（reports/ または output/）
   - 鳥瞰図の更新差分
   - DFDの断片
   - 「わからないこと」リストの更新（解決したもの/新たに出たもの）

### 重要な原則
- 「ありそうな名前」でコードを記述しない。必ずSerenaで実在を確認する
- 修正例は実コードの構造を確認してから書く
- 馴染みの薄いリポジトリは事前に /service-spec で全体像を把握してから組み込む

## Phase 2: 監査で嘘を排除

### 目的
Phase 1の成果物の正確性を検証する。AIはハルシネーションする。

### 手順
1. metsuke（目付役）が成果物を監査
2. 検証項目:
   - 全メソッド名・クラス名が実在するか
   - 全ファイルパスが正しいか
   - コードスニペットが実際のコードと一致するか
   - プロジェクト固有の必須ルール（例: 論理削除条件）の考慮漏れがないか
3. 指摘を修正し、再監査
4. 出力: 監査済みの成果物（修正反映済み）

## Phase 3: 抽象に戻す

### 目的
Phase 1-2で得た断片を統合し、3つの地図を更新する。知識を永続化する。

### 手順
1. 影響分析で判明した連携・フローを鳥瞰図に追加
2. データの流れをDFDに追加
3. 各システムの入口・出口をI/Oインターフェース図に追加
4. ドメイン知識をドメイン知識ディレクトリに永続化（書記が担当）
   - デフォルト: `input/domain/`
   - 拡張構成: `knowledge/domain/`
5. 「わかったこと/わからないこと」リストを更新
6. 出力:
   - 図の管理場所の3つの図を更新
   - ドメイン知識ディレクトリに新規知識を追加

### Phase 3 必須化ルール

**Phase 1-2 の調査完了後、Phase 3（地図更新）を必ず実施すること。**

調査のみで終わると、知見がセッション内に閉じてしまい、次回以降の調査で同じ領域を再度掘ることになる。Phase 3 で地図とドメイン知識を更新することで:
- 次回の Phase 1 の起点が前進する
- 「わからないこと」リストが縮小する
- チーム全体の理解が蓄積される

## 反復
Phase 1-3 を別の変更テーマで繰り返す。繰り返すほど:
- 3つの地図の精度が上がる
- 「わからないこと」リストが縮小する
- 2つ目以降は「あ、ここも同じパターン」が効き始め、速度が上がる

## チーム編成テンプレート

### 中規模（標準）
| 役割 | 担当 | モデル |
|------|------|--------|
| 足軽A | コード追跡・影響分析（investigator） | Sonnet |
| 足軽B | 知識整理・図の更新（scribe） | Sonnet |

### 大規模（リポジトリ横断）
| 役割 | 担当 | モデル |
|------|------|--------|
| 足軽A | リポジトリA側調査（investigator） | Sonnet |
| 足軽B | リポジトリB側調査（investigator） | Sonnet |
| 足軽C | 知識統合・図更新（scribe） | Sonnet |
| metsuke | 品質監査（Phase 2で起用） | Sonnet |

## エージェントパターン対応表
| パターン | 実装形態 | Phase |
|---------|---------|-------|
| Advanced RAG | schema.duckdb + Serena | 全Phase |
| ReAct | /investigate, /service-spec | Phase 1 |
| Self-Reflection | metsuke監査 | Phase 2 |
| Multi-Agent | 将軍+足軽チーム | Phase 1-3 |
| Plan-and-Execute | /impact-analysis + Phase分割 | Phase 1 |
| Knowledge Graph Memory | domain knowledge dir + diagrams/ | Phase 3 |
| Sequential Chain | Phase 0→1→2→3の反復 | 全体 |

---

## I/O仕様

### INPUT
| 種別 | 内容 | 必須/任意 | 例 |
|------|------|-----------|-----|
| Phase | Phase 0, 1, 2, or 3 | 必須 | `Phase 0`, `Phase 1` |
| 変更テーマ | Specific change theme (Phase 1 only) | Phase 1で必須 | `新しい商品カテゴリを追加したい` |
| 調査対象 | Target repositories or features | 任意 | `backend`, `注文処理機能` |

### OUTPUT
| 種別 | 形式 | 出力先 |
|------|------|--------|
| Phase 0 成果物 | overview.md + システム鳥瞰図 + わかったこと/わからないことリスト | プロジェクト情報ディレクトリ（`input/project/` or `knowledge/system/`） |
| Phase 1 成果物 | 影響分析レポート + Service仕様 + DFD断片 + わからないことリスト更新 | `reports/`（or `output/`）, 図の管理場所 |
| Phase 2 成果物 | 監査済み成果物（修正反映済み） | `reports/` (updated) |
| Phase 3 成果物 | 更新された3つの地図 + ドメイン知識 | 図の管理場所, ドメイン知識ディレクトリ |

### 前提条件
- Serena MCP が起動していること
- Phase 0: リポジトリにアクセス可能であること
- Phase 1-3: Phase 0 完了済みであること

### 後続スキル（パイプライン）
Phase 0 → Phase 1 → Phase 2 → Phase 3 → (Phase 1に戻って反復)

### 品質チェックポイント
- [ ] Phase 0: 自動収集で65-73%の情報を得たか
- [ ] Phase 1: 実コードを確認してから報告したか（推測ではなく）
- [ ] Phase 2: 全メソッド名・クラス名が実在するか検証したか
- [ ] Phase 3: ドメイン知識をドメイン知識ディレクトリに永続化したか
