#!/usr/bin/env python3
"""Project Euler Problem 941: de Bruijn's Combination Lock.

The lexicographically least de Bruijn cycle is the FKM concatenation
of Lyndon words whose lengths divide 12.  Thus a combination's order
is determined by its containing Lyndon block and offset; no absolute
position in the 10**12-character cycle is needed.

The C++ decoder starts at a word's minimal rotation and checks the few
preceding FKM blocks needed for boundary-crossing windows.  It then
sorts the ten million sampled combinations by these compact keys.
"""

from pathlib import Path

from _cpp_runner import run_cpp


def solve() -> int:
    return int(
        run_cpp(Path(__file__).with_suffix(".cpp")).strip()
    )


if __name__ == "__main__":
    print(solve())
