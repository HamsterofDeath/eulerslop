#!/usr/bin/env python3
from bisect import bisect_right


LIMIT = 10 ** 12
MOD = 2 ** 32


def _hamming_numbers(limit):
    values = []
    a = 1
    while a <= limit:
        b = a
        while b <= limit:
            c = b
            while c <= limit:
                values.append(c)
                c *= 5
            b *= 3
        a *= 2
    return sorted(values)


def _is_prime(n):
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p

    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2
    for a in (2, 3, 5, 7, 11):
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
            return False
    return True


HAMMING = _hamming_numbers(LIMIT)
HAMMING_PREFIX = [0]
for value in HAMMING:
    HAMMING_PREFIX.append((HAMMING_PREFIX[-1] + value) % MOD)

HAMMING_PRIMES = [
    h + 1
    for h in HAMMING
    if h + 1 > 5 and h + 1 <= LIMIT and _is_prime(h + 1)
]


def _sum_hamming(limit):
    return HAMMING_PREFIX[bisect_right(HAMMING, limit)]


def S(limit):
    # If phi(n) is 5-smooth, every prime p>5 dividing n appears to exponent
    # one and has p-1 5-smooth.  The remaining factor is any 5-smooth number.
    total = 0

    def dfs(start, product):
        nonlocal total
        total = (total + product * _sum_hamming(limit // product)) % MOD
        for i in range(start, len(HAMMING_PRIMES)):
            p = HAMMING_PRIMES[i]
            if product * p > limit:
                break
            dfs(i + 1, product * p)

    dfs(0, 1)
    return total


def solve():
    assert S(100) == 3728
    return S(LIMIT)


if __name__ == "__main__":
    print(solve())
