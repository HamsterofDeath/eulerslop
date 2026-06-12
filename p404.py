import math

import numpy as np


def solve():
    # Ellipse x^2+4y^2=4a^2 in polar form: r^2 = 4a^2/(1+3sin^2(phi)).
    # The 4 intersection points with the rotated copy lie on the bisector
    # directions phi = theta/2 and theta/2+90deg, giving
    #   b^2 = 4a^2/(1+3cos^2(t/2)),  c^2 = 4a^2/(1+3sin^2(t/2))
    # which combine to 1/b^2 + 1/c^2 = 5/(2a)^2, i.e. b^2+c^2 = 5*(bc/(2a))^2.
    # So with (b,c) = k*(x,y) for a primitive solution of x^2+y^2 = 5 z^2
    # (gcd(x,y)=1, z odd, xy even, gcd(z,xy)=1), a = k*x*y/(2z) which is an
    # integer iff z | k; the smallest a is a_min = x*y/2.  The geometric
    # constraints 0<theta<90 translate to z < x < y < 2z.
    # Each primitive triple contributes floor(N / a_min) triplets.
    # Primitives are generated once each (up to order/sign) by
    #   w = (2+i)(m+ni)^2,  m,n>=1, gcd(m,n)=1, m+n odd, m+2n != 0 mod 5,
    # via x0=|2(m^2-n^2)-2mn|, y0=|m^2-n^2+4mn|, z=m^2+n^2.
    N = 10**17
    zmax = math.isqrt(N)  # xy > 2z^2 and a_min = xy/2 <= N force z <= sqrt(N)
    mmax = math.isqrt(zmax)
    total = 0
    for m in range(1, mmax + 1):
        nmax = math.isqrt(zmax - m * m)
        if nmax < 1:
            break
        n = np.arange(1, nmax + 1, dtype=np.int64)
        # unit-orbit representative: m,n >= 1; primitivity conditions
        mask = (np.gcd(n, m) == 1) & ((n + m) & 1 == 1) & ((m + 2 * n) % 5 != 0)
        n = n[mask]
        if n.size == 0:
            continue
        p = m * m - n * n
        q = 2 * m * n
        x0 = np.abs(2 * p - q)
        y0 = np.abs(p + 2 * q)
        x = np.minimum(x0, y0)
        y = np.maximum(x0, y0)
        z = m * m + n * n
        amin = x * y // 2
        good = (z < x) & (amin <= N)
        if good.any():
            total += int((N // amin[good]).sum())
    return total


if __name__ == "__main__":
    print(solve())
