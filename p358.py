#!/usr/bin/env python3

def is_prime(n):
    # deterministic Miller-Rabin for n < 3.3e24 with these bases
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True

def prime_factors(n):
    fs = set()
    d = 2
    while d * d <= n:
        if n % d == 0:
            fs.add(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        fs.add(n)
    return fs

def solve():
    # Every cyclic number is c = (10^(p-1) - 1)/p for a full reptend prime p
    # (a prime for which 10 is a primitive root); c has p-1 digits, which are
    # exactly the repeating digits of 1/p.
    #
    # Leftmost 11 digits "00000000137": the leading digits of 1/p, so
    # floor(10^11 / p) = 137, i.e. p in (10^11/138, 10^11/137].
    #
    # Rightmost 5 digits "56789": c*p = 10^(p-1) - 1 ≡ -1 (mod 10^5), so
    # 56789 * p ≡ -1 (mod 10^5), fixing p mod 10^5.  That leaves only ~53
    # candidates to test for primality and for 10 being a primitive root
    # (ord_p(10) = p-1, checked via the prime factors of p-1).
    M = 10 ** 5
    residue = (-pow(56789, -1, M)) % M
    lo = 10 ** 11 // 138 + 1
    hi = 10 ** 11 // 137

    candidates = []
    start = lo + (residue - lo) % M
    for p in range(start, hi + 1, M):
        if 10 ** 11 // p != 137:
            continue
        if not is_prime(p):
            continue
        if all(pow(10, (p - 1) // q, p) != 1 for q in prime_factors(p - 1)):
            candidates.append(p)
    assert len(candidates) == 1, candidates
    p = candidates[0]

    # Digit sum via Midy's theorem: for a full reptend prime the period p-1 is
    # even and digits half a period apart sum to 9 (since 10^((p-1)/2) ≡ -1
    # mod p), so the digit sum is 9*(p-1)/2.  (Check: p=7 -> 27 = digit sum of
    # 142857; p=17 -> 72 = digit sum of 0588235294117647.)
    assert pow(10, (p - 1) // 2, p) == p - 1
    return 9 * (p - 1) // 2

if __name__ == "__main__":
    print(solve())
