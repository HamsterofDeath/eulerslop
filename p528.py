#!/usr/bin/env python3

MOD = 1_000_000_007


def _binom_small_k(n, k):
    if n < 0 or k < 0 or k > n:
        return 0
    numerator = denominator = 1
    for i in range(1, k + 1):
        numerator = numerator * ((n - k + i) % MOD) % MOD
        denominator = denominator * i % MOD
    return numerator * pow(denominator, MOD - 2, MOD) % MOD


def S(n, k, b):
    # Count y_1+...+y_k <= n with y_i >= 0 and y_i <= b^i.  Without the upper
    # bounds there are C(n+k,k) solutions; subtract violations by
    # inclusion-exclusion after shifting y_i by b^i+1.
    shifts = [b ** i + 1 for i in range(1, k + 1)]
    total = 0
    for mask in range(1 << k):
        shift = 0
        bits = 0
        for i, value in enumerate(shifts):
            if (mask >> i) & 1:
                shift += value
                bits += 1
        term = _binom_small_k(n - shift + k, k)
        total += -term if bits & 1 else term
    return total % MOD


def solve():
    assert S(14, 3, 2) == 135
    assert S(200, 5, 3) == 12949440
    assert S(1000, 10, 5) == 624839075
    return sum(S(10 ** k, k, k) for k in range(10, 16)) % MOD


if __name__ == "__main__":
    print(solve())
