#!/usr/bin/env python3
"""Project Euler 880: parametrized nested radical pairs."""

from pathlib import Path

from _cpp_runner import run_cpp


LIMIT = 10**15


def nested_pair_sum(limit: int) -> int:
    return int(
        run_cpp(
            Path(__file__).with_suffix(".cpp"),
            (limit,),
        ).strip()
    )


def solve() -> int:
    assert nested_pair_sum(1_000) == 2_535
    return nested_pair_sum(LIMIT)


if __name__ == "__main__":
    print(solve())
