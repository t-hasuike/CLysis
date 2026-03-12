# /investigate Example

## Scenario: Service Investigation

### INPUT

```
/investigate OrderService
```

### OUTPUT

```
「上様、調査報告でござる。

【任務】OrderService の仕様調査

【調査対象】
- File: app/Services/Order/OrderService.php
- Lines: 1-450
- Dependencies: 8 services, 3 repositories

【概要】
OrderService は注文処理の中核を担うサービスでござる。
注文作成・更新・キャンセル・状態管理を一元的に処理。

【主要メソッド】
1. createOrder(array $orderData): Order
   - 注文新規作成
   - 在庫チェック + 価格計算 + 決済処理を連携
   - Transaction内で実行

2. updateOrderStatus(int $orderId, string $status): bool
   - 注文ステータス更新
   - 状態遷移ルールを検証（pending→confirmed→shipped→delivered）
   - 不正な遷移は例外送出

3. cancelOrder(int $orderId, string $reason): bool
   - 注文キャンセル処理
   - 決済返金 + 在庫復元を実行
   - キャンセル期限チェック（発送後は不可）

4. calculateTotal(array $items): Money
   - 合計金額計算
   - 商品価格 + 配送料 + 税金
   - クーポン・ポイント割引適用

【依存関係】
- PaymentService: 決済処理委譲
- InventoryService: 在庫管理委譲
- ShippingService: 配送手配委譲
- OrderRepository: DB永続化
- NotificationService: 顧客通知

【特記事項】
- すべてのDB操作はトランザクション内で実行
- キャンセル処理は状態によって分岐（未発送/発送済み）
- エラー時はOrderException→ログ記録→ロールバック
- ステータス遷移は有限オートマトン（FSM）で管理

【懸念点】
- 1メソッドが250行（createOrder） → 分割推奨
- PaymentServiceとの密結合 → インターフェース化検討余地あり

以上、報告完了でござる。」
```

### Notes

- Use `/investigate [ServiceName]` for initial exploration
- Output follows Service仕様サマリー format
- Useful for onboarding or legacy code understanding
- Can be customized with additional flags (e.g., `/investigate OrderService --focus=security`)
