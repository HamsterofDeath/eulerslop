#!/usr/bin/env python3
# Problem 271: Modular Cubes, part 1
#
# n = 13082761331670030 is squarefree (product of the primes 2..43).
# By CRT, x^3 = 1 (mod n) iff x^3 = 1 (mod p) for every prime p | n.
# For each prime we list the cube roots of unity mod p (1 root if p = 2 mod 3
# or p in {2,3}, 3 roots if p = 1 mod 3) and combine all choices with CRT.
# S(n) is the sum of the combined solutions x with 1 < x < n.

def solve():
    n = 13082761331670030

    # Factor n by trial division (its prime factors are all tiny).
    m, primes = n, []
    d = 2
    while d * d <= m:
        if m % d == 0:
            primes.append(d)
            while m % d == 0:
                m //= d
        d += 1
    if m > 1:
        primes.append(m)

    # Cube roots of unity modulo each prime (primes are <= 43, brute force).
    roots = [[x for x in range(1, p) if pow(x, 3, p) == 1] for p in primes]

    # Incremental CRT over all combinations of roots.
    sols = [0]  # solutions modulo `cur` (starts with modulus 1)
    cur = 1
    for p, rs in zip(primes, roots):
        inv = pow(cur, -1, p)
        new = []
        for s in sols:
            for r in rs:
                # x = s (mod cur), x = r (mod p)  ->  x = s + cur * t
                t = ((r - s) * inv) % p
                new.append(s + cur * t)
        sols = new
        cur *= p

    # Exclude x = 1 (and x = 0 cannot occur since gcd(x, n) = 1).
    return sum(s for s in sols if s > 1)

if __name__ == "__main__":
    print(solve())
