#!/usr/bin/env python3
"""Project Euler Problem 943: Self-descriptive Runs.

The generalized Kolakoski word is the fixed point of run expansion:
each input symbol gives the length of the next alternating a/b run.
The C++ implementation repeatedly expands the initial one-letter word,
but stores every intermediate word as a hash-consed grammar DAG.  This
keeps even the 22-trillion-symbol prefix small enough to query exactly.
"""

from pathlib import Path

from _cpp_runner import run_cpp


def solve() -> int:
    return int(run_cpp(Path(__file__).with_suffix(".cpp")).strip())


if __name__ == "__main__":
    print(solve())
