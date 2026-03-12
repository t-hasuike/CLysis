# Full Workflow Example

## Scenario: Adding New Payment Method (QR Code Payment)

This example demonstrates an end-to-end workflow using all skills sequentially.

---

## Phase 1: Project Guidance

### INPUT

```
/project-guide QRコード決済の追加
```

### OUTPUT

```
「上様、参照先を特定いたしました。

【任務】QRコード決済の追加

【参照すべきファイル】
1. input/project/repositories.md → 決済機能の責務境界確認
2. input/domain/payment_methods.md → 既存決済方法の仕様
3. app/Services/Payment/PaymentService.php → 決済処理のコア実装

【調査順序】
1. /investigate PaymentService → 現状把握
2. /service-spec PaymentService → 詳細仕様確認
3. /impact-analysis QRコード決済追加 → 影響範囲分析

以上、報告完了でござる。」
```

---

## Phase 2: Investigation

### INPUT

```
/investigate PaymentService
```

### OUTPUT (Abbreviated)

```
「上様、PaymentService の調査完了でござる。

【概要】
- 現在サポート: クレジットカード、銀行振込
- Strategy pattern 採用（Gateway抽象化）
- 新規決済方法追加は GatewayInterface 実装で可能

【主要メソッド】
- processPayment(): 決済実行
- refund(): 返金処理
- validatePaymentMethod(): 決済方法検証

【依存関係】
- StripeGateway (クレジットカード)
- BankTransferGateway (銀行振込)
- PaymentRepository (DB永続化)

【拡張ポイント】
QRコード決済は新規 QRCodeGateway 実装で対応可能。

以上、報告完了でござる。」
```

---

## Phase 3: Service Specification

### INPUT

```
/service-spec PaymentService
```

### OUTPUT (Abbreviated)

```
「上様、PaymentService 仕様書を作成いたしました。

# PaymentService 仕様サマリー

## 公開メソッド

### processPayment(Order $order, PaymentMethod $method): PaymentResult

**処理フロー**:
1. GatewayFactory::make($method->type) でGateway取得
2. Gateway::charge($order->total) 実行
3. PaymentRepository::save() で記録
4. PaymentResult 返却

**拡張方法**:
新規Gateway追加時:
1. GatewayInterface 実装
2. GatewayFactory に登録
3. PaymentMethod enum に追加

## 依存関係
[詳細略]

以上、報告完了でござる。」
```

---

## Phase 4: Impact Analysis

### INPUT

```
/impact-analysis QRコード決済（PayPay）の追加
```

### OUTPUT (Abbreviated)

```
「上様、影響分析レポートを献上いたします。

# ADR: QRコード決済機能の追加

## Decision

PayPayを決済方法として追加。PayPayGateway を実装し、既存アーキテクチャに統合。

## Consequences

### 影響範囲

#### バックエンド
| File | Impact | Change Type |
|------|--------|-------------|
| `app/Gateways/PayPayGateway.php` | 高 | 新規作成（GatewayInterface実装） |
| `app/Services/Payment/GatewayFactory.php` | 中 | PayPay登録 |
| `app/Models/PaymentMethod.php` | 低 | ENUM追加: `PAYPAY = 'paypay'` |
| `database/migrations/2026_03_06_add_paypay.php` | 高 | payment_methods テーブル更新 |

#### フロントエンド
| File | Impact | Change Type |
|------|--------|-------------|
| `resources/js/components/Checkout/PaymentOptions.tsx` | 高 | QRコード表示UI追加 |
| `resources/js/api/payment.ts` | 中 | PayPay API型定義追加 |

### リスク

| Risk | Severity | Mitigation |
|------|----------|------------|
| PayPay API障害時の顧客体験悪化 | 高 | Fallback UI + 管理者通知 |
| QRコード有効期限切れ | 中 | 自動リフレッシュ機構 |

### 実装計画

#### Phase 1: PayPayGateway実装（3日）
- [ ] PayPay API連携（サンドボックス）
- [ ] QRコード生成・検証ロジック
- [ ] Unit tests（決済成功/失敗/タイムアウト）

#### Phase 2: UI実装（2日）
- [ ] QRコード表示コンポーネント
- [ ] リアルタイム決済ステータス更新（WebSocket）

#### Phase 3: 統合テスト（2日）
- [ ] E2E tests
- [ ] パフォーマンステスト（QRコード生成時間）

以上、報告完了でござる。」
```

