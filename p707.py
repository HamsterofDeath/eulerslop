#!/usr/bin/env python3
"""Project Euler 707: Lights Out."""

MOD = 1_000_000_007


def _degree(poly):
    return poly.bit_length() - 1


def _mul(a, b):
    result = 0
    while b:
        if b & 1:
            result ^= a
        a <<= 1
        b >>= 1
    return result


def _mod(poly, modulus):
    modulus_degree = _degree(modulus)
    while poly and _degree(poly) >= modulus_degree:
        poly ^= modulus << (_degree(poly) - modulus_degree)
    return poly


def _mul_mod(a, b, modulus):
    return _mod(_mul(a, b), modulus)


def _gcd(a, b):
    while b:
        a, b = b, _mod(a, b)
    return a


def _path_poly(n):
    """Characteristic polynomial of the n-vertex path adjacency matrix."""
    previous, current = 1, 0b10
    if n == 0:
        return previous
    if n == 1:
        return current
    for _ in range(2, n + 1):
        previous, current = current, (current << 1) ^ previous
    return current


def _compose_x_plus_one(poly):
    result = 0
    power = 1
    x_plus_one = 0b11
    while poly:
        if poly & 1:
            result ^= power
        poly >>= 1
        power = _mul(power, x_plus_one)
    return result


def _path_poly_mod(n, modulus):
    """Return P_n(x) modulo modulus using 2x2 matrix exponentiation."""

    def mat_mul(left, right):
        a, b, c, d = left
        e, f, g, h = right
        return (
            _mul_mod(a, e, modulus) ^ _mul_mod(b, g, modulus),
            _mul_mod(a, f, modulus) ^ _mul_mod(b, h, modulus),
            _mul_mod(c, e, modulus) ^ _mul_mod(d, g, modulus),
            _mul_mod(c, f, modulus) ^ _mul_mod(d, h, modulus),
        )

    result = (1, 0, 0, 1)
    step = (0b10, 1, 1, 0)
    while n:
        if n & 1:
            result = mat_mul(result, step)
        n >>= 1
        if n:
            step = mat_mul(step, step)
    return result[0]


def solve():
    width = 199
    modulus = _compose_x_plus_one(_path_poly(width))
    exponent_mod = MOD - 1

    fib = [0, 1, 1]
    for _ in range(3, 200):
        fib.append(fib[-1] + fib[-2])

    total = 0
    for height in fib[1:200]:
        nullity = _degree(_gcd(modulus, _path_poly_mod(height, modulus)))
        exponent = (width * (height % exponent_mod) - nullity) % exponent_mod
        total = (total + pow(2, exponent, MOD)) % MOD
    return total


if __name__ == "__main__":
    print(solve())
