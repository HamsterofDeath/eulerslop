#!/usr/bin/env python3
"""Project Euler 892: bipartition imbalance of plane trees."""

from pathlib import Path

from _cpp_runner import run_cpp


LIMIT = 10_000_000


def cutting_imbalance_sum(edge_count: int) -> int:
    return int(
        run_cpp(
            Path(__file__).with_suffix(".cpp"),
            (edge_count, "single"),
        ).strip()
    )


def summatory_cutting_imbalance(limit: int) -> int:
    return int(
        run_cpp(
            Path(__file__).with_suffix(".cpp"),
            (limit,),
        ).strip()
    )


def solve() -> int:
    assert cutting_imbalance_sum(3) == 4
    assert cutting_imbalance_sum(100) == 1_172_122_931
    return summatory_cutting_imbalance(LIMIT)


if __name__ == "__main__":
    print(solve())
