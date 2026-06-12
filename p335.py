#!/usr/bin/env python3
from fractions import Fraction

def mancala_moves(x):
    # Simulate Peter's game: all bowls start with 1 bean; each move empties the
    # current bowl and sows the beans one by one clockwise; the next move starts
    # where the last bean landed.  Stop when all bowls hold exactly 1 bean again.
    bowls = [1] * x
    pos = 0
    moves = 0
    ones = x  # number of bowls currently holding exactly one bean
    while True:
        c = bowls[pos]
        bowls[pos] = 0
        if c == 1:
            ones -= 1
        for s in range(1, c + 1):
            p = (pos + s) % x
            b = bowls[p]
            bowls[p] = b + 1
            if b == 0:
                ones += 1
            elif b == 1:
                ones -= 1
        pos = (pos + c) % x
        moves += 1
        if ones == x:
            return moves

def solve():
    MOD = 7 ** 9
    K = 10 ** 18

    # Sanity checks of the simulator against the values given in the statement.
    assert mancala_moves(5) == 15
    assert mancala_moves(100) == 10920

    # M(2^k+1) grows like 4^k; the dynamics suggest an exponential-sum closed
    # form.  Fit M(2^k+1) = a*4^k + b*3^k + c*2^k + d exactly on k = 0..3 ...
    vals = [mancala_moves(2 ** k + 1) for k in range(9)]
    basis = [lambda k: 4 ** k, lambda k: 3 ** k, lambda k: 2 ** k, lambda k: 1]
    n = len(basis)
    M = [[Fraction(f(k)) for f in basis] + [Fraction(vals[k])] for k in range(n)]
    for col in range(n):  # Gauss-Jordan, exact rational arithmetic
        piv = next(r for r in range(col, n) if M[r][col] != 0)
        M[col], M[piv] = M[piv], M[col]
        M[col] = [v / M[col][col] for v in M[col]]
        for r in range(n):
            if r != col and M[r][col] != 0:
                f = M[r][col]
                M[r] = [a - f * b for a, b in zip(M[r], M[col])]
    coef = [M[r][n] for r in range(n)]

    # ... and verify the closed form against independently simulated k = 4..8.
    for k in range(len(vals)):
        assert sum(c * f(k) for c, f in zip(coef, basis)) == vals[k]

    # Sum_{k=0}^{K} M(2^k+1) = sum over basis terms of coef * geometric series,
    # everything mod 7^9 (3, 2 and the rational coefficients are invertible).
    def geom(q, terms, mod):
        # 1 + q + ... + q^(terms-1) mod `mod`, q coprime checks via inverse
        if q == 1:
            return terms % mod
        return (pow(q, terms, (q - 1) * mod) - 1) // (q - 1) % mod

    total = 0
    qs = [4, 3, 2, 1]
    for c, q in zip(coef, qs):
        g = geom(q, K + 1, MOD)
        num = c.numerator % MOD
        den_inv = pow(c.denominator, -1, MOD)
        total = (total + num * den_inv % MOD * g) % MOD
    return total

if __name__ == "__main__":
    print(solve())
