#!/usr/bin/env python3
"""Project Euler 787: Bezout stone game."""

from pathlib import Path

from _cpp_runner import run_cpp


def h_value(limit: int) -> int:
    return int(run_cpp(Path(__file__).with_suffix(".cpp"), (limit,)).strip())


def solve() -> int:
    assert h_value(4) == 5
    assert h_value(100) == 2_043
    return h_value(1_000_000_000)


if __name__ == "__main__":
    print(solve())
