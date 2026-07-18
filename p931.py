#!/usr/bin/env python3
"""Project Euler Problem 931: Totient Graph.

Reversing the order of summation over divisors and multiples gives

    T(N) = sum_p (p-2) S(floor(N/p))
         + sum_p (p-1) sum_{k>=2} S(floor(N/p**k)),

where S(x)=x(x+1)/2.  The C++ implementation obtains prime counts and
prime sums at all distinct floor-quotients with a combinatorial sieve;
the remaining prime-power terms only require primes through sqrt(N).
"""

from pathlib import Path

from _cpp_runner import run_cpp


def solve() -> int:
    return int(
        run_cpp(Path(__file__).with_suffix(".cpp")).strip()
    )


if __name__ == "__main__":
    print(solve())
