#!/usr/bin/env python3

def solve():
    # Conway's PRIMEGAME state factors as 2^a 3^b 5^c 7^d * f where the "flag"
    # f is one of {1, 11, 13, 17, 19, 23, 29} (never two flags at once).  The
    # 14 fractions then form a small state machine on registers (a,b,c,d):
    #
    #   flag 13: d>0 -> d--, ->17        else ->11
    #   flag 17: c>0 -> c--,a++,b++,->13 elif b>0 -> b--, ->19  else ->1
    #   flag 19: a>0 -> a--, ->23        else d++, ->11
    #   flag 23: c++, ->19
    #   flag 11: b>0 -> b--, ->29        else ->13
    #   flag 29: d++, ->11
    #   flag  1: a>0 -> a--,b++,c++      elif d>0 -> d--   else c++, ->11
    #
    # Tracing this machine shows it trial-divides a candidate C (held in c,
    # with C+0/1 bookkeeping) by every m = C-1, C-2, ... using repeated
    # subtraction, stopping at the first divisor L (L = 1 iff C is prime, in
    # which case the state passes through the pure power 2^C; otherwise
    # L = C / spf(C)).  Counting the fraction applications of every loop
    # exactly (verified step-for-step against a direct Fractran simulation
    # for the first 300 primes) gives closed forms:
    #
    #   moving from candidate C-1 to C:        3(C-1) + L_{C-1} + 1 steps
    #   each failing test of divisor m:        6C + 2*floor(C/m) + 2 steps
    #   the final, passing test of L:          4C + 2*(C//L) + 2 steps
    #     (when C is prime this last step emits 2^C)
    #
    # The sum of floor(C/m) over the failing divisors m in (L, C-1] is
    # evaluated in O(sqrt(C)) with the standard floor-division block trick,
    # so the whole count up to the 10001st prime takes well under a second.

    def sumfloor(C, lo, hi):
        # sum of floor(C/m) for m in [lo, hi]
        s = 0
        m = lo
        while m <= hi:
            q = C // m
            last = min(hi, C // q)
            s += q * (last - m + 1)
            m = last + 1
        return s

    # Smallest-prime-factor sieve large enough to contain the 10001st prime.
    LIMIT = 110000
    spf = list(range(LIMIT + 1))
    i = 2
    while i * i <= LIMIT:
        if spf[i] == i:
            for j in range(i * i, LIMIT + 1, i):
                if spf[j] == j:
                    spf[j] = i
        i += 1

    TARGET = 10001
    total = 0
    prev_L = 1  # divisor at which the previous candidate's loop stopped
    primes_found = 0
    C = 1
    while True:
        C += 1
        total += 3 * (C - 1) + prev_L + 1               # advance to candidate C
        is_prime = spf[C] == C
        L = 1 if is_prime else C // spf[C]
        cnt = (C - 1) - L                               # number of failing tests
        total += cnt * (6 * C + 2)
        if cnt > 0:
            total += 2 * sumfloor(C, L + 1, C - 1)
        total += 4 * C + 2 * (C // L) + 2               # passing test of L
        prev_L = L
        if is_prime:
            primes_found += 1
            if primes_found == TARGET:
                return total

if __name__ == "__main__":
    print(solve())
