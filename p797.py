#!/usr/bin/env python3
"""Project Euler 797: cyclogenic polynomials."""

from pathlib import Path

from _cpp_runner import run_cpp


def q_value(limit: int) -> int:
    return int(run_cpp(Path(__file__).with_suffix(".cpp"), (limit,)).strip())


def solve() -> int:
    assert q_value(10) == 5_598
    return q_value(10_000_000)


if __name__ == "__main__":
    print(solve())
