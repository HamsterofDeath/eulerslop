#!/usr/bin/env python3
"""Project Euler 869: optimal bit-by-bit prime guessing."""

from pathlib import Path

from _cpp_runner import run_cpp


LIMIT = 100_000_000


def expected_score(limit: int) -> str:
    return run_cpp(
        Path(__file__).with_suffix(".cpp"),
        (limit,),
    ).strip()


def solve() -> str:
    assert expected_score(10) == "2.00000000"
    assert expected_score(30) == "2.90000000"
    return expected_score(LIMIT)


if __name__ == "__main__":
    print(solve())
