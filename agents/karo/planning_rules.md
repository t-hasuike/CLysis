# karo/planning_rules.md — Plan Creation Rules

> **Role**: Child file of karo.md. Extended rules for reference during plan creation and delivery phase.
> **Parent File**: `.claude/agents/karo.md`
> **Reference Timing**: Plan creation / proposal classification / inspector evaluation reservation / terminology confirmation / tool confirmation / remediation strategy re-evaluation
> **Section Number**: §14–§17 (preserving original section numbers from karo.md)

---

## Plan Delivery Proposal Classification Obligation

When the advisor returns a plan to the commander, immediately after the "§0 Matters Requiring Commander Approval" section, the advisor must explicitly classify the proposal.

### Classification Axes (3 axes)

- **Axis A: Skill Precision Improvement** (existing skill precision/effectiveness enhancement -> `.claude/skills/*/SKILL.md`)
- **Axis B: Domain Knowledge Accumulation** (persistent team common operational knowledge -> `knowledge/domain/`)
- **Axis C: Operational Rule Improvement** (command/advisor/worker behavior norm improvement -> `shogun.md` / `MEMORY.md` / `karo.md`)

### Application Rules

- Plan must have "§0.5 Proposal Classification" section placed immediately after §0
- Specify applicable axis (A / B / C). Multiple axes are possible
- If no axis applies, mark "Purpose Unclear" -> Commander considers returning the plan
- Pre-rule introduction plans (created before this rule) are not retroactively applied

**Why:** 2026-05-13 KPT. Prevent recurrence of issue where Try (T3 sizename<->frame_name permanence) was about to be executed with unclear purpose. By mandating classification in both commander and advisor pathways, ensure comprehensive coverage of proposal routes.

### Response When Multiple Plans Have Mixed Classification Axes

When multiple related plans result in different proposal classifications (A/B/C axes), explicitly state cross-references and relationship explanations in the plan:

#### Required Documentation Items
- **Current Plan Axis**: Stated in §0.5
- **Related Plan Axes**: When referencing existing plans, include related plan axes
- **Relationship Explanation**: Reason for different axes (e.g., "Current plan = C-axis primary (progress management) / Related ST-2 execution plan = B-axis primary (evaluation results accumulation) / Both are complementary")

#### Application Cases
- Multiple plans within same phase (execution plan + division plan, etc.)
- When referencing related plans in §X

#### Impact of Violation
- When commander references both plans in parallel: "Axes differ but which is correct?" confusion
- Cannot determine complementary relationship between plans

**Why**: 2026-05-13 KPT_2 P3. ST-2 execution plan (B-axis primary) and ST-2 division plan (C-axis primary, A-axis secondary) had different axes, but cross-reference explanations were insufficient—caught by inspector review. Without axis difference relationship explanations, either: worker cannot follow plan instructions (section not found), or worker makes independent judgment about appropriate placement (unplanned decision).

**How to apply**: Add "Related Plans" item to §0.5, including related plan path + axis. If axes differ, add one-line relationship explanation.

## §14. Plan End-of-Document Inspector Evaluation Section Reservation Obligation

When the advisor creates a plan, reserve a "§Final. Inspector Evaluation Result (To be appended after evaluation)" section at the end.

### Required Items
- Section Title: "§N. Inspector Evaluation Result" (N = final section number in plan)
- Content: Blank reservation with note "To be appended after inspector evaluation"
- Placement: Final section of plan
- **Pre-listed Remediation Items List (by severity)**: If remediation needs are discovered within the plan, pre-place a "Remediation Items List" before §N, organized by severity (High/Medium/Low). Purpose is to enable inspector to verify remediation completeness during audit.

### Inspector Append Authority
- Inspector appends evaluation results to reserved section
- **Authority to directly correct advisor errors** (numerical values, line numbers, code excerpts, etc.)
- When correcting, use Edit on relevant plan section + record "Text L? corrected" in §Final inspector evaluation section

### Why
2026-05-14 Commander Instruction: "Rather than advisor and inspector submitting separately, consolidate together." This rule consolidates into one file.

### How to apply
When creating plan, reserve final §N (Inspector Evaluation Result). Inspector directly edits advisor plan (no separate new file creation needed).

## §15. Pre-confirmation of Terminology Commander Wishes to Avoid

Before the advisor begins planning, if commander may wish to avoid specific terminology or expressions, confirm in advance.

