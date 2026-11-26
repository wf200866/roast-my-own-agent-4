#!/usr/bin/env python3
"""Write the one-line entry for make.fun's Roast Your Own Agent bounty."""

from pathlib import Path

# The one line; the whole entry.
ENTRY = (
    "My agent wrote a 500-line plan, a todo list, a checkpoint system and a "
    "verification skill to write one line, then said 'done' with the list open. "
    "The line is done; the todo list would like a word."
)

OUTPUT = Path("/output/entry.txt")


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(ENTRY, encoding="utf-8")
    OUTPUT.chmod(0o644)
    print(ENTRY)


if __name__ == "__main__":
    main()
