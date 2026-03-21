# /service-spec Example

## Scenario: Detailed Service Specification

### INPUT

```
/service-spec PaymentService
```

### OUTPUT

```
"PaymentService specification document created.

# PaymentService Specification Summary

> **Version**: 1.0
> **Last Updated**: 2026-03-06
> **File**: app/Services/Payment/PaymentService.php

## Overview
PaymentService is a service class responsible for payment processing.
Supports 3 types: credit card, bank transfer, and e-money.

## Public Methods

### 1. processPayment(Order $order, PaymentMethod $method): PaymentResult

**Responsibility**: Execute payment (external gateway integration)

**Parameters**:
- `$order`: Order entity
- `$method`: PaymentMethod value object (type: card/bank/emoney)

**Return value**: PaymentResult (success/failure + transactionId)

**Processing flow**:
1. Select Gateway based on payment method (Strategy pattern)
2. Execute Gateway::charge()
3. Record result in payments table
4. Return PaymentResult

**Exceptions**:
- PaymentGatewayException: Gateway error
- InsufficientFundsException: Insufficient balance
- InvalidPaymentMethodException: Unsupported payment method

---

### 2. refund(int $paymentId, ?float $amount = null): RefundResult

**Responsibility**: Refund processing

**Parameters**:
- `$paymentId`: Payment ID to refund
- `$amount`: Refund amount (full amount if null)

**Return value**: RefundResult (success/failure + refundId)

**Processing flow**:
1. Retrieve original payment information
2. Check refund eligibility period (within 90 days of payment)
3. Execute Gateway::refund()
4. Record in refunds table

**Exceptions**:
- RefundExpiredException: Refund period expired
- AlreadyRefundedException: Already refunded

---

### 3. validateCard(string $cardNumber): ValidationResult

**Responsibility**: Credit card number validation (Luhn algorithm)

**Parameters**:
- `$cardNumber`: Card number (16 digits without hyphens)

**Return value**: ValidationResult (valid/invalid + brand: Visa/MasterCard/JCB)

**Processing flow**:
1. Luhn checksum verification
2. Card brand determination (leading digits)
3. Return ValidationResult

**Exceptions**: None (on validation failure: result->isValid = false)

---

## Dependencies

### External Service Integration
- `StripeGateway`: Credit card payments
- `BankTransferGateway`: Bank transfers
- `PayPayGateway`: E-money (QR code payments)

### Repositories
- `PaymentRepository`: payments table operations
- `RefundRepository`: refunds table operations

### Internal Services
- `LoggingService`: Payment log recording (audit trail)

---

## Notable Items

1. **Idempotency guarantee**: Prevents duplicate payments for same orderId + requestId (DB UNIQUE constraint)
2. **Retry mechanism**: Auto-retry up to 3 times on gateway timeout (exponential backoff)
3. **PCI DSS compliance**: Card numbers stored with encryption (at rest encryption)
4. **Audit log**: All payment/refund operations recorded in payment_logs table

---

## Test Coverage
- Unit tests: 92%
- Integration tests: 85%
- Critical path: 100% (payment/refund flows)

Report complete."
```

### Notes

- Use `/service-spec [ServiceName]` for detailed documentation
- Output includes all public methods with parameters, return values, exceptions
- Useful for API documentation or architectural reviews
- Can be saved to `reports/` directory for team reference