### Confirmation Targets (Examples)
- **Industry Terminology**: "Vendor" "Outsourced Partner" etc. -> Commander may prefer alternative phrasing like "external implementation partner"
- **Personal Information**: Personal paths (e.g., username, actual system paths), actual IDs
- **Internal Proprietary Names**: Team names, organization names

### Confirmation Methods
- Search past commander feedback in MEMORY.md / existing plans
- If unclear, confirm directly with commander

### Impact of Violation
- Post-completion remediation replacement cost (17 replacement instances: 2026-05-14 KPT_3 P1)

**Why**: 2026-05-14 KPT_3 P1. Advisor decisively used "Vendor" terminology -> Commander instructed "Don't use the word vendor" -> Post-correction of 17 instances required.

**How to apply**: List "Planned Terminology" in plan opening section. Pre-confirm with commander any terminology with documented feedback history.

## §16. Pre-confirmation of Tool Restriction Matters

When the advisor's plan includes draft prompts for worker implementation using specific tools (gh CLI, specific APIs, etc.), pre-confirm tool restriction matters.

### Confirmation Targets
- **gh CLI**: Subcommand support status (e.g., `gh discussion create` unsupported—GraphQL API required)
- **API Rate Limits**: GitHub API, external service
- **Permission Restrictions**: Write permissions for specific repositories

### Confirmation Methods
- Search similar cases in past worker execution logs
- Reference official documentation
- If uncertain, conduct pre-run dry-run

### Impact of Violation
- Worker execution immediate failure, alternative means discovery cost

**Why**: 2026-05-14 KPT_3 P2. Discussion creation task revealed gh CLI unsupported at worker execution -> switched to GraphQL API. Pre-confirmation would have incorporated alternative approach at planning stage.

**How to apply**: During plan strategy, list tools/commands used in worker prompt draft. Confirm official documentation for gh CLI unsupported commands or API limits.

## §17. Inspector Feedback Response—Remediation Strategy Re-evaluation

When the advisor modifies the plan based on inspector feedback, constantly re-evaluate whether the "remediation strategy itself" creates secondary bugs. If remediation strategy presumes incorrect execution environment, timing, or target scope, the post-correction plan invites further inspector feedback.

### Remediation Strategy Re-evaluation Rules

When addressing inspector feedback, re-evaluate the remediation strategy itself against these 3 perspectives. Verify that remediation solving the feedback doesn't introduce "additional structural errors" at the plan conception stage.

- **Remediation Timing**: Verify the "execution timing" of action/check indicated by remediation strategy is correct. Example: Worker self-check grep—is it "before PR creation" or "immediately before sync execution"? Is it "work-side repository" or "primary-source side"? Incorrect timing design means remediation as planned won't reach expected value (e.g., 0-count confirmation)
- **Remediation Scope**: Verify the target range indicated by remediation strategy (file groups, directory, execution environment) properly addresses the feedback's essence. Example: "Confirm 0 count on worker-side repository"—but worker-side has legitimate references remaining, structurally preventing 0-count outcome. Scope specification itself is incorrect
- **Post-remediation Verification Step**: Explicitly state in plan whether remediation strategy functioned. Without verification step, cannot judge remediation effectiveness nor ensure non-recurrence. Example: Rather than just "grep execution confirms 0 count," include "execution environment, execution directory, expected result"

### Required Documentation Items (Add to Remediation Response Section)

Inspector feedback remediation sections must include:

- **Feedback Source**: Inspector evaluation report path, feedback number
- **Remediation Strategy**: What remediation does and how
- **Remediation Timing**: When remediation strategy executes (pre-PR / pre-sync / post-merge, etc.)
- **Remediation Scope**: File groups/execution environment targeted by strategy (work-side / primary-source-side / both, etc.)
- **Post-remediation Verification Step**: Specific procedure/expected result to confirm remediation succeeded

### Impact of Violation

Skipping remediation strategy re-evaluation creates "new feedback generated post-remediation" cycles. Each additional cycle adds plan remediation/re-evaluation round-trip costs.

### Why

2026-05-18 KPT P3. Plan §4.2 self-check design specified "execute grep on worker-side repository and confirm 0 count," but worker-side has 17 legitimate OSS repository mentions remaining, making 0-count structurally impossible. Inspector lightweight re-evaluation detected as secondary bug "remediation strategy itself structurally incorrect." Pre-evaluating remediation strategy timing/scope at planning stage would have prevented this case.

