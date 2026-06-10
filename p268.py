#!/usr/bin/env python3
from math import comb

def solve():
    # Count n < 10^16 divisible by at least 4 distinct primes < 100.
    # For an n divisible by exactly t >= 4 of the 25 primes, the identity
    #   sum_{k=4}^{t} (-1)^(k-4) C(k-1,3) C(t,k) = 1
    # shows that weighting every squarefree product d of k >= 4 of the primes
    # by (-1)^(k-4) * C(k-1,3) * floor(N/d) counts each such n exactly once.
    # Enumerate the (product <= N) subsets by DFS over primes in increasing
    # order; the product of the 14 smallest primes already exceeds 10^16,
    # so subset sizes stay small and the tree is modest.
    N = 10 ** 16 - 1
    primes = [p for p in range(2, 100)
              if all(p % q for q in range(2, int(p ** 0.5) + 1))]
    np = len(primes)  # 25
    # weight[k] = (-1)^(k-4) * C(k-1, 3) for subset size k
    weight = [0] * 20
    for k in range(4, 20):
        weight[k] = (1 if (k - 4) % 2 == 0 else -1) * comb(k - 1, 3)

    total = 0

    def dfs(start, d, k):
        nonlocal total
        wk = weight[k + 1]
        for j in range(start, np):
            nd = d * primes[j]
            if nd > N:
                break
            if k + 1 >= 4:
                total += wk * (N // nd)
            dfs(j + 1, nd, k + 1)

    dfs(0, 1, 0)
    return total

if __name__ == "__main__":
    print(solve())
