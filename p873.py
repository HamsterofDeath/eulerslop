#!/usr/bin/env python3
"""Project Euler 873: words whose A/B runs require two-C gaps."""

from pathlib import Path

from _cpp_runner import run_cpp


MODULUS = 1_000_000_007


def word_count(a_count: int, b_count: int, c_count: int) -> int:
    return int(
        run_cpp(
            Path(__file__).with_suffix(".cpp"),
            (a_count, b_count, c_count),
        ).strip()
    )


def solve() -> int:
    assert word_count(2, 2, 4) == 32
    assert word_count(4, 4, 44) == 13_908_607_644 % MODULUS
    return word_count(10**6, 10**7, 10**8)


if __name__ == "__main__":
    print(solve())
