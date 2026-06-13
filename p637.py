#!/usr/bin/env python3
"""Project Euler 637: flexible digit sums in bases 10 and 3."""

from pathlib import Path

from _cpp_runner import run_cpp


def solve():
    return run_cpp(Path(__file__).with_suffix(".cpp")).strip()


def main():
    print(solve())


if __name__ == "__main__":
    main()
