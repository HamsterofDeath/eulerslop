#!/usr/bin/env python3
"""Project Euler 702: Jumping Flea."""

from pathlib import Path

from _cpp_runner import run_cpp


def s_value(n: int) -> int:
    return int(run_cpp(Path(__file__).with_suffix(".cpp"), (n,)).strip())


def solve() -> int:
    assert s_value(3) == 42
    assert s_value(5) == 126
    assert s_value(123) == 167_178
    assert s_value(12_345) == 3_185_041_956
    return s_value(123_456_789)


if __name__ == "__main__":
    print(solve())
