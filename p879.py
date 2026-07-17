#!/usr/bin/env python3
"""Project Euler 879: subset DP for touchscreen passwords."""

from pathlib import Path

from _cpp_runner import run_cpp


def password_count(rows: int, columns: int) -> int:
    return int(
        run_cpp(
            Path(__file__).with_suffix(".cpp"),
            (rows, columns),
        ).strip()
    )


def solve() -> int:
    assert password_count(3, 3) == 389_488
    return password_count(4, 4)


if __name__ == "__main__":
    print(solve())
