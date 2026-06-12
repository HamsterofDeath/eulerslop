import math
import numpy as np

MOD = 10**9


def _pyramidal_mod(x):
    """Sum of squares 1^2+...+x^2 = x(x+1)(2x+1)/6, mod MOD, vectorized.

    6 is not invertible mod 10^9, so divide the factors exactly instead:
    one of x, x+1 is even; one of x, x+1, 2x+1 is divisible by 3
    (x%3==0 -> x, x%3==2 -> x+1, x%3==1 -> 2x+1).
    """
    a = x.copy()
    b = x + 1
    c = 2 * x + 1
    even = (a & 1) == 0
    a[even] >>= 1
    b[~even] >>= 1
    m3 = x % 3
    s0 = m3 == 0
    s2 = m3 == 2
    s1 = ~(s0 | s2)
    a[s0] //= 3
    b[s2] //= 3
    c[s1] //= 3
    r = (a % MOD) * (b % MOD) % MOD
    return r * (c % MOD) % MOD


def solve(N=10**15):
    # SIGMA_2(N) = sum_{d=1}^{N} sigma_2 contributions = sum_{d=1}^{N} d^2 * floor(N/d)
    # (each d is counted as a divisor of its floor(N/d) multiples).
    # Split at K = isqrt(N): small d directly, large d grouped by quotient
    # q = floor(N/d), where d ranges over (max(K, N//(q+1)), N//q] and the
    # d^2 block sum comes from the square-pyramidal closed form.
    K = math.isqrt(N)
    total = 0
    CH = 1 << 22

    # Part 1: d = 1..K
    for lo in range(1, K + 1, CH):
        d = np.arange(lo, min(lo + CH, K + 1), dtype=np.int64)
        t = (d * d % MOD) * ((N // d) % MOD) % MOD
        total += int(t.sum())

    # Part 2: d > K, grouped by quotient q = floor(N/d) which runs 1..N//(K+1)
    Q = N // (K + 1)
    for lo in range(1, Q + 1, CH):
        qs = np.arange(lo, min(lo + CH, Q + 1), dtype=np.int64)
        hi = N // qs
        lo_d = np.maximum(K, N // (qs + 1))
        block = (_pyramidal_mod(hi) - _pyramidal_mod(lo_d)) % MOD
        t = (qs % MOD) * block % MOD
        total += int(t.sum())

    return total % MOD


if __name__ == "__main__":
    print(solve())
