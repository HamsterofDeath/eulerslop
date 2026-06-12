#!/usr/bin/env python3

MOD = 1_000_000_123
INV2 = pow(2, -1, MOD)


def _conv(a, b):
    out = {}
    for x, c in a.items():
        for y, d in b.items():
            out[x + y] = (out.get(x + y, 0) + c * d) % MOD
    return {k: v for k, v in out.items() if v}


def _power(poly, exp):
    out = {0: 1}
    for _ in range(exp):
        out = _conv(out, poly)
    return out


EVEN_DIGIT = {1: INV2, -1: INV2}
ODD_COUNT = {1: INV2, -1: -INV2 % MOD}
ODD_DIGIT = {0: 1, 1: INV2, -1: -INV2 % MOD}

# Exponential generating functions:
#   even digits require an even count: cosh(x)
#   odd digits require either zero or an odd count: 1+sinh(x)
# Expanding in e^(a x) makes each length-L count a short sum of a^L.
ALL_PREFIX = _conv(_power(EVEN_DIGIT, 5), _power(ODD_DIGIT, 5))
LEADING_ZERO_PREFIX = _conv(
    _conv(ODD_COUNT, _power(EVEN_DIGIT, 4)),
    _power(ODD_DIGIT, 5),
)


def _sum_a_to_l(a, n):
    a %= MOD
    if a == 0:
        return 0
    if a == 1:
        return n % MOD
    return a * (pow(a, n, MOD) - 1) * pow(a - 1, -1, MOD) % MOD


def _sum_a_to_l_minus_1(a, n):
    a %= MOD
    if a == 0:
        return 1 if n else 0
    if a == 1:
        return n % MOD
    return (pow(a, n, MOD) - 1) * pow(a - 1, -1, MOD) % MOD


def Q(n):
    total = 0
    for a, coeff in ALL_PREFIX.items():
        total += coeff * _sum_a_to_l(a, n)
    for a, coeff in LEADING_ZERO_PREFIX.items():
        total -= coeff * _sum_a_to_l_minus_1(a, n)
    return total % MOD


def solve():
    assert Q(7) == 287975
    assert Q(100) == 123864868
    return sum(Q(2 ** u) for u in range(1, 40)) % MOD


if __name__ == "__main__":
    print(solve())
