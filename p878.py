#!/usr/bin/env python3
"""Project Euler 878: count reduced XOR-quadratic orbits."""

from pathlib import Path

from _cpp_runner import run_cpp


NUMBER_LIMIT = 10**17
VALUE_LIMIT = 1_000_000


def count_solutions(number_limit: int, value_limit: int) -> int:
    return int(
        run_cpp(
            Path(__file__).with_suffix(".cpp"),
            (number_limit, value_limit),
        ).strip()
    )


def solve() -> int:
    assert count_solutions(1_000, 100) == 398
    return count_solutions(NUMBER_LIMIT, VALUE_LIMIT)


if __name__ == "__main__":
    print(solve())
