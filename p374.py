#!/usr/bin/env python3
import math
from array import array

def solve():
    # The product-maximizing partition of n into distinct parts consists of
    # consecutive integers with at most one element adjusted.  With
    # T(k) = k(k+1)/2, the block T(k)-1 <= n <= T(k)+k-1 (k >= 2) tiles all
    # n >= 2; write d = n - (T(k)-1), 0 <= d <= k.  Then (verified by brute
    # force for n <= 100, reproducing sum = 1683550844462):
    #   d = 0:          parts {2..k},             f = k!
    #   1 <= d <= k-1:  parts {2..k+1}\{k+1-d},   f = (k+1)!/(k+1-d)
    #   d = k:          parts {3..k,k+2},         f = k!(k+2)/2
    # and m = k-1 in every case (n = 1 is special: f = m = 1).
    # Summing a full block: sum_d f = k! + (k+1)!*H + k!(k+2)/2 with
    # H = sum_{j=2}^{k} 1/j, all computable mod p with an inverse table.
    N = 10 ** 14
    MOD = 982451653

    # largest k whose block starts at or below N
    K = (math.isqrt(8 * N + 9) - 1) // 2
    while K * (K + 1) // 2 - 1 > N:
        K -= 1
    while (K + 1) * (K + 2) // 2 - 1 <= N:
        K += 1

    # modular inverses of 1..K via the standard recurrence
    inv = array('q', bytes(8 * (K + 1)))
    inv[1] = 1
    for i in range(2, K + 1):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD
    inv2 = (MOD + 1) // 2

    total = 1 if N >= 1 else 0  # n = 1 contributes f*m = 1
    fact_k = 1                  # k! mod MOD (k = 1 here)
    H = 0                       # sum_{j=2}^{k} inv(j) mod MOD
    for k in range(2, K + 1):
        fact_k = fact_k * k % MOD
        H = (H + inv[k]) % MOD
        dmax = N - (k * (k + 1) // 2 - 1)
        if dmax > k:
            dmax = k
        block = fact_k                       # d = 0 term
        dm = dmax if dmax <= k - 1 else k - 1
        if dm >= 1:
            if dm == k - 1:
                hs = H                       # full block: sum_{j=2}^{k} 1/j
            else:                            # final partial block
                hs = sum(inv[j] for j in range(k + 1 - dm, k + 1)) % MOD
            block += fact_k * (k + 1) % MOD * hs
        if dmax == k:
            block += fact_k * (k + 2) % MOD * inv2
        total = (total + (k - 1) * (block % MOD)) % MOD
    return total

if __name__ == "__main__":
    print(solve())
