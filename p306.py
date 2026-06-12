#!/usr/bin/env python3

def solve():
    # Painting two contiguous white squares splits a strip of n into strips of
    # sizes i and n-2-i, so this is the octal game 0.07.  Its Sprague-Grundy
    # values g(n) satisfy g(n) = mex{ g(i) XOR g(n-2-i) : 0 <= i <= n-2 } and
    # are known to become periodic.  We compute g up to a few thousand, detect
    # the period, then count the n <= 10^6 with g(n) != 0 (first-player wins).
    M = 1000000
    N = 3000
    g = [0] * (N + 1)
    for n in range(2, N + 1):
        seen = set()
        for i in range((n - 2) // 2 + 1):  # i and n-2-i give the same XOR
            seen.add(g[i] ^ g[n - 2 - i])
        m = 0
        while m in seen:
            m += 1
        g[n] = m

    # Detect the eventual period starting from a safe offset s.
    s = 200
    period = None
    for cand in range(1, 1001):
        if all(g[n] == g[n + cand] for n in range(s, N - cand + 1)):
            period = cand
            break
    assert period is not None

    # Count losing positions (g == 0) among 1..M.
    losing = sum(1 for n in range(1, N + 1) if g[n] == 0)
    # Offsets r in [0, period) with g(s + r) == 0; positions n > N with
    # (n - s) % period == r are also losing.
    zero_offsets = [r for r in range(period) if g[s + r] == 0]
    for r in zero_offsets:
        # count n in (N, M] with n ≡ s + r (mod period)
        first = N + 1 + ((s + r - (N + 1)) % period)
        if first <= M:
            losing += (M - first) // period + 1
    return M - losing

if __name__ == "__main__":
    print(solve())
