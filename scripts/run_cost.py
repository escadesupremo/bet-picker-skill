"""Print one sentence with the tokens and API-rate cost of the latest bet-picker run.

Reads this Claude Code session's transcript (the newest .jsonl under ~/.claude/projects/,
or a path given as an argument), finds the last time bet-picker was invoked, and
adds up the usage of every model request since then. Subagent runs aren't included.
With --whole-session it counts the whole session instead: the daily agent's cloud runs follow
SKILL.md without invoking the skill, and the agent wants the run's total anyway.
"""
import json
import sys
from pathlib import Path

# USD per million tokens, Anthropic API list prices (October 2026).
PRICES = {
    "claude-opus-5-5": {"input": 4.00, "output": 20.00, "cache_read": 0.20},
    "claude-opus-5": {"input": 5.00, "output": 25.00},
    "claude-sonnet-5-5": {"input": 2.00, "output": 10.00, "cache_read": 0.20},
    "claude-haiku-5-5": {"input": 0.10, "output": 0.50},
    "claude-fable-5-1": {"input": 10.00, "output": 50.00, "cache_read": 0.25},
}
NAMES = {
    "claude-opus-5-5": "Claude Opus 5.5",
    "claude-opus-5": "Claude Opus 5",
    "claude-sonnet-5-5": "Claude Sonnet 5.5",
    "claude-haiku-5-5": "Claude Haiku 5.5",
    "claude-fable-5-1": "Claude Fable 5.1",
}
# Cache writes cost a multiple of the input price: 1.25x for the 5-minute TTL, 2x for 1 hour.
# Where no cache-read price is listed above, it's 0.1x the input price.
CACHE_WRITE_5M, CACHE_WRITE_1H, CACHE_READ = 1.25, 2.0, 0.1


def newest_transcript():
    projects = Path.home() / ".claude" / "projects"
    files = [p for p in projects.glob("*/*.jsonl")]
    return max(files, key=lambda p: p.stat().st_mtime) if files else None


def is_invocation(entry):
    message = entry.get("message") or {}
    content = message.get("content")
    if entry.get("type") == "user":
        # Only what the user typed: tool results can quote the tag too.
        if isinstance(content, str):
            text = content
        else:
            text = " ".join(b.get("text", "") for b in content or [] if isinstance(b, dict) and b.get("type") == "text")
        return "<command-name>/bet-picker</command-name>" in text
    if entry.get("type") == "assistant" and isinstance(content, list):
        return any(
            block.get("type") == "tool_use"
            and block.get("name") == "Skill"
            and (block.get("input") or {}).get("skill") == "bet-picker"
            for block in content
        )
    return False


class NotMeasured(Exception):
    pass


def measure(path=None, whole_session=False):
    """Usage of the latest run: tokens, cost, models and the sentence main() prints."""
    path = Path(path) if path else newest_transcript()
    if not path or not path.exists():
        raise NotMeasured("Couldn't find this session's transcript, so the cost wasn't measured.")

    entries = []
    for line in path.open(encoding="utf-8"):
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    starts = [0] if whole_session else [i for i, e in enumerate(entries) if is_invocation(e)]
    if not starts:
        raise NotMeasured("Couldn't find the start of this bet-picker run, so the cost wasn't measured.")

    # One request can be written as several entries; keep the last usage seen for each.
    requests = {}
    for entry in entries[starts[-1]:]:
        message = entry.get("message") or {}
        if entry.get("type") == "assistant" and message.get("usage"):
            requests[entry.get("requestId") or message.get("id")] = message

    totals = {"input": 0, "output": 0, "cache_read": 0, "cache_write": 0}
    cost = 0.0
    models = set()
    for message in requests.values():
        usage = message["usage"]
        model = message.get("model", "")
        price = PRICES.get(model, PRICES["claude-opus-5-5"])
        models.add(model)
        written = usage.get("cache_creation") or {}
        write_1h = written.get("ephemeral_1h_input_tokens", 0)
        write_5m = usage.get("cache_creation_input_tokens", 0) - write_1h
        totals["input"] += usage.get("input_tokens", 0)
        totals["output"] += usage.get("output_tokens", 0)
        totals["cache_read"] += usage.get("cache_read_input_tokens", 0)
        totals["cache_write"] += write_1h + write_5m
        cost += (
            usage.get("input_tokens", 0) * price["input"]
            + usage.get("output_tokens", 0) * price["output"]
            + usage.get("cache_read_input_tokens", 0) * price.get("cache_read", price["input"] * CACHE_READ)
            + write_1h * price["input"] * CACHE_WRITE_1H
            + write_5m * price["input"] * CACHE_WRITE_5M
        ) / 1_000_000

    total = sum(totals.values())
    rates = " and ".join(sorted(NAMES.get(m, m) for m in models)) or "Claude"
    sentence = (
        f"This analysis used {total:,} tokens over {len(requests)} model calls "
        f"({totals['cache_read']:,} cached reads, {totals['cache_write']:,} cache writes, "
        f"{totals['input']:,} new input, {totals['output']:,} output), "
        f"about ${cost:.2f} at {rates} API rates."
    )
    return {"tokens": total, "calls": len(requests), "cost": cost, "models": ", ".join(sorted(models)), "sentence": sentence}


def main():
    args = [a for a in sys.argv[1:] if a != "--whole-session"]
    try:
        print(measure(args[0] if args else None, whole_session="--whole-session" in sys.argv)["sentence"])
    except NotMeasured as error:
        print(error)


if __name__ == "__main__":
    main()
