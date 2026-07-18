#!/usr/bin/env python3
"""Project Euler Problem 947: Fibonacci Orbit Periods.

The recurrence is the action of the Fibonacci matrix on pairs modulo m.
The C++ implementation computes primitive-vector period distributions
for prime powers, combines them with CRT, and uses divisor inversion to
sum all (possibly imprimitive) vectors through m=1,000,000.
"""

from pathlib import Path

from _cpp_runner import run_cpp


def solve() -> int:
    return int(run_cpp(Path(__file__).with_suffix(".cpp")).strip())


if __name__ == "__main__":
    print(solve())
