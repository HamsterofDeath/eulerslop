#!/usr/bin/env python3
import numpy as np
from math import comb

def solve():
    # Silver dollar game.  Empirically (verified by brute force up to 7
    # coins, and against W(10,2)=324, W(100,10)=1514704946113500):
    # for an odd number C of coins at x_1 < ... < x_C, with gaps
    # g_0 = x_1 - 1, g_i = x_{i+1} - x_i - 1, a position is LOSING for the
    # player to move iff the dollar is not at x_1 and
    #     h_0 XOR g_2 XOR g_4 XOR ... XOR g_{C-1} = 0,
    # where the heaps pair the coins from the right ((x_C,x_{C-1}), ...,
    # (x_3,x_2)) and the leftmost coin plays against the bag:
    #     h_0 = g_0      if the dollar is at x_2,
    #     h_0 = g_0 + 1  if the dollar is at x_3..x_C.
    #
    # Counting losing positions on n squares: S = n - C empty squares are
    # split into K = (C+1)/2 heap gaps, (C-1)/2 free odd gaps and the slack
    # right of x_C (R = K free dimensions, exact sum S).  With
    # N_k(t) = #(k-tuples of nonneg ints, XOR 0, sum t):
    #   dollar at x_2:        sum_t N_K(t) * C(S-t+R-1, R-1)
    #   dollar at x_3..x_C:   (C-2) * sum_t (N_K(t)-N_{K-1}(t))
    #                                  * C(S+1-t+R-1, R-1)
    # (substituting h_0 = g_0 + 1 >= 1 frees one extra empty square).
    # W(n,c) = C(n, c+1)*(c+1) - losing.
    #
    # N_k comes from the bitwise product  prod_b sum_j C(k,2j) y^(2j*2^b)
    # (each bit is set in an even number of heaps), done as array
    # convolutions mod each prime factor of the semiprime modulus
    # (values < 2^20 keep all int64 products safe), then CRT.
    P1, P2 = 1000003, 1000033
    MOD = P1 * P2

    def N_array(k, length, p):
        # N_k(t) mod p for t = 0..length-1
        arr = np.zeros(length, dtype=np.int64)
        arr[0] = 1
        b = 0
        while (2 << b) < length:
            out = arr.copy()
            for j in range(1, k // 2 + 1):
                shift = (2 * j) << b
                if shift >= length:
                    break
                cj = comb(k, 2 * j) % p
                out[shift:] = (out[shift:] + cj * arr[:length - shift]) % p
            arr = out
            b += 1
        return arr

    def W_mod(n, C, p):
        S = n - C
        K = (C + 1) // 2
        R = K
        L = S + 2                       # need t = 0..S+1
        nK = N_array(K, L, p)
        nK1 = N_array(K - 1, L, p)
        # weights wt[u] = C(u + R - 1, R - 1) mod p for u = 0..S+1
        u = np.arange(L, dtype=np.int64)
        wt = np.full(L, pow(1, 1), dtype=np.int64)
        for i in range(1, R):
            wt = wt * ((u + i) % p) % p
        fact = 1
        for i in range(2, R):
            fact = fact * i % p
        wt = wt * pow(fact, p - 2, p) % p
        # dollar at x_2: t = 0..S
        losing = int(np.dot(nK[:S + 1], wt[S::-1]) % p)
        # dollar at x_3..x_C: t = 0..S+1
        diff = (nK - nK1) % p
        losing = (losing + (C - 2) * int(np.dot(diff, wt[::-1]) % p)) % p
        total = comb(n, C) * C % p
        return (total - losing) % p

    def W(n, C):
        w1, w2 = W_mod(n, C, P1), W_mod(n, C, P2)
        return (w1 + P1 * ((w2 - w1) * pow(P1, -1, P2) % P2)) % MOD

    assert W(10, 3) == 324
    assert W(100, 11) == 1514704946113500 % MOD
    return W(10 ** 6, 101)

if __name__ == "__main__":
    print(solve())
