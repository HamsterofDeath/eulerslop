#!/usr/bin/env python3
"""Project Euler Problem 980: The Quaternion Group I.

Interpret x,y,z as i,j,k in Q8.  Inserting a repeated pair or swapping
different neighbours flips the central sign; replacing x by yz (and
cyclic variants) preserves the product.  Replacement parity equals the
final length parity, so a length-100 word is neutral exactly when its
quaternion product is +1.  The C++ solver counts the eight products of
the generated blocks and pairs each product with its inverse.
"""

from pathlib import Path

from _cpp_runner import run_cpp


def solve() -> int:
    return int(run_cpp(Path(__file__).with_suffix(".cpp")).strip())


if __name__ == "__main__":
    print(solve())
