"""Project Euler Problem 926: Total Roundness.

The roundness in base b is the number of k >= 1 for which b^k divides n.
For n=N!, swapping the base and k sums gives

    R(N!) = sum_k (product_p (floor(v_p(N!)/k)+1) - 1).

Group primes by their factorial valuation e. For fixed e, floor(e/k) is
constant on O(sqrt(e)) intervals. A multiplicative difference array applies
each interval factor, after which one prefix product gives every term.
"""

from array import array
from collections import Counter
from math import isqrt


MODULUS = 1_000_000_007
TARGET = 10_000_000


def prime_sieve(limit: int) -> bytearray:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for prime in range(2, isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start : limit + 1 : prime] = b"\x00" * (
                (limit - start) // prime + 1
            )
    return sieve


def factorial_valuation(limit: int, prime: int) -> int:
    result = 0
    quotient = limit
    while quotient:
        quotient //= prime
        result += quotient
    return result


def total_roundness(limit: int) -> int:
    sieve = prime_sieve(limit)
    valuation_counts: Counter[int] = Counter()

    for prime in range(2, limit + 1):
        if sieve[prime]:
            valuation_counts[factorial_valuation(limit, prime)] += 1

    maximum_valuation = max(valuation_counts)
    differences = array("I", [1]) * (maximum_valuation + 2)

    for valuation, count in valuation_counts.items():
        left = 1
        while left <= valuation:
            quotient = valuation // left
            right = valuation // quotient
            factor = pow(quotient + 1, count, MODULUS)

            differences[left] = (
                differences[left] * factor % MODULUS
            )
            differences[right + 1] = (
                differences[right + 1]
                * pow(factor, MODULUS - 2, MODULUS)
                % MODULUS
            )
            left = right + 1

    divisor_count = 1
    result = 0
    for power in range(1, maximum_valuation + 1):
        divisor_count = divisor_count * differences[power] % MODULUS
        result = (result + divisor_count - 1) % MODULUS
    return result


def solve() -> int:
    assert total_roundness(10) == 312
    return total_roundness(TARGET)


if __name__ == "__main__":
    print(solve())
