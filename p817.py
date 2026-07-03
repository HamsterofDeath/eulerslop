#!/usr/bin/env python3
"""Project Euler 817: first square containing a high base-p digit."""

from math import isqrt


P = 1_000_000_007
LIMIT = 100_000


def quotient_digit_candidate(target: int) -> int | None:
    m = isqrt(P * target - 1) + 1
    if m * m < P * (target + 1):
        return m
    return None


def residue_digit_candidate(target: int) -> int | None:
    if pow(target, (P - 1) // 2, P) != 1:
        return None
    root = pow(target, (P + 1) // 4, P)
    return min(root, P - root)


def middle_digit_candidate(a: int, target: int) -> int | None:
    def middle_without_mod(b: int) -> int:
        return 2 * a * b + (b * b) // P

    for k in range(2 * a + 1):
        wanted = target + k * P
        lo, hi = 0, P - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if middle_without_mod(mid) >= wanted:
                hi = mid
            else:
                lo = mid + 1
        if middle_without_mod(lo) == wanted:
            return a * P + lo
    return None


def m_value(d: int) -> int:
    target = P - d
    candidates = [
        candidate
        for candidate in (quotient_digit_candidate(target), residue_digit_candidate(target))
        if candidate is not None
    ]
    best = min(candidates) if candidates else None

    a = 1
    while best is None or a * P < best:
        candidate = middle_digit_candidate(a, target)
        if candidate is not None and (best is None or candidate < best):
            best = candidate
        a += 1

    assert best is not None
    return best


def solve() -> int:
    return sum(m_value(d) for d in range(1, LIMIT + 1))


if __name__ == "__main__":
    print(solve())
