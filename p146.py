#!/usr/bin/env python3
"""p146: Sum of n < 150M where n^2+1, +3, +7, +9, +13, +27 are consecutive primes."""
import sys

def is_prime(n, small_primes):
    if n < 2:
        return False
    for p in small_primes:
        if p * p > n:
            return True
        if n % p == 0:
            return False
    # Miller-Rabin for larger numbers
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in (2, 3, 5, 7, 11, 13, 17):
        if a >= n:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True

def solve():
    limit = 150_000_000
    
    # n must be even, n ≡ 0 mod 5 (or ≡ 0,1,2,3,4? Let's derive properly)
    # From problem description and analysis:
    # n ≡ 10, 80, 130, 200 mod 210 (from mod 2,3,5,7 filtering)
    # But we also need gap numbers composite. Let's sieve more.
    
    # Build a list of admissible residues modulo product of small primes
    # We'll use mod = 2*3*5*7*11*13*17 = 510510
    
    mod = 1
    res = [0]  # start with just 0
    
    target_d = (1, 3, 7, 9, 13, 27)
    gap_d = (5, 11, 15, 17, 19, 21, 23, 25)
    
    for p in (2, 3, 5, 7, 11, 13):
        new_res = []
        for r in res:
            for c in range(p):
                n_mod = r + c * mod
                ok = True
                # Check n^2 + d not divisible by p for any target d
                for d in target_d:
                    if (n_mod * n_mod + d) % p == 0:
                        # Could be equal to p itself, but that's rare for large n
                        if n_mod * n_mod + d == p:
                            continue
                        ok = False
                        break
                if ok:
                    new_res.append(n_mod)
        mod *= p
        res = new_res
    
    # Now also precompute small primes for Miller-Rabin
    sp = []
    sieve = [True] * 10000
    sieve[0] = sieve[1] = False
    for i in range(2, 10000):
        if sieve[i]:
            sp.append(i)
            for j in range(i*i, 10000, i):
                sieve[j] = False
    
    total = 0
    all_d = sorted(set(target_d) | set(gap_d))  # 1,3,5,7,9,11,13,15,17,19,21,23,25,27
    
    for r in res:
        if r > limit:
            continue
        i = 0
        while True:
            n = r + i * mod
            if n >= limit:
                break
            if n < 10:  # n must be at least 10 for the pattern
                i += 1
                continue
            
            # Quick check: n^2+... divisible by small primes
            n2 = n * n
            ok = True
            for p in sp[:50]:  # first 50 primes
                for d in all_d:
                    if (n2 + d) % p == 0:
                        if n2 + d == p:
                            continue
                        # This means n^2+d is composite (or equal to p)
                        # For target_d, this is bad
                        if d in target_d:
                            ok = False
                            break
                if not ok:
                    break
            if not ok:
                i += 1
                continue
            
            # Check target numbers are prime
            primes_ok = True
            for d in target_d:
                if not is_prime(n2 + d, sp):
                    primes_ok = False
                    break
            if not primes_ok:
                i += 1
                continue
            
            # Check gap numbers are NOT prime
            gap_ok = True
            for d in gap_d:
                if is_prime(n2 + d, sp):
                    gap_ok = False
                    break
            if not gap_ok:
                i += 1
                continue
            
            total += n
            i += 1
    
    return total

if __name__ == "__main__":
    print(solve())