**【Human Checkpoint】**

上様に影響分析レポート（output/impact_analysis_paypay.md）を提出し、承認をいただく。

---

## Phase 5: Propose Changes

### INPUT

```
/propose-changes output/impact_analysis_paypay.md
```

### OUTPUT (Abbreviated)

```
「上様、修正提案を献上いたします。

# PayPay決済追加 修正提案

**元レポート**: output/impact_analysis_paypay.md
**提案日**: 2026-03-08

## 変更サマリー

- PayPayGateway 新規作成
- GatewayFactory への PayPay 登録
- PaymentMethod enum へ PAYPAY 追加
- PaymentOptions UI への QRコード表示追加

---

## 修正内容（diff形式）

### 1. app/Gateways/PayPayGateway.php（新規作成）

```diff
+ <?php
+ declare(strict_types=1);
+
+ namespace App\Gateways;
+
+ use App\Contracts\GatewayInterface;
+ use App\ValueObjects\Money;
+ use App\Models\Order;
+
+ class PayPayGateway implements GatewayInterface
+ {
+     public function charge(Order $order, Money $amount): PaymentResult
+     {
+         // QRコード生成ロジック
+         $qrCode = $this->paypayClient->createQRCode([
+             'amount' => $amount->toInt(),
+             'orderId' => $order->id,
+         ]);
+
+         return new PaymentResult(
+             success: true,
+             transactionId: $qrCode->codeId,
+             metadata: ['qr_code_url' => $qrCode->url]
+         );
+     }
+
+     public function refund(string $transactionId, Money $amount): bool
+     {
+         // 返金処理
+     }
+ }
```

### 2. app/Services/Payment/GatewayFactory.php

```diff
  public function make(string $type): GatewayInterface
  {
      return match ($type) {
          'credit_card' => new StripeGateway(),
          'bank_transfer' => new BankTransferGateway(),
+         'paypay' => new PayPayGateway(),
          default => throw new UnsupportedPaymentMethodException(),
      };
  }
```

### 3. app/Models/PaymentMethod.php

```diff
  enum PaymentMethod: string
  {
      case CREDIT_CARD = 'credit_card';
      case BANK_TRANSFER = 'bank_transfer';
+     case PAYPAY = 'paypay';
  }
```

### 4. resources/js/components/Checkout/PaymentOptions.tsx

```diff
+ import { QRCodeDisplay } from '../Payment/QRCodeDisplay';
+
  export const PaymentOptions = () => {
    const [selectedMethod, setSelectedMethod] = useState<PaymentMethod>('credit_card');
+   const [qrCodeUrl, setQRCodeUrl] = useState<string | null>(null);

    return (
      <div>
        <select onChange={(e) => setSelectedMethod(e.target.value)}>
          <option value="credit_card">クレジットカード</option>
          <option value="bank_transfer">銀行振込</option>
+         <option value="paypay">PayPay</option>
        </select>

+       {selectedMethod === 'paypay' && qrCodeUrl && (
+         <QRCodeDisplay url={qrCodeUrl} expiresIn={300} />
+       )}
      </div>
    );
  };
```

---

## レビューポイント

- [ ] PayPayGateway のエラーハンドリングは十分か
- [ ] QRコード有効期限（5分）の UI 表示は適切か
- [ ] Webhook署名検証の実装は含まれているか
- [ ] テストケースは網羅的か

以上、報告完了でござる。」
```

**【Human Checkpoint】**

