# Full Workflow Example

## Scenario: Adding New Payment Method (QR Code Payment)

This example demonstrates an end-to-end workflow using all skills sequentially.

---

## Phase 1: Project Guidance

### INPUT

```
/project-guide Adding QR code payment
```

Note: This workflow example uses skills `/project-guide`, `/current-spec`, `/change-impact`, `/propose-changes`, `/create-pr`, and `/review-code` (formerly `/investigate`, `/service-spec`, `/impact-analysis`, `/code-review`).

### OUTPUT

```
"Reference targets identified.

[Mission] Adding QR code payment

[Files to Reference]
1. knowledge/system/repositories.md -> Verify payment feature responsibility boundaries
2. knowledge/domain/payment_methods.md -> Existing payment method specifications
3. app/Services/Payment/PaymentService.php -> Payment processing core implementation

[Investigation Order]
1. /current-spec PaymentService -> Understand current state and specification
2. /change-impact Adding QR code payment -> Impact scope analysis

Report complete."
```

---

## Phase 2: Investigation

### INPUT

```
/current-spec PaymentService
```

### OUTPUT (Abbreviated)

```
"PaymentService investigation complete.

[Overview]
- Currently supported: Credit card, bank transfer
- Strategy pattern adopted (Gateway abstraction)
- New payment method addition possible via GatewayInterface implementation

[Key Methods]
- processPayment(): Execute payment
- refund(): Refund processing
- validatePaymentMethod(): Payment method validation

[Dependencies]
- StripeGateway (credit card)
- BankTransferGateway (bank transfer)
- PaymentRepository (DB persistence)

[Extension Point]
QR code payment addressable via new QRCodeGateway implementation.

Report complete."
```

---

## Phase 3: Service Specification

### INPUT

(Specification is now included in /current-spec output)

### OUTPUT (Abbreviated)

```
"PaymentService specification document created.

# PaymentService Specification Summary

## Public Methods

### processPayment(Order $order, PaymentMethod $method): PaymentResult

**Processing Flow**:
1. Get Gateway via GatewayFactory::make($method->type)
2. Execute Gateway::charge($order->total)
3. Record via PaymentRepository::save()
4. Return PaymentResult

**Extension Method**:
When adding new Gateway:
1. Implement GatewayInterface
2. Register in GatewayFactory
3. Add to PaymentMethod enum

## Dependencies
[Details omitted]

Report complete."
```

---

## Phase 4: Impact Analysis

### INPUT

```
/change-impact Adding QR code payment (PayPay)
```

### OUTPUT (Abbreviated)

```
"Impact analysis report submitted.

# ADR: Adding QR Code Payment Feature

## Decision

Add PayPay as a payment method. Implement PayPayGateway and integrate with existing architecture.

## Consequences

### Impact Scope

#### Backend
| File | Impact | Change Type |
|------|--------|-------------|
| `app/Gateways/PayPayGateway.php` | High | New creation (GatewayInterface implementation) |
| `app/Services/Payment/GatewayFactory.php` | Medium | Register PayPay |
| `app/Models/PaymentMethod.php` | Low | ENUM addition: `PAYPAY = 'paypay'` |
| `database/migrations/2026_03_06_add_paypay.php` | High | payment_methods table update |

#### Frontend
| File | Impact | Change Type |
|------|--------|-------------|
| `resources/js/components/Checkout/PaymentOptions.tsx` | High | QR code display UI addition |
| `resources/js/api/payment.ts` | Medium | PayPay API type definition addition |

### Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Poor customer experience during PayPay API outage | High | Fallback UI + admin notification |
| QR code expiration | Medium | Auto-refresh mechanism |

### Implementation Plan

#### Phase 1: PayPayGateway Implementation (3 days)
- [ ] PayPay API integration (sandbox)
- [ ] QR code generation/verification logic
- [ ] Unit tests (payment success/failure/timeout)

#### Phase 2: UI Implementation (2 days)
- [ ] QR code display component
- [ ] Real-time payment status update (WebSocket)

#### Phase 3: Integration Testing (2 days)
- [ ] E2E tests
- [ ] Performance tests (QR code generation time)

Report complete."
```

**[Human Checkpoint]**

Submit impact analysis report (reports/impact_analysis_paypay.md) to user for approval.

---

## Phase 5: Propose Changes

### INPUT

