#!/usr/bin/env python3
"""Project Euler 795: alternating gcd sums."""

from array import array
from math import gcd


N = 12_345_678


def direct_g(n: int) -> int:
    return sum((1 if i % 2 == 0 else -1) * gcd(n, i * i) for i in range(1, n + 1))


def phi_and_square_root_kernel(limit: int) -> tuple[array, array]:
    spf = array("I", [0]) * (limit + 1)
    phi = array("I", [0]) * (limit + 1)
    root = array("I", [0]) * (limit + 1)
    exponent = bytearray(limit + 1)

    phi[1] = 1
    root[1] = 1
    primes: list[int] = []

    for n in range(2, limit + 1):
        if spf[n] == 0:
            spf[n] = n
            phi[n] = n - 1
            root[n] = n
            exponent[n] = 1
            primes.append(n)

        for p in primes:
            value = n * p
            if value > limit:
                break
            spf[value] = p
            if p == spf[n]:
                phi[value] = phi[n] * p
                exponent[value] = exponent[n] + 1
                root[value] = root[n] * p if exponent[value] % 2 else root[n]
                break

            phi[value] = phi[n] * (p - 1)
            root[value] = root[n] * p
            exponent[value] = 1

    return phi, root


def summatory_g(limit: int) -> int:
    phi, root = phi_and_square_root_kernel(limit)
    total = 0
    for d in range(1, limit + 1):
        multiples = limit // d
        r = root[d]
        if r % 2:
            total -= phi[d] * ((multiples + 1) // 2)
        else:
            total += phi[d] * (d // r) * multiples * (multiples + 1) // 2
    return total


def solve() -> int:
    assert direct_g(4) == 6
    assert direct_g(1234) == 1233
    assert summatory_g(1234) == 2_194_708
    return summatory_g(N)


if __name__ == "__main__":
    print(solve())
