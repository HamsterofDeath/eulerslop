#!/usr/bin/env python3
import numpy as np

def expected_black(n):
    # State (w, b) = (white, black) sheep. A white bleat (prob w/(w+b)) turns a
    # black sheep white, a black bleat (prob b/(w+b)) turns a white sheep black,
    # so on the diagonal s = w+b the chain moves b -> b-1 w.p. (s-b)/s and
    # b -> b+1 w.p. b/s, absorbing at b=0 (payoff 0) and b=s (payoff s).
    # Removing white sheep drops to diagonal s-1 with b fixed, so with
    # U_s(b) = optimal expected final black sheep we get a per-diagonal
    # optimal stopping problem ("stop" = remove one white sheep):
    #   U_s(b) = max(U_{s-1}(b), ((s-b) U_s(b-1) + b U_s(b+1)) / s).
    # The natural scale of the diagonal-s chain is x_b = sum_{i<b} C(s-1, i)
    # (harmonic: (s-b)(x_b - x_{b-1}) = b (x_{b+1} - x_b)), so U_s is the least
    # concave majorant in x of g(b) = U_{s-1}(b) plus the endpoint (x_s, s).
    # Since U_{s-1} is harmonic-or-concave in its own scale, it is strictly
    # concave in the diagonal-s scale (the factor (s-b)/b beats (s-1-b)/b),
    # hence the majorant is g itself on a prefix [0..j] followed by the single
    # tangent line through the endpoint: with T(b) = sum_{i>=b} C(s-1, i)
    # (distance to the right boundary in natural scale),
    #   j = argmin_b (s - g(b)) / T(b),   U_s(b) = s - sigma_j * T(b) for b > j.
    # We keep the binomial row normalized by 2^(s-1) (Pascal update r -> avg of
    # shifts), so T comes from one reverse cumsum and everything stays O(s) per
    # diagonal. Verified against value iteration and an exact upper-hull solver
    # for small n.
    U = np.array([0.0, 1.0])          # U_1
    r = np.array([0.5, 0.5])          # C(1, i) / 2^1
    for s in range(2, 2 * n + 1):
        T = np.cumsum(r[::-1])[::-1]  # T(b) = sum_{i=b}^{s-1} C(s-1,i)/2^(s-1)
        with np.errstate(divide="ignore", over="ignore"):
            sigma = (s - U) / T       # underflowed T -> inf, never the argmin
        j = int(np.argmin(sigma))
        newU = np.empty(s + 1)
        newU[: j + 1] = U[: j + 1]    # removal optimal: value frozen
        newU[j + 1 : s] = s - sigma[j] * T[j + 1 :]
        newU[s] = float(s)
        U = newU
        if s < 2 * n:                 # Pascal: C(s,i)/2^s from C(s-1,i)/2^(s-1)
            r2 = np.empty(s + 1)
            r2[0] = r[0] / 2
            r2[s] = r[s - 1] / 2
            r2[1:s] = (r[1:] + r[:-1]) / 2
            r = r2
    # No removal is allowed before the first bleat: from (n, n) both moves
    # have probability 1/2 on diagonal 2n.
    return (U[n - 1] + U[n + 1]) / 2

def solve():
    assert f"{expected_black(5):.6f}" == "6.871346"
    return f"{expected_black(10000):.6f}"

if __name__ == "__main__":
    print(solve())
