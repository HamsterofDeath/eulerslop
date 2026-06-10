#!/usr/bin/env python3


def solve():
    LIMIT = 10 ** 9
    TYPE = 100

    # Primes up to TYPE via simple sieve.
    sieve = [True] * (TYPE + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(TYPE ** 0.5) + 1):
        if sieve[i]:
            for j in range(i * i, TYPE + 1, i):
                sieve[j] = False
    primes = [i for i, p in enumerate(sieve) if p]

    # Count numbers <= LIMIT whose prime factors all come from primes[idx:].
    def count(idx, remaining):
        if idx == len(primes):
            return 1
        total = 0
        p = primes[idx]
        while remaining >= 1:
            total += count(idx + 1, remaining)
            remaining //= p
        return total

    return count(0, LIMIT)


if __name__ == "__main__":
    print(solve())
