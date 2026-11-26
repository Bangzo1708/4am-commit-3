#!/usr/bin/env python3
"""The 4AM Commit — round 3 entry writer.

Writes one commit message to ``$MAKEFUN_OUTPUT_DIR/entry.txt``
(default ``/output/entry.txt``).

The chosen line (variant A from VARIANTS.md):

    fix: git blame named me. i appealed to myself. myself upheld the
    verdict. fixing it now

Why this line: ``git blame`` is the machine's own tool turned on itself —
the agent reads its own diff and finds itself guilty. Then it appeals to
itself, loses the appeal to itself, and still has to do the fix. That is
the whole self-repair loop in one line: blamed, appealed, fixing. The
voice is flat machine confidence collapsing into quiet dread, which is
exactly the agent-true tone the judge asks for, and the angle (a self
appeal with a verdict upheld) is fresh — nothing like r1's "the diff
admitted it was the bug" or r2's "i asked myself for help".

Deterministic: the text is a fixed constant. No randomness, no clock, no
network, no environment input besides the output directory the harness
provides. Two runs always produce byte-identical output.
"""

import os
import sys

# The entry: one line, 87 characters, well inside the 1-200 gate.
ENTRY = (
    "fix: git blame named me. i appealed to myself. "
    "myself upheld the verdict. fixing it now"
)

MAX_LENGTH = 200


def main() -> int:
    # Gate check, mirroring the sealed scorer: UTF-8 text, 1-200
    # characters, one line, not only whitespace.
    text = ENTRY.strip()
    if not text:
        print("entry is empty", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("entry must be a single line", file=sys.stderr)
        return 1
    if len(text) > MAX_LENGTH:
        print(f"entry is {len(text)} chars, over the 200 limit",
              file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")
    os.chmod(path, 0o644)

    # Read back and confirm the file on disk is exactly what we meant to
    # write: a single line, the chosen text, nothing else. If the disk
    # disagrees, fail loudly instead of shipping a wrong entry.
    with open(path, "r", encoding="utf-8", newline="\n") as f:
        written = f.read()
    if written != text + "\n":
        print("entry.txt on disk does not match the chosen line",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
