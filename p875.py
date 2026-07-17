#!/usr/bin/env python3
"""Project Euler 875: an eight-variable quadratic congruence."""

from pathlib import Path

from _cpp_runner import run_cpp


LIMIT = 12_345_678


def q_value(modulus: int) -> int:
    return int(
        run_cpp(
            Path(__file__).with_suffix(".cpp"),
            (modulus, "single"),
        ).strip()
    )


def summatory_q(limit: int) -> int:
    return int(
        run_cpp(
            Path(__file__).with_suffix(".cpp"),
            (limit,),
        ).strip()
    )


def solve() -> int:
    assert q_value(4) == 18_432
    assert summatory_q(10) == 18_573_381
    return summatory_q(LIMIT)


if __name__ == "__main__":
    print(solve())
