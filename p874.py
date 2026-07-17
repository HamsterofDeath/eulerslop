#!/usr/bin/env python3
"""Project Euler 874: maximal prime score with a residue constraint."""

from pathlib import Path

from _cpp_runner import run_cpp


def maximal_score(index_limit: int, list_length: int = 0) -> int:
    """Return M(index_limit, list_length); zero requests p(index_limit)."""
    return int(
        run_cpp(
            Path(__file__).with_suffix(".cpp"),
            (index_limit, list_length),
        ).strip()
    )


def solve() -> int:
    assert maximal_score(2, 5) == 14
    return maximal_score(7_000)


if __name__ == "__main__":
    print(solve())
