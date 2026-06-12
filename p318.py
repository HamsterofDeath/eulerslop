#!/usr/bin/env python3
import math

def solve():
    # Let x = (sqrt(p)+sqrt(q))^2 and y = (sqrt(q)-sqrt(p))^2 = p+q-2*sqrt(pq).
    # x and y are conjugate roots of an integer-coefficient quadratic, so
    # x^n + y^n is an integer; hence frac((sqrt p + sqrt q)^(2n)) = 1 - y^n
    # whenever 0 < y < 1 (which is exactly when the fractional part -> 1;
    # if pq is a perfect square y is a positive integer, so y < 1 fails).
    # C(p,q,n) >= 2011  <=>  y^n <= 10^-2011, so
    #   N(p,q) = ceil(2011 / (-log10 y)).
    # Compute y with 40 extra digits via integer sqrt to keep log10 accurate.
    D = 40
    SCALE = 10 ** D
    SCALE2 = 10 ** (2 * D)
    LOGSCALE = float(D)
    total = 0
    for p in range(1, 1006):
        for q in range(p + 1, 2012 - p):
            # y_scaled ~= (p + q - 2*sqrt(p*q)) * 10^D
            y_scaled = (p + q) * SCALE - 2 * math.isqrt(p * q * SCALE2)
            if y_scaled >= SCALE:  # y >= 1: fractional part does not -> 1
                break  # y grows with q for fixed p, so no larger q works
            log10y = math.log10(y_scaled) - LOGSCALE  # negative
            total += math.ceil(2011 / -log10y)
    return total

if __name__ == "__main__":
    print(solve())
