#!/usr/bin/env python3
import math

def solve():
    # n! divisible by (i!)^E  <=>  for every prime p <= i:
    #   v_p(n!) >= E * v_p(i!)   (Legendre valuations).
    # For each prime the minimal such n, n_p, depends only on T_p = E*v_p(i!),
    # and v_p(i!) (hence n_p) only changes when p | i.  Every n_p is
    # non-decreasing in i, so N(i) is a running maximum that we update only
    # for the prime divisors of i.
    #
    # Bounds: with K = (p-1)*T_p, v_p(n!) = (n - s_p(n))/(p-1) gives
    #   K < n_p <= K + (p-1)*(D+1),  D = #base-p digits of n_p,
    # so we binary-search n_p in that window — and we skip the search
    # entirely when even the upper bound cannot beat the current maximum.
    E = 1234567890
    LIMIT = 10 ** 6
    NMAX = 2 * 10 ** 15  # safe upper bound for any n_p that occurs here

    # smallest prime factor sieve
    spf = list(range(LIMIT + 1))
    for p in range(2, int(LIMIT ** 0.5) + 1):
        if spf[p] == p:
            for m in range(p * p, LIMIT + 1, p):
                if spf[m] == m:
                    spf[m] = p

    # slack[p] = (p-1)*(digits_p(NMAX)+1) >= n_p - (p-1)*T_p
    logN = math.log(NMAX)
    slack = [0] * (LIMIT + 1)
    for p in range(2, LIMIT + 1):
        if spf[p] == p:
            slack[p] = (p - 1) * (int(logN / math.log(p)) + 2)

    def legendre(n, p):
        tot = 0
        while n:
            n //= p
            tot += n
        return tot

    def minimal_n(p, T):
        # smallest n with v_p(n!) >= T; it is a multiple of p
        lo = ((p - 1) * T) // p + 1          # n > (p-1)*T  =>  k = n/p
        hi = ((p - 1) * T + slack[p]) // p
        while lo < hi:
            mid = (lo + hi) // 2
            if legendre(mid * p, p) >= T:
                hi = mid
            else:
                lo = mid + 1
        return lo * p

    vcount = [0] * (LIMIT + 1)  # v_p(i!) per prime p
    cur_max = 0
    total = 0
    for i in range(2, LIMIT + 1):
        m = i
        while m > 1:
            p = spf[m]
            while m % p == 0:
                m //= p
                vcount[p] += 1
            T = vcount[p]
            if E * (p - 1) * T + slack[p] > cur_max:
                n_p = minimal_n(p, E * T)
                if n_p > cur_max:
                    cur_max = n_p
        if i >= 10:
            total += cur_max
    return total % 10 ** 18

if __name__ == "__main__":
    print(solve())
