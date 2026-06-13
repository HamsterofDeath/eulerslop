#!/usr/bin/env python3
"""Project Euler 751: a self-generating decimal."""

from decimal import Decimal, ROUND_HALF_UP, getcontext


PLACES = 24


def generated_decimal(theta: Decimal, target_digits: int) -> Decimal:
    b = theta
    parts = []
    while len("".join(parts[1:])) < target_digits + 20:
        a = int(b)
        parts.append(str(a))
        b = Decimal(a) * (b - Decimal(a) + 1)
    return Decimal(parts[0] + "." + "".join(parts[1:]))


def solve() -> str:
    getcontext().prec = 120
    theta = Decimal("2.2")
    for _ in range(20):
        next_theta = generated_decimal(theta, 80)
        if next_theta == theta:
            break
        theta = next_theta

    quantum = Decimal("0." + "0" * (PLACES - 1) + "1")
    return str(theta.quantize(quantum, rounding=ROUND_HALF_UP))


if __name__ == "__main__":
    print(solve())
