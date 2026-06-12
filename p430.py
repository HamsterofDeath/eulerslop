import numpy as np


def solve():
    # Disk i flips iff i lies in [min(A,B), max(A,B)], which happens with
    # probability p_i = 1 - ((i-1)^2 + (N-i)^2)/N^2 per turn (both A,B < i or
    # both > i means no flip). After M independent turns,
    #   P(disk i is white) = (1 + (1-2p_i)^M)/2,
    # so E(N,M) = N/2 + (1/2) * sum_i x_i^M with
    #   x_i = 1 - 2p_i = (2(i-1)^2 + 2(N-i)^2 - N^2)/N^2.
    # (Checks: E(3,1)=10/9, E(3,2)=5/3, E(10,4)~5.157, E(100,10)~51.893.)
    #
    # For N=10^10, M=4000, x_i in [~0, 1) and x_i^M is negligible except near
    # the two edges where x ~ 1 - 4(k+1)/N (k = distance from the edge):
    # x^M ~ exp(-4M(k+1)/N), so only k up to ~ 45*N/(4M) ~ 2.8e7 terms matter
    # (tail beyond exp(-45) sums to < 1e-13). Both edges are symmetric.
    N = 10 ** 10
    M = 4000
    Nf = float(N)  # N^2 = 1e20 exceeds int64; do it in float64 (N is exact)

    K = int(45.0 * N / (4 * M)) + 10
    S = 0.0
    chunk = 4_000_000
    for start in range(0, K, chunk):
        k = np.arange(start, min(start + chunk, K), dtype=np.float64)
        # x = 1 - delta with delta = (4(k+1)N - 2k^2 - 2(k+1)^2)/N^2, computed
        # in float64 without forming N^2 +/- small differences (delta <= ~1e-2,
        # all intermediate quantities carry full relative precision).
        delta = (4.0 * (k + 1.0) * Nf - 2.0 * k * k - 2.0 * (k + 1.0) ** 2) / (Nf * Nf)
        S += float(np.exp(M * np.log1p(-delta)).sum())

    # E = N/2 + (1/2)(left edge + right edge) = N/2 + S by symmetry.
    E = N / 2 + S
    return f"{E:.2f}"


if __name__ == "__main__":
    print(solve())
