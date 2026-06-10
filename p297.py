#!/usr/bin/env python3
import bisect
from functools import lru_cache

# Zeckendorf digit sums.
#
# Let T(N) = sum of z(n) for 0 <= n < N (with z(0) = 0).
# Use Fibonacci numbers F: 1, 2, 3, 5, 8, ...
# For the largest Fibonacci number F_k < N, every n in [F_k, N) has the
# Zeckendorf form F_k + (n - F_k) with n - F_k < F_{k-1}, so
#   T(N) = T(F_k) + (N - F_k) + T(N - F_k).
# Memoized recursion over the (few) distinct arguments runs instantly.

LIMIT = 10**17

FIBS = [1, 2]
while FIBS[-1] < LIMIT:
    FIBS.append(FIBS[-1] + FIBS[-2])


@lru_cache(maxsize=None)
def T(n):
    # Sum of z(m) for 0 <= m < n.
    if n <= 1:
        return 0
    # Largest Fibonacci number strictly below n.
    k = bisect.bisect_left(FIBS, n) - 1
    f = FIBS[k]
    return T(f) + (n - f) + T(n - f)


def solve():
    # Sanity anchor from the statement: sum z(n) for 0 < n < 10^6 = 7894453.
    assert T(10**6) == 7894453
    return T(LIMIT)


if __name__ == "__main__":
    print(solve())
