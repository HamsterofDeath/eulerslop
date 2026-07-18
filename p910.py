#!/usr/bin/env python3
"""Project Euler 910: a much larger L-expression."""

from pathlib import Path

from _cpp_runner import run_cpp


def solve() -> int:
    """Normalize the expression modulo 10^9.

    C_i is Church numeral i.  If P_i(n)=n^i(n+1), then D_i maps
    C_n to C_{P_i(n)}.

    For a numeral transformer with integer action f,

        D_b(f)(n) = f^b(n f(n)).

    In the requested expression the initial transformer is

        f_0 = P_c^(b+1) composed with P_{c+1},

    and the displayed transformation is applied a=12 more times.  The
    C++ implementation evaluates these function powers on all residues
    modulo 5^9, then combines the result with the collapsing 2^9 part.
    """
    return int(
        run_cpp(Path(__file__).with_suffix(".cpp")).strip()
    )


if __name__ == "__main__":
    print(solve())
