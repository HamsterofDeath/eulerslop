#!/usr/bin/env python3
# Project Euler 242: Odd Triplets
#
# f(n, k) = number of k-element subsets of {1..n} with odd sum.
# Count triplets [n, k, f(n,k)] with n, k and f(n,k) all odd, n <= 10^12.
#
# Derivation (verified against direct subset-parity brute force for n <= 200):
# With a = ceil(n/2) odd elements and b = floor(n/2) even elements,
#   sum_k f(n,k) x^k = ((1+x)^n - (1-x)^a (1+x)^b) / 2.
# Analysing parities (Lucas/Kummer on the resulting binomials) shows that
# odd triplets exist only for n == 1 (mod 4), and for such n the number of
# odd k with f(n,k) odd equals 2^(popcount(n) - 1).
#
# Writing n = 4m + 1 (so popcount(n) = popcount(m) + 1), the answer is
#   sum_{m=0}^{M} 2^popcount(m),   M = floor((N-1)/4),
# which has the closed form below using sum_{m < 2^t} 2^popcount(m) = 3^t.


def sum_2_popcount(x):
    """Return sum_{m=0}^{x-1} 2^popcount(m)."""
    total = 0
    ones_above = 0
    for b in range(x.bit_length() - 1, -1, -1):
        if (x >> b) & 1:
            total += (1 << ones_above) * 3 ** b
            ones_above += 1
    return total


def solve():
    n_limit = 10 ** 12
    m_count = (n_limit - 1) // 4 + 1  # number of n <= limit with n == 1 (mod 4)
    return sum_2_popcount(m_count)


if __name__ == "__main__":
    print(solve())
