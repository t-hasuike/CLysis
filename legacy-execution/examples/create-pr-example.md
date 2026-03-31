# /create-pr Usage Example (Two-Phase Workflow)

## Scenario: Express Shipping Addition - Phase 0

This example demonstrates the complete `/create-pr` workflow with --plan and --exec phases.

---

## Phase 1: --plan (Generate Change Proposal)

### Prerequisites

1. `/change-impact` has created an impact analysis report
   - File path: `reports/impact_reports/add_express_shipping.md`
   - Analysis determined that ShippingMethod Enum creation and OrderService modification are needed in Phase 0

### Execution

```bash
/create-pr --plan reports/impact_reports/add_express_shipping.md Phase 0
```

Arguments:
- `reports/impact_reports/add_express_shipping.md`: Impact analysis report path
- `Phase 0`: Target phase for implementation

### Output: Change Proposal

Generated at `reports/proposals/add_express_shipping_phase0.md`:

```markdown
# Express Shipping Addition Change Proposal - Phase 0

**Created**: 2026-03-20
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
| OrderController::create() | Update to getAvailableMethods() call | Medium |
| CheckoutService::validate() | Update SHIPPING_METHODS constant reference | Medium |

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

## Risks and Concerns Summary

### High Risk
None identified

### Medium Risk
- Existing tests may fail if they assume hardcoded SHIPPING_METHODS constant

### Low Risk
- Minimal complexity in type conversion from string to Enum

---

## Approval Checklist

- [x] Presented diffs for all modification points
- [x] Change reasons are clear
- [x] Analyzed impact scope
- [x] Test strategy is specific
- [x] Identified risks and side effects
- [x] Dependencies are organized
```

### [Human Review Point 1]

**User reviews the change proposal and determines:**
- "Diffs are correct and appropriate"
- "Impact analysis is complete"
- "Test strategy is adequate"
- "Ready to proceed with --exec phase"

---

## Phase 2: --exec (Create PR from Approved Proposal)

### Prerequisites

1. Change proposal has been reviewed and approved by user
   - File path: `reports/proposals/add_express_shipping_phase0.md`

### Execution

```bash
/create-pr --exec reports/proposals/add_express_shipping_phase0.md my-ecommerce-app
```

Arguments:
- `reports/proposals/add_express_shipping_phase0.md`: Approved change proposal (from --plan phase)
- `my-ecommerce-app`: Target repository
- Branch name omitted -> auto-generated: `feature/add-express-shipping-phase0`

### Execution Details

#### Step 1: Branch Creation

```bash
git checkout develop
git pull origin develop
git checkout -b feature/add-express-shipping-phase0
```

#### Step 2: Code Changes Applied

| File | Operation | Result |
|------|-----------|--------|
| `app/Enums/ShippingMethod.php` | Create | Success |
| `app/Services/OrderService.php` | Modify | Success |

#### Step 3: Commit

```
Express Shipping: Phase 0 (Foundation Setup)

Why: To add new shipping method "Express," eliminate hardcoded values and switch to dynamic retrieval
What: Created ShippingMethod Enum, changed OrderService to retrieve from Enum
How: Dynamic retrieval of all shipping methods via ShippingMethod::getAll()

Co-Authored-By: Claude <noreply@anthropic.com>
```

#### Step 4: Push

```bash
git push -u origin feature/add-express-shipping-phase0
```

#### Step 5: PR Created

```bash
gh pr create --title "Express Shipping - Phase 0" --body "..." --base develop
```

### Output: Execution Report

Reported to leader:

```
PR creation complete.

[Repository]
my-ecommerce-app

[PR URL]
https://github.com/my-org/my-ecommerce-app/pull/456

[Branch]
feature/add-express-shipping-phase0 → develop

[Changes]
- app/Enums/ShippingMethod.php: Created ShippingMethod Enum (new file)
- app/Services/OrderService.php: Changed shipping methods to dynamic retrieval

[Commit Count]
1 commit

[Test Results]
- Unit tests: PASS
- Integration tests: PASS

[Next Actions]
Please review and approve the PR.

Execution log: reports/pr_logs/add_express_shipping_phase0.md
```

### [Human Review Point 2]

**User reviews the PR:**
- Verifies code quality and test results in GitHub
- Approves and merges the PR
- Implementation complete

---

## Full Pipeline View

```
/project-guide [task] → Gather context
    |
/current-spec [target] → Understand code
    |
/change-impact [change] → Analyze impact
    | [Investigation complete]
    |
/create-pr --plan [report] → Generate proposal
    | Change proposal ready
  [Human Review 1] "Are proposed changes appropriate?"
    | (if approved)
    |
/create-pr --exec [proposal] → Create PR
    | PR URL and execution log
  [Human Review 2] "PR review and merge decision"
    |
Merge to main branch → Implementation Complete
```

---

## Key Points

- **Two-phase design**: --plan for proposal generation, --exec for implementation
- **Human approval gate**: Must approve after --plan before executing --exec
- **Commit messages**: Follow 5W1H format (Why, What, How)
- **PR body**: Includes change summary, test results, and risks from change proposal
- **Execution log**: Recorded for traceability and audit
- **Humans control the process**: AI proposes, humans decide, AI implements

