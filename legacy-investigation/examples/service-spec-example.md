# /service-spec Example

## Scenario: Detailed Service Specification

### INPUT

```
/service-spec PaymentService
```

### OUTPUT

```
「上様、PaymentService の仕様書を作成いたしました。

# PaymentService 仕様サマリー

> **Version**: 1.0
> **Last Updated**: 2026-03-06
> **File**: app/Services/Payment/PaymentService.php

## 概要
PaymentService は決済処理の責務を担うサービスクラスでござる。
クレジットカード・銀行振込・電子マネーの3種類に対応。

## 公開メソッド

### 1. processPayment(Order $order, PaymentMethod $method): PaymentResult

**責務**: 決済実行（外部ゲートウェイ連携）

**パラメータ**:
- `$order`: Order entity
- `$method`: PaymentMethod value object (type: card/bank/emoney)

**戻り値**: PaymentResult（成功/失敗 + transactionId）

**処理フロー**:
1. 決済方法に応じてGateway選択（Strategy pattern）
2. Gateway::charge() 実行
3. 結果をpayments テーブルに記録
4. PaymentResult 返却

**例外**:
- PaymentGatewayException: ゲートウェイエラー
- InsufficientFundsException: 残高不足
- InvalidPaymentMethodException: 未対応決済方法

---

### 2. refund(int $paymentId, ?float $amount = null): RefundResult

**責務**: 返金処理

**パラメータ**:
- `$paymentId`: 返金対象の決済ID
- `$amount`: 返金額（nullの場合は全額）

**戻り値**: RefundResult（成功/失敗 + refundId）

**処理フロー**:
1. 元決済情報を取得
2. 返金可能期限チェック（決済後90日以内）
3. Gateway::refund() 実行
4. refunds テーブルに記録

**例外**:
- RefundExpiredException: 返金期限切れ
- AlreadyRefundedException: 既に返金済み

---

### 3. validateCard(string $cardNumber): ValidationResult

**責務**: クレジットカード番号検証（Luhnアルゴリズム）

**パラメータ**:
- `$cardNumber`: カード番号（ハイフンなし16桁）

**戻り値**: ValidationResult（valid/invalid + brand: Visa/MasterCard/JCB）

**処理フロー**:
1. Luhnチェックサム検証
2. カードブランド判定（先頭桁）
3. ValidationResult 返却

**例外**: なし（バリデーション失敗時は result->isValid = false）

---

## 依存関係

### 外部サービス連携
- `StripeGateway`: クレジットカード決済
- `BankTransferGateway`: 銀行振込
- `PayPayGateway`: 電子マネー（QRコード決済）

### リポジトリ
- `PaymentRepository`: payments テーブル操作
- `RefundRepository`: refunds テーブル操作

### 内部サービス
- `LoggingService`: 決済ログ記録（監査証跡）

---

## 特記事項

1. **冪等性保証**: 同一orderId + requestId での重複決済を防止（DB UNIQUE制約）
2. **リトライ機構**: ゲートウェイタイムアウト時は3回まで自動リトライ（指数バックオフ）
3. **PCI DSS準拠**: カード番号は暗号化して保存（at rest encryption）
4. **監査ログ**: すべての決済・返金操作を payment_logs テーブルに記録

---

## テストカバレッジ
- Unit tests: 92%
- Integration tests: 85%
- Critical path: 100%（決済・返金フロー）

以上、報告完了でござる。」
```

### Notes

- Use `/service-spec [ServiceName]` for detailed documentation
- Output includes all public methods with parameters, return values, exceptions
- Useful for API documentation or architectural reviews
- Can be saved to `output/` directory for team reference
