#!/usr/bin/env python3

def solve():
    # Subtraction game where a move removes a positive square number of stones.
    # Compute Grundy values g(n) for 0 <= n <= 100000 (mex over g(n - k^2)),
    # then count triples 0 <= a <= b <= c <= N with g(a)^g(b)^g(c) == 0
    # (losing for the player to move, by Sprague-Grundy theory).
    N = 100000
    squares = [i * i for i in range(1, int(N ** 0.5) + 1)]
    g = [0] * (N + 1)
    for n in range(1, N + 1):
        seen = 0
        for s in squares:
            if s > n:
                break
            seen |= 1 << g[n - s]
        # mex = position of lowest zero bit of 'seen'
        g[n] = (~seen & (seen + 1)).bit_length() - 1

    # Bucket pile sizes by Grundy value.
    V = 1 << (max(g).bit_length())
    cnt = [0] * V
    for v in g:
        cnt[v] += 1

    # T = ordered triples (a,b,c) with XOR of Grundy values 0.
    T = 0
    for v1 in range(V):
        if cnt[v1] == 0:
            continue
        for v2 in range(V):
            if cnt[v2]:
                T += cnt[v1] * cnt[v2] * cnt[v1 ^ v2]

    # Burnside over S3 to count multisets a <= b <= c:
    # fixed by a transposition: a == b forces g(c) == 0 -> (N+1) * cnt[0];
    # fixed by a 3-cycle: a == b == c forces g(a) == 0 -> cnt[0].
    z = cnt[0]
    return (T + 3 * (N + 1) * z + 2 * z) // 6

if __name__ == "__main__":
    print(solve())
