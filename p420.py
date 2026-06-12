import numpy as np
from math import isqrt


def solve():
    # M = A^2 = B^2 with A != B positive integer 2x2 matrices.  By
    # Cayley-Hamilton M = t*A - det(A)*I, so the two roots have traces
    # t1 > t2 > 0 with det(B) = -det(A) > ... and t1^2 - t2^2 = 4*det(A).
    # Write t1 = p*k, t2 = q*k (gcd(p,q)=1, k = gcd(t1,t2)).  Matching
    # entries forces  a-d = q*u, e-h = p*u,  b = q*beta, c = q*gamma,
    # f = p*beta, g = p*gamma,  and the trace condition collapses to
    #     k^2 - u^2 = 4*beta*gamma,   trace(M) = k^2*(p^2+q^2)/2.
    # Integrality: if p,q both odd we need u == k (mod 2); if p+q odd we
    # need k,u both even.  Positivity of all entries: q*k - p*|u| >= 2.
    # Each M corresponds to exactly one tuple (p,q,k,u,beta,gamma), so
    #     F(N) = sum over valid (p,q,k,u) of d((k^2-u^2)/4).
    N = 10**7
    LIM = 2 * N - 2  # k^2*(p^2+q^2) <= LIM  <=>  trace(M) < N

    # divisor-count sieve up to max (k^2-u^2)/4 (k^2 <= LIM/5 since p^2+q^2>=5)
    vmax = isqrt(LIM // 5) ** 2 // 4 + 1
    dcnt = np.zeros(vmax + 1, dtype=np.int32)
    for i in range(1, vmax + 1):
        dcnt[i::i] += 1

    # all coprime pairs p > q >= 1 admitting k = 2 (i.e. 4*(p^2+q^2) <= LIM)
    pmax = isqrt(LIM // 4 - 1)
    Ps, Qs = [], []
    for p in range(2, pmax + 1):
        q = np.arange(1, p, dtype=np.int64)
        q = q[(np.gcd(q, p) == 1) & (p * p + q * q <= LIM // 4)]
        if q.size:
            Ps.append(np.full(q.size, p, dtype=np.int64))
            Qs.append(q)
    P = np.concatenate(Ps)
    Q = np.concatenate(Qs)
    S = P * P + Q * Q
    KM = np.sqrt(LIM / S).astype(np.int64)
    KM -= (KM * KM * S > LIM)            # fix float rounding
    KM += ((KM + 1) ** 2 * S <= LIM)
    mixed = (P + Q) % 2 == 1

    total = 0
    CH = 200_000  # pairs per chunk to bound memory
    for case in (0, 1):  # 0: p,q both odd (k step 1), 1: mixed (k even only)
        sel = mixed if case else ~mixed
        p_, q_, km_ = P[sel], Q[sel], KM[sel]
        step = 2 if case else 1
        nk_all = km_ // 2 if case else km_ - 1  # k = 2, 2+step, ..., <= km
        for lo in range(0, p_.size, CH):
            pc, qc, nk = p_[lo:lo + CH], q_[lo:lo + CH], nk_all[lo:lo + CH]
            # flatten (pair -> k list)
            idx = np.repeat(np.arange(pc.size), nk)
            off = np.repeat(np.cumsum(nk) - nk, nk)
            k = 2 + step * (np.arange(idx.size) - off)
            pk, qk = pc[idx], qc[idx]
            # u = 0 contribution (k even)
            ke = k[k % 2 == 0]
            total += int(dcnt[ke * ke // 4].sum(dtype=np.int64))
            # positive u: u0 = 1 (k odd) or 2 (k even), u <= (q*k-2)//p
            umax = (qk * k - 2) // pk
            u0 = 2 - (k & 1)
            nu = np.maximum((umax - u0) // 2 + 1, 0)
            jdx = np.repeat(np.arange(k.size), nu)
            uoff = np.repeat(np.cumsum(nu) - nu, nu)
            u = u0[jdx] + 2 * (np.arange(jdx.size) - uoff)
            v = (k[jdx] ** 2 - u * u) // 4
            total += 2 * int(dcnt[v].sum(dtype=np.int64))
    return total


if __name__ == "__main__":
    print(solve())
