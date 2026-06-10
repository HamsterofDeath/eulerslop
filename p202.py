#!/usr/bin/env python3
"""Project Euler 202: Laserbeam.

Unfold the reflections: the triangle's mirror images tile the plane with a
triangular lattice, and a beam entering C and bouncing off n surfaces becomes
a straight segment from C to an image point (a, b) (in the basis of the two
triangle edges at C) with a + b = N = (n + 3) / 2.  The segment must not hit
any lattice vertex on the way, i.e. gcd(a, b) = gcd(a, N) = 1, and the
endpoint must be an image of C, which by the lattice colouring means
(a - b) % 3 == 0, i.e. 2a ≡ N (mod 3).

So we count a in [1, N-1] with a ≡ 2N (mod 3) and gcd(a, N) = 1, by
inclusion-exclusion over the prime factors of N.
"""


def factorize(n):
    primes = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            primes.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        primes.append(n)
    return primes


def count_in_residue(limit, step, residue, modulus):
    """Count x in [1, limit] with x % modulus == residue and step | x."""
    # x = step * k, need step * k ≡ residue (mod modulus)
    kmax = limit // step
    inv = pow(step, -1, modulus)
    c = (residue * inv) % modulus
    if c == 0:
        c = modulus
    if c > kmax:
        return 0
    return (kmax - c) // modulus + 1


def solve(bounces=12017639147):
    N = (bounces + 3) // 2
    r = (2 * N) % 3  # required residue of a modulo 3
    primes = factorize(N)
    # N here is not divisible by 3 (otherwise r would be 0, impossible
    # alongside gcd(a, N) = 1); inclusion-exclusion over squarefree divisors.
    total = 0
    for mask in range(1 << len(primes)):
        d = 1
        bits = 0
        m = mask
        i = 0
        while m:
            if m & 1:
                d *= primes[i]
                bits += 1
            m >>= 1
            i += 1
        cnt = count_in_residue(N - 1, d, r, 3)
        total += -cnt if bits & 1 else cnt
    return total


if __name__ == "__main__":
    print(solve())
