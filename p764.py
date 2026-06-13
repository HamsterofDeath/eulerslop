#!/usr/bin/env python3
"""Project Euler 764: fourth-power Pell-type factorization."""

from pathlib import Path

from _cpp_runner import run_cpp


def s_value(limit: int) -> int:
    return int(run_cpp(Path(__file__).with_suffix(".cpp"), (limit,)).strip())


def solve() -> int:
    assert s_value(100) == 81
    assert s_value(10_000) == 112_851
    assert s_value(10_000_000) == 248_876_211
    return s_value(10_000_000_000_000_000)


if __name__ == "__main__":
    print(solve())
