#!/usr/bin/env python3

from math import comb

MOD = 1_000_000_007


def _pack(poly, shift):
    value = 0
    for coefficient in reversed(poly):
        value = (value << shift) | coefficient
    return value


def _convolve_mod(left, right):
    if not left or not right:
        return []

    # Coefficients are residues in [0, MOD).  Choose a base large enough that
    # no convolution coefficient carries into the next packed digit.
    max_terms = min(len(left), len(right))
    shift = ((MOD - 1) * (MOD - 1) * max_terms).bit_length() + 1
    mask = (1 << shift) - 1
    product = _pack(left, shift) * _pack(right, shift)

    result = [0] * (len(left) + len(right) - 1)
    for i in range(len(result)):
        result[i] = (product & mask) % MOD
        product >>= shift
    return result


def _add_chebyshev_u(poly, degree, scale):
    for r in range(degree // 2 + 1):
        coefficient = comb(degree - r, r) % MOD
        if r & 1:
            coefficient = -coefficient
        if scale < 0:
            coefficient = -coefficient
        power = degree - 2 * r
        poly[power] = (poly[power] + coefficient) % MOD


def _denominator(n):
    """Return det(I - xA) for the adjacency matrix."""
    size = n - 1
    denominator = [0] * (size + 1)
    _add_chebyshev_u(denominator, size, 1)
    _add_chebyshev_u(denominator, size - 1, -1 if size & 1 else 1)

    if denominator[0] != 1:
        inverse = pow(denominator[0], MOD - 2, MOD)
        denominator = [(coefficient * inverse) % MOD for coefficient in denominator]
    return denominator


def _initial_terms(n):
    size = n - 1
    vector = [1] * size
    terms = [0] * size

    for term_index in range(size):
        terms[term_index] = sum(vector) % MOD
        prefix = [0] * size
        running = 0
        for i, value in enumerate(vector):
            running += value
            if running >= MOD:
                running -= MOD
            prefix[i] = running
        vector = prefix[::-1]

    return terms


def _bostan_mori(numerator, denominator, index):
    while index:
        denominator_neg = [
            coefficient if i % 2 == 0 else (-coefficient) % MOD
            for i, coefficient in enumerate(denominator)
        ]

        product = _convolve_mod(numerator, denominator_neg)
        numerator = product[1::2] if index & 1 else product[0::2]

        product = _convolve_mod(denominator, denominator_neg)
        denominator = product[0::2]
        index >>= 1

    return numerator[0] % MOD


def count_tuples(n, tuple_length):
    size = n - 1
    denominator = _denominator(n)
    initial = _initial_terms(n)
    numerator = _convolve_mod(initial, denominator)[:size]
    return _bostan_mori(numerator, denominator, tuple_length - 1)


def solve():
    return count_tuples(5000, 10**12)


if __name__ == "__main__":
    print(solve())
