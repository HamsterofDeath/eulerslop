#!/usr/bin/env python3
import sys
from bisect import bisect_right

def solve():
    # This is Fibonacci nim: a position is losing iff n is a Fibonacci number.
    # With n = F_m + r (Zeckendorf, 0 <= r < F_{m-1}), a winning first move must
    # take a suffix of the Zeckendorf representation, and taking x leaves a
    # losing position iff 2x is smaller than the next (larger) Zeckendorf term.
    # The largest such move:  M(F_m + r) = r if 2r < F_m else M(r),  M(F_m) = 0.
    # (Validated against brute-force game search for n < 300.)
    #
    # For the prefix sum G(x) = sum_{n<=x} M(n), split block [F, x] with F the
    # largest Fibonacci <= x and y = x - F:  r in 1..y contributes r when
    # r <= T = (F-1)//2 (i.e. 2r < F) and M(r) otherwise, so
    #   G(x) = G(F-1) + tri(min(y,T)) + max(0, G(y) - G(T))
    # which memoizes to only a few hundred distinct arguments for x = 10^18.
    sys.setrecursionlimit(10000)
    N = 10 ** 18

    fibs = [1, 2]
    while fibs[-1] <= N:
        fibs.append(fibs[-1] + fibs[-2])

    memo = {0: 0}

    def G(x):
        if x in memo:
            return memo[x]
        f = fibs[bisect_right(fibs, x) - 1]
        y = x - f
        T = (f - 1) // 2
        if y <= T:
            res = G(f - 1) + y * (y + 1) // 2
        else:
            res = G(f - 1) + T * (T + 1) // 2 + G(y) - G(T)
        memo[x] = res
        return res

    assert G(100) == 728  # test value from the problem statement
    return G(N) % 10 ** 8

if __name__ == "__main__":
    print(solve())
