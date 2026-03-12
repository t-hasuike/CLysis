# /build-knowledge Example

## Scenario: Knowledge Base Update

### INPUT

```
/build-knowledge コードレビューで判明した割引計算のビジネスルール

Context:
- PR#123のレビューで、割引計算ロジックが3箇所に分散していることが判明
- ビジネスルールが暗黙知化しており、ドキュメント化が必要
- DiscountService, OrderService, CheckoutController で異なる計算式
```

### OUTPUT

```
「上様、ドメイン知識を蓄積いたしました。

【作業】新規作成
【対象ファイル】input/domain/discount_rules.md

【内容】
- 割引計算の3つのビジネスルール整理
- コード散在箇所の特定
- 統一化推奨事項

【判断理由】
既存の pricing_methods.md は価格設定の種類のみ記載。
割引計算ロジックは別ドメインと判断し、新規ファイル作成。

---

# 割引計算ルール

> **Version**: 1.0
> **Last Updated**: 2026-03-06
> **Source**: PR#123 Code Review

## 概要

割引は「顧客ランク」「注文金額」「キャンペーン」の3要素で決定される。
現状、計算ロジックが3箇所に分散しており、統一が必要。

---

## ビジネスルール

### 1. 顧客ランク別割引率

| ランク | 割引率 | 備考 |
|--------|--------|------|
| 一般 | 0% | デフォルト |
| シルバー | 5% | 累計購入額10万以上 |
| ゴールド | 10% | 累計購入額50万以上 |

### 2. 注文金額による追加割引

| 条件 | 追加割引 |
|------|---------|
| 注文金額 >= 10,000 | +2% |
| 注文金額 >= 50,000 | +5% |
| 注文金額 >= 100,000 | +8% |

### 3. キャンペーン割引の併用ルール

| 条件 | 適用 |
|------|------|
| ランク割引 + 金額割引 | 併用可（加算） |
| ランク割引 + キャンペーン割引 | 高い方のみ適用 |
| 最大割引率 | 20%を上限とする |

---

## 現状の実装箇所

### 分散している計算ロジック

| File | Line | 計算内容 | 問題点 |
|------|------|---------|-------|
| `DiscountService.php` | 145-180 | ランク割引 + 金額割引 | キャンペーン割引未考慮 |
| `OrderService.php` | 234-256 | キャンペーン割引判定のみ | ランク割引を考慮せず |
| `CheckoutController.php` | 89-102 | 最終割引計算(API応答) | ロジック重複(DiscountService呼び出すべき) |

### 問題の影響

1. **不整合リスク**: 3箇所で異なる計算式 → 顧客に誤った割引表示の可能性
2. **保守性低下**: ルール変更時に3ファイル修正必要
3. **テスト困難**: 統一されたテストケースが作成できない

---

## 推奨事項

### 1. 単一責務化

DiscountService に割引計算を集約:

```php
class DiscountService
{
    public function calculateDiscount(
        CustomerRank $rank,
        Money $orderTotal,
        ?Campaign $campaign
    ): Percentage {
        $rankDiscount = $this->getRankDiscount($rank);
        $amountDiscount = $this->getAmountDiscount($orderTotal);
        $campaignDiscount = $this->getCampaignDiscount($campaign);

        $baseDiscount = $rankDiscount->add($amountDiscount);
        $finalDiscount = max($baseDiscount, $campaignDiscount);

        return min($finalDiscount, Percentage::of(20)); // 上限20%
    }
}
```

### 2. ルールの外部化

割引ルールを `config/discount.php` に定義:

```php
return [
    'rank_discounts' => [
        'general' => 0,
        'silver' => 5,
        'gold' => 10,
    ],
    'amount_discounts' => [
        10000 => 2,
        50000 => 5,
        100000 => 8,
    ],
    'max_discount_rate' => 20,
];
```

### 3. テスト戦略

統一されたテストケースを作成:

```php
public function test_discount_for_silver_rank_customer()
{
    // Given: シルバーランク、注文金額8,000円
    // When: calculateDiscount() 実行
    // Then: 5%（ランク割引のみ）
}

public function test_discount_cap_at_maximum()
{
    // Given: ゴールドランク、注文金額100,000円、キャンペーン15%
    // When: calculateDiscount() 実行
    // Then: 20%（上限適用）
}
```

---

## バージョン履歴

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-03-06 | 初版作成(PR#123レビュー結果) |

---

以上、報告完了でござる。」
```

### Notes

- Use `/build-knowledge [Topic/Context]` to create or update domain knowledge
- Output is saved to `input/domain/` directory
- Includes business rules, implementation status, and recommendations
- Useful for onboarding, knowledge sharing, and preventing knowledge loss
- Knowledge base grows iteratively with each code review/investigation
