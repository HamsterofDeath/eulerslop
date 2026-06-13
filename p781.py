#!/usr/bin/env python3
"""Project Euler 781: Feynman diagrams."""

from pathlib import Path

from _cpp_runner import run_cpp


def f_value(n: int) -> int:
    return int(run_cpp(Path(__file__).with_suffix(".cpp"), (n,)).strip())


def solve() -> int:
    assert f_value(4) == 5
    assert f_value(8) == 319
    return f_value(50_000)


if __name__ == "__main__":
    print(solve())
