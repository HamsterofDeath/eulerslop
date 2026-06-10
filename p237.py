#!/usr/bin/env python3
"""Project Euler 237: Tours on a 4 x n playing board.

T(n) counts Hamiltonian paths on a 4-row, n-column grid that start in the
top-left corner, end in the bottom-left corner, and visit every cell once.
Strategy: brute-force T(n) for small n by DFS, verify the linear recurrence
T(n) = 2T(n-1) + 2T(n-2) - 2T(n-3) + T(n-4) against those values (and the
given T(10) = 2329), then evaluate T(10^12) mod 10^8 by matrix exponentiation.
"""

MOD = 10 ** 8
ROWS = 4


def brute(n):
    """Count Hamiltonian paths from (0,0) to (ROWS-1,0) on a ROWS x n grid."""
    total_cells = ROWS * n
    visited = [[False] * n for _ in range(ROWS)]
    target = (ROWS - 1, 0)
    count = 0

    def dfs(r, c, depth):
        nonlocal count
        if (r, c) == target:
            if depth == total_cells:
                count += 1
            return
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < ROWS and 0 <= nc < n and not visited[nr][nc]:
                visited[nr][nc] = True
                dfs(nr, nc, depth + 1)
                visited[nr][nc] = False

    visited[0][0] = True
    dfs(0, 0, 1)
    return count


def mat_mul(a, b, mod):
    size = len(a)
    return [
        [sum(a[i][k] * b[k][j] for k in range(size)) % mod for j in range(size)]
        for i in range(size)
    ]


def mat_pow(m, e, mod):
    size = len(m)
    result = [[int(i == j) for j in range(size)] for i in range(size)]
    while e:
        if e & 1:
            result = mat_mul(result, m, mod)
        m = mat_mul(m, m, mod)
        e >>= 1
    return result


def solve():
    # Small values by direct enumeration.
    small = [brute(n) for n in range(1, 8)]  # T(1) .. T(7)

    # Verify the recurrence T(n) = 2T(n-1) + 2T(n-2) - 2T(n-3) + T(n-4).
    coeffs = (2, 2, -2, 1)
    for i in range(4, len(small)):
        expected = (coeffs[0] * small[i - 1] + coeffs[1] * small[i - 2]
                    + coeffs[2] * small[i - 3] + coeffs[3] * small[i - 4])
        assert small[i] == expected, "recurrence failed at n=%d" % (i + 1)

    # Extend exactly to n=10 and check against the value given in the problem.
    seq = list(small)
    while len(seq) < 10:
        seq.append(coeffs[0] * seq[-1] + coeffs[1] * seq[-2]
                   + coeffs[2] * seq[-3] + coeffs[3] * seq[-4])
    assert seq[9] == 2329, "T(10) mismatch: %d" % seq[9]

    # Matrix exponentiation: state vector (T(n), T(n-1), T(n-2), T(n-3)).
    m = [
        [2, 2, -2, 1],
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
    ]
    n = 10 ** 12
    p = mat_pow(m, n - 4, MOD)
    # Multiply by the seed vector (T(4), T(3), T(2), T(1)).
    seeds = (small[3], small[2], small[1], small[0])
    return sum(p[0][j] * seeds[j] for j in range(4)) % MOD


if __name__ == "__main__":
    print(solve())
