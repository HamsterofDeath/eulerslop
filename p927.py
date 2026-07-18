#!/usr/bin/env python3
"""Project Euler Problem 927: Prime-ary Tree.

Modulo a prime q, an exponent prime p not dividing q-1 makes
x -> x**p + 1 a permutation.  Its orbit from 1 must contain 0 because
0 is the unique predecessor of 1.  It is therefore enough to test the
finitely many prime divisors of q-1.

The C++ implementation tests those functional graphs, rules out every
relevant prime square with the exponent-two orbit, and sums all
squarefree products of the remaining primes.
"""

from pathlib import Path

from _cpp_runner import run_cpp


def prime_tree_sum(limit: int) -> int:
    return int(
        run_cpp(
            Path(__file__).with_suffix(".cpp"),
            (limit,),
        ).strip()
    )


def solve() -> int:
    assert prime_tree_sum(20) == 18
    assert prime_tree_sum(1_000) == 2_089
    return prime_tree_sum(10_000_000)


if __name__ == "__main__":
    print(solve())
