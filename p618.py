#!/usr/bin/env python3

MOD = 10**9


def primes_up_to(limit):
    sieve = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        sieve[0] = 0
    if limit >= 1:
        sieve[1] = 0
    p = 2
    while p * p <= limit:
        if sieve[p]:
            start = p * p
            sieve[start : limit + 1 : p] = b"\x00" * (((limit - start) // p) + 1)
        p += 1
    return [i for i in range(2, limit + 1) if sieve[i]]


def fibonacci_numbers(count):
    fib = [0, 1, 1]
    while len(fib) <= count:
        fib.append(fib[-1] + fib[-2])
    return fib


def solve():
    fib = fibonacci_numbers(24)
    limit = fib[24]
    sums = [0] * (limit + 1)
    sums[0] = 1

    for prime in primes_up_to(limit):
        for value in range(prime, limit + 1):
            sums[value] = (sums[value] + prime * sums[value - prime]) % MOD

    return sum(sums[fib[k]] for k in range(2, 25)) % MOD


if __name__ == "__main__":
    print(solve())