上様に修正提案を確認いただき、承認をいただく。

---

## Phase 6: Create PR

### INPUT

```
/create-pr output/propose_changes_paypay.md backend
```

### OUTPUT (Abbreviated)

```
「上様、PR作成完了でござる。

【作業内容】
1. ブランチ作成: feature/add-paypay-payment
2. コード修正: 提案diff通りに実装
3. コミット: "Add PayPay payment gateway integration"
4. PR作成: #456

【PR URL】
https://github.com/your-org/backend/pull/456

【PR内容】
# PayPay決済ゲートウェイ追加

## Summary
- PayPayGateway 実装
- GatewayFactory に PayPay 登録
- PaymentMethod enum に PAYPAY 追加
- QRコード表示 UI 追加

## Test Plan
- [ ] Unit tests (PayPayGatewayTest)
- [ ] Integration tests (決済フロー E2E)
- [ ] Manual QA (サンドボックス環境で QRコード決済実行)

## Related
- Impact Analysis: output/impact_analysis_paypay.md
- Change Proposal: output/propose_changes_paypay.md

以上、報告完了でござる。」
```

**【Human Checkpoint】**

上様が PR をレビュー・承認し、マージを指示する。

---

## Phase 7: Build Knowledge

### INPUT

```
/build-knowledge PayPay決済のビジネスルールと実装パターン

Context:
- 影響分析で判明した実装パターンをドメイン知識として蓄積
- 今後のQRコード決済（LINE Pay, d払い等）追加時の参考資料
```

### OUTPUT (Abbreviated)

```
「上様、ドメイン知識を蓄積いたしました。

【作業】新規作成
【対象ファイル】input/domain/qr_code_payment_rules.md

【内容】
- QRコード決済の共通パターン
- PayPay固有の仕様
- セキュリティ要件

# QRコード決済ルール

## 共通パターン

すべてのQRコード決済は以下フローに従う:

1. QRコード生成リクエスト（サーバー → 決済プロバイダ）
2. QRコード表示（UI）
3. 顧客がスマホアプリでスキャン
4. 決済完了通知（Webhook）
5. 注文ステータス更新

## PayPay固有仕様

- QRコード有効期限: 5分
- リトライ: 3回まで（指数バックオフ）
- Webhook署名検証必須（HMAC-SHA256）

## セキュリティ要件

- QRコードに注文IDを含めない（ワンタイムトークンのみ）
- Webhook受信時は署名検証 + IPホワイトリスト
- 決済完了後、QRコードを無効化

以上、報告完了でござる。」
```

---

## Summary: Full Workflow

| Phase | Skill | Purpose | Output |
|-------|-------|---------|--------|
| 1 | `/project-guide` | 参照先特定 | 調査順序のガイダンス |
| 2 | `/investigate` | 現状把握 | Service概要・拡張ポイント |
| 3 | `/service-spec` | 詳細仕様確認 | メソッド仕様・依存関係 |
| 4 | `/impact-analysis` | 影響範囲分析 | ADR形式のレポート |
| 5 | `/propose-changes` | 修正提案作成 | diff形式の変更提案 |
| 6 | `/create-pr` | PR作成 | ブランチ・コミット・PR |
| 7 | `/build-knowledge` | ドメイン知識蓄積 | input/domain/ への追加 |

### Key Benefits

- **段階的理解**: 概要 → 詳細 → 影響 → 知識化
- **再利用可能**: 次回類似タスク時に input/domain/ 参照
- **チーム共有**: ドキュメントがそのままオンボーディング資料に

### Typical Timeline

- Small feature (like above): 1-2 days
- Medium feature: 3-5 days
- Large feature: 1-2 weeks

---

## Notes

- This workflow is sequential, but phases can be parallelized if multiple features are worked on simultaneously
- Each skill output is self-contained and can be reviewed independently
- The `/code-review` skill fits naturally after implementation (not shown in this example)
- Terminology can be customized by editing `prompts/terminology.md`
