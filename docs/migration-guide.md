# Migration Guide — v0.x → v1.0 (Plugin Architecture)

> **Version**: 1.0
> **Last Updated**: 2026-03-09

## Overview

decouple-legacy v1.0 でプラグインアーキテクチャに移行しました。
従来の単一 `skills/` ディレクトリから、4つの専門特化プラグインに分割されました。

## What's New in v1.0

### 1. Plugin Architecture
- **4つのモジュラープラグイン**: legacy-investigation, legacy-analysis, legacy-execution, legacy-knowledge
- **個別インストール可能**: 必要なプラグインのみインストール可能
- **Marketplace対応**: `claude plugin marketplace add` でインストール可能

### 2. Commands (NEW)
- **ワークフローの自動化**: 複数スキルをチェーンした `/investigate-flow` 等のコマンドを追加
- **人間チェックポイント明示**: 各フェーズで人間の承認を待つタイミングが明確化

### 3. Quality Validation
- **validate_plugins.py**: プラグイン構造・frontmatter の検証スクリプトを追加

## Directory Changes

| Before (v0.x) | After (v1.0) |
|---------------|-------------|
| `skills/project-guide/` | `legacy-investigation/skills/project-guide/` |
| `skills/investigate/` | `legacy-investigation/skills/investigate/` |
| `skills/service-spec/` | `legacy-investigation/skills/service-spec/` |
| `skills/impact-analysis/` | `legacy-analysis/skills/impact-analysis/` |
| `skills/legacy-analyze/` | `legacy-analysis/skills/legacy-analyze/` |
| `skills/propose-changes/` | `legacy-execution/skills/propose-changes/` |
| `skills/create-pr/` | `legacy-execution/skills/create-pr/` |
| `skills/code-review/` | `legacy-execution/skills/code-review/` |
| `skills/build-knowledge/` | `legacy-knowledge/skills/build-knowledge/` |
| `skills/templates/` | `legacy-knowledge/skills/templates/` |
| `prompts/` | `legacy-knowledge/prompts/` |

### New Additions (v1.0)

| Directory | Description |
|-----------|-------------|
| `legacy-investigation/commands/` | `/investigate-flow`, `/bug-hunt`, `/understand` |
| `legacy-analysis/commands/` | `/deep-dive` |
| `legacy-execution/commands/` | `/implement`, `/review` |
| `{plugin}/.claude-plugin/` | Plugin metadata directory |

## Migration Steps

### Step 1: Backup Existing Setup

```bash
# Backup your current skills directory
cp -r .claude/skills/ .claude/skills.backup/
```

### Step 2: Remove Old Skills

```bash
# Remove old skills (they will be replaced by plugins)
rm -rf .claude/skills/project-guide
rm -rf .claude/skills/investigate
rm -rf .claude/skills/service-spec
rm -rf .claude/skills/impact-analysis
rm -rf .claude/skills/legacy-analyze
rm -rf .claude/skills/propose-changes
rm -rf .claude/skills/create-pr
rm -rf .claude/skills/code-review
rm -rf .claude/skills/build-knowledge
rm -rf .claude/skills/templates
```

### Step 3: Install Plugins

#### Option A: CLI Installation (Recommended)

```bash
# Add marketplace
claude plugin marketplace add decouple-legacy /path/to/decouple-legacy

# Install plugins
claude plugin install legacy-investigation@decouple-legacy
claude plugin install legacy-analysis@decouple-legacy
claude plugin install legacy-execution@decouple-legacy
claude plugin install legacy-knowledge@decouple-legacy
```

#### Option B: Manual Installation

```bash
# Copy skills from each plugin
cp -r /path/to/decouple-legacy/legacy-investigation/skills/* .claude/skills/
cp -r /path/to/decouple-legacy/legacy-analysis/skills/* .claude/skills/
cp -r /path/to/decouple-legacy/legacy-execution/skills/* .claude/skills/
cp -r /path/to/decouple-legacy/legacy-knowledge/skills/* .claude/skills/

# Copy commands (if supported by your setup)
mkdir -p .claude/commands/
cp -r /path/to/decouple-legacy/legacy-investigation/commands/* .claude/commands/
cp -r /path/to/decouple-legacy/legacy-analysis/commands/* .claude/commands/
cp -r /path/to/decouple-legacy/legacy-execution/commands/* .claude/commands/
```

