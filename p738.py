#!/usr/bin/env python3
"""Project Euler 738: unordered multiplicative partitions."""

from pathlib import Path

from _cpp_runner import run_cpp


def d_value(limit: int, max_length: int) -> int:
    return int(run_cpp(Path(__file__).with_suffix(".cpp"), (limit, max_length)).strip())


def solve() -> int:
    assert d_value(10, 10) == 153
    assert d_value(100, 100) == 35_384
    return d_value(10_000_000_000, 10_000_000_000)


if __name__ == "__main__":
    print(solve())
