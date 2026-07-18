#!/usr/bin/env python3
"""Project Euler Problem 942: Mersenne Square Root.

For p=2**q-1, Gauss's quadratic sum

    sum_{j=1}^{q-1} Legendre(j,q) * 2**j

squares to q modulo p.  Its two residues have complementary q-bit
patterns.  Since the target exponent is 1 modulo 8, the minimal branch
has bit 0 and bits j+1 for the quadratic nonresidues j modulo q.
The C++ implementation marks those residues and sums the selected
powers directly modulo 1,000,000,007.
"""

from pathlib import Path

from _cpp_runner import run_cpp


def solve() -> int:
    return int(
        run_cpp(Path(__file__).with_suffix(".cpp")).strip()
    )


if __name__ == "__main__":
    print(solve())
