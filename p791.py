#!/usr/bin/env python3
"""Project Euler 791: average and variance."""

from pathlib import Path

from _cpp_runner import run_cpp


def summatory(limit: int) -> int:
    return int(run_cpp(Path(__file__).with_suffix(".cpp"), (limit,)).strip())


def solve() -> int:
    assert summatory(5) == 48
    assert summatory(1_000) == 37_048_340
    return summatory(100_000_000)


if __name__ == "__main__":
    print(solve())
