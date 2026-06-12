#!/usr/bin/env python3
import numpy as np

def solve():
    # Valid numberings of the gnomon L(m,n) are linear extensions of its cell
    # poset.  Rotating the constraints (value < cell below, value < cell left)
    # turns the gnomon into the straight Young diagram
    #   lambda = (m repeated k times, k repeated n times),  k = m - n,
    # so LC(m,n) is the number of standard Young tableaux of lambda:
    #   LC = T! / prod(hook lengths),  T = m^2 - n^2  (hook length formula).
    # Validated: LC(3,0)=42, LC(5,3)=250250, LC(6,3)=406029023400,
    # LC(10,5) mod 76543217 = 61251715.
    MOD = 76543217  # prime, and MOD > T so T! has no factor of MOD
    m, n = 10000, 5000
    k = m - n
    T = m * m - n * n

    # Hook lengths come row-wise as two arithmetic runs of step 1:
    #   row i <= k:   j=1..k   -> hooks (m+n+1-i .. 2m-i)
    #                 j=k+1..m -> hooks (k-i+1 .. m-i)
    #   row i  > k:   j=1..k   -> hooks (m+1-i .. m+k-i)
    # Multiply each run via prefix factorials mod MOD (all hooks <= 2m-1 < MOD).
    H = 2 * m
    fact = [1] * (H + 1)
    for i in range(1, H + 1):
        fact[i] = fact[i - 1] * i % MOD
    hooks_num = 1
    hooks_den = 1
    for i in range(1, k + 1):
        hooks_num = hooks_num * fact[2 * m - i] % MOD * fact[m - i] % MOD
        hooks_den = hooks_den * fact[m + n - i] % MOD * fact[k - i] % MOD
    for i in range(k + 1, m + 1):
        hooks_num = hooks_num * fact[m + k - i] % MOD
        hooks_den = hooks_den * fact[m - i] % MOD
    hooks = hooks_num * pow(hooks_den, MOD - 2, MOD) % MOD

    # T! mod MOD via chunked numpy pairwise-product reduction (values < MOD
    # ~ 2^27, so pairwise products fit easily in uint64).
    res = 1
    CHUNK = 8_000_000
    x = 1
    while x <= T:
        hi = min(x + CHUNK, T + 1)
        arr = np.arange(x, hi, dtype=np.uint64)
        while arr.size > 1:
            if arr.size & 1:
                res = res * int(arr[-1]) % MOD
                arr = arr[:-1]
            arr = arr[0::2] * arr[1::2] % MOD
        res = res * int(arr[0]) % MOD
        x = hi

    return res * pow(hooks, MOD - 2, MOD) % MOD

if __name__ == "__main__":
    print(solve())
