#!/usr/bin/env python3
"""p149: Max-sum subsequence in any direction in 2000x2000 grid."""
def solve():
    N = 2000
    total_cells = N * N
    
    # Generate s_k
    s = [0] * (total_cells + 1)
    for k in range(1, 56):
        s[k] = (100003 - 200003*k + 300007*k*k*k) % 1000000 - 500000
    for k in range(56, total_cells + 1):
        s[k] = (s[k-24] + s[k-55] + 1000000) % 1000000 - 500000
    
    # Fill grid
    grid = [[0]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            grid[i][j] = s[i*N + j + 1]
    
    def kadane(arr):
        best = arr[0]
        cur = arr[0]
        for x in arr[1:]:
            cur = max(x, cur + x)
            best = max(best, cur)
        return best
    
    best = 0
    
    # Horizontal
    for i in range(N):
        best = max(best, kadane(grid[i]))
    
    # Vertical
    for j in range(N):
        col = [grid[i][j] for i in range(N)]
        best = max(best, kadane(col))
    
    # Diagonal (top-left to bottom-right)
    # Starting row 0, cols 0..N-1
    for j in range(N):
        diag = []
        r, c = 0, j
        while r < N and c < N:
            diag.append(grid[r][c])
            r += 1
            c += 1
        best = max(best, kadane(diag))
    # Starting row 1..N-1, col 0
    for i in range(1, N):
        diag = []
        r, c = i, 0
        while r < N and c < N:
            diag.append(grid[r][c])
            r += 1
            c += 1
        best = max(best, kadane(diag))
    
    # Anti-diagonal (top-right to bottom-left)
    for j in range(N):
        diag = []
        r, c = 0, j
        while r < N and c >= 0:
            diag.append(grid[r][c])
            r += 1
            c -= 1
        best = max(best, kadane(diag))
    for i in range(1, N):
        diag = []
        r, c = i, N - 1
        while r < N and c >= 0:
            diag.append(grid[r][c])
            r += 1
            c -= 1
        best = max(best, kadane(diag))
    
    return best

if __name__ == "__main__":
    print(solve())