### Step 4: Update CLAUDE.md

**No changes required** for skill paths. Skills are installed to `.claude/skills/` as before.

**Optional**: Add references to new commands:

```markdown
## Workflow Commands
- `/investigate-flow [target]` — Investigation pipeline
- `/implement [proposal path]` — Implementation pipeline
- `/review [PR number]` — Review pipeline
```

### Step 5: Verify Installation

```bash
# Test a skill
claude /investigate [some target]

# Test a command (if supported)
claude /investigate-flow [some target]
```

## CLAUDE.md Updates

### No Breaking Changes

スキルのパスは変更なし。プラグインインストール時に自動的に `.claude/skills/` に配置されます。

**Before (v0.x)**:
```markdown
## Skills
This project uses skills from decouple-legacy:
- /investigate — Code investigation
```

**After (v1.0)**: Same! No changes needed.
```markdown
## Skills
This project uses skills from decouple-legacy:
- /investigate — Code investigation
```

### Optional: Document Commands

新しいコマンド機能を使用する場合、CLAUDE.md に記載を推奨:

```markdown
## Workflow Commands
- `/investigate-flow [target]` — 調査パイプライン（project-guide → investigate → service-spec → impact-analysis）
- `/implement [proposal]` — 実装パイプライン（propose-changes → create-pr）
- `/review [PR number]` — レビューパイプライン（project-guide → code-review）
```

## New Features in v1.0

### Commands: Workflow Automation

Commands are **pre-configured pipelines** that chain multiple skills together with human checkpoints.

**Example**: `/investigate-flow [target]`

Runs the following sequence:
1. `/project-guide [target]` — Get context
2. `/investigate [target]` — Find code
3. `/service-spec [target]` — Document specification
4. `/impact-analysis [target]` — Analyze impact
5. 【Human Checkpoint】Review full report

**Benefits**:
- Reduces manual typing of skill sequences
- Enforces consistent workflows
- Makes human checkpoints explicit

### Marketplace: Easy Installation

```bash
# Add marketplace
claude plugin marketplace add decouple-legacy /path/to/decouple-legacy

# List available plugins
claude plugin marketplace list

# Install a specific plugin
claude plugin install legacy-investigation@decouple-legacy
```

### Validation: Quality Checks

Run validation before committing:

```bash
python3 validate_plugins.py
```

Checks:
- Plugin structure (skills, commands, examples, .claude-plugin/)
- Skill frontmatter format
- Command frontmatter format
- marketplace.json and plugin.json validity

## Rollback Plan

If migration causes issues, rollback to v0.x:

```bash
# Remove new plugins
rm -rf .claude/skills/*

# Restore old skills
cp -r .claude/skills.backup/* .claude/skills/
```

## FAQ

### Q: Do I need to install all 4 plugins?

**A**: No. Install only the plugins you need. For example:
- Investigation only: `legacy-investigation`
- Investigation + Analysis: `legacy-investigation` + `legacy-analysis`
- Full workflow: All 4 plugins

### Q: Can I still use individual skills like before?

**A**: Yes. `/investigate [target]` works the same as v0.x.

### Q: What's the difference between skills and commands?

**A**:
- **Skills**: Atomic tasks (e.g., `/investigate`)
- **Commands**: Pre-configured workflows (e.g., `/investigate-flow` = multiple skills chained)

### Q: Do I need to update my CLAUDE.md?

**A**: No breaking changes. Optionally add references to new commands.

### Q: How do I know if migration was successful?

**A**: Run a test skill:

```bash
claude /investigate [some target]
```

If it works, migration succeeded.

## Support

If you encounter issues:
1. Check `validate_plugins.py` output for errors
2. Review this migration guide
3. Open an issue on GitHub with logs

## Links

- [README.md](../README.md) — Full documentation
- [ARCHITECTURE.md](../ARCHITECTURE.md) — Architecture details
- [validate_plugins.py](../validate_plugins.py) — Validation script
