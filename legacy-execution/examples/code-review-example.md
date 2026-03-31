# /code-review Example

## Scenario: Pull Request Review

### INPUT

```
/code-review PR#123 - Adding new product category
```

### OUTPUT

```
"Code review results submitted.

# Code Review Report: PR#123

> **PR Title**: Add new product category feature
> **Author**: developer-san
> **Files Changed**: 8 files (+320, -45)
> **Review Date**: 2026-03-06

---

## 1. Code Quality Check

### [Pass]

- **Type safety**: `declare(strict_types=1)` declared in all files
- **Naming conventions**: PSR-12 compliant (methods: camelCase, classes: PascalCase)
- **Test coverage**: 85% for new code (meets 80% threshold)
- **Security**: SQL injection prevention in place (using Eloquent ORM)

### [Warning] Warnings

| File | Line | Issue | Suggestion |
|------|------|-------|------------|
| `ProductService.php` | 123 | Method is 150 lines | Recommend splitting `createProduct()` into 3 methods |
| `CategoryRepository.php` | 45 | N+1 query detected | Apply Eager Loading with `with(['products'])` |
| `ProductController.php` | 67 | Insufficient error handling | Add try-catch + log recording |

### [NG] Must Fix

| File | Line | Issue | Action Required |
|------|------|-------|-----------------|
| `Product.php` | 89 | `$fillable` contains sensitive info | Move `is_internal_use` to `$guarded` |
| `CategoryService.php` | 234 | Missing soft-delete check | Must add soft-delete flag condition to WHERE clause |

---

## 2. Business Logic Check

### [Pass]

- **Category hierarchy**: Supports up to 3 levels (per specification)
- **Product-Category relation**: Many-to-many relation correctly implemented
- **Permission check**: Admin-only category creation (Policy applied)

### [Warning] Warnings

| File | Issue | Business Impact |
|------|-------|----------------|
| `CategoryService.php` | Product handling undefined when deleting category | Products may become orphaned -> specification clarification needed |
| `ProductController.php` | No inventory consistency check on category change | Possible inventory management impact |

### Suggestions

1. **Cascade delete**: Clarify specification for handling child categories/products on category deletion
2. **Audit log**: Recommend recording category change history in audit_logs table
3. **Performance**: Consider introducing cache for category tree retrieval (Redis)

---

## 3. Test Strategy

### Existing Tests

- [Pass] Unit tests: `CategoryServiceTest.php` (15 test cases)
- [Pass] Feature tests: `CategoryApiTest.php` (8 test cases)
- [Warning] Integration tests: None -> recommend adding

### Recommended Additional Tests

```php
// Add to CategoryServiceTest.php
public function test_deleting_category_with_products_should_handle_gracefully()
{
    // Given: Category has products linked
    // When: Delete category
    // Then: Appropriate exception or product reassignment
}

public function test_category_tree_respects_max_depth()
{
    // Given: 3-level category tree
    // When: Attempt to add 4th level
    // Then: ValidationException
}
```

---

## 4. Migration Verification

### [Pass]

- **Rollback possible**: `down()` method implemented
- **Foreign key constraints**: `categories.parent_id` -> `categories.id` correctly set
- **Index**: UNIQUE index on `categories.slug` (SEO support)

### [Warning] Warnings

- No composite index on `product_category` intermediate table -> recommend adding:
  ```php
  $table->index(['product_id', 'category_id']);
  ```

---

## 5. Overall Evaluation

| Category | Rating | Comment |
|----------|--------|---------|
| Code Quality | Medium Good | Minor refactoring recommended |
| Security | High Needs Fix | Must fix soft-delete check gap |
| Testing | Low Excellent | Good coverage |
| Performance | Medium Good | N+1 query fix recommended |
| Business Logic | Medium Needs Clarification | Category deletion specification needs confirmation |

### Approval Status: **Conditional Approval**

Merge-ready after fixing the following 2 items:

1. [NG] `CategoryService.php:234` - Add soft-delete check
2. [NG] `Product.php:89` - Fix `$fillable`

Other [Warning] items can be addressed in next Sprint.

---

Report complete."
```

### Notes

- Use `/code-review [PR Number/Description]` for pull request reviews
- Output includes code quality + business logic checks
- Severity indicators: [Pass], [Warning], [NG] Must Fix
- Provides actionable suggestions with line numbers
- Useful for maintaining code quality standards
