#!/usr/bin/env python3
"""Project Euler Problem 989: Fibonacci Sum.

Roots of x^2-x-1 modulo n correspond to primitive reduced elements of
norm n in Z[phi]:

    G(n) = #{(a,b): a >= 2b > 0, gcd(a,b)=1,
                     a^2-ab-b^2=n}.

Binet's formula converts F_n into two modular exponential weights.
Möbius inversion removes the gcd condition, and

    4(a^2-ab-b^2) = (2a-b)^2 - 5b^2

splits the remaining sum into two parity branches.  The C++ solver
evaluates their moving power ranges with sliding windows in
O(sqrt(N) log N) time.
"""

from pathlib import Path

from _cpp_runner import run_cpp


def solve() -> int:
    return int(run_cpp(Path(__file__).with_suffix(".cpp")).strip())


if __name__ == "__main__":
    print(solve())