```
/propose-changes reports/impact_analysis_paypay.md
```

### OUTPUT (Abbreviated)

```
"Change proposal submitted.

# PayPay Payment Addition Change Proposal

**Source Report**: reports/impact_analysis_paypay.md
**Proposal Date**: 2026-03-08

## Change Summary

- PayPayGateway new creation
- Register PayPay in GatewayFactory
- Add PAYPAY to PaymentMethod enum
- Add QR code display to PaymentOptions UI

---

## Changes (diff format)

### 1. app/Gateways/PayPayGateway.php (new creation)

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
+         // QR code generation logic
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
+         // Refund processing
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
          <option value="credit_card">Credit Card</option>
          <option value="bank_transfer">Bank Transfer</option>
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

## Review Points

- [ ] Is PayPayGateway error handling sufficient?
- [ ] Is the QR code expiration (5 min) UI display appropriate?
- [ ] Is Webhook signature verification included?
- [ ] Are test cases comprehensive?

Report complete."
```

**[Human Checkpoint]**

Submit change proposal to user for review and approval.

---

## Phase 6: Create PR

### INPUT

```
/create-pr reports/propose_changes_paypay.md backend
```

### OUTPUT (Abbreviated)

```
"PR creation complete.

[Work Performed]
1. Branch creation: feature/add-paypay-payment
2. Code changes: Implemented per proposal diffs
3. Commit: "Add PayPay payment gateway integration"
4. PR created: #456

[PR URL]
https://github.com/your-org/backend/pull/456

[PR Content]
# Add PayPay Payment Gateway

## Summary
- PayPayGateway implementation
- Register PayPay in GatewayFactory
- Add PAYPAY to PaymentMethod enum
- Add QR code display UI

## Test Plan
- [ ] Unit tests (PayPayGatewayTest)
- [ ] Integration tests (payment flow E2E)
- [ ] Manual QA (QR code payment in sandbox environment)

## Related
- Impact Analysis: reports/impact_analysis_paypay.md
- Change Proposal: reports/propose_changes_paypay.md

Report complete."
```

**[Human Checkpoint]**

User reviews, approves, and instructs merge of the PR.

---

## Phase 7: Build Knowledge

### INPUT

(Domain knowledge is now accumulated during the investigation and analysis phases)

### OUTPUT (Abbreviated)

```
"Domain knowledge accumulated.

[Action] New creation
[Target File] knowledge/domain/qr_code_payment_rules.md

[Content]
- QR code payment common patterns
- PayPay-specific specifications
- Security requirements

# QR Code Payment Rules

## Common Patterns

All QR code payments follow this flow:

1. QR code generation request (server -> payment provider)
2. QR code display (UI)
3. Customer scans with smartphone app
4. Payment completion notification (Webhook)
5. Order status update

## PayPay-Specific Specifications

- QR code expiration: 5 minutes
- Retry: Up to 3 times (exponential backoff)
- Webhook signature verification required (HMAC-SHA256)

## Security Requirements

- Do not include order ID in QR code (one-time token only)
- On Webhook receipt: signature verification + IP whitelist
- Invalidate QR code after payment completion

Report complete."
```

---

## Summary: Full Workflow

| Phase | Skill | Purpose | Output |
|-------|-------|---------|--------|
| 1 | `/project-guide` | Identify references | Investigation order guidance |
| 2 | `/current-spec` | Code investigation + detailed specification | Service overview, extension points, method specs |
| 3 | `/change-impact` | Impact scope analysis | ADR-format report |
| 4 | `/propose-changes` | Create change proposal | Diff-format change proposal |
| 5 | `/create-pr` | Create PR | Branch, commit, PR |
| 6 | `/review-code` | PR review | Code quality validation |

### Key Benefits

- **Progressive understanding**: Overview -> detail -> impact -> knowledge capture
- **Reusable**: Reference knowledge/domain/ for similar future tasks
- **Team sharing**: Documents serve as onboarding materials

### Typical Timeline

- Small feature (like above): 1-2 days
- Medium feature: 3-5 days
- Large feature: 1-2 weeks

---

## Notes

- This workflow is sequential, but phases can be parallelized if multiple features are worked on simultaneously
- Each skill output is self-contained and can be reviewed independently
- The `/review-code` skill fits naturally after implementation (see Phase 6 above)
- Terminology can be customized by editing `config/terminology.md`
