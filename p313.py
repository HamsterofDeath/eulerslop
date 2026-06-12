#!/usr/bin/env python3

def solve():
    # Sliding game: red counter goes from top-left to bottom-right, blank
    # starts bottom-right. BFS over states (red_pos, blank_pos) on all grids
    # with 2 <= m, n <= 8 reveals the exact pattern (verified below):
    #   S(m,n) = 6*max(m,n) + 2*min(m,n) - 13   for m != n
    #   S(n,n) = 8*n - 11                        (extra cost on the diagonal)
    # Intuition: the blank walks to the far side of the red counter, then each
    # diagonal step of the counter costs 5 blank moves + 1 counter move along
    # the long axis (6 per unit) and 2 per unit along the short axis, with a
    # final straight run; equal dimensions force one extra 2-move detour.
    from collections import deque

    def bfs(m, n):
        start = ((0, 0), (m - 1, n - 1))
        dist = {start: 0}
        q = deque([start])
        while q:
            red, blank = q.popleft()
            if red == (m - 1, n - 1):
                return dist[(red, blank)]
            br, bc = blank
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = br + dr, bc + dc
                if 0 <= nr < m and 0 <= nc < n:
                    ns = (blank if (nr, nc) == red else red, (nr, nc))
                    if ns not in dist:
                        dist[ns] = dist[(red, blank)] + 1
                        q.append(ns)

    for m in range(2, 9):
        for n in range(2, 9):
            want = 8 * n - 11 if m == n else 6 * max(m, n) + 2 * min(m, n) - 13
            assert bfs(m, n) == want, (m, n)
    assert 6 * 5 + 2 * 4 - 13 == 25  # S(5,4) = 25 as stated

    # S(n,n) = 8n - 11 = p^2 needs p^2 + 11 = 0 mod 8, but odd p^2 = 1 mod 8
    # (and p=2 gives 4 < 5), so squares never contribute. For m != n with
    # a = max > b = min >= 2: 6a + 2b - 13 = p^2 (odd, so p != 2), i.e.
    # 3a + b = M := (p^2 + 13) / 2 with constraints b >= 2 and b < a:
    #   b = M - 3a >= 2  ->  a <= (M - 2) // 3
    #   b < a            ->  a >  M / 4
    # Every integer a in that range works; each unordered pair counts twice
    # (m-by-n and n-by-m grids are distinct).
    def grids(prime_limit):
        sieve = bytearray([1]) * prime_limit
        sieve[0] = sieve[1] = 0
        for i in range(2, int(prime_limit ** 0.5) + 1):
            if sieve[i]:
                sieve[i * i::i] = bytearray(len(sieve[i * i::i]))
        total = 0
        for p in range(3, prime_limit):
            if sieve[p]:
                M = (p * p + 13) // 2
                c = (M - 2) // 3 - M // 4
                if c > 0:
                    total += 2 * c
        return total

    assert grids(100) == 5482  # check value from the problem statement
    return grids(10 ** 6)

if __name__ == "__main__":
    print(solve())
