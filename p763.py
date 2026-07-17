#!/usr/bin/env python3
"""Project Euler 763: amoebas in a three-dimensional grid."""

from pathlib import Path

from _cpp_runner import run_cpp


def d_value(divisions: int) -> int:
    if divisions < 0:
        raise ValueError("the number of divisions cannot be negative")
    if divisions == 0:
        return 1
    return int(run_cpp(Path(__file__).with_suffix(".cpp"), (divisions,)).strip())


def solve() -> int:
    return d_value(10_000)


if __name__ == "__main__":
    print(solve())
