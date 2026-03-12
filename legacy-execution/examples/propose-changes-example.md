# /propose-changes 使用例

## シナリオ: Express Shipping 機能追加 - Phase 0（基盤整備）

### 前提

1. `/impact-analysis` で影響分析レポートが作成済み
   - ファイルパス: `output/impact_reports/add_express_shipping.md`
   - Phase 0 で ShippingMethod Enum 作成、OrderService 修正が必要と判明

### 実行

```
/propose-changes output/impact_reports/add_express_shipping.md Phase 0
```

### 出力例

`output/proposals/add_express_shipping_phase0.md` に以下の修正提案書が生成される:

---

```markdown
# Express Shipping 追加 修正提案書 - Phase 0

**作成日**: 2026-03-08
**対象リポジトリ**: my-ecommerce-app
**元レポート**: `output/impact_reports/add_express_shipping.md`

---

## 修正概要

ShippingMethod Enum を作成し、OrderService のハードコードされた配送方法を動的取得に変更する。

---

## 修正内容一覧

### 修正1: ShippingMethod Enum 作成

**ファイルパス**: `app/Enums/ShippingMethod.php`（新規）
**影響度**: 高
**修正理由**: 配送方法のハードコードを排除し、一元管理する

#### 修正内容（新規ファイル）

```php
<?php

declare(strict_types=1);

namespace App\Enums;

enum ShippingMethod: string
{
    case STANDARD = 'standard';
    case EXPRESS = 'express';    // 新規追加

    public static function getAll(): array
    {
        return array_map(fn($case) => $case->value, self::cases());
    }

    public function getDeliveryDays(): int
    {
        return match($this) {
            self::STANDARD => 5,
            self::EXPRESS => 2,
        };
    }
}
```

#### テスト方針

- **ユニットテスト**: getAll() が全配送方法を返すことを検証
- **ユニットテスト**: getDeliveryDays() が正しい日数を返すことを検証

---

### 修正2: OrderService - 配送方法の動的取得化

**ファイルパス**: `app/Services/OrderService.php`
**影響度**: 高
**修正理由**: ハードコード配列を Enum からの動的取得に変更

#### 修正前のコード（該当箇所）

```php
// 行番号: 45-48
private const SHIPPING_METHODS = ['standard'];

public function getDeliveryDays(string $method): int
{
    return $method === 'standard' ? 5 : 3;
}
```

#### 修正後のコード（diff形式）

```diff
--- a/app/Services/OrderService.php
+++ b/app/Services/OrderService.php
@@ -1,6 +1,7 @@
 <?php

 namespace App\Services;
+use App\Enums\ShippingMethod;

 class OrderService
 {
@@ -45,9 +46,9 @@
-    private const SHIPPING_METHODS = ['standard'];
-
-    public function getDeliveryDays(string $method): int
+    public function getAvailableMethods(): array
     {
-        return $method === 'standard' ? 5 : 3;
+        return ShippingMethod::getAll();
+    }
+
+    public function getDeliveryDays(string $method): int
+    {
+        $shippingMethod = ShippingMethod::from($method);
+        return $shippingMethod->getDeliveryDays();
     }
```

#### 影響範囲

| 影響箇所 | 変更内容 | リスク評価 |
|---------|---------|-----------|
| OrderController::create() | getAvailableMethods() の呼び出しに変更 | 中 |
| CheckoutService::validate() | SHIPPING_METHODS 定数の参照を変更 | 中 |

#### テスト方針

- **ユニットテスト**: getAvailableMethods() が Enum から取得することを検証
- **統合テスト**: OrderController が新しい配送方法を受け付けることを確認

---

## 修正順序（依存関係）

```
1. ShippingMethod Enum 作成
   ↓
2. OrderService 修正（Enum を使用）
   ↓
3. OrderController 修正（Phase 1 で対応）
```

---

## 承認チェックリスト

- [x] 全ての修正箇所にdiffを提示したか
- [x] 修正理由が明確か
- [x] 影響範囲を分析したか
- [x] テスト方針が具体的か
- [x] リスク・副作用を洗い出したか
- [x] 修正順序が適切か

---

## 次のアクション

1. **上様のご裁可**: この修正提案書をレビュー・承認
2. **`/create-pr` 起動**: 承認後、この提案書を入力として PR 作成
```

---

### ポイント

- diff 形式で修正前後が一目瞭然
- 修正理由・影響範囲・テスト方針が各修正に紐づく
- 人間が承認してから次工程（/create-pr）に進む
- 根幹思想「AIが提示、人が確認」を体現
