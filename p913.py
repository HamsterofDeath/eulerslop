"""Project Euler Problem 913: Row-major vs Column-major.

For an n by m matrix, transposition sends every non-endpoint flattened index
``x`` to ``m*x modulo (n*m - 1)``.  The residues with additive order d split
into ``phi(d) / ord_d(m)`` cycles.  The two endpoints are separate fixed
points, so the minimum number of swaps follows from the total cycle count.
"""

from functools import cache
from math import isqrt, lcm


MAX_PRODUCT = 100 * 100


def primes_through(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[:2] = b"\x00\x00"
    for prime in range(2, isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start : limit + 1 : prime] = b"\x00" * (
                (limit - start) // prime + 1
            )
    return [number for number in range(2, limit + 1) if sieve[number]]


PRIMES = primes_through(isqrt(MAX_PRODUCT**2 + 1))


@cache
def factor(number: int) -> tuple[tuple[int, int], ...]:
    factors = []
    for prime in PRIMES:
        if prime * prime > number:
            break
        if number % prime:
            continue

        exponent = 0
        while number % prime == 0:
            number //= prime
            exponent += 1
        factors.append((prime, exponent))

    if number > 1:
        factors.append((number, 1))
    return tuple(factors)


def merge_factors(
    *factorizations: tuple[tuple[int, int], ...],
) -> tuple[tuple[int, int], ...]:
    merged: dict[int, int] = {}
    for factorization in factorizations:
        for prime, exponent in factorization:
            merged[prime] = merged.get(prime, 0) + exponent
    return tuple(sorted(merged.items()))


def transpose_modulus_factors(
    product: int,
    power: int,
) -> tuple[tuple[int, int], ...]:
    if power == 1:
        return factor(product - 1)
    if power == 4:
        return merge_factors(
            factor(product - 1),
            factor(product + 1),
            factor(product * product + 1),
        )
    raise ValueError("only the checkpoint and target powers are supported")


@cache
def prime_power_orders(base: int, prime: int, exponent: int) -> tuple[int, ...]:
    """Return the order of base modulo prime, prime**2, ..., prime**exponent."""
    order = prime - 1
    for divisor, _ in factor(prime - 1):
        while order % divisor == 0 and pow(base, order // divisor, prime) == 1:
            order //= divisor

    orders = [order]
    modulus = prime
    for _ in range(2, exponent + 1):
        modulus *= prime
        if pow(base, order, modulus) != 1:
            order *= prime
        orders.append(order)
    return tuple(orders)


def residue_cycle_count(rows: int, columns: int, power: int) -> int:
    """Count cycles among residues modulo (rows*columns)**power - 1."""
    product = rows * columns
    base = columns**power

    # Map each possible multiplicative order to the total phi(d) of divisors
    # d having that order. This combines equal-order terms before summing.
    order_weights = {1: 1}
    for prime, exponent in transpose_modulus_factors(product, power):
        orders = prime_power_orders(base, prime, exponent)
        choices = [(1, 1)]
        phi = prime - 1
        for index, order in enumerate(orders):
            if index:
                phi *= prime
            choices.append((order, phi))

        next_weights: dict[int, int] = {}
        for old_order, old_weight in order_weights.items():
            for prime_order, prime_phi in choices:
                combined_order = lcm(old_order, prime_order)
                next_weights[combined_order] = (
                    next_weights.get(combined_order, 0) + old_weight * prime_phi
                )
        order_weights = next_weights

    return sum(weight // order for order, weight in order_weights.items())


def minimum_swaps(rows: int, columns: int, power: int = 1) -> int:
    entries = (rows * columns) ** power
    # The modular residue cycles include index 0; index entries-1 is the
    # additional fixed endpoint.
    return entries - 1 - residue_cycle_count(rows, columns, power)


def range_sum(power: int) -> int:
    return sum(
        minimum_swaps(rows, columns, power)
        for rows in range(2, 101)
        for columns in range(rows, 101)
    )


def solve() -> int:
    assert minimum_swaps(3, 4) == 8
    assert range_sum(1) == 12_578_833
    return range_sum(4)


if __name__ == "__main__":
    print(solve())
