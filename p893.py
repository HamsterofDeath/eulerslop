#!/usr/bin/env python3
"""Project Euler 893: minimum-cost matchstick expressions."""

from pathlib import Path

from _cpp_runner import run_cpp


LIMIT = 1_000_000


def summatory_minimum_cost(limit: int) -> int:
    return int(
        run_cpp(
            Path(__file__).with_suffix(".cpp"),
            (limit,),
        ).strip()
    )


def solve() -> int:
    assert summatory_minimum_cost(100) == 916
    return summatory_minimum_cost(LIMIT)


if __name__ == "__main__":
    print(solve())
