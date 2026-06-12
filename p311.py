import numpy as np


def solve():
    # O is the midpoint of BD, so BO = DO. Let m = AO = CO and BO = DO.
    # Apollonius (median AO of triangle ABD): AB^2 + AD^2 = 2*AO^2 + 2*BO^2,
    # and likewise (median CO of triangle CBD): BC^2 + CD^2 = 2*CO^2 + 2*BO^2.
    # AB^2 + AD^2 must be an integer equal to 2*m^2 + BD^2/2, so BD is even:
    # BD = 2p with p = BO integer, and AB^2+AD^2 = BC^2+CD^2 = 2(m^2+p^2) = S.
    #
    # Conversely, place B=(-p,0), D=(p,0), A above / C below the x-axis at
    # distance m from O.  With a=AB, e=AD: a^2 = m^2+p^2+2p*x_A, so any
    # representation S = a^2 + e^2 with p-m < a < e < p+m yields a valid A
    # (|x_A| < m), and similarly (b,c) for C.  Convexity is automatic since
    # |x_A|,|x_C| < m <= p puts the AC crossing of the x-axis inside (-p,p).
    #
    # Representations of S = 2s (s = m^2+p^2) as u^2+v^2 biject with those of
    # s via (u,v) = (p-m, p+m); u determines the rep, and u < v iff m >= 1,
    # u >= 1 iff m < p.  Requirements AB<BC<CD<AD become: pick two reps
    # (a,e),(b,c) of S with a < b < c < e, i.e. two distinct reps with
    # u < v each, and the diagonal rep (m,p) must satisfy m>=1 and p-m < a.
    # Since p-m is itself the u-value of the diagonal's rep, each quadrilateral
    # corresponds to choosing 3 reps of s with m >= 1 (smallest u = diagonal,
    # other two = sides).  Hence per s the count is C(t,3) where
    # t(s) = #{(m,p): 1 <= m <= p, m^2+p^2 = s}.
    #
    # Constraint AB^2+BC^2+CD^2+AD^2 = 2S = 4s <= N, so s <= N/4.
    N = 10**10
    M = N // 4

    # Sieve t(s) for all s <= M: for each m, bump counts at m^2 + p^2 (p >= m).
    counts = np.zeros(M + 1, dtype=np.uint8)
    m = 1
    while 2 * m * m <= M:
        pmax = int((M - m * m) ** 0.5)
        while m * m + pmax * pmax > M:
            pmax -= 1
        p = np.arange(m, pmax + 1, dtype=np.int64)
        idx = m * m + p * p  # distinct indices for fixed m -> safe fancy +=
        counts[idx] += 1
        m += 1

    # B(N) = sum over s of C(t(s), 3); tally t-value frequencies in chunks.
    hist = np.zeros(256, dtype=np.int64)
    chunk = 1 << 25
    for i in range(0, M + 1, chunk):
        hist += np.bincount(counts[i:i + chunk], minlength=256)
    total = 0
    for t in range(3, 256):
        total += hist[t] * (t * (t - 1) * (t - 2) // 6)
    return total


if __name__ == "__main__":
    print(solve())
