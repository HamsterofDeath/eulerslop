#!/usr/bin/env python3

def count_le(M, k):
    # Count m in [1, M] with m not divisible by 5 and carries5(m + m) <= k,
    # where carries5 counts the carries when adding m + m in base 5
    # (including a final carry out of the top digit).
    #
    # Digit DP over base-5 digits of m, least significant first.
    # State: (carry into next digit, number of carries so far (capped),
    #         flag "suffix of m <= suffix of M as numbers").
    if M < 1:
        return 0
    digs = []
    t = M
    while t:
        digs.append(t % 5)
        t //= 5
    cap = k + 1  # cap carry counts; anything > k is a fail bucket
    # dp[(carry, ncar, le_flag)] = count
    dp = {(0, 0, 1): 1}
    for p, b in enumerate(digs):
        ndp = {}
        lo = 1 if p == 0 else 0  # least significant digit nonzero (5 does not divide m)
        for (c, nc, f), w in dp.items():
            for a in range(lo, 5):
                tot = 2 * a + c
                cout = 1 if tot >= 5 else 0
                nc2 = min(nc + cout, cap)
                f2 = 1 if (a < b or (a == b and f)) else 0
                key = (cout, nc2, f2)
                ndp[key] = ndp.get(key, 0) + w
        dp = ndp
    # The carry out of the top digit was already counted when it was emitted.
    return sum(w for (c, nc, f), w in dp.items() if f and nc <= k)

def solve():
    # f5(m!) = (m - s5(m)) / 4 by Legendre, with s5 the base-5 digit sum.
    # The condition f5((2i-1)!) < 2 f5(i!) simplifies to s5(2i-1) >= 2 s5(i).
    # Writing s5(2i) = 2 s5(i) - 4c (c = carries when adding i+i in base 5)
    # and s5(2i-1) = s5(2i) - 1 + 4t (t = v5(2i) = v5(i), borrowing through
    # the t trailing zeros), the condition becomes 4(t - c) >= 1, i.e. t > c.
    #
    # So count i <= N with v5(i) > carries5(i + i). Split off the trailing
    # zeros: i = 5^t * m with 5 not dividing m; doubling the trailing zeros
    # produces no carries, so carries5(i+i) = carries5(m+m) and we need
    # carries5(m+m) <= t - 1 with m <= N / 5^t. Sum a digit DP over t >= 1.
    N = 10 ** 18
    total = 0
    t = 1
    while 5 ** t <= N:
        total += count_le(N // 5 ** t, t - 1)
        t += 1
    return total

if __name__ == "__main__":
    print(solve())
