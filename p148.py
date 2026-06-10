#!/usr/bin/env python3
"""p148: Pascal's triangle entries not divisible by 7 in first 10^9 rows.
Using Lucas's theorem and base-7 digit DP."""
def g(n):
    """g(n) = product(digit_i+1) for base-7 digits of n."""
    if n < 7:
        return n + 1
    q, r = divmod(n, 7)
    return g(q) * (r + 1)

def F(N):
    """F(N) = sum_{n=0}^{N-1} g(n)."""
    if N <= 0:
        return 0
    if N < 7:
        return N * (N + 1) // 2
    q, r = divmod(N, 7)
    # S = 7*8//2 = 28 = sum_{t=0}^{6} (t+1)
    return F(q) * 28 + g(q) * r * (r + 1) // 2

def solve():
    return F(10**9)

if __name__ == "__main__":
    print(solve())
