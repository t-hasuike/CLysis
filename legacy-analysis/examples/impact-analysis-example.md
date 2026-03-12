# /impact-analysis Example

## Scenario: New Feature Impact Analysis

### INPUT

```
/impact-analysis 新しい配送方法（エクスプレス配送）の追加
```

### OUTPUT

```
「上様、影響分析レポートを献上いたします。

# ADR: エクスプレス配送機能の追加

> **Status**: Proposed
> **Date**: 2026-03-06
> **Decision Makers**: Team Lead, Product Manager

## Context

現在の配送方法は「通常配送（3-5日）」「速達配送（1-2日）」の2種類。
顧客から「当日配送」の要望が多く、競合他社も対応済み。
新たに「エクスプレス配送（当日）」を追加する。

---

## Decision

ShippingService に Express配送ロジックを追加し、以下を実装:

1. 配送方法の追加（shipping_methods テーブル）
2. 配送料金計算ロジックの拡張
3. 在庫確保・配送業者API連携
4. UI: 購入フロー内での配送方法選択肢追加

---

## Consequences

### 影響範囲（ファイル一覧）

#### バックエンド
| File | Impact | Change Type |
|------|--------|-------------|
| `app/Services/Shipping/ShippingService.php` | 高 | Method追加: `calculateExpressFee()` |
| `app/Services/Order/OrderService.php` | 中 | Express配送時の在庫確保ロジック追加 |
| `database/migrations/2026_03_06_add_express_shipping.php` | 高 | shipping_methods テーブルにレコード追加 |
| `app/Models/ShippingMethod.php` | 低 | 定数追加: `TYPE_EXPRESS = 'express'` |
| `app/Http/Controllers/CheckoutController.php` | 中 | API レスポンスに配送方法追加 |

#### フロントエンド
| File | Impact | Change Type |
|------|--------|-------------|
| `resources/js/components/Checkout/ShippingOptions.tsx` | 高 | Express配送の選択肢追加（UI/UX） |
| `resources/js/api/shipping.ts` | 中 | API型定義更新: `ShippingMethod` enum |

#### インフラ
| File | Impact | Change Type |
|------|--------|-------------|
| `config/shipping.php` | 中 | 配送業者API設定追加（Express専用） |
| `.env.example` | 低 | 環境変数追加: `EXPRESS_SHIPPING_API_KEY` |

---

### リスク

| Risk | Severity | Mitigation |
|------|----------|------------|
| 配送業者APIのレート制限 | 高 | リトライ機構 + キャッシュ導入 |
| 在庫切れ時の顧客体験悪化 | 中 | リアルタイム在庫チェック + UI警告表示 |
| 配送料金計算の複雑化 | 低 | Strategy pattern適用で保守性確保 |

---

### 実装計画

#### Phase 1: バックエンド実装（1週間）
- [ ] Migration作成・実行
- [ ] ShippingService拡張
- [ ] 配送業者API連携（サンドボックス）
- [ ] Unit tests作成

#### Phase 2: フロントエンド実装（3日）
- [ ] UI/UX設計レビュー
- [ ] ShippingOptions コンポーネント更新
- [ ] E2E tests作成

#### Phase 3: 統合テスト（2日）
- [ ] ステージング環境デプロイ
- [ ] QA実施（配送料金計算・在庫連携）
- [ ] パフォーマンステスト

#### Phase 4: 本番リリース（1日）
- [ ] Feature flag有効化（段階的ロールアウト）
- [ ] モニタリング設定（配送業者API成功率）
- [ ] ロールバック手順確認

---

### 代替案

#### Alternative 1: 外部配送業者のみ対応（自社配送は対象外）
- Pros: 実装コスト削減（50%減）
- Cons: 顧客体験の一貫性低下

#### Alternative 2: 特定地域のみ提供
- Pros: リスク低減、段階的展開
- Cons: 機能利用可否が複雑化（郵便番号チェック必要）

**決定**: 全地域・全配送業者で対応（Alternative案は採用せず）

---

以上、報告完了でござる。」
```

### Notes

- Use `/impact-analysis [Feature Description]` for new features or architecture changes
- Output follows ADR (Architecture Decision Record) format
- Includes file-level impact assessment with severity indicators
- Provides implementation plan with phases
- Useful for sprint planning and technical design reviews
