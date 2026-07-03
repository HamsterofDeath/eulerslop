#!/usr/bin/env python3
"""Project Euler 839: chip moves to the nondecreasing integer minorant."""

from pathlib import Path

from _cpp_runner import run_cpp


def solve() -> str:
    return run_cpp(Path(__file__).with_suffix(".cpp")).strip()


if __name__ == "__main__":
    print(solve())
