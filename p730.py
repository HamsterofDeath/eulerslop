#!/usr/bin/env python3
"""Project Euler 730: shifted Pythagorean triples."""

from pathlib import Path

from _cpp_runner import run_cpp


def solve() -> int:
    return int(run_cpp(Path(__file__).with_suffix(".cpp")).strip())


if __name__ == "__main__":
    print(solve())
