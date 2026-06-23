# karo/validation_rules.md — Validation and Precision Check Rules

> **Role**: Child file of karo.md. Extended rules for reference during plan precision check and worker delegation verification phase.
> **Parent File**: `.claude/agents/karo.md`
> **Reference Timing**: Plan precision check / pre-execution confirmation / judgment logic documentation
> **Section Number**: §7–§12, §19 (preserving original section numbers from karo.md)

---

### 7. Multiple File Same-Type Rule Cross-verification Confirmation

When plan documents same-type rules across multiple files (e.g., shogun.md / create-pr/SKILL.md / MEMORY.md, etc.), cross-verify each file's item count and granularity. Integrity breakdown (one file missing items) generates inspector detection -> remediation re-work (source: 2026-05-10 afternoon KPT Problem 1).

### 8. OSS Repository Reflection Plan Strategy—Bilateral Actual Execution Scan Confirmation

When strategizing plan for OSS public repository reflection, verify **both work-repository-side differences AND OSS repository current implementation via actual execution scan**. OSS side may already have translation, generalization, or upper-compatibility enhancements in progress; using only work-repository-side differences as reference basis can result in unnecessary edits.

Specific Checks:
- Read OSS repository target file and verify current state
- Detect current status of security keywords (proprietary repo name / organization name / application codes, etc.)
- Confirm presence/absence of framework development, systematization
- Judge integrating optimal portions from bilateral sides
- **When specifying target files in plan/delegation prompt, explicitly state BOTH work-repository-side path AND OSS repository-side path.** When identical line numbers exist (e.g., L54) on both sides, which side becomes context-dependent, creating confusion risk during commander's delegation prompt transcription.

  Documentation format (example):
  - Work-repository-side: `<work-repo-root>/.claude/skills/<skill>/SKILL.md L<line-number>`
  - OSS-repository-side: `<OSS-repo-root>/<category>/skills/<skill>/SKILL.md L<line-number>(requires re-scan)`

  OSS repository-side line numbers likely diverge from actual execution. After §8 bilateral execution scan results, document both-side paths. Form "OSS-side: L?? (requires re-scan)" interim notation, delegating actual execution scan to worker.

(Source: 2026-05-11 morning KPT Problem 1 — current-distortion was OSS repository upper-compatible, overlooked at plan conception)
(Source: 2026-05-11 evening KPT Problem 1 — plan "work-repo-side L54" mistranscribed to delegation prompt as "OSS-repo-side L54")

**OSS Reflection Timing Criterion**: Reference `docs/sync-to-oss-procedure.md` "Sync Timing Criterion" section. Follow composite rule of high priority immediate sync and medium-or-lower theme convergence 7-day upper limit.

### 9. Policy Actuality Consistency Check

During plan strategy, verify existing policy documents (README / rules / manuals, etc.—broadly reference documents, excluding code implementation files) documentation aligns with implementation actuality.

Specific Checks:
- Verify target document documentation date/time
- Confirm documentation content matches latest commander decision (reference memory/ feedback)
- Verify actual implementation files count/language/composition matches documentation
- Upon discovering divergence, confirm in plan review whether to include "policy document update" with commander

(Source: 2026-05-11 Sixth Session KPT Problem 1 — knowledge/domain/README.md L63 "English (OSS public-release assumed)" diverged from implementation reality (37 Japanese files). Advisor plan v1 premised on above policy, generating plan hand-back v1->v2->v3 cycles)
(Source: reports/investigation/20260511_knowledge_domain_language_policy_recheck.md — factual investigation evidence)

### 10. Numerical Value Count Actual Execution Scan Confirmation Criterion

Plan numerical values/counts (line numbers, distortion counts, scope-by-breakdown aggregate, file counts, etc.) must base on actual execution results. Planning from estimate values forces large modifications at implementation stage, directing worker delegation prompts with incorrect foundation.

Specific Checks:
- **Actual Execution Mandatory**: Obtain actual measured values using `Read` / `Grep` / `wc -l`, etc. Prohibit scanning only opening of file and estimating "approximately X count"
- **Source Documentation**: Numerals documented in plan must include foundation (file path, line number, command execution result). Example: "Distortion count: 205 items (reports/distortions_integrated_summary.md aggregate, as of 2026-05-11)"
- **Clear Distinction: Estimate vs. Actual**: Plan items unable to verify at strategy stage: explicitly mark "approximate" "target," distinguishing from measured values. Example: "Modification location estimate: 40-50 files (exact count to confirm at execution stage)"
- **Re-scan Trigger**: Numerical values (especially file counts, line counts) created 3+ days before plan strategy age recommend re-scan prior to worker delegation

