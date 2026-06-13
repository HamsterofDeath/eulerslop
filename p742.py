#!/usr/bin/env python3
"""Project Euler 742: minimum-area symmetric grid polygon."""

from pathlib import Path

from _cpp_runner import run_cpp


def area(vertices: int) -> int:
    return int(run_cpp(Path(__file__).with_suffix(".cpp"), (vertices,)).strip())


def solve() -> int:
    assert area(4) == 1
    assert area(8) == 7
    assert area(40) == 1039
    assert area(100) == 17473
    return area(1000)


if __name__ == "__main__":
    print(solve())
