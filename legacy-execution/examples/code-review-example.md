# /code-review Example

## Scenario: Pull Request Review

### INPUT

```
/code-review PR#123 - 新しい商品カテゴリ追加
```

### OUTPUT

```
「上様、コードレビュー結果を献上いたします。

# Code Review Report: PR#123

> **PR Title**: Add new product category feature
> **Author**: developer-san
> **Files Changed**: 8 files (+320, -45)
> **Review Date**: 2026-03-06

---

## 1. コード品質チェック

### [Pass]

- **型安全性**: すべてのファイルで `declare(strict_types=1)` 宣言済み
- **命名規則**: PSR-12準拠（メソッド: camelCase, クラス: PascalCase）
- **テストカバレッジ**: 新規コード85%（基準80%クリア）
- **セキュリティ**: SQLインジェクション対策済み（Eloquent ORM使用）

### [注意] Warnings

| File | Line | Issue | Suggestion |
|------|------|-------|------------|
| `ProductService.php` | 123 | メソッドが150行 | `createProduct()` を3メソッドに分割推奨 |
| `CategoryRepository.php` | 45 | N+1クエリ発生 | `with(['products'])` でEager Loading適用 |
| `ProductController.php` | 67 | エラーハンドリング不足 | try-catch + ログ記録追加 |

### [NG] Must Fix

| File | Line | Issue | Action Required |
|------|------|-------|-----------------|
| `Product.php` | 89 | `$fillable` に機密情報含む | `is_internal_use` を `$guarded` に移動 |
| `CategoryService.php` | 234 | 論理削除チェック漏れ | `where('delflag', '0')` 追加必須 |

---

## 2. ビジネスロジックチェック

### [Pass]

- **カテゴリ階層構造**: 最大3階層まで対応（仕様通り）
- **商品-カテゴリ関連**: 多対多リレーション正しく実装
- **権限チェック**: 管理者のみカテゴリ作成可能（Policy適用済み）

### [注意] Warnings

| File | Issue | Business Impact |
|------|-------|----------------|
| `CategoryService.php` | カテゴリ削除時に紐づく商品の扱いが未定義 | 商品が孤立する可能性 → 仕様確認必要 |
| `ProductController.php` | カテゴリ変更時の在庫整合性チェックなし | 在庫管理に影響の可能性 |

### Suggestions

1. **カスケード削除**: カテゴリ削除時、子カテゴリ・商品をどう扱うか仕様明確化
2. **監査ログ**: カテゴリ変更履歴を audit_logs テーブルに記録推奨
3. **パフォーマンス**: カテゴリツリー取得にキャッシュ導入検討（Redis）

---

## 3. テスト戦略

### 既存テスト

- [Pass] Unit tests: `CategoryServiceTest.php`（15 test cases）
- [Pass] Feature tests: `CategoryApiTest.php`（8 test cases）
- [注意] Integration tests: なし → 推奨追加

### 追加推奨テスト

```php
// CategoryServiceTest.php に追加
public function test_deleting_category_with_products_should_handle_gracefully()
{
    // Given: カテゴリに商品が紐づいている
    // When: カテゴリ削除実行
    // Then: 適切な例外 or 商品の再配置
}

public function test_category_tree_respects_max_depth()
{
    // Given: 3階層のカテゴリツリー
    // When: 4階層目追加試行
    // Then: ValidationException
}
```

---

## 4. マイグレーション確認

### [Pass]

- **ロールバック可能**: `down()` メソッド実装済み
- **外部キー制約**: `categories.parent_id` → `categories.id` 正しく設定
- **インデックス**: `categories.slug` にUNIQUEインデックス（SEO対応）

### [注意] Warnings

- `product_category` 中間テーブルに複合インデックスなし → 追加推奨:
  ```php
  $table->index(['product_id', 'category_id']);
  ```

---

## 5. 総合評価

| 項目 | 評価 | コメント |
|------|------|---------|
| コード品質 | 中 Good | 小規模リファクタ推奨 |
| セキュリティ | 高 Needs Fix | 論理削除チェック漏れ修正必須 |
| テスト | 低 Excellent | カバレッジ良好 |
| パフォーマンス | 中 Good | N+1クエリ対策推奨 |
| ビジネスロジック | 中 Needs Clarification | カテゴリ削除仕様確認必要 |

### Approval Status: **Conditional Approval**

以下2点修正後、マージ可能でござる:

1. [NG] `CategoryService.php:234` - 論理削除チェック追加
2. [NG] `Product.php:89` - `$fillable` 修正

その他[注意]項目は次Sprintで対応可。

---

以上、報告完了でござる。」
```

### Notes

- Use `/code-review [PR Number/Description]` for pull request reviews
- Output includes code quality + business logic checks
- Severity indicators: [Pass], [注意] Warning, [NG] Must Fix
- Provides actionable suggestions with line numbers
- Useful for maintaining code quality standards
