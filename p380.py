#!/usr/bin/env python3
import math

def solve():
    # A maze where every cell is reachable from the top-left by exactly one
    # path is precisely a spanning tree of the m x n grid graph, so C(m,n)
    # is its spanning-tree count.  By the matrix-tree theorem this equals
    #   (1/(mn)) * prod over (i,j) != (0,0) of (mu_i + nu_j),
    # where mu_i = 4 sin^2(i*pi/(2m)) and nu_j = 4 sin^2(j*pi/(2n)) are the
    # Laplacian eigenvalues of the paths P_m and P_n (the grid is their
    # Cartesian product).  Only 5 significant digits are needed, so summing
    # log10 of the 49999 eigenvalues with fsum (error ~1e-11) is exact
    # enough; the sin^2 form avoids the cancellation of 2 - 2cos.
    m, n = 100, 500
    mu = [4 * math.sin(math.pi * i / (2 * m)) ** 2 for i in range(m)]
    nu = [4 * math.sin(math.pi * j / (2 * n)) ** 2 for j in range(n)]
    logs = [math.log10(a + b) for a in mu for b in nu if a + b > 0]
    log10c = math.fsum(logs) - math.log10(m * n)

    # scientific notation, 5 significant digits, lowercase e
    e = math.floor(log10c)
    mant = 10 ** (log10c - e)
    s = f"{mant:.4f}"
    if s.startswith("10"):  # rounding carried the mantissa to 10.0000
        e += 1
        s = f"{mant / 10:.4f}"
    return f"{s}e{e}"

if __name__ == "__main__":
    print(solve())
