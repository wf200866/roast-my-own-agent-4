#!/usr/bin/env python3
"""make.fun "Roast Your Own Agent" entry.

The program's only job is to put one line of text in /output/entry.txt.  The
gate refuses anything that is not 1..200 characters of UTF-8 text, so every
constraint is checked here too: a bad edit fails locally instead of at grading
time.  The write goes through a temporary file in the destination directory and
an atomic rename, so a reader never sees a half-written entry.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

# One line, 196 characters.  The joke: the agent over-planned a one-line task.
ENTRY = (
    "My agent wrote a 500-line plan, a todo list, a checkpoint system and a "
    "verification skill to write one line, then said 'done' with the list open. "
    "The line is done; the todo list would like a word."
)

MAX_CHARS = 200
DEFAULT_OUTPUT = Path("/output/entry.txt")
MODE = 0o644


class GateError(ValueError):
    """The text would be rejected by the competition gate."""


def check_entry(text: str) -> str:
    """Return *text* if it passes the gate, else raise GateError.

    Gate rules: UTF-8, 1..200 characters, not only white space.  This entry is
    also required to be a single line, which is stricter than the gate on
    purpose: the joke only works as one line.
    """
    if "\n" in text or "\r" in text:
        raise GateError("entry must be a single line")
    if not text.strip():
        raise GateError("entry is empty or only white space")
    if not 1 <= len(text) <= MAX_CHARS:
        raise GateError(f"entry must be 1..{MAX_CHARS} characters, got {len(text)}")
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:  # lone surrogates cannot be written as UTF-8
        raise GateError(f"entry is not valid UTF-8: {exc}") from exc
    return text


def write_entry(text: str, output: Path) -> Path:
    """Atomically write *text* to *output* as UTF-8, mode 0644."""
    output.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{output.name}.", dir=output.parent)
    tmp = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        tmp.chmod(MODE)
        os.replace(tmp, output)
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise
    return output


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write the one-line roast to /output/entry.txt."
    )
    parser.add_argument(
        "-o",
        "--out",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="destination file (default: %(default)s)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate the entry and print its stats without writing anything",
    )
    parser.add_argument("--json", action="store_true", help="print a JSON summary")
    return parser.parse_args(argv)


def report(text: str, output: Path | None, as_json: bool) -> None:
    data = {
        "chars": len(text),
        "bytes": len(text.encode("utf-8")),
        "lines": 1 if "\n" not in text else text.count("\n") + 1,
        "output": str(output) if output is not None else None,
        "entry": text,
    }
    if as_json:
        print(json.dumps(data, ensure_ascii=False))
    elif output is None:
        print(f"{data['chars']} chars, {data['bytes']} bytes, 1 line (not written)")
    else:
        print(text)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        text = check_entry(ENTRY)
    except GateError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.check:
        report(text, None, args.json)
        return 0

    write_entry(text, args.out)
    report(text, args.out, args.json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
