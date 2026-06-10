#!/usr/bin/env python3
# Project Euler 283: Integer sided triangles with integral area/perimeter ratio.
#
# Write the tangent lengths x = s-a, y = s-b, z = s-c (s = semiperimeter).
# Heron gives Area^2 = s*x*y*z and Area = r*s (r = inradius), so
# x*y*z = r^2 * (x+y+z).  Area/perimeter = r/2 = m, hence with q = 4*m^2:
#     x*y*z = q * (x + y + z),   0 < x <= y <= z,   perimeter = 2(x+y+z).
# (x, y, z must be integers: the all-half-odd-integer case forces an odd
# product to equal an even one.)  From x^3 <= xyz <= 3*q*z we get x <= sqrt(3q).
#
# For fixed m and x, solving for z gives z = q(x+y)/(xy-q) and the identity
#     (x*y - q) * (x*z - q) = q * (x^2 + q)
# so each solution corresponds to a divisor pair d*e = D := q*(x^2+q) with
# d <= e, d >= x^2 - q (i.e. y >= x), and x | d+q, x | e+q.
#
# Speed: D = 4m^2 * (x^2 + 4m^2).  We know the factorisation of 4m^2 and we
# factor all values x^2 + 4m^2 (x = 1..floor(2m*sqrt(3))) at once with a
# quadratic-polynomial sieve: an odd prime p not dividing 2m divides
# x^2 + 4m^2 iff x = +-2m*sqrt(-1) (mod p), so we only touch arithmetic
# progressions, using precomputed sqrt(-1) mod p for p = 1 (mod 4), p <= 4m.
# After removing primes <= 4m the leftover cofactor is 1 or prime, because
# x^2 + 4m^2 <= 16 m^2.  Divisors of D are then enumerated directly.

from math import isqrt

M_MAX = 1000


def prime_data(limit):
    """primes <= limit and sqrt(-1) mod p for p = 1 (mod 4)."""
    sieve = bytearray([1]) * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for i in range(2, isqrt(limit) + 1):
        if sieve[i]:
            sieve[i * i:: i] = bytearray(len(sieve[i * i:: i]))
    primes = [i for i in range(2, limit + 1) if sieve[i]]
    root = {}
    for p in primes:
        if p % 4 == 1:
            # sqrt(-1) mod p via Euler: g^((p-1)/4) for a non-residue g
            g = 2
            while pow(g, (p - 1) // 2, p) != p - 1:
                g += 1
            root[p] = pow(g, (p - 1) // 4, p)
    return primes, root


def factor_int(n, primes):
    f = {}
    for p in primes:
        if p * p > n:
            break
        while n % p == 0:
            f[p] = f.get(p, 0) + 1
            n //= p
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def solve():
    primes, root = prime_data(4 * M_MAX)
    total = 0

    for m in range(1, M_MAX + 1):
        q = 4 * m * m
        X = isqrt(3 * q)  # x <= 2m*sqrt(3)
        # vals[x] = remaining unfactored part of x^2 + q, fac[x] = factor dict
        vals = [0] * (X + 1)
        fac = [None] * (X + 1)
        for x in range(1, X + 1):
            vals[x] = x * x + q
            fac[x] = {}

        two_m = 2 * m
        pmax = isqrt(X * X + q)  # remove primes up to sqrt(max value)
        for p in primes:
            if p > pmax:
                break
            if p == 2 or two_m % p == 0:
                # p | x^2 + 4m^2 iff p | x^2; step through multiples (and for
                # p = 2 odd m: x even). Cheap: at most X/p starting points.
                start = p
                step = p
            else:
                if p % 4 != 1:
                    continue
                r = (two_m * root[p]) % p
                start = None  # handled below (two progressions)
                step = p
            if start is not None:
                for x0 in range(start, X + 1, step):
                    v = vals[x0]
                    e = 0
                    while v % p == 0:
                        v //= p
                        e += 1
                    if e:
                        vals[x0] = v
                        fac[x0][p] = e
            else:
                for r0 in (r, p - r):
                    for x0 in range(r0 if r0 else p, X + 1, p):
                        v = vals[x0]
                        e = 0
                        while v % p == 0:
                            v //= p
                            e += 1
                        if e:
                            vals[x0] = v
                            fac[x0][p] = e
                    if r == p - r:
                        break

        qfac = factor_int(q, primes)

        for x in range(1, X + 1):
            f = dict(qfac)
            for p, e in fac[x].items():
                f[p] = f.get(p, 0) + e
            leftover = vals[x]
            if leftover > 1:  # cofactor is prime (x^2+q <= 16m^2, p > 4m)
                f[leftover] = f.get(leftover, 0) + 1

            D = q * (x * x + q)
            # enumerate all divisors of D
            divs = [1]
            for p, e in f.items():
                pe = []
                pk = 1
                for _ in range(e):
                    pk *= p
                    pe.append(pk)
                divs += [d * pp for d in divs for pp in pe]

            dmin = x * x - q
            s = isqrt(D)
            for d in divs:
                if d < dmin or d > s:
                    continue
                if (d + q) % x:
                    continue
                e2 = D // d
                if (e2 + q) % x:
                    continue
                y = (d + q) // x
                z = (e2 + q) // x
                total += 2 * (x + y + z)

    return total


if __name__ == "__main__":
    print(solve())
