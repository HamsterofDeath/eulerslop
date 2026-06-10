#!/usr/bin/env python3
"""p188: Tetration

Find the last 8 digits of 1777 ^^ 1855.
Uses recursive Euler's totient theorem.
"""

def phi(n):
    result = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1
    if n > 1:
        result -= result // n
    return result

def tetrate(a, b, m):
    if m == 1:
        return 0
    if b == 1:
        return a % m
    phi_m = phi(m)
    exponent = tetrate(a, b - 1, phi_m)
    return pow(a, exponent, m)

def solve():
    return tetrate(1777, 1855, 10**8)

if __name__ == "__main__":
    print(solve())
