#!/usr/bin/env python3
from functools import lru_cache


P = sum(1 << i for i in range(5))  # 1+x+x^2+x^3+x^4 over F_2


def _poly_mul(a, b):
    out = 0
    shift = 0
    while b:
        if b & 1:
            out ^= a << shift
        b >>= 1
        shift += 1
    return out


def _cartier(poly, parity):
    # Keep coefficients whose exponent has the requested parity, then divide
    # the exponent by two.  This is the even/odd coefficient split over F_2.
    out = 0
    poly >>= parity
    idx = 0
    while poly:
        if poly & 1:
            out |= 1 << idx
        poly >>= 2
        idx += 1
    return out


@lru_cache(maxsize=None)
def _transition(multiplier, bit):
    poly = _poly_mul(multiplier, P) if bit else multiplier
    return tuple(x for x in (_cartier(poly, 0), _cartier(poly, 1)) if x)


@lru_cache(maxsize=None)
def _weight(multiplier, exponent):
    if exponent == 0:
        return multiplier.bit_count()
    return sum(_weight(next_multiplier, exponent // 2)
               for next_multiplier in _transition(multiplier, exponent & 1))


def Q(k):
    return _weight(1, k)


def solve():
    assert Q(3) == 7
    assert Q(10) == 17
    assert Q(100) == 35
    return sum(Q(10 ** k) for k in range(1, 19))


if __name__ == "__main__":
    print(solve())
