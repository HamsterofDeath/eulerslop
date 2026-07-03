#!/usr/bin/env python3
"""Project Euler 804: lattice points in x^2+xy+41y^2."""

from pathlib import Path

from _cpp_runner import run_cpp


def solve() -> int:
    return int(run_cpp(Path(__file__).with_suffix(".cpp")).strip())


if __name__ == "__main__":
    print(solve())
