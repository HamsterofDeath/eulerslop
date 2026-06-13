#!/usr/bin/env python3
from functools import lru_cache
from math import gcd


LAST_NINE = 1_000_000_000


def integer_nth_root(n, exponent):
    if exponent == 1:
        return n

    low = 1
    high = 1 << ((n.bit_length() + exponent - 1) // exponent)
    while pow(high, exponent) <= n:
        high <<= 1

    while low + 1 < high:
        mid = (low + high) // 2
        if pow(mid, exponent) <= n:
            low = mid
        else:
            high = mid
    return low


@lru_cache(maxsize=None)
def mobius_upto(limit):
    mu = [0] * (limit + 1)
    if limit >= 1:
        mu[1] = 1
    primes = []
    composite = [False] * (limit + 1)

    for n in range(2, limit + 1):
        if not composite[n]:
            primes.append(n)
            mu[n] = -1
        for p in primes:
            value = n * p
            if value > limit:
                break
            composite[value] = True
            if n % p == 0:
                mu[value] = 0
                break
            mu[value] = -mu[n]
    return tuple(mu)


def phi_upto(limit):
    phi = list(range(limit + 1))
    for n in range(2, limit + 1):
        if phi[n] == n:
            for multiple in range(n, limit + 1, n):
                phi[multiple] -= phi[multiple] // n
    return phi


@lru_cache(maxsize=None)
def height_counts(limit):
    """Count integers 2..limit by maximal perfect-power exponent."""
    max_exponent = limit.bit_length() - 1
    mu = mobius_upto(max_exponent)

    powers = [0] * (max_exponent + 1)
    for exponent in range(1, max_exponent + 1):
        powers[exponent] = integer_nth_root(limit, exponent) - 1

    counts = [0] * (max_exponent + 1)
    for exponent in range(1, max_exponent + 1):
        counts[exponent] = sum(
            mu[multiple] * powers[exponent * multiple]
            for multiple in range(1, max_exponent // exponent + 1)
        )
    return tuple(counts)


def proto_log_values(limit):
    counts = height_counts(limit)
    max_exponent = len(counts) - 1

    reduced_pairs = sum(
        counts[a] * counts[b]
        for a in range(1, max_exponent + 1)
        for b in range(1, max_exponent + 1)
        if gcd(a, b) == 1
    )

    phi = phi_upto(max_exponent)
    rational_classes = 1 + 2 * sum(phi[2:])

    same_root_pairs = counts[1]
    for exponent in range(2, max_exponent + 1):
        root_limit = integer_nth_root(limit, exponent)
        primitive_roots = height_counts(root_limit)[1]
        same_root_pairs += 2 * phi[exponent] * primitive_roots

    return reduced_pairs - same_root_pairs + rational_classes


def solve():
    return proto_log_values(10**18) % LAST_NINE


if __name__ == "__main__":
    print(solve())
