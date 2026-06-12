#!/usr/bin/env python3
from math import isqrt


def primes_upto(limit):
    is_prime = bytearray(b"\x01") * (limit + 1)
    is_prime[0:2] = b"\x00\x00"
    for p in range(2, isqrt(limit) + 1):
        if is_prime[p]:
            start = p * p
            is_prime[start : limit + 1 : p] = b"\x00" * (((limit - start) // p) + 1)
    return [p for p in range(limit + 1) if is_prime[p]]


PRIMES = primes_upto(4000)


def crt_residues(p, required_primes, sign):
    residues = [0]
    modulus = 1
    for prime in required_primes:
        target = (sign * p) % prime
        inverse = pow(modulus, -1, prime)
        new_residues = []
        for residue in residues:
            t = (-residue * inverse) % prime
            new_residues.append(residue + modulus * t)

            t = ((target - residue) * inverse) % prime
            value = residue + modulus * t
            if value != new_residues[-1]:
                new_residues.append(value)
        modulus *= prime
        residues = new_residues
    return residues, modulus


def V(p):
    q = next(prime for prime in PRIMES if prime * prime > p)
    required = [prime for prime in PRIMES if prime < q]

    best = None

    residues, modulus = crt_residues(p, required, 1)
    upper = p // 2
    best_b = 0
    for residue in residues:
        if residue == 0:
            candidate = (upper // modulus) * modulus
        elif residue <= upper:
            candidate = residue + ((upper - residue) // modulus) * modulus
        else:
            continue
        best_b = max(best_b, candidate)
    if best_b:
        best = p - best_b

    residues, modulus = crt_residues(p, required, -1)
    best_diff_b = None
    for residue in residues:
        candidate = residue if residue > 0 else modulus
        if candidate % p == 0:
            candidate += modulus
        if best_diff_b is None or candidate < best_diff_b:
            best_diff_b = candidate
    diff_a = p + best_diff_b
    return diff_a if best is None else min(best, diff_a)


def S(limit):
    return sum(V(p) for p in PRIMES if p < limit)


def solve():
    assert V(2) == 1
    assert V(37) == 22
    assert V(151) == 165
    assert S(10) == 10
    assert S(200) == 7177
    return S(3800)


if __name__ == "__main__":
    print(solve())
