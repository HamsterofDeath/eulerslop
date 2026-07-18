#!/usr/bin/env python3
"""Project Euler 908: periodic clock sequences."""

from pathlib import Path

from _cpp_runner import run_cpp


def clock_sequence_count(maximum_period: int) -> int:
    """Return C(maximum_period).

    For a period word with total W, its cyclic prefix sums must contain
    every triangular residue modulo W.  If there are r(W) required
    residues, choosing p-r(W) of the remaining residues creates

        binomial(W-r(W), p-r(W))

    representations of length p.  Minimal periods are recovered by
    divisor inversion.

    For odd W, 8*T_n+1=(2n+1)^2 makes r(W) the number of quadratic
    residues modulo W.  Powers of two multiply both W and r(W) by the
    same factor, allowing the C++ implementation to generate all and
    only relevant moduli multiplicatively.
    """
    return int(
        run_cpp(
            Path(__file__).with_suffix(".cpp"),
            (maximum_period,),
        ).strip()
    )


def solve() -> int:
    assert clock_sequence_count(3) == 3
    assert clock_sequence_count(4) == 7
    assert clock_sequence_count(10) == 561
    return clock_sequence_count(10**4)


if __name__ == "__main__":
    print(solve())
