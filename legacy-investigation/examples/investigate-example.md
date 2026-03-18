# /investigate Example

## Scenario: Service Investigation

### INPUT

```
/investigate OrderService
```

### OUTPUT

```
"Investigation report.

[Mission] OrderService specification investigation

[Investigation Target]
- File: app/Services/Order/OrderService.php
- Lines: 1-450
- Dependencies: 8 services, 3 repositories

[Overview]
OrderService is the core service handling order processing.
It centrally manages order creation, updates, cancellation, and status management.

[Key Methods]
1. createOrder(array $orderData): Order
   - Create new order
   - Coordinates stock check + price calculation + payment processing
   - Executed within a transaction

2. updateOrderStatus(int $orderId, string $status): bool
   - Update order status
   - Validates state transition rules (pending -> confirmed -> shipped -> delivered)
   - Throws exception on invalid transitions

3. cancelOrder(int $orderId, string $reason): bool
   - Order cancellation processing
   - Executes payment refund + stock restoration
   - Cancellation deadline check (not allowed after shipment)

4. calculateTotal(array $items): Money
   - Total amount calculation
   - Product price + shipping fee + tax
   - Coupon and point discount application

[Dependencies]
- PaymentService: Payment processing delegation
- InventoryService: Stock management delegation
- ShippingService: Shipping arrangement delegation
- OrderRepository: DB persistence
- NotificationService: Customer notification

[Notable Items]
- All DB operations execute within transactions
- Cancellation processing branches by status (pre-shipment/post-shipment)
- On error: OrderException -> log recording -> rollback
- Status transitions managed by finite state machine (FSM)

[Concerns]
- 1 method is 250 lines (createOrder) -> recommend splitting
- Tight coupling with PaymentService -> consider interface extraction

Report complete."
```

### Notes

- Use `/investigate [ServiceName]` for initial exploration
- Output follows Service specification summary format
- Useful for onboarding or legacy code understanding
- Can be customized with additional flags (e.g., `/investigate OrderService --focus=security`)
