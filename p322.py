#!/usr/bin/env python3
import numpy as np

def T(m, n):
    # Count n <= i < m with C(i, n) == 0 (mod 10).  Substitute j = i - n,
    # 0 <= j < J = m - n.  By Kummer's theorem, the exponent of a prime p in
    # C(n+j, n) equals the number of carries when adding n + j in base p, so
    #   C not divisible by 2  <=>  no binary carries   <=>  j & n == 0
    #   C not divisible by 5  <=>  no base-5 carries   <=>  j_d <= 4 - n_d
    #                                                       for every digit d.
    # Inclusion-exclusion:  T = J - N2 - N5 + N25.
    J = m - n

    # N2: digit DP over binary, j < J with j a submask of ~n.
    free_below = [0] * (J.bit_length() + 1)        # free (zero) bits of n below b
    for b in range(J.bit_length()):
        free_below[b + 1] = free_below[b] + (0 if (n >> b) & 1 else 1)
    N2 = 0
    for b in range(J.bit_length() - 1, -1, -1):
        if (J >> b) & 1:
            # put 0 at bit b (below J's prefix), lower free bits arbitrary
            N2 += 1 << free_below[b]
            if (n >> b) & 1:
                break                              # cannot match J's 1-bit; done
    # (j == J itself is never counted: loop only counts j strictly below J)

    # N5: digit DP over base 5, j < J with every digit j_d <= L_d = 4 - n_d.
    D = 1
    while 5 ** D <= J:
        D += 1
    Ld = [4 - (n // 5 ** d) % 5 for d in range(D)]
    Jd = [(J // 5 ** d) % 5 for d in range(D)]
    prod = [1] * (D + 1)                           # choices for digits < d
    for d in range(D):
        prod[d + 1] = prod[d] * (Ld[d] + 1)
    N5 = 0
    for d in range(D - 1, -1, -1):
        N5 += min(Jd[d], Ld[d] + 1) * prod[d]
        if Jd[d] > Ld[d]:
            break

    # N25: both conditions at once.  n = 10^12 - 10 has mostly 4s in base 5,
    # so the set of admissible low parts r = j mod 5^Dn (the "box") is tiny
    # (4800 values).  Write j = q*5^Dn + r; digits >= Dn are unconstrained in
    # base 5, so for each r we only need to count q with (q*5^Dn + r) & n == 0
    # and j < J -- done vectorised with numpy over all q at once.
    Dn = 0
    t = n
    while t:
        Dn += 1
        t //= 5
    C5 = 5 ** Dn
    box = [0]
    for d in range(Dn):
        lim = 4 - (n // 5 ** d) % 5
        box = [r + v * 5 ** d for r in box for v in range(lim + 1)]
    qC = np.arange((J - 1) // C5 + 1, dtype=np.int64) * C5
    N25 = 0
    for r in box:
        tvals = qC + r
        N25 += int(np.count_nonzero(((tvals & n) == 0) & (tvals < J)))

    return J - N2 - N5 + N25

def solve():
    assert T(10 ** 9, 10 ** 7 - 10) == 989697000   # given check value
    return T(10 ** 18, 10 ** 12 - 10)

if __name__ == "__main__":
    print(solve())
