#!/usr/bin/env python3
"""Project Euler 782: distinct rows and columns."""

from pathlib import Path

from _cpp_runner import run_cpp


def c_sum(n: int) -> int:
    return int(run_cpp(Path(__file__).with_suffix(".cpp"), (n,)).strip())


def solve() -> int:
    assert c_sum(5) == 64
    assert c_sum(10) == 274
    assert c_sum(20) == 1150
    return c_sum(10_000)


if __name__ == "__main__":
    print(solve())
