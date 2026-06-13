#!/usr/bin/env python3
"""Project Euler 739: summation process on Lucas numbers."""

from pathlib import Path

from _cpp_runner import run_cpp


def f_value(length: int) -> int:
    return int(run_cpp(Path(__file__).with_suffix(".cpp"), (length,)).strip())


def solve() -> int:
    assert f_value(8) == 2_663
    assert f_value(20) == 742_296_999
    return f_value(100_000_000)


if __name__ == "__main__":
    print(solve())
