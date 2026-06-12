#!/usr/bin/env python3
import math

def solve():
    # P(some chip has >= 3 defects) = 1 - P(every chip has <= 2 defects).
    # Count assignments of k labelled defects to n labelled chips where exactly
    # j chips receive 2 defects (and k-2j chips receive 1):
    #   ways(j) = k! / (2^j * j! * (k-2j)!) * n! / (n-k+j)!
    # (partition defects into j unordered pairs and k-2j singletons, then
    # assign the k-j blocks to distinct chips).  Divide by n^k.
    # We sum t_j = ways(j)/n^k using the exact term ratio
    #   t_{j+1}/t_j = (k-2j)(k-2j-1) / (2 (j+1) (n-k+j+1)).
    k, n = 20000, 1000000

    # t_0 = n (n-1) ... (n-k+1) / n^k = prod_{i=1}^{k-1} (1 - i/n)
    log_t0 = 0.0
    for i in range(1, k):
        log_t0 += math.log1p(-i / n)
    t = math.exp(log_t0)

    total = t
    for j in range(k // 2):
        t *= (k - 2 * j) * (k - 2 * j - 1) / (2.0 * (j + 1) * (n - k + j + 1))
        total += t

    return "%.10f" % (1.0 - total)

if __name__ == "__main__":
    print(solve())
