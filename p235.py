#!/usr/bin/env python3
from decimal import Decimal, getcontext


def solve():
    getcontext().prec = 40
    target = Decimal(-600_000_000_000)

    def s(r):
        # s(5000) = sum_{k=1}^{5000} (900 - 3k) * r^(k-1)
        total = Decimal(0)
        power = Decimal(1)
        for k in range(1, 5001):
            total += (900 - 3 * k) * power
            power *= r
        return total

    # s(r) is strictly decreasing in r on (1, 1.01): the dominant late terms
    # are negative and grow with r. Bisect for s(r) = target.
    lo, hi = Decimal("1.0"), Decimal("1.01")
    for _ in range(80):
        mid = (lo + hi) / 2
        if s(mid) > target:
            lo = mid
        else:
            hi = mid

    r = (lo + hi) / 2
    return str(r.quantize(Decimal("1.000000000000")))


if __name__ == "__main__":
    print(solve())