Impact of Violation: During advisor plan inspector evaluation, "numerical error" "actual execution omission" receives medium or above severity rating. Root cause for plan hand-back (v1->v2->v3) cycles.

(Source: 2026-05-01 KPT Problem 2 — Proposal Table ST-3.1 documented distortion count "200 items," actual execution showed 205 items. Estimate vs. measured distinction insufficient—noted as issue)

- **Multiple Section Line Number Match Confirmation**: When plan references same file's line numbers across multiple sections (e.g., §1.1 Actual Execution Results / §3.2 Append Position / §4.3 Insert Position), pre-finalization conduct self-check verifying all section line numbers base on identical actual execution result. Self-check example: `grep -n "L[0-9]\{2,\}" {plan path}` lists line number reference locations, verify all match identical `wc -l` measured value.

(Source: 2026-05-18 KPT_pm P2 — Plan §1.1 actual execution line count and §4.3 insert position line number desynchronized at finalization)

- **Line Count Estimation Buffer Rule**: When plan estimates added/modified lines, include **+1 to +2 line buffer** for Markdown formatting cleanup (inter-section space, bullet-list-end spacing adjustment). Example: "Estimated additional lines: +4 to +6 lines (min value: body 4 lines, max value: buffer-inclusive)" and document using 2-value min/max rather than single "(+X lines)." Single-value notation causes precision misunderstanding.

(Source: 2026-05-18 KPT_evening P2 — Plan +15 line prediction vs. implementation +18 lines (Δ+3 lines). Markdown formatting cleanup space not accounted in plan)

- **Body Transcription Type Exception (±50% Buffer)**: Plan body (table specification, section definition, etc.) transcribed to separate file (DEVELOPMENT.md, karo.md, etc.) verbatim should allow **±50% buffer** from transcription-source line count. Trigger Condition: (1) transcription source is advisor plan §X table/list-format specification, AND (2) transcription destination is existing file append (not new file creation—this exception inapplicable). Reason: Transcription introduces variable table column width, spacing, Markdown line-break elements, exceeding ±20% specification.

(Source: 2026-05-19 KPT_session7 P3 — DEVELOPMENT.md append +56 lines vs. plan predict +15–+25 lines (+124% excess). Body transcription type added special exception-rule to accommodate actuality)

- **New File Creation Type Exception Rule (±100% Buffer)**: New file creation type planning should allow **±100% buffer** of estimated lines (minimum half to maximum double).
  - Trigger Condition (1): New file creation (not existing file append)
  - Trigger Condition (2): Document type one of: SPEC document / Framework definition / Guideline / Mapping document
  - Source: KPT_session8 P2 / KPT_session9 P2 / KPT_session10 P3 (consecutive 3 times not executed—Five Whys mandatory enforcement target)

### 11. Append-destination Section Actual Existence Confirmation Criterion

When advisor plan proposes append to "shogun.md / karo.md / MEMORY.md / other rule documents," explicitly confirm append-destination section name existence in plan.

Specific Checks:
- **Append-destination File Path**: Absolute path specification
- **Append-destination Section Name**: Exact section header in file (e.g., "## Required Explicit Items for Worker Delegation")
- **Existence Confirmation Method**: Document confirmation command and result in plan: e.g., `grep -n "^## Relevant Section" {file}`, etc.
- **Append Position Explicit**: "Append to existing section end" "Insert new between §N and §N+1" etc., state relative position to existing section
- **Section Nonexistence Response**: When append-destination section nonexistent: state "existing section nonexistent—new section append" and document new section position (file end / after specific section, etc.)

**Why**: 2026-05-13 KPT P2. Proposal classification framework plan assumed shogun.md "Commander Report/Approval Request Format" section as append-destination, but inspector feedback revealed unconfirmed existence. Worker during execution either: unable follow plan instructions (section not found), or worker judges appropriate position independently (unplanned decision). Plan-stage section name existence confirmation prevents both scenarios.

**How to apply**: During strategy, actually execute-scan (Read / grep) append-destination file and confirm relevant section name. Document confirmation command (e.g., `grep -n "^## Section Name" /path/to/file.md`) and execution result in plan. When section undetected: explicitly state "new section append."

