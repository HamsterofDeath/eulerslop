#!/usr/bin/env python3
from fractions import Fraction


def solve():
    n = 100  # players
    half = n // 2  # gaps 0..50 by symmetry

    # Each die moves -1 (roll 1), +1 (roll 6) or stays, each with prob 1/6, 1/6, 4/6.
    # Change in (pos1 - pos2): s1 - s2 in {-2..2} with probabilities (out of 36):
    deltas = {-2: 1, -1: 8, 0: 18, 1: 8, 2: 1}

    def fold(g):
        # Map a raw signed gap onto 0..half (circle of n players).
        g %= n
        return min(g, n - g)

    # E[g] = expected remaining turns with current gap g (1 <= g <= half), E[0] = 0.
    # E[g] = 1 + sum_d p_d * E[fold(g + d)]
    # Build linear system A x = b over Fractions for unknowns E[1..half].
    m = half
    A = [[Fraction(0) for _ in range(m)] for _ in range(m)]
    b = [Fraction(1) for _ in range(m)]

    for g in range(1, half + 1):
        row = A[g - 1]
        row[g - 1] += 1
        for d, w in deltas.items():
            ng = fold(g + d)
            if ng != 0:
                row[ng - 1] -= Fraction(w, 36)

    # Gaussian elimination with partial pivoting (exact arithmetic).
    for col in range(m):
        piv = next(r for r in range(col, m) if A[r][col] != 0)
        if piv != col:
            A[col], A[piv] = A[piv], A[col]
            b[col], b[piv] = b[piv], b[col]
        inv = A[col][col]
        for r in range(col + 1, m):
            if A[r][col] != 0:
                factor = A[r][col] / inv
                for c in range(col, m):
                    A[r][c] -= factor * A[col][c]
                b[r] -= factor * b[col]

    x = [Fraction(0)] * m
    for r in range(m - 1, -1, -1):
        s = b[r] - sum(A[r][c] * x[c] for c in range(r + 1, m))
        x[r] = s / A[r][r]

    expected = x[half - 1]  # start with dice at opposite players: gap = 50
    return f"{float(expected):.6f}"


if __name__ == "__main__":
    print(solve())
