#!/usr/bin/env python3

from math import comb, isqrt

# Scale: costs sqrt(k), sqrt(F_k) are handled as integers A = round(sqrt(k)*10^30)
# via isqrt, keeping ~26 safe digits after all arithmetic — far beyond the 8 needed.
SC = 10 ** 30


def f_capped(X, A, B, n):
    # With budget x, the max searchable interval satisfies
    #   f(x) = f(x-a) + f(x-b) + 1   (f = 0 for x < 0),
    # which unrolls to f(x) = sum_{i*a+j*b <= x} C(i+j, i): each worst-case
    # answer path with i "lower" (cost a) and j "higher" (cost b) replies
    # contributes its C(i+j, i) orderings.  For fixed j the row sum over
    # i = 0..m telescopes (hockey stick) to C(m+j+1, j+1).  Capped at n.
    total = 0
    j = 0
    while j * B <= X:
        m = (X - j * B) // A
        total += comb(m + j + 1, j + 1)
        if total >= n:
            return n
        j += 1
    return total


def C(n, A, B):
    # C(n,a,b) = min{ x = i*a + j*b : f(x) >= n }; f only jumps at such x.
    # Get an upper bound by doubling along the diagonal, then for each j
    # binary-search the minimal i (f is monotone in x, hence in i).
    X = A + B
    while f_capped(X, A, B, n) < n:
        X *= 2
    best = X
    j = 0
    while j * B <= best:
        i_hi = (best - j * B) // A  # only i that could beat the incumbent
        if f_capped(i_hi * A + j * B, A, B, n) >= n:
            lo, hi = 0, i_hi
            while lo < hi:
                mid = (lo + hi) // 2
                if f_capped(mid * A + j * B, A, B, n) >= n:
                    hi = mid
                else:
                    lo = mid + 1
            best = min(best, lo * A + j * B)
        j += 1
    return best


def solve():
    fib = [0, 1, 1]
    while len(fib) < 31:
        fib.append(fib[-1] + fib[-2])
    n = 10 ** 12
    total = 0
    for k in range(1, 31):
        A = isqrt(k * SC * SC)
        B = isqrt(fib[k] * SC * SC)
        total += C(n, A, B)
    # round the scaled integer sum to 8 decimals (irrational tail, no ties)
    q = (total + 5 * 10 ** 21) // 10 ** 22
    return f"{q // 10 ** 8}.{q % 10 ** 8:08d}"


if __name__ == "__main__":
    print(solve())
