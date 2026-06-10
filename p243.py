#!/usr/bin/env python3
from fractions import Fraction


def is_resilient_below(d, phi, num, den):
    # R(d) = phi / (d - 1) < num / den  <=>  phi * den < num * (d - 1)
    return phi * den < num * (d - 1)


def solve():
    target = Fraction(15499, 94744)
    num, den = target.numerator, target.denominator

    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]

    best = None
    primorial = 1
    phi_primorial = 1
    for i, p in enumerate(primes):
        primorial *= p
        phi_primorial *= (p - 1)
        next_p = primes[i + 1] if i + 1 < len(primes) else primes[-1] + 2
        # Try d = primorial * m for m = 1 .. next_p - 1.
        # Restrict m so all its prime factors divide the primorial; then
        # phi(primorial * m) = phi(primorial) * m. (For m < next_p this
        # holds automatically, since any prime factor of m is < next_p.)
        for m in range(1, next_p):
            d = primorial * m
            if best is not None and d >= best:
                break
            phi = phi_primorial * m
            if is_resilient_below(d, phi, num, den):
                best = d
                break
        if best is not None and primorial >= best:
            break

    return best


def _verify_example():
    # R(12) = phi(12)/11 = 4/11, and 12 is smallest with R(d) < 4/10
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

    assert Fraction(phi(12), 11) == Fraction(4, 11)
    for d in range(2, 13):
        below = Fraction(phi(d), d - 1) < Fraction(4, 10)
        assert below == (d == 12)


if __name__ == "__main__":
    _verify_example()
    print(solve())
