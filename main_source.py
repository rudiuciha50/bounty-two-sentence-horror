#!/usr/bin/env python3
"""Two-Sentence Horror -- make.fun bounty entry.

The gate takes /output/entry.txt as UTF-8 text of 1 to 400 characters, not
white space only. A judge then reads two entries at a time and keeps the one
that frightens it more, weighing in this order: that it really is a horror
story in exactly two sentences, that the second sentence turns the first and
makes it worse on a second read, that the horror is implied rather than
explained, that the prose is concrete, and that the idea is not a familiar
twist retold.

So the program does one thing: it writes the story, and it refuses to write
anything the gate would reject.

First draft below: the monitor has been dead since Tuesday, so the crying has
to be live, and the narrator follows it to a crib she emptied an hour ago.
The "had to be live" clause is doing the judge's work for it -- it explains
the dread instead of leaving the reader inside it.
"""

import os
import sys

OUTPUT_DIR = "/output"
OUTPUT_NAME = "entry.txt"

# Draft 4, the one that ships. One word changed and one kept: "baby" goes in,
# because "monitor" alone could be a screen and a reader should not spend the
# first clause wondering which -- the story is a nursery from the third word on,
# and the dread needs no help after that. "Instead" stays: it is the narrator
# still calling the open door a solution, which is the joke the second sentence
# takes away.
STORY = (
    "The baby monitor died on Tuesday, so I leave the nursery door open "
    "instead. Tonight it was shut, and the crying on the other side stopped "
    "the moment I touched the handle."
)

MAX_CHARS = 400


def flatten(text: str) -> str:
    """One line, single spaces, no leading or trailing white space."""
    return " ".join(text.split())


def refusal(line: str) -> str | None:
    """What the gate would refuse, or None when the story passes."""
    if not line:
        return "the entry is empty"
    if line.isspace():
        return "the entry is only white space"
    if len(line) > MAX_CHARS:
        return f"{len(line)} characters, over the {MAX_CHARS} cap"
    if "\n" in line or "\r" in line:
        return "more than one line"
    return None


def main() -> int:
    line = flatten(STORY)
    problem = refusal(line)
    if problem:
        print(f"refusing to write: {problem}", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", OUTPUT_DIR)
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, OUTPUT_NAME)
    with open(target, "w", encoding="utf-8") as handle:
        handle.write(line + "\n")

    print(f"wrote {target} ({len(line)} characters)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
