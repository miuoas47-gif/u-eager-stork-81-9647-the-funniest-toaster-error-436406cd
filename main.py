#!/usr/bin/env python3
"""The Funniest Toaster Error Message — make.fun entry.

Writes one original toaster error message to
$MAKEFUN_OUTPUT_DIR/entry.txt (falling back to /output), then
validates the file and reads it back to confirm it matches.

Stdlib only, no network, no arguments, deterministic: every run
produces the exact same bytes.
"""

import os
import sys

LINE = "E06: Fork detected. We need to talk."

MAX_CHARS = 120


def output_path() -> str:
    """Directory for the entry file, from the environment or /output."""
    directory = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return os.path.join(directory, "entry.txt")


def validate(text: str) -> None:
    """Check the line against the competition gate."""
    if not text:
        raise ValueError("entry is empty")
    if text != text.strip():
        raise ValueError("entry has leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if len(text) > MAX_CHARS:
        raise ValueError(f"entry is {len(text)} chars, over the {MAX_CHARS} limit")


def main() -> int:
    validate(LINE)

    path = output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(LINE)

    with open(path, "r", encoding="utf-8") as handle:
        written = handle.read()
    # Validate what actually landed on disk, not just the constant.
    validate(written)
    if written != LINE:
        raise ValueError("read-back mismatch: entry.txt does not match the line")

    print(f"Wrote {len(LINE)} characters to {path}: {LINE!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
