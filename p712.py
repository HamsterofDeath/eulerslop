#!/usr/bin/env python3
from pathlib import Path

from _cpp_runner import run_cpp


def solve():
    return int(run_cpp(Path(__file__).with_suffix(".cpp")).strip())


if __name__ == "__main__":
    print(solve())
