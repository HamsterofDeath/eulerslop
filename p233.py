#!/usr/bin/env python3
def solve():
    LIMIT = 10**11
    TARGET = 420

    # The circle through (0,0), (N,0), (0,N), (N,N) has center (N/2, N/2) and
    # radius^2 = N^2/2.  A lattice point (x,y) lies on it iff
    #   (2x-N)^2 + (2y-N)^2 = 2N^2,
    # and every representation u^2 + v^2 = 2N^2 automatically has u, v = N (mod 2),
    # so f(N) = r2(2N^2), the number of ways to write 2N^2 as an ordered sum of
    # two squares (signs included).  By the classical formula,
    #   r2(n) = 4 * prod over primes p = 1 (mod 4) of (e_p + 1)
    # provided every prime = 3 (mod 4) divides n to an even power (always true
    # for 2N^2).  With p^b || N (p = 1 mod 4), the exponent in 2N^2 is 2b, so
    #   f(N) = 4 * prod (2b + 1).
    # f(N) = 420  <=>  prod (2b + 1) = 105.
    target_prod = TARGET // 4  # 105

    # All multisets of exponents {b} with prod (2b+1) = 105, i.e. factorizations
    # of 105 into factors >= 3 (each factor odd automatically).
    def factorizations(n, min_factor):
        result = []
        f = min_factor
        while f * f <= n:
            if n % f == 0:
                for rest in factorizations(n // f, f):
                    result.append([f] + rest)
            f += 1
        result.append([n])
        return result

    patterns = []
    for fac in factorizations(target_prod, 3):
        patterns.append(tuple(sorted(((d - 1) // 2 for d in fac), reverse=True)))
    # patterns: (52,), (17, 1), (10, 2), (7, 3), (3, 2, 1)

    # N = C * m where C = prod p_i^{b_i} over distinct primes p_i = 1 (mod 4)
    # following a pattern, and m has no prime factor = 1 (mod 4).

    # Smallest primes = 1 (mod 4), used only for bound computations.
    small_p1 = [5, 13, 17, 29, 37, 41, 53, 61, 73, 89]

    # Largest prime we may ever need: in each feasible pattern, give the
    # smallest exponent to the unknown prime and the other exponents to the
    # smallest 1-mod-4 primes.
    prime_bound = 100
    for exps in patterns:
        head = 1
        for i, e in enumerate(exps[:-1]):
            head *= small_p1[i] ** e
        if head <= LIMIT:
            rest = LIMIT // head
            e_last = exps[-1]
            b = int(round(rest ** (1.0 / e_last))) + 2
            while b ** e_last > rest:
                b -= 1
            prime_bound = max(prime_bound, b)

    # Largest m we may ever need: LIMIT // (smallest possible core).
    xmax = 1
    for exps in patterns:
        core = 1
        for i, e in enumerate(exps):
            core *= small_p1[i] ** e
        if core <= LIMIT:
            xmax = max(xmax, LIMIT // core)

    # Sieve of Eratosthenes up to prime_bound; collect primes = 1 (mod 4).
    sieve = bytearray([1]) * (prime_bound + 1)
    sieve[0:2] = b"\x00\x00"
    for i in range(2, int(prime_bound**0.5) + 1):
        if sieve[i]:
            sieve[i * i :: i] = bytearray(len(range(i * i, prime_bound + 1, i)))
    p1mod4 = [i for i in range(5, prime_bound + 1) if sieve[i] and i % 4 == 1]

    # Prefix sums S[x] = sum of m <= x whose prime factors are all != 1 (mod 4).
    bad = bytearray(xmax + 1)
    for p in p1mod4:
        if p > xmax:
            break
        bad[p::p] = bytearray([1]) * len(range(p, xmax + 1, p))
    S = [0] * (xmax + 1)
    acc = 0
    for i in range(1, xmax + 1):
        if not bad[i]:
            acc += i
        S[i] = acc

    # Enumerate cores: assign distinct 1-mod-4 primes to the exponents of each
    # pattern (exponents sorted descending; equal exponents get strictly
    # increasing prime indices to avoid double counting).
    total = 0

    def rec(exps, i, prod, used, prev_idx):
        nonlocal total
        if i == len(exps):
            total += prod * S[LIMIT // prod]
            return
        e = exps[i]
        lim = LIMIT // prod
        start = prev_idx + 1 if i > 0 and exps[i] == exps[i - 1] else 0
        for idx in range(start, len(p1mod4)):
            pe = p1mod4[idx] ** e
            if pe > lim:
                break
            if idx in used:
                continue
            used.add(idx)
            rec(exps, i + 1, prod * pe, used, idx)
            used.discard(idx)

    for exps in patterns:
        rec(exps, 0, 1, set(), -1)

    return total


if __name__ == "__main__":
    print(solve())
