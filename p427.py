import numpy as np

MOD = 1_000_000_009


def _pow_table(base, length, p):
    # arr[e] = base^e mod p for e in [0, length), built by doubling.
    arr = np.ones(1, dtype=np.int64)
    cur = base % p
    while arr.size < length:
        arr = np.concatenate([arr, arr * cur % p])
        cur = cur * cur % p
    return arr[:length]


def f_mod(n, p=MOD):
    # f(n) = sum over n-sequences of longest-run length
    #      = sum_{t=1..n} #{L(S) >= t} = n*n^n - sum_{k=0}^{n-1} A_k,
    # where A_k = #sequences whose maximal runs all have length <= k.
    # A run structure with m runs contributes n*(n-1)^(m-1) sequences, run
    # lengths forming a composition of n into m parts in [1,k].  Summing the
    # geometric series over m gives A_k = n*([z^(n-1)] - [z^(n-1-k)]) of
    # 1/(1 - n z + (n-1) z^(k+1)), and
    #   [z^e] = sum_{j>=0, e-jk>=j} (-1)^j C(e-jk, j) (n-1)^j n^(e-j(k+1)).
    # Total work over all k is O(n log n) terms, vectorized with numpy.
    if n == 1:
        return 1 % p

    # factorials and inverse factorials up to n-1
    fact = np.empty(n, dtype=np.int64)
    f = 1
    fact[0] = 1
    for i in range(1, n):
        f = f * i % p
        fact[i] = f
    inv_fact = np.empty(n, dtype=np.int64)
    inv = pow(f, p - 2, p)
    inv_fact[n - 1] = inv
    for i in range(n - 1, 0, -1):
        inv = inv * i % p
        inv_fact[i - 1] = inv

    powN = _pow_table(n, n, p)              # n^e, e < n
    jmax_all = (n - 1) // 2                 # j(k+1) <= n-1 with k >= 1
    pw1 = _pow_table(n - 1, jmax_all + 1, p)

    B = max(1, int(n ** 0.5))
    s1 = 0  # sum over j>=1, k>=1 of T1(k,j)   (the [z^(n-1)] terms)
    s2 = 0  # sum over j>=1, k>=1 of T2(k,j)   (the [z^(n-1-k)] terms)

    def block(m, j):
        # sum of C(m, j) * n^(m-j) elementwise (values already validated m>=j)
        v = fact[m] * inv_fact[m - j] % p
        v = v * powN[m - j] % p
        return v

    # small j: vectorize over k
    for j in range(1, min(B, jmax_all) + 1):
        coef = pw1[j] * int(inv_fact[j]) % p
        sgn = -1 if j & 1 else 1
        k1 = (n - 1 - j) // j               # T1 needs n-1-jk >= j
        if k1 >= 1:
            k = np.arange(1, k1 + 1, dtype=np.int64)
            t = int(block(n - 1 - j * k, j).sum() % p)
            s1 += sgn * coef * t % p
        k2 = (n - 1 - j) // (j + 1)         # T2 needs n-1-k(j+1) >= j
        if k2 >= 1:
            k = np.arange(1, k2 + 1, dtype=np.int64)
            t = int(block(n - 1 - (j + 1) * k, j).sum() % p)
            s2 += sgn * coef * t % p

    # large j (> B): vectorize over j for each small k
    k = 1
    while (n - 1) // (k + 1) > B:
        jhi1 = (n - 1) // (k + 1)           # T1: j(k+1) <= n-1
        j = np.arange(B + 1, jhi1 + 1, dtype=np.int64)
        v = block(n - 1 - j * k, j) * pw1[j] % p
        v = v * inv_fact[j] % p
        v = np.where(j & 1 == 1, p - v, v)
        s1 += int(v.sum() % p)
        jhi2 = (n - 1 - k) // (k + 1)       # T2: j(k+1) <= n-1-k
        if jhi2 > B:
            j = np.arange(B + 1, jhi2 + 1, dtype=np.int64)
            v = block(n - 1 - k - j * k, j) * pw1[j] % p
            v = v * inv_fact[j] % p
            v = np.where(j & 1 == 1, p - v, v)
            s2 += int(v.sum() % p)
        k += 1

    # j = 0 contributions
    s1 = (s1 + (n - 1) * int(powN[n - 1])) % p
    s2 = (s2 + int(powN[: n - 1].sum() % p)) % p

    sum_A = n % p * ((s1 - s2) % p) % p     # sum_{k=1}^{n-1} A_k (A_0 = 0)
    return (pow(n, n + 1, p) - sum_A) % p


def solve():
    return f_mod(7_500_000)


if __name__ == "__main__":
    print(solve())
