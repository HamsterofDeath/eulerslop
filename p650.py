#!/usr/bin/env python3
"""Project Euler 650: Divisors of Binomial Product."""

MOD = 1_000_000_007
LIMIT = 20_000


def smallest_prime_factors(limit):
    """Linear sieve returning SPF values and the prime list up to limit."""
    spf = [0] * (limit + 1)
    primes = []
    for n in range(2, limit + 1):
        if spf[n] == 0:
            spf[n] = n
            primes.append(n)
        for p in primes:
            composite = n * p
            if composite > limit or p > spf[n]:
                break
            spf[composite] = p
    return spf, primes


def add_factorization(n, spf, prime_index, exponent_sums, weighted_sums):
    """Add v_p(n) and n*v_p(n) to the running factorial exponent sums."""
    remaining = n
    while remaining > 1:
        p = spf[remaining]
        exponent = 0
        while remaining % p == 0:
            remaining //= p
            exponent += 1
        index = prime_index[p]
        exponent_sums[index] += exponent
        weighted_sums[index] += n * exponent


def solve(limit=LIMIT, mod=MOD):
    spf, primes = smallest_prime_factors(limit)
    prime_index = {p: i for i, p in enumerate(primes)}
    inverse_p_minus_1 = [pow(p - 1, mod - 2, mod) for p in primes]

    exponent_sums = [0] * len(primes)
    weighted_sums = [0] * len(primes)
    total = 0
    active_primes = 0

    for n in range(1, limit + 1):
        add_factorization(n, spf, prime_index, exponent_sums, weighted_sums)
        while active_primes < len(primes) and primes[active_primes] <= n:
            active_primes += 1

        divisor_sum = 1
        for index in range(active_primes):
            p = primes[index]
            # If A=sum v_p(i) and W=sum i*v_p(i), then
            # v_p(B(n)) = 2W - (n+1)A for product_k C(n,k).
            exponent = 2 * weighted_sums[index] - (n + 1) * exponent_sums[index]
            if exponent:
                divisor_sum = (
                    divisor_sum
                    * (pow(p, exponent + 1, mod) - 1)
                    * inverse_p_minus_1[index]
                ) % mod

        total = (total + divisor_sum) % mod

    return total


if __name__ == "__main__":
    print(solve())
