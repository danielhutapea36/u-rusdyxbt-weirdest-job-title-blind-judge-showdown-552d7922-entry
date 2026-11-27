#!/usr/bin/env python3
"""Weirdest Job Title: Blind Judge Showdown — make.fun entry.

Writes one job title, the weirdest one we could think of, to
/output/entry.txt. Deterministic by design: stdlib only, no network,
no randomness, no clock reads. Two runs produce byte-identical output.

The title: Professional Stand-In Grandma for Holiday Dinners.
A stand-in is a real job — someone hired to be somewhere in
someone else's place. A grandma is the one person a family cannot
hire: she is supposed to be yours, she has known you since you
were small, and she asks the questions nobody else is allowed to
ask. Put the two together at a holiday dinner and the picture
forms on its own: a professional, hired by the hour, arriving
with a casserole she did not cook, sitting in grandma's chair,
and asking when you are getting married — to a table of strangers
who are paying her to do it.
"""

import os

# The title is a single constant so the choice stays visible in the
# code: the joke is the title itself, a real-sounding job with one
# hilariously specific twist, and nothing is assembled around it.
_TITLE = "Professional Stand-In Grandma for Holiday Dinners"

MAX_TITLE_CHARS = 60  # competition ceiling for the single job title


def build_title() -> str:
    """Return the one job title to enter.

    The result must be exactly one title: a stray leading or trailing
    space, or a title that is only white space, would silently break
    the entry format, so fail loudly instead of writing a malformed
    file.
    """
    title = _TITLE
    if not title.strip():
        raise ValueError("title must not be only white space")
    if title != title.strip():
        raise ValueError("title must not start or end with white space")
    if any(ch in "\n\r" for ch in title):
        raise ValueError("title must be a single line")
    return title


def resolve_output_path() -> str:
    """Return the path of the file the title is written to.

    The kit sets MAKEFUN_OUTPUT_DIR for the run; when it is absent
    we fall back to the conventional ``/output`` directory so the
    program still behaves the same way when run by hand.
    """
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(output_dir, "entry.txt")


def main() -> None:
    """Write the title to the output file, with no trailing newline.

    The gate requires 1 to 60 characters of UTF-8 text, so the title
    is validated here before it is written: one title, not only
    white space, and within the limit. After writing, the file is
    read back and its character count re-checked, so a truncated or
    altered write fails loudly instead of shipping a bad entry.
    """
    title = build_title()
    if not 1 <= len(title) <= MAX_TITLE_CHARS:
        raise ValueError("title must be 1 to 60 characters")
    output_path = resolve_output_path()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="") as handle:
        handle.write(title)
    with open(output_path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != title:
        raise ValueError("written title does not match the built title")
    if not 1 <= len(written) <= MAX_TITLE_CHARS:
        raise ValueError("written title is outside 1 to 60 characters")


if __name__ == "__main__":
    main()
