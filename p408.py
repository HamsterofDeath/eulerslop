import math

import numpy as np

MOD = 1_000_000_007


def prefix_prod_mod(a):
    # In-place Hillis-Steele prefix product mod MOD (int64 safe: values < 2^30, products < 2^60).
    n = len(a)
    shift = 1
    while shift < n:
        a[shift:] = a[shift:] * a[:-shift] % MOD
        shift <<= 1
    return a


def solve(n=10_000_000):
    # Inadmissible points: (a^2, b^2) with a^2 + b^2 a perfect square -> Pythagorean leg pairs.
    S = math.isqrt(n)
    A = np.arange(1, S + 1, dtype=np.int64)
    s = A[:, None] ** 2 + A[None, :] ** 2
    r = np.sqrt(s.astype(np.float64)).astype(np.int64)
    ok = (r * r == s) | ((r + 1) * (r + 1) == s)
    ai, bi = np.nonzero(ok)
    xs = (A[ai] ** 2).astype(np.int64)
    ys = (A[bi] ** 2).astype(np.int64)

    # Factorials and inverse factorials up to 2n via vectorized prefix products.
    N = 2 * n
    fact = np.ones(N + 1, dtype=np.int64)
    fact[1:] = np.arange(1, N + 1, dtype=np.int64)
    prefix_prod_mod(fact)
    suf = np.ones(N + 1, dtype=np.int64)
    suf[1:] = np.arange(N, 0, -1, dtype=np.int64)
    prefix_prod_mod(suf)  # suf[m] = N*(N-1)*...*(N-m+1)
    # inv_fact[i] = inv(N!) * prod(i+1..N) = inv(i!)
    inv_fact = suf[::-1] * pow(int(fact[N]), MOD - 2, MOD) % MOD

    def binom(m, k):
        # vectorized binomial C(m, k) mod p
        return fact[m] * inv_fact[k] % MOD * inv_fact[m - k] % MOD

    # Sort bad points by coordinate sum; f[i] = #paths (0,0)->p_i avoiding earlier bad points.
    order = np.argsort(xs + ys, kind="stable")
    xs, ys = xs[order], ys[order]
    k = len(xs)
    f = np.zeros(k, dtype=np.int64)
    for i in range(k):
        x, y = int(xs[i]), int(ys[i])
        total = int(binom(x + y, x))
        if i:
            dx = x - xs[:i]
            dy = y - ys[:i]
            m = (dx >= 0) & (dy >= 0)
            if m.any():
                dxm, dym = dx[m], dy[m]
                ways = fact[dxm + dym] * inv_fact[dxm] % MOD * inv_fact[dym] % MOD
                total -= int((f[:i][m] * ways % MOD).sum() % MOD)
        f[i] = total % MOD

    # Subtract paths passing through their first bad point.
    ans = int(binom(2 * n, n))
    dx = n - xs
    dy = n - ys
    ways = fact[dx + dy] * inv_fact[dx] % MOD * inv_fact[dy] % MOD
    ans -= int((f * ways % MOD).sum() % MOD)
    return ans % MOD


if __name__ == "__main__":
    print(solve())
