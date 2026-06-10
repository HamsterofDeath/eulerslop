#!/usr/bin/env python3

def T(n):
    """Sum of all balanced numbers below 10^n (exact)."""
    # A k-digit number is balanced if its first ceil(k/2) digits sum to the
    # same value as its last ceil(k/2) digits.  For odd k the middle digit
    # belongs to both halves, so it cancels: the outer (k-1)/2 digits on each
    # side must have equal sums and the middle digit is free.
    #
    # DP over m-digit strings, keyed by digit sum s:
    #   cnt_f[s], val_f[s]: count / total numeric value of strings with any
    #                       digits (suffixes, leading zeros allowed)
    #   cnt_l[s], val_l[s]: same but first digit 1-9 (prefixes)
    max_m = n // 2  # longest half length needed (excluding middle digit)

    total = 9 * 10 // 2 if n >= 1 else 0  # k = 1: digits 1..9 are balanced

    # m = 1 base case
    cnt_f = {d: 1 for d in range(10)}
    val_f = {d: d for d in range(10)}
    cnt_l = {d: 1 for d in range(1, 10)}
    val_l = {d: d for d in range(1, 10)}

    for m in range(1, max_m + 1):
        # even length k = 2m: number = A * 10^m + B, sum(A) = sum(B)
        if 2 * m <= n:
            p = 10 ** m
            for s, c in cnt_l.items():
                if s in cnt_f:
                    total += val_l[s] * p * cnt_f[s] + c * val_f[s]
        # odd length k = 2m + 1: number = A * 10^(m+1) + d * 10^m + B,
        # sum(A) = sum(B), middle digit d in 0..9 free
        if 2 * m + 1 <= n:
            p = 10 ** m
            for s, c in cnt_l.items():
                if s in cnt_f:
                    total += (10 * val_l[s] * 10 * p * cnt_f[s]
                              + c * cnt_f[s] * 45 * p
                              + c * 10 * val_f[s])
        # extend halves by one digit (append on the right)
        if m < max_m:
            ncf, nvf, ncl, nvl = {}, {}, {}, {}
            for s, c in cnt_f.items():
                v = val_f[s]
                for d in range(10):
                    t = s + d
                    ncf[t] = ncf.get(t, 0) + c
                    nvf[t] = nvf.get(t, 0) + v * 10 + d * c
            for s, c in cnt_l.items():
                v = val_l[s]
                for d in range(10):
                    t = s + d
                    ncl[t] = ncl.get(t, 0) + c
                    nvl[t] = nvl.get(t, 0) + v * 10 + d * c
            cnt_f, val_f, cnt_l, val_l = ncf, nvf, ncl, nvl

    return total

def solve():
    assert T(1) == 45
    assert T(2) == 540
    assert T(5) == 334795890
    return T(47) % 3 ** 15

if __name__ == "__main__":
    print(solve())
