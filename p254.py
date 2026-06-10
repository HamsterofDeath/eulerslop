#!/usr/bin/env python3
import numpy as np
from math import factorial

# f(n) = sum of factorials of digits of n;  sf(n) = digitsum(f(n));
# g(i) = smallest n with sf(n) = i;  sg(i) = digitsum(g(i)).
#
# For a target value F = f(n), the smallest n is the "canonical" one: write
# F = a9*9! + t with t in [0, 9!) and t = sum_{k=1..8} a_k*k!, 0 <= a_k <= k
# (unique factorial-base form); then n's digits are a_1 ones, ..., a_8 eights,
# a_9 nines in ascending order.  (Any representation violating a_k <= k can be
# shortened by k+1 copies of k! -> (k+1)!, and digit 0 never helps.)
#
# So g(i) = best over F with digitsum(F) = i, where "best" minimizes the
# number of digits a9 + s(t) (s(t) = sum a_k), then the digit string.
# Writing X = a9*362880 = H*10^6 + L, every F in [X, X+362880) is H'|v with
# 6-digit tail v, so digitsum(F) = ds(H) + ds6(v) (or carry: ds(H+1)+ds6(v-10^6)).
# For each a9 we look up tails v with the required digit sum from precomputed
# per-digit-sum sorted lists and pick t = v - L minimizing (s(t), digits(t)).
# a9 is scanned from a lower bound (from the smallest number with digit sum i)
# while a9 <= best total length, which is exhaustive.

FACT = [factorial(k) for k in range(10)]
NF = 362880  # 9!

def tdigits(t):
    # canonical factorial-base digits of t < 9!, as ascending digit string
    out = []
    for k in range(8, 0, -1):
        a, t = divmod(t, FACT[k])
        out.append(str(k) * a)
    return "".join(reversed(out))

def solve():
    # digit sums of all 6-digit tails
    v = np.arange(10 ** 6, dtype=np.int64)
    ds6 = np.zeros(10 ** 6, dtype=np.int8)
    x = v.copy()
    for _ in range(6):
        ds6 += (x % 10).astype(np.int8)
        x //= 10
    by_ds = {j: np.flatnonzero(ds6 == j) for j in range(55)}  # sorted asc

    # s(t) = number of digits of canonical representation of t < 9!
    t = np.arange(NF, dtype=np.int64)
    s_arr = np.zeros(NF, dtype=np.int8)
    rem = t.copy()
    for k in range(8, 0, -1):
        s_arr += (rem // FACT[k]).astype(np.int8)
        rem %= FACT[k]

    dsint = lambda x: sum(map(int, str(x)))

    total = 0
    for i in range(1, 151):
        # smallest number with digit sum i -> lower bound for F, hence for a9
        q9, r9 = divmod(i, 9)
        minF = int(("" if r9 == 0 else str(r9)) + "9" * q9)
        a9 = a9_start = max(0, -(-(minF - (NF - 1)) // NF))
        best = None  # (total_len, tstr, a9, s)
        while best is None or a9 <= best[0]:
            X = a9 * NF
            H, L = divmod(X, 10 ** 6)
            cand_t = []
            j1 = i - dsint(H)
            if 0 <= j1 <= 54:
                arr = by_ds[j1]
                a = np.searchsorted(arr, L, side="left")
                b = np.searchsorted(arr, min(10 ** 6 - 1, L + NF - 1), side="right")
                if b > a:
                    cand_t.append(arr[a:b] - L)
            if L + NF - 1 >= 10 ** 6:
                j2 = i - dsint(H + 1)
                if 0 <= j2 <= 54:
                    arr = by_ds[j2]
                    b = np.searchsorted(arr, L + NF - 1 - 10 ** 6, side="right")
                    if b > 0:
                        cand_t.append(arr[:b] + (10 ** 6 - L))
            if cand_t:
                ts = np.concatenate(cand_t)
                if a9 == 0:
                    ts = ts[ts > 0]  # n must be a positive integer
                if ts.size:
                    sv = s_arr[ts]
                    smin = int(sv.min())
                    tstr = min(tdigits(int(tt)) for tt in ts[sv == smin])
                    length = a9 + smin
                    if best is None or length < best[0] or (
                        length == best[0]
                        and tstr.ljust(len(best[1]) + 1, "9")
                        < best[1].ljust(len(tstr) + 1, "9")
                    ):
                        best = (length, tstr, a9, smin)
            a9 += 1
            assert a9 - a9_start < 10 ** 7, "search runaway"
        total += sum(map(int, best[1])) + 9 * best[2]
    return total

if __name__ == "__main__":
    print(solve())
