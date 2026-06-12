#!/usr/bin/env python3
import numpy as np
from math import isqrt

# Theory.  Let M(x,y)=1 if cell (x,y) is chosen an odd number of times.
# Cell (x,y) gets flipped R_y + C_x - M(x,y) times (R_y, C_x = number of
# chosen cells in row y / column x), which must equal B(x,y), the initial
# black configuration: B(x,y)=1 iff (N-1)^2 <= x^2+y^2 < N^2.
#
# Even N: the system forces the unique solution
#     M(x,y) = B(x,y) XOR p(x) XOR p(y),
# where p(t) = parity of the number of black cells in column t (= row t,
# B is symmetric).  So T(N) = popcount(M).  With k = #{t : p(t)=1}:
#     T(N) = 2k(N-k) + sum(B) - 2 * #{black cells with p(x) XOR p(y) = 1}.
#
# Odd N: solvable iff all rows/columns of B have the same parity; the
# solutions are M = B XOR u_y XOR v_x with parity(u) = parity(v).  Flipping
# t rows/columns toggles >= 2t(N-t) - small cells, while B has only ~1.6N
# black cells and each row/column holds at most ~sqrt(2N) of them, so for
# N >= 29 the minimum is u = v = 0, i.e. T(N) = sum(B).  Tiny odd N are
# minimised by brute force over u (with the best parity-consistent v).

CH = 1 << 21  # chunk of x values (multiple of 8 for bit packing)

def isqrt_np(v):
    # exact floor sqrt of an int64 array (values up to ~2^62)
    r = np.sqrt(v.astype(np.float64)).astype(np.int64)
    r -= (r * r > v)
    r -= (r * r > v)
    r += ((r + 1) * (r + 1) <= v)
    r += ((r + 1) * (r + 1) <= v)
    return r

def lohi(xs, N):
    # black cells in column x are y in [lo(x), hi(x)] (empty if lo > hi):
    # hi = max y with y^2 < N^2 - x^2 (capped at N-1), lo = ceil(sqrt((N-1)^2-x^2))
    hi = isqrt_np(N * N - 1 - xs * xs)
    np.minimum(hi, N - 1, out=hi)
    m = (N - 1) * (N - 1) - xs * xs
    s = isqrt_np(m)
    lo = np.where(s * s == m, s, s + 1)
    return lo, hi

def hi_scalar(x, N):
    return min(N - 1, isqrt(N * N - 1 - x * x))

def T_even(N):
    sumB = 0
    k = 0
    cross_upper = 0  # black cells with y > x and p(x) XOR p(y) = 1
    # packed bit array of p(t) for already-processed t (we go top-down,
    # and every black cell with y > x has its p(y) computed before x)
    packed = np.zeros(N // 8 + 1, dtype=np.uint8)
    xe = N
    while xe > 0:
        # pick chunk [xa, xe) keeping the spread of hi() below CH
        H = hi_scalar(xe - 1, N)
        t = H + CH
        m = N * N - 1 - t * (t + 2)
        if m <= 0:
            xa_min = 0
        else:
            s = isqrt(m)
            xa_min = s if s * s == m else s + 1
        xa = max(0, xe - CH, xa_min)
        xa -= xa % 8  # keep byte alignment
        xs = np.arange(xa, xe, dtype=np.int64)
        lo, hi = lohi(xs, N)
        cnt = hi - lo + 1  # >= 0 automatically (lo = hi+1 when empty)
        px = (cnt & 1).astype(np.uint8)
        sumB += int(cnt.sum())
        k += int(px.sum())
        # store p bits for this chunk; xa is a multiple of 8, and only the
        # topmost chunk can end unaligned (its zero padding lies beyond N-1)
        packed[xa // 8: xa // 8 + (len(px) + 7) // 8] = np.packbits(px)
        # black cells strictly above the diagonal: y in [max(lo,x+1), hi]
        q_lo = np.maximum(lo, xs + 1)
        np.minimum(q_lo, hi + 1, out=q_lo)  # clamp empty runs
        length = hi - q_lo + 1
        if int(length.max()) > 0:
            wlo = int(q_lo.min())
            whi = int(hi.max())
            wbits = np.unpackbits(packed[wlo // 8: whi // 8 + 1])
            off = wlo - 8 * (wlo // 8)
            wbits = wbits[off: off + (whi - wlo + 1)]
            Pw = np.zeros(whi - wlo + 2, dtype=np.int64)
            Pw[1:] = np.cumsum(wbits, dtype=np.int64)
            ones = Pw[hi + 1 - wlo] - Pw[q_lo - wlo]
            contrib = np.where(px == 1, length - ones, ones)
            cross_upper += int(np.where(length > 0, contrib, 0).sum())
        xe = xa
    cross = 2 * cross_upper  # B is symmetric; diagonal black cells give 0
    return 2 * k * (N - k) + sumB - 2 * cross

def T_odd(N):
    # solvable only if every column parity equals cnt(0) = 1 (odd);
    # cheap necessary test first: column N-1 holds isqrt(2N-2)+1 cells
    if (isqrt(2 * N - 2) + 1) % 2 == 0:
        return 0
    sumB = 0
    for xa in range(0, N, CH):
        xs = np.arange(xa, min(N, xa + CH), dtype=np.int64)
        lo, hi = lohi(xs, N)
        cnt = hi - lo + 1
        if int(((cnt & 1) == 0).sum()) > 0:
            return 0
        sumB += int(cnt.sum())
    if N > 24:
        return sumB  # u = v = 0 is optimal (see header note)
    # brute force tiny odd boards: minimise sum(B xor u_y xor v_x)
    xs = np.arange(N, dtype=np.int64)
    lo, hi = lohi(xs, N)
    B = ((np.arange(N)[None, :] >= lo[:, None]) &
         (np.arange(N)[None, :] <= hi[:, None])).astype(np.int64)
    best = None
    for u in range(1 << N):
        ub = (u >> np.arange(N)) & 1
        Bp = B ^ ub[None, :]
        ones = Bp.sum(axis=1)
        v = (N - ones < ones).astype(np.int64)
        cost = int(np.minimum(ones, N - ones).sum())
        if (int(v.sum()) & 1) != (int(ub.sum()) & 1):
            cost += int(np.abs(N - 2 * ones).min())
        if best is None or cost < best:
            best = cost
    return best

def solve():
    assert T_even(10) == 29 and T_even(1000) == 395253  # given values
    total = 0
    for i in range(3, 32):
        N = (1 << i) - i
        total += T_even(N) if N % 2 == 0 else T_odd(N)
    return total

if __name__ == "__main__":
    print(solve())
