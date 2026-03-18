# /build-knowledge Example

## Scenario: Knowledge Base Update

### INPUT

```
/build-knowledge Discount calculation business rules discovered during code review

Context:
- PR#123 review revealed that discount calculation logic is spread across 3 locations
- Business rules have become tacit knowledge and need documentation
- Different calculation formulas in DiscountService, OrderService, and CheckoutController
```

### OUTPUT

```
"Domain knowledge has been accumulated.

[Action] New creation
[Target File] input/domain/discount_rules.md

[Content]
- Organized 3 discount calculation business rules
- Identified code dispersion locations
- Unification recommendations

[Judgment Reason]
Existing pricing_methods.md only describes pricing types.
Judged discount calculation logic as a separate domain and created a new file.

---

# Discount Calculation Rules

> **Version**: 1.0
> **Last Updated**: 2026-03-06
> **Source**: PR#123 Code Review

## Overview

Discounts are determined by 3 factors: 'customer rank,' 'order amount,' and 'campaign.'
Currently, calculation logic is spread across 3 locations and needs unification.

---

## Business Rules

### 1. Customer Rank-Based Discount Rate

| Rank | Discount Rate | Notes |
|------|--------------|-------|
| General | 0% | Default |
| Silver | 5% | Cumulative purchases over 100,000 |
| Gold | 10% | Cumulative purchases over 500,000 |

### 2. Additional Discount by Order Amount

| Condition | Additional Discount |
|-----------|-------------------|
| Order amount >= 10,000 | +2% |
| Order amount >= 50,000 | +5% |
| Order amount >= 100,000 | +8% |

### 3. Campaign Discount Combination Rules

| Condition | Application |
|-----------|------------|
| Rank discount + Amount discount | Can combine (additive) |
| Rank discount + Campaign discount | Higher one only applies |
| Maximum discount rate | Capped at 20% |

---

## Current Implementation Locations

### Dispersed Calculation Logic

| File | Line | Calculation Content | Issue |
|------|------|-------------------|-------|
| `DiscountService.php` | 145-180 | Rank discount + Amount discount | Campaign discount not considered |
| `OrderService.php` | 234-256 | Campaign discount determination only | Rank discount not considered |
| `CheckoutController.php` | 89-102 | Final discount calculation (API response) | Logic duplication (should call DiscountService) |

### Impact of the Problem

1. **Inconsistency risk**: Different formulas in 3 locations -> possible incorrect discount display to customers
2. **Reduced maintainability**: 3 files need modification when rules change
3. **Testing difficulty**: Cannot create unified test cases

---

## Recommendations

### 1. Single Responsibility

Consolidate discount calculation into DiscountService:

```php
class DiscountService
{
    public function calculateDiscount(
        CustomerRank $rank,
        Money $orderTotal,
        ?Campaign $campaign
    ): Percentage {
        $rankDiscount = $this->getRankDiscount($rank);
        $amountDiscount = $this->getAmountDiscount($orderTotal);
        $campaignDiscount = $this->getCampaignDiscount($campaign);

        $baseDiscount = $rankDiscount->add($amountDiscount);
        $finalDiscount = max($baseDiscount, $campaignDiscount);

        return min($finalDiscount, Percentage::of(20)); // Cap at 20%
    }
}
```

### 2. Externalize Rules

Define discount rules in `config/discount.php`:

```php
return [
    'rank_discounts' => [
        'general' => 0,
        'silver' => 5,
        'gold' => 10,
    ],
    'amount_discounts' => [
        10000 => 2,
        50000 => 5,
        100000 => 8,
    ],
    'max_discount_rate' => 20,
];
```

### 3. Test Strategy

Create unified test cases:

```php
public function test_discount_for_silver_rank_customer()
{
    // Given: Silver rank, order amount 8,000
    // When: Execute calculateDiscount()
    // Then: 5% (rank discount only)
}

public function test_discount_cap_at_maximum()
{
    // Given: Gold rank, order amount 100,000, campaign 15%
    // When: Execute calculateDiscount()
    // Then: 20% (cap applied)
}
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-03-06 | Initial version (PR#123 review results) |

---

Report complete."
```

### Notes

- Use `/build-knowledge [Topic/Context]` to create or update domain knowledge
- Output is saved to `input/domain/` directory
- Includes business rules, implementation status, and recommendations
- Useful for onboarding, knowledge sharing, and preventing knowledge loss
- Knowledge base grows iteratively with each code review/investigation
