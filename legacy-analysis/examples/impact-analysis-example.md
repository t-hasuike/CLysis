# /impact-analysis Example

## Scenario: New Feature Impact Analysis

### INPUT

```
/impact-analysis Adding a new shipping method (Express Shipping)
```

### OUTPUT

```
"Impact analysis report submitted.

# ADR: Adding Express Shipping Feature

> **Status**: Proposed
> **Date**: 2026-03-06
> **Decision Makers**: Team Lead, Product Manager

## Context

Current shipping methods are "Standard Shipping (3-5 days)" and "Priority Shipping (1-2 days)."
Customers frequently request "same-day delivery," and competitors already offer it.
Adding "Express Shipping (same-day)" as a new option.

---

## Decision

Add Express shipping logic to ShippingService and implement the following:

1. Add shipping method (shipping_methods table)
2. Extend shipping fee calculation logic
3. Inventory reservation and carrier API integration
4. UI: Add shipping method selection in the checkout flow

---

## Consequences

### Impact Scope (File List)

#### Backend
| File | Impact | Change Type |
|------|--------|-------------|
| `app/Services/Shipping/ShippingService.php` | High | Add method: `calculateExpressFee()` |
| `app/Services/Order/OrderService.php` | Medium | Add inventory reservation logic for Express shipping |
| `database/migrations/2026_03_06_add_express_shipping.php` | High | Add record to shipping_methods table |
| `app/Models/ShippingMethod.php` | Low | Add constant: `TYPE_EXPRESS = 'express'` |
| `app/Http/Controllers/CheckoutController.php` | Medium | Add shipping method to API response |

#### Frontend
| File | Impact | Change Type |
|------|--------|-------------|
| `resources/js/components/Checkout/ShippingOptions.tsx` | High | Add Express shipping option (UI/UX) |
| `resources/js/api/shipping.ts` | Medium | Update API type definition: `ShippingMethod` enum |

#### Infrastructure
| File | Impact | Change Type |
|------|--------|-------------|
| `config/shipping.php` | Medium | Add carrier API configuration (Express-specific) |
| `.env.example` | Low | Add environment variable: `EXPRESS_SHIPPING_API_KEY` |

---

### Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Carrier API rate limiting | High | Retry mechanism + cache introduction |
| Poor customer experience when out of stock | Medium | Real-time stock check + UI warning display |
| Increased complexity of shipping fee calculation | Low | Apply Strategy pattern to ensure maintainability |

---

### Implementation Plan

#### Phase 1: Backend Implementation (1 week)
- [ ] Create and run migration
- [ ] Extend ShippingService
- [ ] Carrier API integration (sandbox)
- [ ] Create unit tests

#### Phase 2: Frontend Implementation (3 days)
- [ ] UI/UX design review
- [ ] Update ShippingOptions component
- [ ] Create E2E tests

#### Phase 3: Integration Testing (2 days)
- [ ] Deploy to staging environment
- [ ] QA execution (shipping fee calculation, stock integration)
- [ ] Performance testing

#### Phase 4: Production Release (1 day)
- [ ] Enable feature flag (gradual rollout)
- [ ] Monitoring setup (carrier API success rate)
- [ ] Verify rollback procedure

---

### Alternatives

#### Alternative 1: Support External Carriers Only (exclude self-delivery)
- Pros: 50% reduction in implementation cost
- Cons: Reduced consistency of customer experience

#### Alternative 2: Offer in Specific Regions Only
- Pros: Risk reduction, gradual rollout
- Cons: Feature availability becomes complex (postal code check required)

**Decision**: Support all regions and all carriers (alternatives not adopted)

---

Report complete."
```

### Notes

- Use `/impact-analysis [Feature Description]` for new features or architecture changes
- Output follows ADR (Architecture Decision Record) format
- Includes file-level impact assessment with severity indicators
- Provides implementation plan with phases
- Useful for sprint planning and technical design reviews
