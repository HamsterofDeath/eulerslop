#!/usr/bin/env python3
"""Project Euler 870: transition values of generalized Fibonacci Nim."""

from pathlib import Path

from _cpp_runner import run_cpp


INDEX = 123_456


def transition_value(index: int) -> str:
    return run_cpp(
        Path(__file__).with_suffix(".cpp"),
        (index,),
    ).strip()


def solve() -> str:
    assert transition_value(1) == "1.0000000000"
    assert transition_value(2) == "2.0000000000"
    assert transition_value(22) == "6.3043478261"
    return transition_value(INDEX)


if __name__ == "__main__":
    print(solve())
