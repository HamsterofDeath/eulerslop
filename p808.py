#!/usr/bin/env python3
"""Project Euler 808: reversible prime squares."""

from math import isqrt


def is_prime(n: int) -> bool:
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

    for a in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        if a % n == 0:
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


def primes_up_to(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for p in range(2, isqrt(limit) + 1):
        if sieve[p]:
            start = p * p
            sieve[start : limit + 1 : p] = b"\x00" * (((limit - start) // p) + 1)
    return [p for p in range(limit + 1) if sieve[p]]


def reverse_int(n: int) -> int:
    return int(str(n)[::-1])


def reversible_prime_squares(count: int) -> list[int]:
    limit = 1_000_000
    while True:
        found: list[int] = []
        for p in primes_up_to(limit):
            square = p * p
            reverse = reverse_int(square)
            if reverse == square:
                continue
            root = isqrt(reverse)
            if root * root == reverse and is_prime(root):
                found.append(square)
                if len(found) == count:
                    return found
        limit *= 2


def solve() -> int:
    values = reversible_prime_squares(50)
    assert values[:2] == [169, 961]
    return sum(values)


if __name__ == "__main__":
    print(solve())
