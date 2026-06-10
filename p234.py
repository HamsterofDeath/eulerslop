#!/usr/bin/env python3


def sieve(n):
    is_prime = bytearray([1]) * (n + 1)
    is_prime[0] = is_prime[1] = 0
    for i in range(2, int(n ** 0.5) + 1):
        if is_prime[i]:
            is_prime[i * i::i] = bytearray(len(is_prime[i * i::i]))
    return [i for i in range(n + 1) if is_prime[i]]


def sum_multiples(k, lo, hi):
    """Sum of multiples of k in the inclusive range [lo, hi]."""
    if lo > hi:
        return 0
    a = (lo - 1) // k
    b = hi // k
    return k * (b * (b + 1) - a * (a + 1)) // 2


def semidivisible_sum(limit, primes):
    total = 0
    for p, q in zip(primes, primes[1:]):
        if p * p >= limit:
            break
        # n with lps(n) = p and ups(n) = q satisfies p^2 < n < q^2;
        # n = p^2 and n = q^2 have lps = ups, divisible by both.
        lo = p * p + 1
        hi = min(q * q - 1, limit)
        total += (sum_multiples(p, lo, hi)
                  + sum_multiples(q, lo, hi)
                  - 2 * sum_multiples(p * q, lo, hi))
    return total


def solve():
    limit = 999966663333
    primes = sieve(1000100)
    assert semidivisible_sum(15, primes) == 30
    assert semidivisible_sum(1000, primes) == 34825
    return semidivisible_sum(limit, primes)


if __name__ == "__main__":
    print(solve())
