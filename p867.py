#!/usr/bin/env python3
"""Project Euler 867: tilings of a regular dodecagon."""

from pathlib import Path

from _cpp_runner import run_cpp


def solve(side_length: int = 10) -> int:
    return int(
        run_cpp(
            Path(__file__).with_suffix(".cpp"),
            (side_length,),
        ).strip()
    )


if __name__ == "__main__":
    print(solve())
