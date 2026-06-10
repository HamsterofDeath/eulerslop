#!/usr/bin/env python3
from math import gcd, isqrt

def solve():
    # A perfect triangle is a primitive Pythagorean triple (a, b, c) whose
    # hypotenuse c is a perfect square, c = q^2 <= 10^16.
    #
    # Primitive triples: a = m^2 - n^2, b = 2mn, c = m^2 + n^2 with
    # gcd(m, n) = 1, m > n >= 1, m and n of opposite parity.
    #
    # Requiring c = m^2 + n^2 = q^2 means (n, m, q) is itself a primitive
    # Pythagorean triple (gcd(m, n) = 1), so {m, n} = {s^2 - t^2, 2st} and
    # q = s^2 + t^2 for coprime s > t >= 1 of opposite parity.
    # This double parametrization enumerates every perfect triangle exactly
    # once. c <= 10^16 means q = s^2 + t^2 <= 10^8.
    #
    # Super-perfect additionally needs area = a*b/2 divisible by 6 and 28,
    # i.e. by lcm(6, 28) = 84. We count perfect triangles failing that.
    limit_q = 10 ** 8  # q = sqrt(c) <= 10^8
    count = 0
    s_max = isqrt(limit_q - 1)
    for s in range(2, s_max + 1):
        s2 = s * s
        t_hi = min(s - 1, isqrt(limit_q - s2))
        # opposite parity: t starts at 1 for even s, 2 for odd s
        for t in range(1 + (s & 1), t_hi + 1, 2):
            if gcd(s, t) != 1:
                continue
            m = s2 - t * t
            n = 2 * s * t
            a = abs(m * m - n * n)
            b = 2 * m * n
            # area = a * b / 2; b is even, so test a * (b // 2) mod 84
            if (a * (b >> 1)) % 84:
                count += 1
    return count

if __name__ == "__main__":
    print(solve())
