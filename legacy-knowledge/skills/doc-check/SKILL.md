---
name: doc-check
description: Document integrity diagnosis skill. Detects dead links, naming convention violations, README mismatch, and reports/ promotion readiness. Runs at the end of documentation work.
---

> This is a generic skill from [CLysis](https://github.com/t-hasuike/CLysis).
> Terminology can be customized via `config/terminology.md`.

# /doc-check — Document Integrity Verification (Diagnosis)

## Role

**Diagnosis (Health Check)**: Inspects document integrity and reports problems. Does not fix or reorganize — only detects and reports.

**Role responsibilities**:
| Role | Responsibility |
|------|---|
| **Leader** | Review diagnosis results, determine remediation strategy |
| **Planner** | For large-scale diagnosis, plan inspection approach (optional) |
| **Worker** | Execute checklist items (dead-link detection, naming rules, README consistency, promotion readiness) |
| **Auditor** | Audit the diagnosis results themselves (ensure no detection gaps) |

**Strict compliance with F002**: Leader does not personally run diagnostics. Delegate execution to workers.

**Distinction from `/doc-organize`**:
- `/doc-check` = **Judge** (integrity verification + As-Is/To-Be promotion judgment + placement error detection)
- `/doc-organize` = **Execute** (judgment results → actual file placement/reorganization)

```
/doc-check (diagnosis) → detect problems, promotion decision
       ↓ if problems found
/doc-organize (execution) → actually fix files
```

Diagnosis only? Use `/doc-check` alone. Need to reorganize? Use `/doc-check` → `/doc-organize` in sequence.

### Language and Tone

Clear, professional reporting with business etiquette. Clearly state OK/NG, explicitly state what is unclear.

---

## Activation Timing

- **Required**: Run after documentation work (file additions, renames, integrations)
- **Recommended**: Final verification before session end
- **Optional**: When decision maker explicitly requests "verify integrity"

---

## Checklist Items

### 1. Dead-Link Detection

Scan all `.md` files under knowledge/ for Markdown links `[text](path)` and verify link targets exist.

**Execution**: `bash scripts/check-dead-links.sh`

**Scope**:
- All `.md` files under knowledge/
- CLAUDE.md (@references)
- workspace/ contents
- .claude/skills/ contents

**Excluded**: External URLs (http/https), mailto links, anchor-only links (#)

### 2. Naming Convention Check

Verify knowledge/ files follow naming conventions by character type.

| Prefix | Perspective | Target |
|--------|------------|--------|
| `birdseye_` | Bird's eye view (overview) | High-level overviews, architecture diagrams |
| `fisheye_` | Fish eye view (time-series) | Time-series flows, process tracing |
| `wormseye_` | Worm's eye view (detail) | Implementation details, specifications |
| (none) | Excluded | README.md, templates, indices, root lists, _reference/ contents |

**Check method**: Scan knowledge/system/ and knowledge/domain/ `.md` files (excluding: README.md, filenames ending in `_template.md`, files in `_reference/` directories) for required prefix. Report any unprefixed files.

**Execution command**:

```bash
find knowledge/domain/ knowledge/system/ -name "*.md" \
  ! -name "README.md" ! -name "*_template.md" ! -path "*/_reference/*" \
  | while read f; do
  basename="$(basename "$f" .md)"
  if [[ ! "$basename" =~ ^(birdseye|fisheye|wormseye)_ ]]; then
    echo "[NAMING VIOLATION] $f"
  fi
done
```

**Pass criteria**: Output is empty (zero violations)

### 3. README Consistency Check

Cross-reference knowledge/README.md against actual directory structure.

- **Undocumented files**: Exist in directory but not listed in README.md
- **Non-existent files**: Listed in README.md but not actually in directory

### 4. reports/ Promotion Readiness

Verify promotion status of files in reports/.

**Promotion Decision Criteria (Purpose-Based)**:

| Investigation Purpose | Promotion Timing | Decision Maker |
|--------|------------|--------|
| Current spec survey (As-Is) | **Immediate promotion** | Leader/Worker |
| Future plans, improvement proposals (To-Be) | **Hold** (promote after decision maker approval) | Decision maker |
| One-time investigation | **Discard candidate** (discard if valueless) | Leader |

**Check content**:
- List reports/ files without `> **Promoted**` mark
- Judge each: "As-Is (promote immediately)" or "To-Be (wait for decision)"
- Suggest `/doc-organize` activation if promotion candidates exist

### 4-b. Mark Omission Detection (Cross-Reference Check)

For unpromoted files, run heuristics to detect "possible mark omission".
**Results are suggestive only; final judgment is leader's.**

**Procedure**:
1. Extract keywords from unpromoted filename (minus extension/prefix)
   - Example: `c19_bulk_delivery_90days_investigation.md` → `bulk_delivery_90days`
   - Example: `pr37_arrangement_route_draft.md` → `pr37_arrangement_route`
2. Grep knowledge/ for keywords (case-insensitive)
3. Interpret results using the 4-tier judgment table:

   | Hit Count | Judgment | Label | Action |
   |-----------|---------|-------|--------|
   | 5+ hits | Definitively reflected | `[Promoted candidate]` | Recommend adding promotion mark |
   | 3-4 hits | Partially reflected (strong) | `[Review needed]` | Consult leader for judgment |
   | 1-2 hits | Partially reflected (weak) | `[Info]` | Record as information. No immediate action required |
   | 0 hits | Not reflected | `[Not reflected]` | Recommend discard evaluation |

**Prohibition**: Do not judge by grep matches alone. For each hit, verify one line of the hit file's content to confirm the keyword appears in the context of "same information reflected." Do not miscount partial filename matches or unrelated context hits.

**Caveat**: Keyword grep detects "some content exists" but NOT "information fully integrated." Human judgment is final.

**Future enhancement (Phase 2)**: Add YAML front-matter (`promoted_to:` field) to reports/ files for structured tracking, improving accuracy.

---

## I/O Specification

### INPUT
| Type | Content | Required/Optional |
|------|---------|-----------|
| Scope | knowledge/ / reports/ / all | Optional (default: all) |

### OUTPUT
| Type | Format | Destination |
|------|--------|-------------|
| Diagnosis report | Markdown (4-section structure) | reports/ + stdout |

### Prerequisites
- scripts/check-dead-links.sh exists
- knowledge/README.md is current

### Downstream Skills (Pipeline)

| Skill | Condition | Instruction |
|-------|-----------|-------------|
| `/doc-organize` | When 1+ promotion candidates detected | Save diagnosis results, then report to leader for approval before executing `/doc-organize` |

> **When To-Be (awaiting decision) items are numerous**: Present the full list to decision maker and await priority judgment before executing
>
> **Fallback**: If prerequisites are not met, report to leader and await further instructions

---

## Output Format

```
=== /doc-check Execution Results ===

## 1. Dead-Link Detection
- Detected: X cases
- [DEAD] filename:line -> link target

## 2. Naming Convention Check
- Violations: X cases
- [NAMING] filename -> missing prefix

## 3. README Consistency
- Undocumented: X cases
- Non-existent: X cases

## 4. reports/ Promotion Readiness
- Unpromoted (As-Is, recommend immediate): X cases
- Unpromoted (To-Be, awaiting decision): X cases
- Promoted: X cases

=== Summary ===
Problems found: X cases (requires action)
OR
No problems found: Integrity check complete
```

---

## Follow-up Actions

- Dead-link → Fix links in target files
- Naming violations → Rename files + update references
- README undocumented → Add to README.md
- Promotion candidates → Activate `/doc-organize` or confirm decision maker approval

---

## Related Skills

- `/doc-organize` — Execute organization/filing based on diagnosis
- `/doc-update` — Maintain knowledge/ freshness

---

## Reference Files

- `scripts/check-dead-links.sh` — Dead-link detection script
- `knowledge/README.md` — Document structure (single source of truth)
