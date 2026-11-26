#!/usr/bin/env python3
"""Entry for make.fun's "Roast Your Own Agent" bounty.

Writes exactly one line to /output/entry.txt: the roast. The program rejects
anything the gate would refuse (empty, blank-only, multi-line, non-UTF-8 or
over 200 characters), so a bad edit fails here instead of at grading time.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# The whole entry: one line, 196 characters, roasting the agent that
# over-planned a one-line job and then called it done.
ENTRY = (
    "My agent wrote a 500-line plan, a todo list, a checkpoint system and a "
    "verification skill to write one line, then said 'done' with the list open. "
    "The line is done; the todo list would like a word."
)

DEFAULT_OUTPUT = Path("/output/entry.txt")
MAX_CHARS = 200


def validate(entry: str) -> str:
    """Return the entry unchanged, or raise ValueError if it fails the gate."""
    if not entry.strip():
        raise ValueError("entry is empty or only whitespace")
    if "\n" in entry or "\r" in entry:
        raise ValueError("entry must be a single line")
    if not 1 <= len(entry) <= MAX_CHARS:
        raise ValueError(f"entry must be 1..{MAX_CHARS} characters, got {len(entry)}")
    try:
        entry.encode("utf-8")
    except UnicodeEncodeError as exc:  # lone surrogates and the like
        raise ValueError(f"entry is not valid UTF-8: {exc}") from exc
    return entry


def write_entry(entry: str, output: Path) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(entry, encoding="utf-8")
    output.chmod(0o644)
    return output


def parse_args(argv: list[str]) -> tuple[Path, bool]:
    output, as_json, args = DEFAULT_OUTPUT, False, list(argv)
    while args:
        arg = args.pop(0)
        if arg in ("-o", "--out"):
            if not args:
                raise ValueError("--out needs a path")
            output = Path(args.pop(0))
        elif arg == "--json":
            as_json = True
        elif arg in ("-h", "--help"):
            print(
                "usage: main.py [--out PATH] [--json]\n\n"
                "Writes the one-line roast to PATH (default /output/entry.txt)."
            )
            raise SystemExit(0)
        else:
            raise ValueError(f"unknown argument: {arg}")
    return output, as_json


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    try:
        output, as_json = parse_args(argv)
        entry = validate(ENTRY)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    write_entry(entry, output)
    if as_json:
        print(json.dumps({"chars": len(entry), "output": str(output), "entry": entry}, ensure_ascii=False))
    else:
        print(entry)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
