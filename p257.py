#!/usr/bin/env python3
from math import gcd, isqrt

# Triangle a <= b <= c; E on AB (bisector from C), G on AC (bisector from B).
# AE = bc/(a+b), AG = bc/(a+c)  =>  R := area(ABC)/area(AEG) = (a+b)(a+c)/(bc).
# R = 1 + a(a+b+c)/(bc), and a <= b <= c gives 1 < R <= 4, so R in {2,3,4}.
#
# R = 4: (3b-a)(3c-a) = 4a^2 with 3b-a, 3c-a >= 2a forces a = b = c:
#        equilateral triangles, floor(L/3) of them.
#
# R = 2: bc = a(a+b+c) <=> (b-a)(c-a) = 2a^2.  With p = b-a, q = c-a:
#   pq = 2a^2; non-degeneracy and ordering force a < p <= q (then the
#   triangle inequality holds automatically).  Let d = gcd(p,q); p/d, q/d are
#   coprime with product 2*(a/d)^2 (one of them carries the factor 2 and each
#   odd prime appears to an even power), hence
#     {p, q} = {2 d s^2, d t^2},  gcd(s,t) = 1, t odd,  a = d s t.
#   Form 2A: p = 2ds^2, q = dt^2 : sqrt(2) s < t < 2s; perimeter d(2s+t)(s+t).
#   Form 2B: p = ds^2, q = 2dt^2 : t < s < sqrt(2) t, s odd;
#            perimeter d(s+2t)(s+t).
#
# R = 3: 2bc = a(a+b+c) <=> (2b-a)(2c-a) = 3a^2.  With p = 2b-a, q = 2c-a:
#   pq = 3a^2, a < p <= q, and p ≡ q ≡ a (mod 2) so that b, c are integers.
#   Similarly {p, q} = {3 d s^2, d t^2}, gcd(s,t) = 1, 3 ∤ t, a = d s t.
#   Form 3A: p = 3ds^2, q = dt^2 : sqrt(3) s < t < 3s; perimeter d(3s+t)(s+t)/2.
#   Form 3B: p = ds^2, q = 3dt^2 : t < s < sqrt(3) t, 3 ∤ s;
#            perimeter d(s+3t)(s+t)/2.
#   Parity: if s and t are both odd then p, q, a share parity for every d;
#   otherwise d must be even (d = 2e, perimeter e*P0).
#
# Each (a,b,c) corresponds to exactly one (form, s, t, d) since d = gcd(p,q)
# and the splitting of p/d, q/d is unique.  Count multiples of each primitive
# perimeter up to L.

L = 100_000_000


def family2A():
    total = 0
    s = 1
    while (2 * s + isqrt(2 * s * s) + 1) * (s + isqrt(2 * s * s) + 1) <= L:
        t0 = isqrt(2 * s * s) + 1          # smallest t with t > sqrt(2) s
        for t in range(t0, 2 * s):
            P0 = (2 * s + t) * (s + t)
            if P0 > L:
                break
            if t % 2 == 1 and gcd(s, t) == 1:
                total += L // P0
        s += 1
    return total


def family2B():
    total = 0
    t = 1
    while (t + 1 + 2 * t) * (t + 1 + t) <= L:
        for s in range(t + 1, isqrt(2 * t * t) + 1):   # t < s <= floor(sqrt2 t)
            P0 = (s + 2 * t) * (s + t)
            if P0 > L:
                break
            if s % 2 == 1 and gcd(s, t) == 1:
                total += L // P0
        t += 1
    return total


def family3A():
    # Note: L // P0 == 0 automatically when P0 > L, so the parity cases
    # need no separate perimeter thresholds; loop while P0 <= 2L.
    total = 0
    s = 1
    while True:
        t0 = isqrt(3 * s * s) + 1          # smallest t with t > sqrt(3) s
        if (3 * s + t0) * (s + t0) > 2 * L:
            return total
        for t in range(t0, 3 * s):
            P0 = (3 * s + t) * (s + t)
            if P0 > 2 * L:
                break
            if t % 3 == 0 or gcd(s, t) != 1:
                continue
            if (s & 1) and (t & 1):
                total += (2 * L) // P0     # any d, perimeter d*P0/2 <= L
            else:
                total += L // P0           # d = 2e, perimeter e*P0 <= L
        s += 1


def family3B():
    total = 0
    t = 1
    while True:
        s0 = t + 1
        if (s0 + 3 * t) * (s0 + t) > 2 * L:
            return total
        for s in range(s0, isqrt(3 * t * t) + 1):
            P0 = (s + 3 * t) * (s + t)
            if P0 > 2 * L:
                break
            if s % 3 == 0 or gcd(s, t) != 1:
                continue
            if (s & 1) and (t & 1):
                total += (2 * L) // P0
            else:
                total += L // P0
        t += 1


def solve():
    return L // 3 + family2A() + family2B() + family3A() + family3B()


if __name__ == "__main__":
    print(solve())
