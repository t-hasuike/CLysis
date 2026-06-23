# Advisor Delegation Rules: Worker Delegation Rules

> **Overview**: Advisor (karo) checklist of 12 required items to follow when creating worker delegation prompts. Manual reference per situation using Read.
> **Parent**: `.claude/agents/karo.md`
> **Version**: 1.0
> **Last Updated**: 2026-05-19

## §18. Required Items Checklist for Worker Delegation Prompt Creation

When the advisor includes a worker implementation prompt draft in the plan, verify all checklist items before returning to commander. Functions as cross-check against MEMORY.md "Required Explicit Items for Worker Delegation" (L91–L98).

### Required Checklist (12 Items)

| # | Item | Verification Perspective |
|---|------|---------|
| 1 | Role Explicitness | Does prompt opening include "You are a worker (executor)"? |
| 2 | Output Path | Is output destination specified as absolute path (stdout-only prohibited)? Also explicitly instruct "Include `ls -la [output path]` or `wc -l [output path]` execution result as evidence in completion report"? |
| 3 | Completion Condition | Is completion clearly defined (what constitutes "complete")? |
| 4 | Alternative Action | Is fallback action specified when blocked/uncertain (e.g., "report partial results without stopping")? |
| 5 | Edit Target Path Explicit | Is "Edit target is [specific_paths] only / others prohibited" stated with absolute path? |
| 6 | git -C Pattern | If git operations exist, does format use `git -C /path` instead of `cd /path && git`? |
| 7 | git add Explicit Specification | If git add exists, does it name files explicitly instead of `git add -A` / `git add .`? |
| 8 | Absolute Path | Are all command/file paths absolute paths (relative paths prohibited: §12 reference)? |
| 9 | Sensitive Information Absent | Are API keys, passwords, personal paths absent? |
| 10 | Inspector Lightweight Audit Output Destination Specified | If inspector delegation exists, when advisory plan present, does it state "output destination = §N append" (independent file creation prohibited. MEMORY.md L14–L17 reference)? |
| 11 | Self-Modification Warning Response | For delegations editing `.claude/` files, does prompt body include prior mention "Self-Modification security warning possible. Warning triggered > report to commander > obtain explicit commander approval > resume remaining work"? |
| 12 | Proper File Forbidden Symbol Confirmation | For delegations creating/updating primary-source files (`.claude/` subdirectory, `knowledge/` subdirectory, `reports/` proper source equivalent), does completion condition include "Emoji: `grep -nP "[\x{1F000}-\x{1FAFF}]" <target file>` is 0 count. Arrows/rule lines (U+2190-2BFF) forbidden within prose (regular text)—code blocks permitted"? |

### Early Skeleton Creation Principle (G2)

For worker delegations involving outcome files, explicitly state the following early skeleton creation principle in advisor's plan:

**Principle Content**:
- When worker begins research/analysis, first pre-create small skeleton file using Write (file title, creation date, table of contents sufficient—100-200 characters target)
- At this point, file preservation prevents worst-case "research results completely lost"
- Subsequently, append main text using Edit (approximately 400 characters per paragraph target)
- If final Edit exhausted resources, skeleton existence prevents situation "file doesn't exist at all"

**Delegation Prompt Example Expression**:
```
Step 1 (Early Priority Write): Generate skeleton file first
  File path: [output path]
  Content: Title, creation date, overview, table of contents only (approximately 100 characters)

Step 2 (Body Edit Append): Successively add §1, §2...
  Report/confirm per situation in small divisions

Step 3 (Complete): Append final section
```

**Advisor Verification Items (Addition to §18 Checklist)**:
- Does worker plan include "early skeleton creation" notation? (particularly for 600+ character documents)
- Is step division "Step 1 Write" "Step 2 Edit" explicitly stated?

### Completion Report Actual Existence Verification Evidence (G3)

When worker submits completion report, beyond just "saved to file," advisor plan must require the following actual existence verification evidence:

**Required Evidence**:
- `ls -la [saved file path]` execution result (verify permissions, size, update date/time)
  OR
- `wc -l [saved file path]` execution result (verify file line count)

**Delegation Prompt Documentation Example**:
```
## Completion Report Required Items

Include the following evidence in report:

Execute: ls -la [output path]
Result: -rw-r--r-- 1 ... YYYY-MM-DD HH:MM [filename]

OR

Execute: wc -l [output path]
Result: [N] [file path]
```

**Advisor Verification Items**:
- Does worker plan include instruction to verify existence using ls or wc?
- Does prompt accept report containing only "saved" without evidence?

### Why

2026-05-18 KPT_pm P3. Advisor plan's worker delegation prompt draft lacked "Alternative Action Instruction (what to do if blocked)" (inspector feedback—Low 1 item). MEMORY.md L91–L98 required explicit items weren't incorporated into advisor plan creation process—detected as structural omission.

### How to apply

After creating "## Worker Implementation Prompt" "## Delegation Prompt Draft" sections in plan, verify all 12 checklist items. If any item not addressed, modify relevant prompt draft before returning to commander. If verified, may record "Delegation Prompt §18 Checklist: 12/12 Verified" in plan.

**Effectiveness Verification**: In next KPT Problem section, if "inspector evaluation storage format" related items appear, check whether actual delegation prompt from this session included "output destination = §N" (via chat log or work log grep: "output destination = §N"). If item 10 reflected in actual delegation prompt "process incorporation effective," if not reflected "rerun kpt/SKILL.md Five Whys mandatory."
