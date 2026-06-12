#!/usr/bin/env python3

def solve():
    # Seating happens in three phases.  Phase 1: while some empty seat has all
    # its neighbours empty, people take such seats.  When it ends, the k
    # occupied seats split the row into internal gaps of size 1 or 2 (a gap of
    # 3 would still have a middle seat with both neighbours empty) and edge
    # gaps of size 0 or 1.  Since phase-1 seats are pairwise non-adjacent,
    # every ordering of them obeys the rule: k! orders.
    #
    # Phase 2: seats with exactly one occupied neighbour.  Each size-2 gap
    # offers 2 choices (taking one seat blocks the other into phase 3) and
    # each size-1 edge gap offers its single seat.  With a size-2 gaps and
    # e in {0,1,2} occupied edge gaps that is (a+e)! * 2^a sequences.
    #
    # Phase 3: the remaining seats - the (k-1-a) size-1 internal gaps plus the
    # leftover seat of each size-2 gap - always k-1 seats, in any order:
    # (k-1)! ways.
    #
    # Seat count: N = 2k - 1 + a + e, so a = N + 1 - e - 2k, and the size-2
    # gaps can be chosen among the k-1 internal gaps in C(k-1, a) ways while
    # the edge pattern gives C(2, e) choices:
    #   T(N) = sum_e C(2,e) sum_k C(k-1,a) 2^a k! (a+e)! (k-1)!
    N = 10 ** 6
    MOD = 100_000_007  # prime, larger than N so no factorial vanishes

    fact = [1] * (N + 2)
    for i in range(1, N + 2):
        fact[i] = fact[i - 1] * i % MOD
    inv_fact = [1] * (N + 2)
    inv_fact[N + 1] = pow(fact[N + 1], MOD - 2, MOD)
    for i in range(N + 1, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD
    pow2 = [1] * (N + 1)
    for i in range(1, N + 1):
        pow2[i] = pow2[i - 1] * 2 % MOD

    total = 0
    for e, ce in ((0, 1), (1, 2), (2, 1)):
        k_min = (N + 2 - e + 2) // 3  # a <= k-1
        k_max = (N + 1 - e) // 2      # a >= 0
        for k in range(max(1, k_min), k_max + 1):
            a = N + 1 - e - 2 * k
            binom = fact[k - 1] * inv_fact[a] % MOD * inv_fact[k - 1 - a] % MOD
            term = binom * pow2[a] % MOD * fact[k] % MOD
            term = term * fact[a + e] % MOD * fact[k - 1] % MOD
            total = (total + ce * term) % MOD
    return total

if __name__ == "__main__":
    print(solve())
