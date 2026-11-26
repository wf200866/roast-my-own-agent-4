#!/usr/bin/env python3
"""One-line roast for make.fun's "Roast Your Own Agent".

All the program does is place a single line of text at
/output/entry.txt. The competition gate only accepts 1..200 characters of
UTF-8 on one line, so the same rules are enforced here first: a bad line
fails on this machine with a plain error instead of failing at grading.
The file is published through a temporary sibling plus an atomic rename,
so nobody ever observes a half-written entry.
"""

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

# The roast, 196 characters on one line. The joke is the overplanner: the
# agent drafted a 500-line plan, a todo list, a checkpoint system and a
# verification skill just to produce this one line, then announced "done"
# while the todo list was still open.
ENTRY = (
    "My agent wrote a 500-line plan, a todo list, a checkpoint system and a "
    "verification skill to write one line, then said 'done' with the list open. "
    "The line is done; the todo list would like a word."
)

LIMIT = 200
OUT_DEFAULT = Path("/output/entry.txt")
FILE_MODE = 0o644


class GateError(ValueError):
    """Raised when the line would not pass the competition gate."""


def validate(text):
    """Check *text* against the gate; return it unchanged or raise."""
    if "\n" in text or "\r" in text:
        raise GateError("the entry has to be one line, no line breaks")
    if not text.strip():
        raise GateError("the entry is blank")
    if len(text) > LIMIT:
        raise GateError("the entry is %d characters, the gate allows at most %d" % (len(text), LIMIT))
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        # A lone surrogate has no UTF-8 form, so it can never be stored.
        raise GateError("the entry is not encodable as UTF-8: %s" % exc) from exc
    return text


def emit(text, dest):
    """Write *text* to *dest* atomically as UTF-8, mode 0644."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    handle, tmp_name = tempfile.mkstemp(prefix=".%s." % dest.name, dir=dest.parent)
    tmp = Path(tmp_name)
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="") as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        tmp.chmod(FILE_MODE)
        os.replace(tmp, dest)
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise
    return dest


def build_parser():
    """The command line: where to write, and the no-write modes."""
    parser = argparse.ArgumentParser(description="Publish the one-line roast to /output/entry.txt.")
    parser.add_argument(
        "--out",
        "-o",
        type=Path,
        default=OUT_DEFAULT,
        help="where to write the entry (default: %(default)s)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="only validate the line and print its size, write nothing",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="print the result as JSON instead of plain text",
    )
    return parser


def show(text, dest, as_json):
    """Report what was (or would be) written."""
    info = {
        "chars": len(text),
        "bytes": len(text.encode("utf-8")),
        "lines": 1,
        "output": None if dest is None else str(dest),
        "entry": text,
    }
    if as_json:
        print(json.dumps(info, ensure_ascii=False))
    elif dest is None:
        print("%d chars, %d bytes, 1 line, not written" % (info["chars"], info["bytes"]))
    else:
        print(text)


def main(argv=None):
    args = build_parser().parse_args(sys.argv[1:] if argv is None else argv)
    try:
        line = validate(ENTRY)
    except GateError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 2
    if args.check:
        show(line, None, args.json)
        return 0
    try:
        emit(line, args.out)
    except OSError as exc:
        # A failed write should end with a plain error, not a traceback.
        print("error: cannot write %s: %s" % (args.out, exc), file=sys.stderr)
        return 1
    show(line, args.out, args.json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
