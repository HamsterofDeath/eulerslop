#!/usr/bin/env python3
"""Project Euler 648: Skipping Squares."""


MOD = 10**9
DEGREE = 1000


def _set_coefficient(poly: list[int], degree: int, value: int, mod: int) -> None:
    if degree < len(poly):
        poly[degree] = value % mod


def solve(max_degree: int = DEGREE, mod: int = MOD) -> int:
    if max_degree == 0:
        return 1

    # c_m is the probability of skipping m^2.  Between m^2 and (m+1)^2,
    # c_{m+1} = c_m h_m, where
    # h_m = (1-rho) * sum((rho - 1)^i, i=0..2m-1).
    # Since c_m has no terms below degree m-1, only m <= max_degree + 1
    # can affect the requested coefficient sum.
    coefficients = [0] * (max_degree + 1)

    current = [0] * (max_degree + 1)
    _set_coefficient(current, 0, 1, mod)
    _set_coefficient(current, 1, -1, mod)
    _set_coefficient(coefficients, 0, 1, mod)
    _set_coefficient(coefficients, 1, -1, mod)

    multiplier = [0] * (max_degree + 1)
    _set_coefficient(multiplier, 1, 1, mod)
    _set_coefficient(multiplier, 2, -1, mod)

    # Delta for h_2 - h_1.  Each later delta is multiplied by (1-rho)^2.
    delta = [0] * (max_degree + 1)
    _set_coefficient(delta, 1, 1, mod)
    _set_coefficient(delta, 2, -3, mod)
    _set_coefficient(delta, 3, 3, mod)
    _set_coefficient(delta, 4, -1, mod)

    for square_index in range(1, max_degree + 1):
        next_length = len(current) - 1
        next_current = [0] * next_length
        h = multiplier
        c = current

        for out_degree in range(next_length):
            term = 0
            h_index = out_degree + 1
            for in_degree in range(out_degree + 1):
                term += c[in_degree] * h[h_index - in_degree]
            next_current[out_degree] = term % mod

        current = next_current
        offset = square_index
        for degree, value in enumerate(current, offset):
            coefficients[degree] = (coefficients[degree] + value) % mod

        if square_index == max_degree:
            break

        delta_limit = min(max_degree, 2 * (square_index + 1))
        for degree in range(1, delta_limit + 1):
            multiplier[degree] = (multiplier[degree] + delta[degree]) % mod

        next_delta = [0] * (max_degree + 1)
        next_delta_limit = min(max_degree, delta_limit + 2)
        for degree in range(1, next_delta_limit + 1):
            value = delta[degree] - 2 * delta[degree - 1]
            if degree >= 2:
                value += delta[degree - 2]
            next_delta[degree] = value % mod
        delta = next_delta

    return sum(coefficients) % mod


if __name__ == "__main__":
    print(solve())
