#!/usr/bin/env python3
from math import isqrt


ALLOWED_DIVISORS = {1, 2, 4, 22, 28}
BASE = 308  # lcm(4, 22, 28)


def _prime_list(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for p in range(2, isqrt(limit) + 1):
        if sieve[p]:
            start = p * p
            sieve[start:limit + 1:p] = b"\x00" * ((limit - start) // p + 1)
    return [i for i in range(limit + 1) if sieve[i]]


PRIMES = _prime_list(1_000_000)
PRIME_CACHE = {}


def is_prime(n):
    if n in PRIME_CACHE:
        return PRIME_CACHE[n]
    if n < 2:
        PRIME_CACHE[n] = False
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            PRIME_CACHE[n] = n == p
            return PRIME_CACHE[n]

    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2
    for a in (2, 3, 5, 7):
        if a >= n:
            continue
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            PRIME_CACHE[n] = False
            return False
    PRIME_CACHE[n] = True
    return True


def _factor(n):
    factors = []
    for p in PRIMES:
        if p * p > n:
            break
        if n % p == 0:
            exp = 0
            while n % p == 0:
                n //= p
                exp += 1
            factors.append((p, exp))
    if n > 1:
        factors.append((n, 1))
    return factors


def has_denominator_20010(k):
    # The denominator of Bernoulli_k is the product of primes p with p-1 | k.
    # 20010 = 2*3*5*23*29, so k must be a multiple of 308 and no other
    # divisor d of k may have d+1 prime.
    divisors = [1]
    for p, exp in _factor(k):
        current = divisors[:]
        power = 1
        for _ in range(exp):
            power *= p
            for d in current:
                nd = d * power
                if nd not in ALLOWED_DIVISORS and is_prime(nd + 1):
                    return False
                divisors.append(nd)
    return True


def F(index):
    found = 0
    multiplier = 1
    while True:
        k = BASE * multiplier
        if has_denominator_20010(k):
            found += 1
            if found == index:
                return k
        multiplier += 1


def solve():
    assert F(1) == 308
    assert F(10) == 96404
    return F(100_000)


if __name__ == "__main__":
    print(solve())