Reference: `reports/2026.05.18_kpt.md` Problem P3 / `reports/metsuke_review/20260511_pr133_plan_re_review.md` (lightweight re-evaluation report—§4.2 self-check execution timing error detected)

### How to apply

When developing remediation plan version, explicitly state "Remediation Timing," "Remediation Scope," "Post-remediation Verification Step" in inspector feedback response section. Concretely document execution environment (worker repo / primary-source repo / OSS repo which one?) and expected result (0 count / N count / specific pattern detection) the remediation strategy addresses. After finalizing remediation strategy, conduct self-check: "Does this remediation strategy have correct timing and scope?" before returning to commander.

### Pre-delivery Self-verification Checklist

Advisor must verify all 6 items before submitting plan to inspector lightweight audit:

1. **Line Number Match Confirmation**: When plan documents line numbers for same file across multiple sections, verify all section line numbers match same measured `wc -l` value (§10 Multiple Section Line Number Match Confirmation). Verification command: `grep -nE "L[0-9]{2,}" {plan path}` to list line number references and cross-check
2. **Terminology Pre-confirmation**: Verify plan terminology/proprietary terms don't include expressions commander wishes to avoid (§15). Reference MEMORY.md feedback
3. **Estimation Explicitly Marked**: Probability/count/time estimates must include "(estimated value / advisor estimate)" or "approximate" notation (CLAUDE.md Required Rule 5)
4. **Range Notation**: Expected additional lines/modification lines must use 2-value min/max notation (§10 Line Count Estimation Buffer Rule). Verify single-value "(+X lines)" notation doesn't remain
5. **Worker Delegation Prompt 10 Items**: If plan includes worker delegation prompt draft, verify §18 checklist all 10 items confirmed. Special attention to "deletion/cleanup procedure," "alternative action," "inspector lightweight audit output destination specification (§N append)" absence
6. **Numerical Consistency Confirmation**: When estimated lines/added lines documented across multiple sections (e.g., §2.x Estimated Lines and §5.x Delegation Prompt Completion Condition), verify all section values based on same actual execution results (§10 Multiple Section Line Number Match Confirmation). Verification command: `grep -nE "\+[0-9]+|[0-9]+〜[0-9]+ ?lines" {plan path}` to list line count references and cross-check all sections

Why: KPT_session4 P2 (2026-05-18). Markdown distribution implementation plan's inspector feedback 3 items (Medium 1: cleanup procedure absent / Low 1: line number 2-line offset / Low 1: estimation notation absent) were all pre-detectable. Incorporating plan-stage self-verification checkpoint reduces inspector round-trip cost.

## SS18. Symbol Rule Revision Task Pre-execution Scan Obligation

For tasks involving symbol rules (forbidden symbols, allowed symbols, in-code-block retention, etc.), advisor must complete the following pre-execution scans before design:

### Pre-execution Scan Requirements

1. Conduct full-count symbol grep of target files
   - Emoji detection: `grep -rnP "[\x{1F000}-\x{1FAFF}]" .claude/` (forbidden—all locations remediation target)
   - Arrow/rule line detection: `grep -rnP "[\x{2190}-\x{2BFF}]" .claude/` (prose (regular text) remediation target only. In-code-block permitted)
   - Distinguish and report counts separately: within code blocks (```-enclosed areas) vs. within prose
   - Counts must be actual numbers from grep output, not estimates (estimation prohibited)

2. Design plan based on scan results
   - Use scan result counts as basis for work scope estimation
   - Prohibit approximate expressions like "approximately N lines." Use actual counts (e.g., "122 lines")
   - Report emoji count (all location remediation) and arrow/rule line prose-only count separately

3. Fence-tracking necessity judgment
   - When in-code-block retention rule applies, specify implementation method enabling fence-tracking
   - Explicitly state in worker delegation prompt "Code Block Retention: Required/Not Required"

### Background

- 2026-06-16 KPT P3: Inspector plan evaluation count estimate "approximately 8 lines" actually 122 items (approximately 15x divergence)
- 2026-06-16 KPT P1: Worker scan scope omission misstatement (10 items missing)
- 2026-06-16 KPT P2: Code block unintended replacement (fence-tracking unused)
- Five Whys Conclusion: Plan design based on estimation approximation sequentially caused estimate error, scan omission, boundary judgment error
