# /create-pr Usage Example

## Scenario: Express Shipping Addition - Phase 0 PR Creation

### Prerequisites

1. `/propose-changes` has created a change proposal
   - File path: `output/proposals/add_express_shipping_phase0.md`
2. User has reviewed and approved the change proposal

### Execution

```
/create-pr output/proposals/add_express_shipping_phase0.md my-ecommerce-app
```

Arguments:
- `output/proposals/add_express_shipping_phase0.md`: Change proposal path
- `my-ecommerce-app`: Target repository
- Branch name omitted -> auto-generated: `feature/add-express-shipping-phase0`

### Execution Details

#### 1. Branch Creation

```bash
git checkout develop
git pull origin develop
git checkout -b feature/add-express-shipping-phase0
```

#### 2. Code Changes

| File | Operation | Result |
|------|-----------|--------|
| `app/Enums/ShippingMethod.php` | Write (new) | Success |
| `app/Services/OrderService.php` | Edit | Success |

#### 3. Commit

```
Express Shipping: Phase 0 (Foundation Setup)

Why: To add new shipping method "Express," eliminate hardcoded values and switch to dynamic retrieval
What: Created ShippingMethod Enum, changed OrderService to retrieve from Enum
How: Dynamic retrieval of all shipping methods via ShippingMethod::getAll()

Co-Authored-By: Claude <noreply@anthropic.com>
```

#### 4. PR Creation

```bash
gh pr create --title "Express Shipping - Phase 0 (Foundation Setup)" \
  --body "..." --base develop
```

### Output Example

#### Report to Leader

```
"PR creation complete.

[PR URL]
https://github.com/my-org/my-ecommerce-app/pull/456

[Changes]
- app/Enums/ShippingMethod.php: Created ShippingMethod Enum (new)
- app/Services/OrderService.php: Changed shipping methods to dynamic retrieval

[Commit Count] 1

[Test Results]
- Unit tests: PASS
- Integration tests: PASS

[Next Actions]
Please review and approve the PR.

Execution log: output/pr_logs/add_express_shipping_phase0.md
"
```

---

### Key Points

- Execute only after change proposal is approved
- Commit messages follow 5W1H format
- PR body includes change summary, test results, and risks
- Execution log recorded for traceability
- Humans review and approve PR before merge

### Full Pipeline View

```
/investigate -> /service-spec -> /impact-analysis
    |
/propose-changes
    | Change proposal
  [Human Review 1] Are the changes appropriate?
    |
/create-pr
    | PR URL
  [Human Review 2] PR review and approval
    |
Merge -> Implementation Complete
```
