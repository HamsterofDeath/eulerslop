#!/usr/bin/env python3

def solve():
    # A list with gcd d and lcm l corresponds bijectively (divide by d) to a
    # list with gcd 1 and lcm m = l/d.  Let h(m) be the number of size-N lists
    # with gcd exactly 1 and lcm exactly m.  Then
    #   f(G, L, N) = sum_{m <= L/G} h(m) * #{d : d >= G, d*m <= L}
    #              = sum_{m <= L/G} h(m) * (floor(L/m) - G + 1).
    # h is multiplicative: for p^e || m the N exponents lie in [0, e] with
    # min 0 and max e, giving (e+1)^N - 2*e^N + (e-1)^N choices per prime.
    G = 10 ** 6
    L = 10 ** 12
    N = 10 ** 18
    MOD = 101 ** 4

    M = L // G  # = 10^6, the largest possible lcm/gcd ratio

    # per-exponent factor c[e] = (e+1)^N - 2*e^N + (e-1)^N (mod MOD)
    maxe = M.bit_length()  # 2^e <= M
    powN = [pow(k, N, MOD) for k in range(maxe + 3)]
    c = [1] + [(powN[e + 1] - 2 * powN[e] + powN[e - 1]) % MOD
               for e in range(1, maxe + 1)]

    # smallest prime factor sieve up to M
    spf = list(range(M + 1))
    for i in range(2, int(M ** 0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, M + 1, i):
                if spf[j] == j:
                    spf[j] = i

    # h(m) computed multiplicatively via the spf decomposition
    h = [0] * (M + 1)
    h[1] = 1
    for m in range(2, M + 1):
        p = spf[m]
        rest = m // p
        e = 1
        while rest % p == 0:
            rest //= p
            e += 1
        h[m] = h[rest] * c[e] % MOD

    total = 0
    for m in range(1, M + 1):
        total += h[m] * ((L // m - G + 1) % MOD)
    return total % MOD

if __name__ == "__main__":
    print(solve())
