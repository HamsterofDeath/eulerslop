#!/usr/bin/env python3
import numpy as np


def game_M(n):
    # Direct game simulation (used only to verify the fast method for small n).
    # Positions are indices k with counter c = s_k; a move goes to j > k with
    # s_j - s_k <= n.  The first terminal (no-move) position is T = 2^(n+1)-2,
    # since popcount(2^(n+1)-1) = n+1 > n.  Move windows are contiguous, so any
    # position that could jump past T can also land on T; hence win/lose values
    # below T are exact by backward induction up to T.
    T = (1 << (n + 1)) - 2
    s = [0]
    for i in range(1, T + 2):
        s.append(s[-1] + i.bit_count())
    lose = bytearray(T + 1)
    for k in range(T, -1, -1):
        j = k + 1
        v = 1                       # losing unless some move reaches a losing pos
        while j <= T and s[j] - s[k] <= n:
            if lose[j]:
                v = 0
                break
            j += 1
        lose[k] = v
    # M(n) = largest first move d = s_j <= n landing on a losing position
    return max((s[j] for j in range(1, T + 1) if s[j] <= n and lose[j]),
               default=0)


def make_fast_M():
    # Exact fast computation of M(n), derived as follows:
    # 1) Losing positions form a single chain down from T: since move windows
    #    are contiguous, k is losing iff it cannot reach the next losing
    #    position above, i.e. the next losing k' below b is max{k : s_k < s_b - n}.
    #    M(n) is the bottom chain value (the unique losing c in [0, n]).
    # 2) Walking the chain down from T consumes descending integers k in greedy
    #    blocks whose popcount sum just exceeds n; M(n) is the leftover sum.
    # 3) Substituting x = 2^(n+1)-1-k (bit complement, pop(k) = N - pop(x) with
    #    N = n+1) turns this into an ascending renewal over all N-bit x:
    #        c += N - pop(x); if c >= N: c = 0
    #    for x = 0..2^N-1, starting c = 0; M(n) is the final carry.
    # 4) That renewal is evaluated by composing block-crossing maps:
    #    cross(j,k) = carry map of a block of 2^k numbers whose high prefix has
    #    popcount j; cross(j,k) = cross(j+1,k-1) o cross(j,k-1), with the level-0
    #    map c -> 0 if c >= j else c + N - j.  For large n only the final block
    #    matters: if the map of the last 2^K numbers is a constant map (the carry
    #    is "erased" by resets), M(n) is that constant, independent of the carry
    #    entering the block -- verified, with fallback to the full exact triangle.
    def triangle(N, jlo, K):
        c = np.arange(N, dtype=np.int32)
        j = (jlo + np.arange(K + 1, dtype=np.int32))[:, None]
        A = np.where(c[None, :] >= j, 0, c[None, :] + N - j)
        for _ in range(K):
            A = np.take_along_axis(A[1:], A[:-1], axis=1)
        return A[0]

    def M(n, K0=32):
        N = n + 1
        if N <= 2 * K0:
            return int(triangle(N, 0, N)[0])      # full range, entry carry 0
        K = K0
        while True:
            F = triangle(N, N - K, K)             # map of the final 2^K numbers
            if K == N or (F == F[0]).all():       # full range / carry erasure
                return int(F[0])
            K = min(2 * K, N)
    return M


def solve():
    fast_M = make_fast_M()
    # verify the fast method against genuine game simulation for small n
    for n in range(1, 15):
        assert fast_M(n) == game_M(n), n
    # statement checks: M(2)=2, M(7)=1, M(20)=4, sum_{1..20} M^3 = 8150
    assert fast_M(2) == 2 and fast_M(7) == 1 and fast_M(20) == 4
    assert sum(fast_M(n) ** 3 for n in range(1, 21)) == 8150
    return sum(fast_M(n) ** 3 for n in range(1, 1001))


if __name__ == "__main__":
    print(solve())
