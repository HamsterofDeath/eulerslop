#!/usr/bin/env python3
import numpy as np

def solve():
    # By the law of cosines every angle of an integer-sided triangle has a
    # rational cosine; by Niven's theorem the only rational angles (in
    # degrees) with rational cosine are 0, 60, 90, 120, 180. So we count
    # triangles with perimeter <= N containing a 60, 90 or 120 degree angle
    # (mutually exclusive except equilateral, which has only 60s).
    #
    # Primitive families, for m > n >= 1, gcd(m, n) = 1 (verified against
    # brute force for small N):
    #  90:  (m-n) odd:        perimeter 2m(m+n)            [Pythagorean]
    #  120: (m-n) % 3 != 0:   a=m^2-n^2, b=2mn+n^2, c=m^2+mn+n^2,
    #                         perimeter (2m+n)(m+n)
    #  60:  each 120-triple (a,b,c) yields the two 60-triples (a, a+b, c)
    #       and (b, a+b, c), perimeters 3m(m+n) and (2m+n)(m+2n);
    #       plus the equilateral family (perimeter 3k).
    # Each primitive triple contributes floor(N / perimeter) multiples.
    N = 10 ** 8

    total = N // 3  # equilateral triangles
    m_max = int((N / 2) ** 0.5) + 2
    for m in range(2, m_max + 1):
        n = np.arange(1, m, dtype=np.int64)
        n = n[np.gcd(n, m) == 1]
        if n.size == 0:
            continue
        d = m - n
        # 90 degrees
        p = 2 * m * (m + n)
        sel = (d % 2 == 1) & (p <= N)
        total += int(np.sum(N // p[sel]))
        # 120 and the two 60 families share the (m-n) % 3 != 0 condition
        n3 = n[d % 3 != 0]
        for p in ((2 * m + n3) * (m + n3),
                  3 * m * (m + n3),
                  (2 * m + n3) * (m + 2 * n3)):
            p = p[p <= N]
            total += int(np.sum(N // p))
    return total

if __name__ == "__main__":
    print(solve())
