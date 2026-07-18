#!/usr/bin/env python3
"""Project Euler Problem 952: Order Modulo Factorial.

The order modulo n! is the LCM of the orders modulo every prime power
in n!.  The C++ implementation sieves the primes, strips factors from
q-1 to find the order modulo each q, and then applies exact q-adic
lifting to reach q**v_q(n!).
"""

from pathlib import Path

from _cpp_runner import run_cpp


def solve() -> int:
    return int(run_cpp(Path(__file__).with_suffix(".cpp")).strip())


if __name__ == "__main__":
    print(solve())
