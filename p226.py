#!/usr/bin/env python3
from math import sqrt, asin, floor

# Blancmange (Takagi) curve: T(x) = sum_{n>=0} s(2^n x) / 2^n,
# where s(x) is the distance from x to the nearest integer.
# Circle C: centre (1/4, 1/2), radius 1/4.
# We need the area below T(x) and inside C.

TERMS = 60

def s(x):
    f = x - floor(x)
    return f if f <= 0.5 else 1.0 - f

def blancmange(x):
    total = 0.0
    scale = 1.0
    for _ in range(TERMS):
        total += s(x) * scale
        x *= 2.0
        scale *= 0.5
    return total

def blancmange_integral(x):
    # Exact antiderivative: integral_0^x T(t) dt = sum_{n>=0} 4^{-n} * S(2^n x)
    # where S(y) = integral_0^y s(u) du = floor(y)/4 + g(frac(y)),
    # g(f) = f^2/2 for f <= 1/2, else 1/4 - (1-f)^2/2.
    total = 0.0
    scale = 1.0
    for _ in range(TERMS):
        k = floor(x)
        f = x - k
        g = 0.5 * f * f if f <= 0.5 else 0.25 - 0.5 * (1.0 - f) * (1.0 - f)
        total += scale * (0.25 * k + g)
        x *= 2.0
        scale *= 0.25
    return total

def circle_lower(x):
    # Lower half of the circle (x-1/4)^2 + (y-1/2)^2 = 1/16
    return 0.5 - sqrt(0.0625 - (x - 0.25) ** 2)

def circle_lower_integral(x):
    # Antiderivative of 1/2 - sqrt(1/16 - (x-1/4)^2)
    u = x - 0.25
    return 0.5 * x - 0.5 * (u * sqrt(0.0625 - u * u) + 0.0625 * asin(4.0 * u))

def solve():
    # The curve passes through (1/2, 1/2), the rightmost point of C.
    # Find the left intersection a in (0, 1/4) where T(x) meets the
    # lower arc of C; on (a, 1/2) the curve stays above the lower arc
    # (and below the upper arc), so the requested area is
    # integral_a^{1/2} (T(x) - lower(x)) dx.
    f = lambda x: blancmange(x) - circle_lower(x)
    lo, hi = 1e-9, 0.25  # f(lo) < 0, f(0.25) = 1/2 - 1/4 > 0
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        if f(mid) < 0.0:
            lo = mid
        else:
            hi = mid
    a = 0.5 * (lo + hi)

    area = (blancmange_integral(0.5) - blancmange_integral(a)) \
         - (circle_lower_integral(0.5) - circle_lower_integral(a))
    return f"{area:.8f}"

if __name__ == "__main__":
    print(solve())
