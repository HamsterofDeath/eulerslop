#!/usr/bin/env python3
from bisect import bisect_right
from functools import lru_cache
from math import comb, isqrt


N = 10**16
MOD = 1_000_000_007
ROOT = isqrt(N)
DIRECT_LIMIT = 10_000_000
MAX_K = 8


def primes_up_to(n):
    """Return all primes <= n using an odd-only sieve."""
    if n < 2:
        return []
    size = n // 2 + 1
    sieve = bytearray(b"\x01") * size
    sieve[0] = 0
    for i in range(1, isqrt(n) // 2 + 1):
        if sieve[i]:
            p = 2 * i + 1
            start = (p * p) // 2
            sieve[start::p] = b"\x00" * (((size - 1 - start) // p) + 1)
    return [2] + [2 * i + 1 for i in range(1, size) if sieve[i]]


def integer_nth_root(n, k):
    lo, hi = 1, int(n ** (1.0 / k)) + 3
    while hi**k <= n:
        hi *= 2
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid**k <= n:
            lo = mid
        else:
            hi = mid - 1
    return lo


def direct_sums(limit, primes):
    omega = bytearray(limit + 1)
    squarefree = bytearray(b"\x01") * (limit + 1)
    squarefree[0] = 0

    for p in primes:
        if p > limit:
            break
        for m in range(p, limit + 1, p):
            omega[m] += 1
        pp = p * p
        if pp <= limit:
            for m in range(pp, limit + 1, pp):
                squarefree[m] = 0

    sums = [0] * (MAX_K + 1)
    sums[0] = N
    for d in range(2, limit + 1):
        if squarefree[d]:
            k = omega[d]
            if k <= MAX_K:
                sums[k] += N // (d * d)
    return sums


def tail_sums(start, primes):
    @lru_cache(maxsize=None)
    def count_products(x, k, first_index):
        """Count products of k increasing primes from primes[first_index:] <= x."""
        if k == 0:
            return 1
        if first_index >= len(primes) or x < primes[first_index]:
            return 0
        if k == 1:
            return max(0, bisect_right(primes, x) - first_index)

        total = 0
        limit = integer_nth_root(x, k)
        end = bisect_right(primes, limit, first_index)
        for i in range(first_index, end):
            total += count_products(x // primes[i], k - 1, i + 1)
        return total

    @lru_cache(maxsize=None)
    def squarefree_with_k_prime_factors(x, k):
        if x < 1:
            return 0
        if k == 0:
            return 1
        return count_products(x, k, 0)

    sums = [0] * (MAX_K + 1)
    max_value = N // (start * start)

    for value in range(1, max_value + 1):
        lo = max(start, isqrt(N // (value + 1)) + 1)
        while lo * lo * (value + 1) <= N:
            lo += 1

        hi = isqrt(N // value)
        while (hi + 1) * (hi + 1) * value <= N:
            hi += 1
        if hi > ROOT:
            hi = ROOT

        if lo > hi:
            continue

        for k in range(1, MAX_K + 1):
            count = (
                squarefree_with_k_prime_factors(hi, k)
                - squarefree_with_k_prime_factors(lo - 1, k)
            )
            sums[k] += value * count
    return sums


def solve():
    primes = primes_up_to(ROOT)
    a = direct_sums(DIRECT_LIMIT, primes)
    tail = tail_sums(DIRECT_LIMIT + 1, primes)
    for k in range(MAX_K + 1):
        a[k] += tail[k]

    counts = [0] * (MAX_K + 1)
    for k in range(MAX_K, -1, -1):
        counts[k] = sum(
            (-1) ** (j - k) * comb(j, k) * a[j]
            for j in range(k, MAX_K + 1)
        )

    answer = 1
    for count in counts:
        if count:
            answer = (answer * (count % MOD)) % MOD
    return answer


if __name__ == "__main__":
    print(solve())
