# /create-pr 使用例

## シナリオ: Express Shipping 追加 - Phase 0 の PR 作成

### 前提

1. `/propose-changes` で修正提案書が作成済み
   - ファイルパス: `output/proposals/add_express_shipping_phase0.md`
2. 上様が修正提案書をレビュー・承認済み

### 実行

```
/create-pr output/proposals/add_express_shipping_phase0.md my-ecommerce-app
```

引数:
- `output/proposals/add_express_shipping_phase0.md`: 修正提案書パス
- `my-ecommerce-app`: 対象リポジトリ
- ブランチ名省略 → 自動生成: `feature/add-express-shipping-phase0`

### 実行内容

#### 1. ブランチ作成

```bash
git checkout develop
git pull origin develop
git checkout -b feature/add-express-shipping-phase0
```

#### 2. コード修正

| ファイル | 操作 | 結果 |
|---------|------|------|
| `app/Enums/ShippingMethod.php` | Write（新規） | 成功 |
| `app/Services/OrderService.php` | Edit | 成功 |

#### 3. コミット

```
Express Shipping: Phase 0（基盤整備）

Why: 新配送方法「Express」を追加するため、ハードコードを排除し動的取得に変更
What: ShippingMethod Enum 作成、OrderService を Enum から取得に変更
How: ShippingMethod::getAll() メソッドで全配送方法を動的取得

Co-Authored-By: Claude <noreply@anthropic.com>
```

#### 4. PR作成

```bash
gh pr create --title "Express Shipping - Phase 0（基盤整備）" \
  --body "..." --base develop
```

### 出力例

#### 将軍への報告

```
「上様、PR作成が完了いたしました。

【PR URL】
https://github.com/my-org/my-ecommerce-app/pull/456

【修正内容】
- app/Enums/ShippingMethod.php: ShippingMethod Enum 作成（新規）
- app/Services/OrderService.php: 配送方法を動的取得に変更

【コミット数】1件

【テスト結果】
- ユニットテスト: PASS
- 統合テスト: PASS

【次のアクション】
PR のレビュー・承認をお願いいたします。

実行ログ: output/pr_logs/add_express_shipping_phase0.md
」
```

---

### ポイント

- 修正提案書の承認後にのみ実行
- コミットメッセージは5W1H形式
- PR本文に修正概要・テスト結果・リスクを記載
- 実行ログを記録し、トレーサビリティを確保
- 人間がPRレビュー・承認してからマージ

### パイプライン全体像

```
/investigate → /service-spec → /impact-analysis
    ↓
/propose-changes
    ↓ 修正提案書
  【人間の確認①】修正内容が妥当か
    ↓
/create-pr
    ↓ PR URL
  【人間の確認②】PRレビュー・承認
    ↓
マージ → 実装完了
```
