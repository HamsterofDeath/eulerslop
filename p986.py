#!/usr/bin/env python3
"""Project Euler Problem 986: Another Infinite Game.

Suppose M moves place token pairs onto the target.  Working leftwards,
let a_k be the minimum number of prerequisite moves whose destination
is k squares before the target.  Token availability gives

    a_k = floor((a_(k-d) + a_(k-c-d)) / 2),

starting with a_(c+d) = M and zeros before it.  The plan is finite
exactly when this recurrence dies out.  Otherwise its cyclic state
converges to a positive constant.  Consequently G(c,d) is one plus
twice the largest mortal M.

The C++ solver binary-searches that threshold, removes gcd(c,d), and
evaluates independent coprime pairs in parallel.
"""

from pathlib import Path

from _cpp_runner import run_cpp


def solve() -> int:
    return int(run_cpp(Path(__file__).with_suffix(".cpp")).strip())


if __name__ == "__main__":
    print(solve())
