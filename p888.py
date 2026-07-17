#!/usr/bin/env python3
"""Project Euler 888: periodic Grundy values and a Walsh transform."""

from pathlib import Path

from _cpp_runner import run_cpp


PILE_LIMIT = 12_491_249
PILE_COUNT = 1_249
MODULUS = 912_491_249


def losing_position_count(pile_limit: int, pile_count: int) -> int:
    return int(
        run_cpp(
            Path(__file__).with_suffix(".cpp"),
            (pile_limit, pile_count),
        ).strip()
    )


def solve() -> int:
    assert losing_position_count(12, 4) == 204
    assert (
        losing_position_count(124, 9)
        == 2_259_208_528_408 % MODULUS
    )
    return losing_position_count(PILE_LIMIT, PILE_COUNT)


if __name__ == "__main__":
    print(solve())
