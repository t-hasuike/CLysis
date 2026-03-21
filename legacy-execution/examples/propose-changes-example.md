# /propose-changes Usage Example

## Scenario: Express Shipping Feature Addition - Phase 0 (Foundation Setup)

### Prerequisites

1. `/impact-analysis` has created an impact analysis report
   - File path: `reports/impact_reports/add_express_shipping.md`
   - Phase 0 determined that ShippingMethod Enum creation and OrderService modification are needed

### Execution

```
/propose-changes reports/impact_reports/add_express_shipping.md Phase 0
```

### Output Example

The following change proposal is generated at `reports/proposals/add_express_shipping_phase0.md`:

---

```markdown
# Express Shipping Addition Change Proposal - Phase 0

**Created**: 2026-03-08
**Target Repository**: my-ecommerce-app
**Source Report**: `reports/impact_reports/add_express_shipping.md`

---

## Change Overview

Create ShippingMethod Enum and change OrderService's hardcoded shipping methods to dynamic retrieval.

---

## Change List

### Change 1: ShippingMethod Enum Creation

**File Path**: `app/Enums/ShippingMethod.php` (new)
**Impact**: High
**Change Reason**: Eliminate hardcoded shipping methods and centralize management

#### Change Content (new file)

```php
<?php

declare(strict_types=1);

namespace App\Enums;

enum ShippingMethod: string
{
    case STANDARD = 'standard';
    case EXPRESS = 'express';    // New addition

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

#### Test Strategy

- **Unit test**: Verify getAll() returns all shipping methods
- **Unit test**: Verify getDeliveryDays() returns correct number of days

---

### Change 2: OrderService - Dynamic Shipping Method Retrieval

**File Path**: `app/Services/OrderService.php`
**Impact**: High
**Change Reason**: Change hardcoded array to dynamic retrieval from Enum

#### Code Before Change (relevant section)

```php
// Line numbers: 45-48
private const SHIPPING_METHODS = ['standard'];

public function getDeliveryDays(string $method): int
{
    return $method === 'standard' ? 5 : 3;
}
```

#### Code After Change (diff format)

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

#### Impact Scope

| Affected Area | Change Description | Risk Assessment |
|---------------|-------------------|-----------------|
| OrderController::create() | Change to getAvailableMethods() call | Medium |
| CheckoutService::validate() | Change SHIPPING_METHODS constant reference | Medium |

#### Test Strategy

- **Unit test**: Verify getAvailableMethods() retrieves from Enum
- **Integration test**: Verify OrderController accepts new shipping methods

---

## Change Order (Dependencies)

```
1. Create ShippingMethod Enum
   |
2. Modify OrderService (uses Enum)
   |
3. Modify OrderController (address in Phase 1)
```

---

## Approval Checklist

- [x] Presented diffs for all modification points
- [x] Change reasons are clear
- [x] Analyzed impact scope
- [x] Test strategy is specific
- [x] Identified risks and side effects
- [x] Change order is appropriate

---

## Next Actions

1. **User approval**: Review and approve this change proposal
2. **Launch `/create-pr`**: After approval, use this proposal as input to create PR
```

---

### Key Points

- Before/after clearly visible in diff format
- Change reason, impact scope, and test strategy linked to each change
- Proceeds to next step (/create-pr) only after human approval
- Embodies the core philosophy: "AI presents, humans review"
