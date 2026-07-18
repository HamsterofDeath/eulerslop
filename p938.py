#!/usr/bin/env python3
"""Project Euler Problem 938: Removing Cards.

For R=2k, ignore black-black draws that leave the state unchanged and
merge the remaining transitions into independent death processes.
Their rates are 1,3,...,2k-1 for red pairs and 2,4,...,2B for black
cards.  If T is the red extinction time, exp(-2T) is Beta(1/2,k), so

    P(2k,B) = 1 - (k)_B / (k+1/2)_B.

The C++ implementation evaluates this ratio as a logarithmic product.
"""

from pathlib import Path

from _cpp_runner import run_cpp


def solve() -> str:
    return run_cpp(
        Path(__file__).with_suffix(".cpp")
    ).strip()


if __name__ == "__main__":
    print(solve())
