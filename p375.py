#!/usr/bin/env python3

def solve():
    # S_{n+1} = S_n^2 mod 50515093 is eventually periodic. Detect the cycle
    # (it turns out S_1, S_2, ... is purely periodic with period ~6.3M).
    #
    # Let G(j) = sum_{i<=j} min(S_i..S_j), so M(N) = sum_{j<=N} G(j).
    # G is maintained with a monotonic stack of (value, count): pushing S_j
    # pops all entries >= S_j and merges their counts, and G changes by
    # S_j * merged_count - sum(popped value*count).
    #
    # Once j passes the first occurrence p1c of the cycle minimum vmin, the
    # bottom stack entry is pinned at vmin and everything above it depends
    # only on the values since the last occurrence of vmin, which repeat with
    # period lam. Hence G(j + lam) = G(j) + vmin * lam for all j >= p1c, and
    # the tail of the sum collapses to arithmetic series.
    MOD = 50515093
    N = 2_000_000_000

    # cycle detection, storing the sequence S_1..S_{mu+lam-1}
    s = 290797
    pos = {}
    seq = []
    j = 0
    while True:
        s = s * s % MOD
        j += 1
        if s in pos:
            mu = pos[s]            # S_j for j >= mu repeats with period lam
            lam = j - pos[s]
            break
        pos[s] = j
        seq.append(s)
    del pos

    cyc_min = min(seq[mu - 1:])
    p1c = seq.index(cyc_min) + 1   # first index achieving the cycle minimum
    B = p1c
    q, r = divmod(N - B, lam)

    # simulate G(j) for j = 1..B+lam, accumulating
    #   sum1  = sum of G(j) for j <= B
    #   s_all = sum of G(B+a) for a = 1..lam
    #   s_r   = sum of G(B+a) for a = 1..r
    vs, cs = [], []  # monotonic stack: values (increasing) and run counts
    G = 0
    sum1 = s_all = s_r = 0
    top = mu + lam - 1
    for j in range(1, B + lam + 1):
        v = seq[j - 1] if j <= top else seq[mu + (j - mu) % lam - 1]
        acc = 1
        while vs and vs[-1] >= v:
            pv = vs.pop()
            pc = cs.pop()
            G -= pv * pc
            acc += pc
        vs.append(v)
        cs.append(acc)
        G += v * acc
        if j <= B:
            sum1 += G
        else:
            s_all += G
            if j - B <= r:
                s_r += G

    # M(N) = sum1 + sum over a,m of G(B+a) + m*vmin*lam
    #   a <= r gets m = 0..q, a > r gets m = 0..q-1
    return (sum1 + q * s_all + s_r
            + cyc_min * lam * (r * q * (q + 1) // 2 + (lam - r) * q * (q - 1) // 2))

if __name__ == "__main__":
    print(solve())
