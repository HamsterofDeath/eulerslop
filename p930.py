#!/usr/bin/env python3
"""Project Euler Problem 930: The Gathering.

After quotienting out a common rotation, the ball positions form a
random walk on Z_n**(m-1), stopped at the origin.  The mean hitting time
from the uniform distribution is its Kemeny constant:

    sum 1 / (1 - (sum_j cos(2*pi*k_j/n))/m),

where the nonzero Fourier modes satisfy sum_j k_j = 0 modulo n.
The C++ implementation groups equal frequencies by multiplicity, so at
most binomial(n+m-1, n-1) cases are needed for each pair (n, m).
"""

from pathlib import Path

from _cpp_runner import run_cpp


def solve() -> str:
    scientific = run_cpp(
        Path(__file__).with_suffix(".cpp")
    ).strip()
    return scientific.replace("e+", "e")


if __name__ == "__main__":
    print(solve())
