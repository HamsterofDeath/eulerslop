#!/usr/bin/env python3
"""Project Euler 664: an army of one."""

from math import ceil, exp, fsum, log, sqrt


PHI = (1.0 + sqrt(5.0)) / 2.0
LOG_PHI = log(PHI)


def _score_log(n: int) -> float:
    """Return log_phi(phi^3 * sum(d^n / phi^d, d>=1))."""
    if n == 0:
        return 4.0

    center = max(1, int(round(n / LOG_PHI)))

    def log_term(d: int) -> float:
        return n * log(d) - d * LOG_PHI

    mode = center
    best = log_term(mode)
    for d in range(max(1, center - 8), center + 9):
        value = log_term(d)
        if value > best:
            mode = d
            best = value

    parts = [1.0]

    d = mode - 1
    while d >= 1:
        delta = log_term(d) - best
        if delta < -60.0:
            break
        parts.append(exp(delta))
        d -= 1

    d = mode + 1
    while True:
        delta = log_term(d) - best
        if delta < -60.0:
            break
        parts.append(exp(delta))
        d += 1

    return (best + log(fsum(parts))) / LOG_PHI + 3.0


def F(n: int) -> int:
    value = _score_log(n)
    nearest = round(value)
    if abs(value - nearest) < 1e-9:
        return nearest
    return ceil(value)


def solve() -> int:
    return F(1_234_567)


if __name__ == "__main__":
    print(solve())
