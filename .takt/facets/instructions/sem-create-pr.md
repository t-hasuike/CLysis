<!-- This instruction facet is based on the TAKT framework (https://github.com/nrslib/takt), MIT License, Copyright (c) 2026 Masanobu Naruse. -->
# SEM Create PR - PR Creation Procedure

## Overview

Push the SEM-draft.md that passed the G2 gate to the project's working branch and create a PR.

---

## Procedure

### Step 1: Confirm the state of the clone

```bash
git -C <repo clone path> status --short
git -C <repo clone path> branch
```

Confirm that the clone is on the main branch and the working tree is clean.

### Step 2: Create a branch

```bash
git -C <repo clone path> checkout -b docs/sem<number>-<domain-name>-domain main
```

### Step 3: Place the file

Place SEM-draft.md with the canonical file name under [your-project-knowledge-dir]/semantic/.

File-name rule: `SEM-XX_<domain-name>_domain_model.md`

### Step 4: Commit

```bash
git -C <repo clone path> add [your-project-knowledge-dir]/semantic/SEM-XX_<domain-name>_domain_model.md
git -C <repo clone path> commit -m "$(cat <<'EOF'
docs: create SEM-XX <domain-name> semantic model

When: YYYY-MM-DD
Who: sem-scribe (SEM Writer workflow)
What: created the semantic model for the SEM-XX <domain-name> domain
Why: to record the business meaning of the <domain-name> domain in a form developers can reference
How: created following the 6-chapter structure of the /current-semantic skill (Overview, ER diagram, Column definitions, Flag table, Pitfalls, SQL)
EOF
)"
```

`git add -A` is prohibited. Specify the target files explicitly.
Do not include `#` comments in git commands.

### Step 5: Push and create the PR

```bash
git -C <repo clone path> push origin docs/sem<number>-<domain-name>-domain
```

```bash
gh pr create --repo [your-repo] --title "docs: create SEM-XX <domain-name> semantic model" --body "$(cat <<'EOF'
## Summary

Created the semantic model (SEM) for the SEM-XX <domain-name> domain.

## What was created

- Target domain: <domain-name>
- Target tables: <primary table names>
- 6-chapter structure: Overview, ER diagram, Column definitions, Flag table, Pitfalls, SQL samples

## Quality confirmation

- G2 quality gate: pass (see sem-audit.md)
- mermaid validation: 0 errors
- Forbidden-keyword grep: 0
- Unicode symbol grep: 0
- Pitfalls: <N>
- Soft-delete condition: applied to every SQL statement

## Review request

Please review focusing on the accuracy of business meaning (the domain description in chapter 1, the column meanings in chapter 3, and the flag values in chapter 4).
EOF
)"
```

### Step 6: Report the PR URL

After the PR is created successfully, report the PR URL to the leader.

---

## Notes

- Pushing directly to the main branch is prohibited.
- `git add -A` is prohibited (specify the target files explicitly).
- Do not include `#` comments in gh commands.
- On PR creation failure, report ABORT (record the failure reason and the last operation).
