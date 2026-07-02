#!/usr/bin/env python3
"""Project Euler 792: 2-adic valuation of 3*S(n)+4.

S(n) = sum_{k=1}^n (-2)^k C(2k,k).  The full series sum_{k>=0} (-2)^k C(2k,k)
converges 2-adically (term valuation k + s2(k)) to L with L^2 = 1/9 and
L == 1 mod 4, i.e. L = -1/3.  Hence 3*S(n) + 4 = -3 * T(n) where
T(n) = sum_{k>n} (-2)^k C(2k,k), so u(n) = nu2(T(n)).

Factor the tail's first term out: with m = n and k_i = m + 1 + i,
T(m) = (-2)^{m+1} C(2m+2, m+1) * sum_{j>=0} r_j,
r_j = prod_{i=1}^{j} (-4)(2 k_i - 1) / k_i.

nu2(r_j) >= 2j - (j + log2(m+j)) grows linearly, so truncating at J terms
determines nu2 exactly once the partial sum's valuation is safely below the
truncation error's valuation.  Everything is exact integer arithmetic:
multiply through by prod k_i and track nu2 of the integer sum.
"""

N = 10 ** 4
BASE_J = 160


def nu2(x: int) -> int:
    return (x & -x).bit_length() - 1


def s2(x: int) -> int:
    return bin(x).count("1")


def u(m: int) -> int:
    j_terms = BASE_J
    while True:
        ks = [m + 1 + i for i in range(1, j_terms + 1)]
        suffix = [1] * (j_terms + 1)
        for idx in range(j_terms - 1, -1, -1):
            suffix[idx] = suffix[idx + 1] * ks[idx]
        total = suffix[0]  # j = 0 term: 1 * prod(all k_i)
        prefix = 1
        for j in range(1, j_terms + 1):
            prefix *= -4 * (2 * ks[j - 1] - 1)
            total += prefix * suffix[j]
        # nu2(sum r_j) = nu2(total) - nu2(prod k_i)
        denom_v = sum(nu2(k) for k in ks)
        sum_v = nu2(total) - denom_v
        # truncation error valuation lower bound
        err_v = min(
            2 * j - (j + max(m + j_terms, 2).bit_length())
            for j in (j_terms + 1,)
        )
        if sum_v < err_v - 8:
            lead_v = (m + 1) + s2(m + 1)  # nu2((-2)^{m+1} C(2m+2,m+1))
            return lead_v + sum_v
        j_terms *= 2


def brute_u(n: int) -> int:
    s = 0
    c = 1  # C(2k,k)
    for k in range(1, n + 1):
        c = c * 2 * (2 * k - 1) // k
        s += (-2) ** k * c
    return nu2(3 * s + 4)


def solve() -> int:
    for n in (1, 2, 3, 4, 5, 7, 12, 20, 33, 64, 100):
        assert u(n) == brute_u(n), (n, u(n), brute_u(n))
    assert sum(u(n ** 3) for n in range(1, 6)) == 241
    return sum(u(n ** 3) for n in range(1, N + 1))


if __name__ == "__main__":
    print(solve())
