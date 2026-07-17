#!/usr/bin/env python3
"""Project Euler 886: alternating multiset DP for coprime permutations."""

from pathlib import Path

from _cpp_runner import run_cpp


LIMIT = 34


def permutation_count(limit: int) -> int:
    return int(
        run_cpp(
            Path(__file__).with_suffix(".cpp"),
            (limit,),
        ).strip()
    )


def solve() -> int:
    assert permutation_count(4) == 2
    assert permutation_count(10) == 576
    return permutation_count(LIMIT)


if __name__ == "__main__":
    print(solve())
