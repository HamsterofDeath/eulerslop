#!/usr/bin/env python3
"""Project Euler 689: Binary Series."""

import math


THRESHOLD = 0.5
INTEGRAL_LIMIT = 1500.0
STEP = 0.2
PRODUCT_TERMS = 1000


def _tail_fourth_power_sum(n):
    return math.pi**4 / 90.0 - sum(1.0 / (k**4) for k in range(1, n + 1))


def _probability_greater_than_half():
    """Evaluate the Bernoulli-sum distribution by Fourier inversion."""
    phase = math.pi**2 / 12.0 - THRESHOLD
    half_inverse_squares = [1.0 / (2.0 * n * n) for n in range(1, PRODUCT_TERMS + 1)]
    tail_fourths = _tail_fourth_power_sum(PRODUCT_TERMS)

    def characteristic_product(t):
        product = 1.0
        for coefficient in half_inverse_squares:
            product *= math.cos(t * coefficient)

        # For the omitted factors, log(cos(u)) = -u^2/2 + O(u^4).
        return product * math.exp(-(t * t) * tail_fourths / 8.0)

    def integrand(t):
        if t == 0.0:
            return phase
        return math.sin(phase * t) * characteristic_product(t) / t

    intervals = int(round(INTEGRAL_LIMIT / STEP))
    if intervals % 2:
        intervals += 1

    total = integrand(0.0) + integrand(intervals * STEP)
    for index in range(1, intervals):
        total += (4 if index % 2 else 2) * integrand(index * STEP)

    integral = total * STEP / 3.0
    cdf = 0.5 - integral / math.pi
    return 1.0 - cdf


def solve():
    return f"{_probability_greater_than_half():.8f}"


if __name__ == "__main__":
    print(solve())
