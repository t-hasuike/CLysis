#!/usr/bin/env python3
"""
Mini reflection hook.
Called from the PostToolUse event, tracks tool usage count and outputs
a reflection prompt every 15 tool calls to encourage pattern recognition
and skill creation.
"""
import json
import sys
import os
from pathlib import Path
from datetime import datetime

# Counter directory (session-scoped tracking)
COUNTER_DIR = Path("/tmp/clysis_reflection")
COUNTER_DIR.mkdir(exist_ok=True)


def get_counter_file(session_id: str) -> Path:
    return COUNTER_DIR / f"tool_count_{session_id}.json"


def main():
    try:
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return

    session_id = input_data.get("session_id", "unknown")
    tool_name = input_data.get("tool_name", "")

    # Load or initialize counter file
    counter_file = get_counter_file(session_id)

    if counter_file.exists():
        try:
            data = json.loads(counter_file.read_text())
        except (json.JSONDecodeError, OSError):
            data = {"count": 0, "tools_used": [], "last_reflection": 0}
    else:
        data = {"count": 0, "tools_used": [], "last_reflection": 0}

    data["count"] += 1

    # Record recent tool usage (keep last 30 entries)
    data["tools_used"].append({
        "tool": tool_name,
        "time": datetime.now().isoformat()
    })
    if len(data["tools_used"]) > 30:
        data["tools_used"] = data["tools_used"][-30:]

    # Trigger reflection every 15 tool calls
    since_last = data["count"] - data["last_reflection"]

    if since_last >= 15:
        data["last_reflection"] = data["count"]

        # Summarize tool usage pattern for the last 15 calls
        recent_tools = data["tools_used"][-15:]
        tool_freq: dict = {}
        for t in recent_tools:
            name = t["tool"]
            tool_freq[name] = tool_freq.get(name, 0) + 1

        # Top 3 most-used tools
        top_tools = sorted(tool_freq.items(), key=lambda x: -x[1])[:3]
        tool_summary = ", ".join(f"{name}({count}x)" for name, count in top_tools)

        reflection_msg = (
            f"[Mini Reflection ({data['count']} tool calls reached)]\n"
            f"Recent 15-call tool pattern: {tool_summary}\n"
            "Review:\n"
            "- Are you repeating the same work pattern? Consider creating a skill.\n"
            "- Are you deviating from the original objective?\n"
            "- Is there a learning worth saving to feedback memory?"
        )

        print(reflection_msg)

    # Persist counter
    try:
        counter_file.write_text(json.dumps(data, ensure_ascii=False))
    except OSError:
        pass


if __name__ == "__main__":
    main()
