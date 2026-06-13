#!/usr/bin/env python3
"""Project Euler 779: prime factor and p-adic order averages."""

from decimal import Decimal, ROUND_HALF_UP, getcontext


LIMIT = 10_000_000


def primes_up_to(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, int(limit**0.5) + 1):
        if sieve[p]:
            start = p * p
            sieve[start : limit + 1 : p] = b"\x00" * (((limit - start) // p) + 1)
    return [i for i in range(2, limit + 1) if sieve[i]]


def truncated_sums(limit: int) -> tuple[Decimal, Decimal]:
    getcontext().prec = 50
    alive = Decimal(1)
    total = Decimal(0)
    k1_average = Decimal(0)

    for p in primes_up_to(limit):
        d = Decimal(p)
        total += alive / (d * (d - 1) * (d - 1))
        k1_average += alive / (d * d * (d - 1))
        alive *= (d - 1) / d

    return total, k1_average


def round_12(value: Decimal) -> str:
    return str(value.quantize(Decimal("0.000000000001"), rounding=ROUND_HALF_UP))


def solve() -> str:
    total, k1_average = truncated_sums(LIMIT)
    assert round_12(k1_average) == "0.282419756159"
    return round_12(total)


if __name__ == "__main__":
    print(solve())
