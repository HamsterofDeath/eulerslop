#!/usr/bin/env python3
"""Project Euler 789: minimal product for optimal pairings."""

from pathlib import Path

from _cpp_runner import run_cpp


def optimal_product(prime: int) -> int:
    return int(run_cpp(Path(__file__).with_suffix(".cpp"), (prime,)).strip())


def solve() -> int:
    assert optimal_product(5) == 4
    return optimal_product(2_000_000_011)


if __name__ == "__main__":
    print(solve())
