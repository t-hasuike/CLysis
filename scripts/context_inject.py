#!/usr/bin/env python3
"""
Dynamic context injection script.
Called from the UserPromptSubmit hook, analyzes keywords in the prompt and
outputs relevant feedback memory file paths and knowledge directory contents to stdout.

Configuration:
  CLYSIS_MEMORY_DIR  - Override the default memory directory path
                       Default: ~/.claude/projects/<project-hash>/memory
  CLYSIS_KNOWLEDGE_DIR - Override the default knowledge directory path
                         Default: ./knowledge (relative to project root)
"""
import json
import sys
import os
import re
from pathlib import Path


def find_memory_dir() -> Path:
    """Resolve the memory directory path.

    Priority:
    1. CLYSIS_MEMORY_DIR environment variable
    2. Auto-detect from ~/.claude/projects/ (first match with /memory subdir)
    """
    env_override = os.environ.get("CLYSIS_MEMORY_DIR")
    if env_override:
        return Path(env_override)

    # Auto-detect: find first project memory directory under ~/.claude/projects/
    projects_dir = Path.home() / ".claude" / "projects"
    if projects_dir.exists():
        for project_dir in sorted(projects_dir.iterdir()):
            memory_dir = project_dir / "memory"
            if memory_dir.is_dir():
                return memory_dir

    # Fallback: return a non-existent path (graceful degradation)
    return projects_dir / "unknown" / "memory"


def find_knowledge_dir() -> Path:
    """Resolve the knowledge directory path.

    Priority:
    1. CLYSIS_KNOWLEDGE_DIR environment variable
    2. ./knowledge relative to current working directory
    """
    env_override = os.environ.get("CLYSIS_KNOWLEDGE_DIR")
    if env_override:
        return Path(env_override)

    return Path.cwd() / "knowledge"


def main():
    # Read JSON from stdin
    try:
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return

    prompt = input_data.get("prompt", "")
    if not prompt:
        return

    MEMORY_DIR = find_memory_dir()
    KNOWLEDGE_DIR = find_knowledge_dir()

    # Keyword-to-file mapping: keywords in prompt -> relevant memory files or knowledge paths
    keyword_feedback_map = {
        # Presenting options / approvals
        r"present|proposal|approval|option|alternative|decision": [
            "feedback_decision_format.md",
            "feedback_uesama_presentation_substantive_review.md",
        ],
        # Worker delegation
        r"delegate|worker|task|assign": [
            "feedback_worker_stall.md",
            "feedback_hallucination_prevention.md",
        ],
        # PR / commits / version control
        r"PR|pull.?request|commit|push|branch": [
            "feedback_metsuke_pr_check.md",
        ],
        # Comparison / analysis / impact
        r"compar|analys|impact|effect": [
            "feedback_comparison_task_karo.md",
        ],
        # Retrospective / KPT
        r"KPT|retrospective|keep|problem|try": [
            "feedback_kpt_parallel_task_identification.md",
        ],
        # Diagrams / mermaid
        r"mermaid|diagram|flowchart|sequence": [
            "feedback_mermaid_syntax_pitfalls.md",
        ],
        # Debugging / errors / investigation
        r"hypothes|error|bug|debug|investigat": [
            "feedback_hypothesis_check.md",
        ],
        # Print / fulfillment domain
        r"print|fulfillment|delivery|shipping": [
            "knowledge/domain/pr3_fulfillment/",
        ],
        # Contract / pricing domain
        r"contract|price|pricing|plan|wholesale": [
            "knowledge/domain/pr2_contract/",
        ],
        # Event / photo / upload domain
        r"event|photo|photograph|upload|shoot": [
            "knowledge/domain/pr3_service_use/",
        ],
        # Sales / incentive / finance domain
        r"sales|incentive|aggregat|financ|revenue": [
            "knowledge/domain/pr3_sales_incentive/",
        ],
    }

    matched_files: set = set()

    for pattern, files in keyword_feedback_map.items():
        if re.search(pattern, prompt, re.IGNORECASE):
            matched_files.update(files)

    if not matched_files:
        return

    # Build output
    output_lines = []
    output_lines.append("[Dynamic Context Injection] Related feedback/knowledge:")

    for f in sorted(matched_files):
        if f.startswith("knowledge/"):
            # For knowledge directories, list up to 5 markdown files
            rel_path = f.replace("knowledge/", "", 1)
            dir_path = KNOWLEDGE_DIR / rel_path
            if dir_path.exists():
                md_files = sorted(dir_path.glob("*.md"))[:5]
                output_lines.append(f"  [{f}] Related files:")
                for md in md_files:
                    output_lines.append(f"    - {md.name}")
        else:
            # For memory files, extract description from frontmatter
            file_path = MEMORY_DIR / f
            if file_path.exists():
                try:
                    content = file_path.read_text(encoding="utf-8")
                    desc_match = re.search(r"description:\s*(.+)", content)
                    desc = desc_match.group(1).strip() if desc_match else ""
                    output_lines.append(f"  - {f}: {desc}")
                except Exception:
                    output_lines.append(f"  - {f}")

    if len(output_lines) > 1:
        print("\n".join(output_lines))


if __name__ == "__main__":
    main()