### 12. Worker Implementation Prompt Absolute Path Required

When advisor plan includes worker implementation prompt draft, all command examples, file paths, grep targets must specify absolute paths:

#### Required Items
- **File Path**: `/absolute/path/to/{org}/{repo}/...` format absolute paths
- **Command Example**: `ls /absolute/path/` `find /absolute/path -name ...` `grep -n "pattern" /absolute/path` format
- **Relative Path Prohibited**: `ls .github/` `find ./laravel/` `grep -n . *` etc.

#### Impact of Violation
- Worker execution directory uncertain (project-root assurance absent)
- Relative-path commands immediate fail -> evaluation data collection fail -> re-delegation cost

#### Self-check
- Post-strategy, use `grep -nE "ls \.\|find [a-z]\|grep .*-n [^/]" {plan}` to detect remainder
- Confirm 0-count detection before returning to commander

**Why**: 2026-05-13 KPT_2 P2. ST-2 execution plan (492 lines) had 2 relative path locations remaining—inspector feedback revealed. Worker execution failure risk created.

**How to apply**: During strategy, grep worker prompt draft section for relative paths. If detected, substitute absolute paths then re-grep confirming 0-count.

## Pre-execution Confirmation

Before reporting plan decomposition results to commander, verify:

- [ ] Can each subtask complete independently by single worker?
- [ ] No multiple worker edits to same file occur?
- [ ] Dependencies explicit? Execution order appropriate?
- [ ] Parallel-executable tasks explicitly identified?
- [ ] Each subtask worker assignment appropriate (expertise domain match)?
- [ ] Risks/cautions identified?

## §19. Judgment Logic Documentation Principle

Advisor plan decomposition, decision criteria, scope boundaries must avoid vague expression—define via checklist-format conditions.

- **Judgment Condition Documentation**: Prohibit vague branch descriptions "situation-dependent," "case-by-case." Express branches "X case result Y, Z case result W" checklist-format
- **Threshold Explicit**: Worker delegation size criteria, scope boundary, quality decision criteria specified via numerical/explicit text, not entrusting to worker contextual judgment (= LLM arbitrary judgment)
- **Decision-Reject Foundation Recording**: When judging subtask "out-of-scope," explicitly state plan foundation (reason, condition)

Why: R5 Deterministic Logic. Agent behavior norm judgment logic should be controlled via explicit rules, not LLM "atmosphere."

### Commander Presentation Comparison Table Creation—Perspective Checklist

Before advisor presents comparison table of options to commander, verify these 4 perspectives:

1. **Precision/Success Probability Perspective Explicit**: Does comparison include each option's "precision, success probability, failure cost" comparison axis? Document as "Estimated Success Probability: approximately XX% (estimated value / advisor estimate)" format
2. **Time-axis Exclusion**: Does prompt list only time-axis "completes quickly" "time-consuming" as merit/demerit? Place time as supplemental info or omit from comparison
3. **Substantive Characteristic Comparison**: Compare each option not via "order (which comes first)" but via "substantive characteristics each option possesses (precision, rollback-feasibility, cumulative risk, etc.)"
4. **Commander Interest Alignment Confirmation**: Before presentation, confirm "Does comparison axis contain information commander requires for decision-making?"

Why: KPT_session4 P1 (2026-05-18). Markdown distribution option A/B comparison presented time-axis only, commander feedback "Want precision comparison." Commander pre-presentation confirmation process lacked perspective-check.

5. **Concrete Event Documentation Obligation**: When documenting success probability/failure cost figures (e.g., approximately 70%), always concurrently document:
   - **Failure-case Concrete Event**: "What specifically occurs if option fails" in 1+ sentences
   - **Success-case Concrete Event**: "What specifically is achieved if option succeeds" in 1+ sentences
   - **Prohibited Documentation**: "Success probability: approximately 90%" only (standalone figure prohibited)
   - **Approved Documentation**: "Success probability: approximately 90% (failure case: karo.md end boundary blank-lines become disordered / success case: planning_rules.md independent plan capability)"

Why: KPT_session5 P1 (2026-05-18) Five Whys. Prior Try T1 added 4 perspectives, but this session saw 2 re-occurs with figure-only documentation. Five Whys deepest layer "pre-presentation substance review process mandatory" addressed via 5th item addition.
