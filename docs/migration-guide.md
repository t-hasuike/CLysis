# Migration Guide -- v0.x to v1.0 (Plugin Architecture)

> **Version**: 1.0
> **Last Updated**: 2026-03-09

## Overview

CLysis v1.0 migrated to a plugin architecture.
The previous single `skills/` directory has been split into 4 specialized plugins.

## What's New in v1.0

### 1. Plugin Architecture
- **4 modular plugins**: legacy-investigation, legacy-analysis, legacy-execution, legacy-knowledge
- **Individual installation**: Install only the plugins you need
- **Marketplace support**: Install via `claude plugin marketplace add`

### 2. Commands (NEW)
- **Workflow automation**: Added commands like `/investigate-flow` that chain multiple skills
- **Explicit human checkpoints**: Clearly defined timing for human approval at each phase

### 3. Quality Validation
- **validate_plugins.py**: Added validation script for plugin structure and frontmatter

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
claude plugin marketplace add CLysis /path/to/CLysis

# Install plugins
claude plugin install legacy-investigation@CLysis
claude plugin install legacy-analysis@CLysis
claude plugin install legacy-execution@CLysis
claude plugin install legacy-knowledge@CLysis
```

#### Option B: Manual Installation

```bash
# Copy skills from each plugin
cp -r /path/to/CLysis/legacy-investigation/skills/* .claude/skills/
cp -r /path/to/CLysis/legacy-analysis/skills/* .claude/skills/
cp -r /path/to/CLysis/legacy-execution/skills/* .claude/skills/
cp -r /path/to/CLysis/legacy-knowledge/skills/* .claude/skills/

# Copy commands (if supported by your setup)
mkdir -p .claude/commands/
cp -r /path/to/CLysis/legacy-investigation/commands/* .claude/commands/
cp -r /path/to/CLysis/legacy-analysis/commands/* .claude/commands/
cp -r /path/to/CLysis/legacy-execution/commands/* .claude/commands/
```

### Step 4: Update CLAUDE.md

**No changes required** for skill paths. Skills are installed to `.claude/skills/` as before.

**Optional**: Add references to new commands:

```markdown
## Workflow Commands
- `/investigate-flow [target]` -- Investigation pipeline
- `/implement [proposal path]` -- Implementation pipeline
- `/review [PR number]` -- Review pipeline
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

Skill paths are unchanged. Skills are automatically placed in `.claude/skills/` during plugin installation.

**Before (v0.x)**:
```markdown
## Skills
This project uses skills from CLysis:
- /investigate -- Code investigation
```

**After (v1.0)**: Same! No changes needed.
```markdown
## Skills
This project uses skills from CLysis:
- /investigate -- Code investigation
```

### Optional: Document Commands

If using the new command features, documenting in CLAUDE.md is recommended:

```markdown
## Workflow Commands
- `/investigate-flow [target]` -- Investigation pipeline (project-guide -> investigate -> service-spec -> impact-analysis)
- `/implement [proposal]` -- Implementation pipeline (propose-changes -> create-pr)
- `/review [PR number]` -- Review pipeline (project-guide -> code-review)
```

## New Features in v1.0

### Commands: Workflow Automation

Commands are **pre-configured pipelines** that chain multiple skills together with human checkpoints.

**Example**: `/investigate-flow [target]`

Runs the following sequence:
1. `/project-guide [target]` -- Get context
2. `/investigate [target]` -- Find code
3. `/service-spec [target]` -- Document specification
4. `/impact-analysis [target]` -- Analyze impact
5. [Human Checkpoint] Review full report

**Benefits**:
- Reduces manual typing of skill sequences
- Enforces consistent workflows
- Makes human checkpoints explicit

### Marketplace: Easy Installation

```bash
# Add marketplace
claude plugin marketplace add CLysis /path/to/CLysis

# List available plugins
claude plugin marketplace list

# Install a specific plugin
claude plugin install legacy-investigation@CLysis
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

- [README.md](../README.md) -- Full documentation
- [ARCHITECTURE.md](../ARCHITECTURE.md) -- Architecture details
- [validate_plugins.py](../validate_plugins.py) -- Validation script
