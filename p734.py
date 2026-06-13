#!/usr/bin/env python3
"""Project Euler 734: prime bitwise-OR tuples."""


MOD = 1_000_000_007
N = 10**6
K = 999_983


def prime_flags(limit: int, size: int) -> tuple[bytearray, list[int]]:
    flags = bytearray(b"\x01") * size
    flags[0] = 0
    flags[1] = 0
    root = int(limit**0.5)
    for p in range(2, root + 1):
        if flags[p]:
            start = p * p
            flags[start : limit + 1 : p] = b"\x00" * ((limit - start) // p + 1)
    for value in range(limit + 1, size):
        flags[value] = 0
    return flags, [value for value in range(2, limit + 1) if flags[value]]


def t_value(limit: int, length: int) -> int:
    size = 1
    while size <= limit:
        size <<= 1
    bits = size.bit_length() - 1
    flags, primes = prime_flags(limit, size)

    counts = [0] * size
    for prime in primes:
        counts[prime] = 1

    for bit in range(bits):
        step = 1 << bit
        for mask in range(size):
            if mask & step:
                counts[mask] += counts[mask ^ step]

    exact = [pow(count, length, MOD) for count in counts]
    for bit in range(bits):
        step = 1 << bit
        for mask in range(size):
            if mask & step:
                exact[mask] = (exact[mask] - exact[mask ^ step]) % MOD

    return sum(exact[prime] for prime in primes) % MOD


def solve() -> int:
    assert t_value(5, 2) == 5
    assert t_value(100, 3) == 3355
    assert t_value(1000, 10) == 2071632
    return t_value(N, K)


if __name__ == "__main__":
    print(solve())
